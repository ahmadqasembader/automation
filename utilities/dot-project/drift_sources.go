package projects

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"regexp"
	"sort"
	"strings"
	"sync"
	"time"
)

// ── Multi-repo parsing ────────────────────────────────────────────────────────

// ParseAllRepos extracts every valid GitHub org/repo pair from a
// project.yaml repositories[] list, preserving order.
// Non-GitHub URLs (e.g., GitLab, plain HTTPS) are silently skipped.
func ParseAllRepos(repositories []string) []RepoRef {
	const prefix = "https://github.com/"
	var out []RepoRef
	for _, u := range repositories {
		u = strings.TrimSuffix(strings.TrimSpace(u), "/")
		if !strings.HasPrefix(u, prefix) {
			continue
		}
		parts := strings.SplitN(strings.TrimPrefix(u, prefix), "/", 3)
		if len(parts) >= 2 && parts[0] != "" && parts[1] != "" {
			out = append(out, RepoRef{Org: parts[0], Repo: parts[1]})
		}
	}
	return out
}

// ParsePrimaryRepo extracts the GitHub org and repo name from the first GitHub
// URL in a project's repositories list.
//
//	"https://github.com/kubernetes/kubernetes" → ("kubernetes", "kubernetes", nil)
//
// Returns an error only if no valid GitHub URL is found.
func ParsePrimaryRepo(repositories []string) (org, repo string, err error) {
	refs := ParseAllRepos(repositories)
	if len(refs) == 0 {
		return "", "", fmt.Errorf("no valid github.com repository URL found in repositories list")
	}
	return refs[0].Org, refs[0].Repo, nil
}

// ── Contributor activity fetching ─────────────────────────────────────────────

// repoActivity holds the raw per-repo activity data before aggregation.
type repoActivity struct {
	repo     string               // "org/repo"
	commits  map[string]int       // handle → commit count
	prs      map[string]int       // handle → merged PR count
	lastSeen map[string]time.Time // handle → most recent activity date
	fetchErr error
}

// FetchAllRepoActivity fans out concurrent activity fetches across all repos
// in refs using up to concurrency parallel goroutines, then returns a
// per-handle aggregated ActivitySummary map.
//
// since defines how far back to look.
// token is the GitHub personal access token; baseURL overrides the API
// endpoint (empty = api.github.com, useful for testing).
func FetchAllRepoActivity(
	ctx context.Context,
	refs []RepoRef,
	since time.Time,
	token string,
	client *http.Client,
	baseURL string,
	concurrency int,
) (activity map[string]*ActivitySummary, scanned []string, errs []error) {
	if baseURL == "" {
		baseURL = defaultGitHubAPIURL
	}
	if concurrency <= 0 {
		concurrency = DefaultConcurrency
	}

	results := make([]repoActivity, len(refs))
	sem := make(chan struct{}, concurrency)
	var wg sync.WaitGroup

	for i, ref := range refs {
		wg.Add(1)
		go func(idx int, r RepoRef) {
			defer wg.Done()
			sem <- struct{}{}
			defer func() { <-sem }()

			ra := repoActivity{
				repo:     r.Org + "/" + r.Repo,
				commits:  make(map[string]int),
				prs:      make(map[string]int),
				lastSeen: make(map[string]time.Time),
			}

			// Commits via stats/contributors (1 API call per repo, with 202 retry).
			commits, dates, err := fetchContributorStats(ctx, r.Org, r.Repo, since, token, client, baseURL)
			if err != nil {
				ra.fetchErr = fmt.Errorf("%s: commits: %w", ra.repo, err)
				results[idx] = ra
				return
			}
			ra.commits = commits
			for h, t := range dates {
				if cur, ok := ra.lastSeen[h]; !ok || t.After(cur) {
					ra.lastSeen[h] = t
				}
			}

			// Merged PRs (paginated, stops once PRs are older than since).
			prs, prDates, err := fetchMergedPRs(ctx, r.Org, r.Repo, since, token, client, baseURL)
			if err != nil {
				// Non-fatal: record the error but keep commit data.
				ra.fetchErr = fmt.Errorf("%s: PRs: %w", ra.repo, err)
			}
			ra.prs = prs
			for h, t := range prDates {
				if cur, ok := ra.lastSeen[h]; !ok || t.After(cur) {
					ra.lastSeen[h] = t
				}
			}

			results[idx] = ra
		}(i, ref)
	}
	wg.Wait()

	// Aggregate across repos into a single per-handle map.
	aggregate := make(map[string]*ActivitySummary)

	for _, ra := range results {
		scanned = append(scanned, ra.repo)
		if ra.fetchErr != nil {
			errs = append(errs, ra.fetchErr)
		}
		for h, n := range ra.commits {
			s := ensureEntry(aggregate, h)
			s.Commits += n
			addRepo(s, ra.repo)
			if t := ra.lastSeen[h]; !t.IsZero() && t.After(s.LastSeen) {
				s.LastSeen = t
			}
		}
		for h, n := range ra.prs {
			s := ensureEntry(aggregate, h)
			s.MergedPRs += n
			addRepo(s, ra.repo)
			if t := ra.lastSeen[h]; !t.IsZero() && t.After(s.LastSeen) {
				s.LastSeen = t
			}
		}
	}

	return aggregate, scanned, errs
}

