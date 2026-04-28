package projects

import (
	"encoding/json"
	"fmt"
	"net/http"
	"regexp"
	"strings"
)

// FetchUpstreamHandles fetches maintainer handles from a project's primary repo
// governance files (MAINTAINERS, MAINTAINERS.md, CODEOWNERS, OWNERS).
// It reuses the existing fetchFromGitHub / discoverGovernanceFiles infrastructure.
// Returns the merged handle list, the governance file names that were found, and any error.
//
// Handles that look like GitHub org team slugs (e.g., sig-release-leads,
// wg-security) are filtered out to reduce false positives.
func FetchUpstreamHandles(org, repo, token string, client *http.Client, baseURL string) (handles []string, sources []string, err error) {
	ghData, err := fetchFromGitHub(org, repo, token, client, baseURL)
	if err != nil {
		return nil, nil, fmt.Errorf("fetching GitHub data for %s/%s: %w", org, repo, err)
	}

	// Filter out handles that are almost certainly GitHub org team slugs rather
	// than individual user accounts.  This is the primary source of false
	// positives when CODEOWNERS uses bare team-slug references without the
	// "org/" prefix.
	var filtered []string
	for _, h := range ghData.Maintainers {
		if !isLikelyTeamSlug(h) {
			filtered = append(filtered, h)
		}
	}

	// Build a best-effort list of which governance file types likely contributed.
	// We always search all four file names regardless of which ones are present;
	// "searched" is more accurate than "found" or "scanned".
	if len(filtered) > 0 {
		sources = []string{"MAINTAINERS/MAINTAINERS.md", "CODEOWNERS", "OWNERS"}
	}

	return filtered, sources, nil
}

// teamSlugPrefixes are well-known CNCF/Kubernetes team naming prefixes that
// indicate an org team slug rather than a personal GitHub account.
var teamSlugPrefixes = []string{
	"sig-", "wg-", "committee-", "toc-", "tag-",
	"cncf-", "k8s-infra-",
}

// teamSlugSuffixes are common suffixes that identify org teams.
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
	// 4+ hyphen segments like "sig-contributor-experience-approvers"
	if manySegmentsRE.MatchString(h) {
		return true
	}
	return false
}

// FetchGitHubTeamMembers fetches all members of an org team via the GitHub
// Teams API, following pagination automatically.
// The token must have the read:org scope.
// Returns handles (lowercase) or an error if the team does not exist or the
// token lacks sufficient permissions.
func FetchGitHubTeamMembers(org, teamSlug, token string, client *http.Client, baseURL string) ([]string, error) {
	if baseURL == "" {
		baseURL = defaultGitHubAPIURL
	}

	var all []string
	nextURL := fmt.Sprintf("%s/orgs/%s/teams/%s/members?per_page=100", baseURL, org, teamSlug)

	for nextURL != "" {
		page, next, err := fetchTeamMembersPage(nextURL, token, client)
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

// teamMember is the per-member shape returned by the GitHub Teams members API.
type teamMember struct {
	Login string `json:"login"`
}

// fetchTeamMembersPage performs a single paginated request to the GitHub Teams
// members API.  It uses defer for body cleanup so every code path closes the
// response body and the error is always checked.
// Returns the page of members, the next-page URL (empty if last page), and any error.
func fetchTeamMembersPage(url, token string, client *http.Client) ([]teamMember, string, error) {
	req, err := http.NewRequest("GET", url, nil)
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
	defer resp.Body.Close() //nolint:errcheck // response body close errors are not actionable

	// Capture the Link header before consuming the body.
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
//
// Example header value:
//
//	<https://api.github.com/...?page=2>; rel="next", <...>; rel="last"
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

// ParsePrimaryRepo extracts the GitHub org and repo name from the first GitHub
// URL in a project's repositories list.
//
//	"https://github.com/kubernetes/kubernetes" → ("kubernetes", "kubernetes", nil)
//
// Returns an error only if no valid GitHub URL is found.
func ParsePrimaryRepo(repositories []string) (org, repo string, err error) {
	const prefix = "https://github.com/"
	for _, repoURL := range repositories {
		repoURL = strings.TrimSuffix(strings.TrimSpace(repoURL), "/")
		if !strings.HasPrefix(repoURL, prefix) {
			continue
		}
		parts := strings.SplitN(strings.TrimPrefix(repoURL, prefix), "/", 3)
		if len(parts) >= 2 && parts[0] != "" && parts[1] != "" {
			return parts[0], parts[1], nil
		}
	}
	return "", "", fmt.Errorf("no valid github.com repository URL found in repositories list")
}
