package main

import (
	"context"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"time"

	"gopkg.in/yaml.v3"

	"projects"
)

// main is the entry point for the drift health-check CLI.
//
// Exit codes:
//
//	0 — not stale, no action needed
//	1 — stale; issue body written to -report (workflow should open/update issue)
//	2 — fatal error (bad flags, unreadable file, GitHub API failure)
func main() {
	var (
		projectYAMLPath = flag.String("project-yaml", "project.yaml", "Path to project.yaml")
		maintainersPath = flag.String("maintainers-yaml", "maintainers.yaml", "Path to maintainers.yaml")
		githubToken     = flag.String("github-token", "", "GitHub personal access token (or set GITHUB_TOKEN env var)")
		teamName        = flag.String("team", "project-maintainers", "Team name in maintainers.yaml to read")
		reportPath      = flag.String("report", "", "Write Markdown issue body to this file path")
		stalenessDays   = flag.Int("staleness-days", projects.DefaultStalenessThresholdDays,
			"Days without an update before the health-check issue fires")
		lastUpdatedDays = flag.Int("last-updated-days", -1,
			"Days since maintainers.yaml was last git-committed (-1 = use file mtime)")
		activityMonths = flag.Int("activity-months", projects.DefaultActivityWindowMonths,
			"How many months back to look for contributor activity")
		concurrency = flag.Int("concurrency", projects.DefaultConcurrency,
			"Max parallel GitHub API repo fetches")
		topContributors = flag.Int("top-contributors", projects.DefaultTopContributors,
			"How many non-maintainer contributors to surface in the issue body")
	)
	flag.Parse()

	// Context is cancelled on SIGINT (Ctrl-C), which propagates to all
	// in-flight HTTP requests and lets the process exit cleanly.
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	token := *githubToken
	if token == "" {
		token = os.Getenv("GITHUB_TOKEN")
	}

	client := &http.Client{Timeout: projects.DefaultHTTPTimeout}

	// ── Staleness check ───────────────────────────────────────────────────────
	daysSince := *lastUpdatedDays
	if daysSince < 0 {
		// Fall back to file mtime (unreliable in CI; prefer git log via -last-updated-days).
		if fi, err := os.Stat(*maintainersPath); err == nil {
			daysSince = int(time.Since(fi.ModTime()).Hours() / 24)
		}
	}

	isStale := daysSince >= 0 && daysSince > *stalenessDays
	if !isStale {
		fmt.Fprintf(os.Stderr, "not stale (%d/%d days) — no action needed\n",
			daysSince, *stalenessDays)
		os.Exit(0)
	}

	fmt.Fprintf(os.Stderr, "stale: %d days since last update (threshold: %d)\n",
		daysSince, *stalenessDays)

	// ── Load project data ─────────────────────────────────────────────────────
	maintainerHandles, projectID, org, err := projects.LoadProjectHandlesForTeam(*maintainersPath, *teamName)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(2)
	}

	projData, err := os.ReadFile(*projectYAMLPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error reading %s: %v\n", *projectYAMLPath, err)
		os.Exit(2)
	}
	var project projects.Project
	if err := yaml.Unmarshal(projData, &project); err != nil {
		fmt.Fprintf(os.Stderr, "error parsing %s: %v\n", *projectYAMLPath, err)
		os.Exit(2)
	}

	repos := projects.ParseAllRepos(project.Repositories)
	if len(repos) == 0 {
		// Fall back: use org from maintainers.yaml as single repo.
		if org != "" {
			repos = []projects.RepoRef{{Org: org, Repo: org}}
			fmt.Fprintf(os.Stderr, "warning: no GitHub repos in project.yaml; falling back to %s/%s\n", org, org)
		} else {
			fmt.Fprintln(os.Stderr, "error: no GitHub repositories found in project.yaml")
			os.Exit(2)
		}
	}

	fmt.Fprintf(os.Stderr, "scanning %d repo(s) for activity (window: %d months, concurrency: %d)\n",
		len(repos), *activityMonths, *concurrency)

	// ── Fetch contributor activity across all repos ───────────────────────────
	since := time.Now().UTC().AddDate(0, -*activityMonths, 0)
	activity, scanned, fetchErrs := projects.FetchAllRepoActivity(
		ctx, repos, since, token, client, "", *concurrency,
	)

	// Log fetch errors as warnings — they're non-fatal (partial data is still useful).
	for _, e := range fetchErrs {
		fmt.Fprintf(os.Stderr, "warning: %v\n", e)
	}

	fmt.Fprintf(os.Stderr, "fetched activity for %d repo(s), found %d unique contributor(s)\n",
		len(scanned), len(activity))

	// ── Build activity lists ──────────────────────────────────────────────────
	maintainerActivity, topActive := projects.BuildHealthCheckActivityLists(
		activity, maintainerHandles, *topContributors,
	)

	// Pick up to 3 handles to @mention in the issue greeting, choosing the
	// most active maintainers first (maintainerActivity is already sorted by
	// activity desc).  This mirrors the onboarding issue convention in
	// provision.sh::create_onboarding_issue() while preferring handles that
	// are clearly still engaged with the project.
	const maxMentions = 3
	var mentionHandles []string
	for _, a := range maintainerActivity {
		if len(mentionHandles) >= maxMentions {
			break
		}
		mentionHandles = append(mentionHandles, a.Handle)
	}

	result := projects.HealthCheckResult{
		ProjectID:              projectID,
		Org:                    org,
		TeamName:               *teamName,
		IsStale:                true,
		DaysSinceUpdate:        daysSince,
		StalenessDaysThreshold: *stalenessDays,
		MentionHandles:         mentionHandles,
		MaintainerActivity:     maintainerActivity,
		TopNewContributors:     topActive,
		CheckedAt:              time.Now().UTC(),
	}

	// ── Write issue body ──────────────────────────────────────────────────────
	issueBody := projects.FormatActivityIssue(result)

	if *reportPath != "" {
		if err := os.WriteFile(*reportPath, []byte(issueBody), 0o644); err != nil {
			fmt.Fprintf(os.Stderr, "error writing report to %s: %v\n", *reportPath, err)
			os.Exit(2)
		}
		fmt.Fprintf(os.Stderr, "issue body written to %s\n", *reportPath)
	} else {
		fmt.Print(issueBody)
	}

	// ── Summary ───────────────────────────────────────────────────────────────
	fmt.Fprintf(os.Stderr, "summary: project=%s stale=%d days maintainers=%d active-contributors=%d\n",
		projectID, daysSince, len(maintainerHandles), len(topActive))

	os.Exit(1) // stale — caller (workflow) should open/update the issue
}