func ensureEntry(m map[string]*ActivitySummary, handle string) *ActivitySummary {
	if s, ok := m[handle]; ok {
		return s
	}
	s := &ActivitySummary{Handle: handle}
	m[handle] = s
	return s
}

func addRepo(s *ActivitySummary, repo string) {
	for _, r := range s.ReposTouched {
		if r == repo {
			return
		}
	}
	s.ReposTouched = append(s.ReposTouched, repo)
}

// ── stats/contributors ────────────────────────────────────────────────────────

type contributorWeek struct {
	W int `json:"w"` // Unix timestamp of the week start
	C int `json:"c"` // commit count for that week
}

type contributorEntry struct {
	Author struct {
		Login string `json:"login"`
	} `json:"author"`
	Weeks []contributorWeek `json:"weeks"`
}

// fetchContributorStats calls GET /repos/{org}/{repo}/stats/contributors,
// retrying up to 3 times on 202 (GitHub computes stats asynchronously).
// Returns per-handle commit counts and latest-activity dates, filtered to
// the window defined by since.
func fetchContributorStats(
	ctx context.Context,
	org, repo string,
	since time.Time,
	token string,
	client *http.Client,
	baseURL string,
) (commits map[string]int, lastSeen map[string]time.Time, err error) {
	url := fmt.Sprintf("%s/repos/%s/%s/stats/contributors", baseURL, org, repo)
	sinceUnix := since.Unix()

	const maxRetries = 3
	for attempt := 0; attempt < maxRetries; attempt++ {
		if attempt > 0 {
			time.Sleep(time.Duration(attempt*3) * time.Second)
		}

		req, reqErr := http.NewRequestWithContext(ctx, "GET", url, nil)
		if reqErr != nil {
			return nil, nil, fmt.Errorf("building stats request: %w", reqErr)
		}
		if token != "" {
			req.Header.Set("Authorization", "token "+token)
		}
		req.Header.Set("Accept", "application/vnd.github.v3+json")

		resp, doErr := client.Do(req)
		if doErr != nil {
			return nil, nil, fmt.Errorf("stats/contributors request: %w", doErr)
		}

		switch resp.StatusCode {
		case http.StatusAccepted:
			// GitHub is still computing; retry after backoff.
			resp.Body.Close() //nolint:errcheck
			continue
		case http.StatusNoContent:
			resp.Body.Close() //nolint:errcheck
			return make(map[string]int), make(map[string]time.Time), nil
		}

		if resp.StatusCode != http.StatusOK {
			resp.Body.Close() //nolint:errcheck
			return nil, nil, fmt.Errorf("stats/contributors HTTP %d for %s/%s", resp.StatusCode, org, repo)
		}

		var entries []contributorEntry
		decErr := json.NewDecoder(resp.Body).Decode(&entries)
		resp.Body.Close() //nolint:errcheck
		if decErr != nil {
			return nil, nil, fmt.Errorf("parsing stats/contributors: %w", decErr)
		}

		commitMap := make(map[string]int, len(entries))
		lastSeenMap := make(map[string]time.Time, len(entries))

		for _, e := range entries {
			login := strings.ToLower(e.Author.Login)
			if login == "" {
				continue
			}
			for _, w := range e.Weeks {
				if int64(w.W) < sinceUnix || w.C == 0 {
					continue
				}
				commitMap[login] += w.C
				// Track the end of the latest week with commits.
				wEnd := time.Unix(int64(w.W), 0).Add(7 * 24 * time.Hour)
				if cur, ok := lastSeenMap[login]; !ok || wEnd.After(cur) {
					lastSeenMap[login] = wEnd
				}
			}
		}
		return commitMap, lastSeenMap, nil
	}

	return nil, nil, fmt.Errorf(
		"stats/contributors for %s/%s still returning 202 after %d retries — try again later",
		org, repo, maxRetries,
	)
}

// ── Merged PRs ────────────────────────────────────────────────────────────────

type prEntry struct {
	MergedAt  *time.Time `json:"merged_at"`
	UpdatedAt time.Time  `json:"updated_at"`
	User      struct {
		Login string `json:"login"`
	} `json:"user"`
}

// fetchMergedPRs fetches merged PRs for a repo since the given time,
// following pagination and stopping early once all PRs on a page are older
// than since (PRs are returned newest-first).
func fetchMergedPRs(
	ctx context.Context,
	org, repo string,
	since time.Time,
	token string,
	client *http.Client,
	baseURL string,
) (counts map[string]int, lastSeen map[string]time.Time, err error) {
	counts = make(map[string]int)
	lastSeen = make(map[string]time.Time)

	nextURL := fmt.Sprintf(
		"%s/repos/%s/%s/pulls?state=closed&sort=updated&direction=desc&per_page=100",
		baseURL, org, repo,
	)

	for nextURL != "" {
		page, next, done, pageErr := fetchPRPage(ctx, nextURL, since, token, client)
		if pageErr != nil {
			return counts, lastSeen, pageErr
		}
		for _, pr := range page {
			if pr.MergedAt == nil || pr.MergedAt.Before(since) || pr.User.Login == "" {
				continue
			}
			login := strings.ToLower(pr.User.Login)
			counts[login]++
			if cur, ok := lastSeen[login]; !ok || pr.MergedAt.After(cur) {
				lastSeen[login] = *pr.MergedAt
			}
		}
		if done {
			break
		}
		nextURL = next
	}
	return counts, lastSeen, nil
}

// fetchPRPage fetches one page of pull requests.
// done is true when every PR on this page was updated before since.
func fetchPRPage(
	ctx context.Context,
	url string,
	since time.Time,
	token string,
	client *http.Client,
) (page []prEntry, next string, done bool, err error) {
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return nil, "", false, fmt.Errorf("building PR request: %w", err)
	}
	if token != "" {
		req.Header.Set("Authorization", "token "+token)
	}
	req.Header.Set("Accept", "application/vnd.github.v3+json")

	resp, err := client.Do(req)
	if err != nil {
		return nil, "", false, fmt.Errorf("PR list request: %w", err)
	}
	defer resp.Body.Close() //nolint:errcheck

	linkHeader := resp.Header.Get("Link")

	if resp.StatusCode != http.StatusOK {
		return nil, "", false, fmt.Errorf("PR list HTTP %d", resp.StatusCode)
	}

	if err := json.NewDecoder(resp.Body).Decode(&page); err != nil {
		return nil, "", false, fmt.Errorf("parsing PR list: %w", err)
	}

	// If every PR on this page was last updated before the window, all
	// subsequent pages will be too (results are newest-first by updated_at),
	// so we can stop early.  We check updated_at, not merged_at, because
	// merged_at ≤ updated_at always holds — a PR with updated_at < since
	// could not have been merged inside the window.
	allOld := len(page) > 0
	for _, pr := range page {
		if pr.UpdatedAt.After(since) {
			allOld = false
			break
		}
	}

	return page, parseLinkNext(linkHeader), allOld, nil
}

// ── Result building ───────────────────────────────────────────────────────────

// BuildHealthCheckActivityLists splits aggregated activity into two sorted
// lists: one for current maintainers (most active first) and one for top
// contributors not in the maintainer set (capped at topN).
func BuildHealthCheckActivityLists(
	activity map[string]*ActivitySummary,
	maintainerHandles []string,
	topN int,
) (maintainerActivity []ActivitySummary, topContributors []ActivitySummary) {
	maintainerSet := make(map[string]bool, len(maintainerHandles))
	for _, h := range maintainerHandles {
		maintainerSet[strings.ToLower(h)] = true
	}

	// Build maintainer rows — include even those with zero activity.
	for _, h := range maintainerHandles {
		h = strings.ToLower(h)
		if s, ok := activity[h]; ok {
			maintainerActivity = append(maintainerActivity, *s)
		} else {
			maintainerActivity = append(maintainerActivity, ActivitySummary{Handle: h})
		}
	}
	sortActivityDesc(maintainerActivity)

	// Build top-contributor rows — skip maintainers and team slugs.
	for _, s := range activity {
		if !maintainerSet[s.Handle] && !isLikelyTeamSlug(s.Handle) {
			topContributors = append(topContributors, *s)
		}
	}
	sortActivityDesc(topContributors)
	if topN > 0 && len(topContributors) > topN {
		topContributors = topContributors[:topN]
	}

	// Sort repo lists alphabetically for stable output.
	for i := range maintainerActivity {
		sort.Strings(maintainerActivity[i].ReposTouched)
	}
	for i := range topContributors {
		sort.Strings(topContributors[i].ReposTouched)
	}

	return maintainerActivity, topContributors
}

// ── Team slug filter ──────────────────────────────────────────────────────────

var teamSlugPrefixes = []string{
	"sig-", "wg-", "committee-", "toc-", "tag-",
	"cncf-", "k8s-infra-",
}

var teamSlugSuffixes = []string{
	"-approvers", "-reviewers", "-leads", "-maintainers",
	"-owners", "-members", "-admins",
}

// manySegmentsRE matches handles with 4 or more hyphen-separated segments,
// which are extremely unlikely to be personal GitHub usernames.
var manySegmentsRE = regexp.MustCompile(`^[a-z0-9]+(?:-[a-z0-9]+){3,}$`)

// isLikelyTeamSlug returns true when a lowercase handle looks like a GitHub
// org team slug rather than an individual user account.
func isLikelyTeamSlug(h string) bool {
	h = strings.ToLower(h)
	for _, pfx := range teamSlugPrefixes {
		if strings.HasPrefix(h, pfx) {
			return true
		}
	}
	for _, sfx := range teamSlugSuffixes {
		if strings.HasSuffix(h, sfx) {
			return true
		}
	}
	return manySegmentsRE.MatchString(h)
}

// ── GitHub Teams API ──────────────────────────────────────────────────────────

// FetchGitHubTeamMembers fetches all members of an org team via the GitHub
// Teams API, following pagination automatically.
// The token must have the read:org scope.
func FetchGitHubTeamMembers(ctx context.Context, org, teamSlug, token string, client *http.Client, baseURL string) ([]string, error) {
	if baseURL == "" {
		baseURL = defaultGitHubAPIURL
	}
	var all []string
	nextURL := fmt.Sprintf("%s/orgs/%s/teams/%s/members?per_page=100", baseURL, org, teamSlug)
	for nextURL != "" {
		page, next, err := fetchTeamMembersPage(ctx, nextURL, token, client)
		if err != nil {
			return nil, err
		}
		for _, m := range page {
			if m.Login != "" {
				all = append(all, strings.ToLower(m.Login))
			}
		}
		nextURL = next
	}
	return all, nil
}

type teamMember struct {
	Login string `json:"login"`
}

func fetchTeamMembersPage(ctx context.Context, url, token string, client *http.Client) ([]teamMember, string, error) {
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return nil, "", fmt.Errorf("building teams request: %w", err)
	}
	if token != "" {
		req.Header.Set("Authorization", "token "+token)
	}
	req.Header.Set("Accept", "application/vnd.github.v3+json")

	resp, err := client.Do(req)
	if err != nil {
		return nil, "", fmt.Errorf("GitHub Teams API request failed: %w", err)
	}
	defer resp.Body.Close() //nolint:errcheck

	linkHeader := resp.Header.Get("Link")

	switch resp.StatusCode {
	case 404:
		return nil, "", fmt.Errorf("GitHub team not found (404)")
	case 403:
		return nil, "", fmt.Errorf("GitHub Teams API: permission denied (403) — token needs read:org scope")
	}
	if resp.StatusCode != http.StatusOK {
		return nil, "", fmt.Errorf("GitHub Teams API returned HTTP %d", resp.StatusCode)
	}

	var page []teamMember
	if err := json.NewDecoder(resp.Body).Decode(&page); err != nil {
		return nil, "", fmt.Errorf("parsing teams members response: %w", err)
	}
	return page, parseLinkNext(linkHeader), nil
}

// parseLinkNext extracts the URL for rel="next" from a GitHub Link header.
// Returns "" when there are no more pages.
func parseLinkNext(linkHeader string) string {
	if linkHeader == "" {
		return ""
	}
	for _, part := range strings.Split(linkHeader, ",") {
		part = strings.TrimSpace(part)
		segments := strings.Split(part, ";")
		if len(segments) < 2 {
			continue
		}
		urlPart := strings.TrimSpace(segments[0])
		relPart := strings.TrimSpace(segments[1])
		if relPart == `rel="next"` &&
			strings.HasPrefix(urlPart, "<") &&
			strings.HasSuffix(urlPart, ">") {
			return urlPart[1 : len(urlPart)-1]
		}
	}
	return ""
}
