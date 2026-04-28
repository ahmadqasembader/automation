package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"time"

	"gopkg.in/yaml.v3"

	"projects"
)

// Exit codes:
//
//	0 — no drift detected, maintainers are in sync
//	1 — drift (or staleness) detected
//	2 — fatal error (bad flags, unreadable file, etc.)
func main() {
	var (
		projectYAMLPath = flag.String("project-yaml", "project.yaml", "Path to project.yaml")
		maintainersPath = flag.String("maintainers-yaml", "maintainers.yaml", "Path to maintainers.yaml")
		githubToken     = flag.String("github-token", "", "GitHub personal access token (or set GITHUB_TOKEN env var)")
		teamName        = flag.String("team", "project-maintainers", "Team name in maintainers.yaml to compare against upstream")
		checkOnly       = flag.Bool("check-only", false, "Print drift summary; exit 1 if drift found, exit 0 if clean (no files written)")
		reportPath      = flag.String("report", "", "Write Markdown PR-body to this file path")
		outputPatched   = flag.String("output-patched", "", "Write patched maintainers.yaml to this file path (implies patch)")
		stalenessDays   = flag.Int("staleness-days", 90, "Days without an update before the staleness warning fires")
		lastUpdatedDays = flag.Int("last-updated-days", -1, "Days since maintainers.yaml was last git-committed (-1 = use file mtime)")
		githubTeamSlug  = flag.String("github-team-slug", "", "Optional: GitHub org team slug to use as upstream source instead of governance files")
	)
	flag.Parse()

	token := *githubToken
	if token == "" {
		token = os.Getenv("GITHUB_TOKEN")
	}

	client := &http.Client{Timeout: projects.DefaultHTTPTimeout}

	// ── Load project handles from maintainers.yaml ────────────────────────────
	projectHandles, projectID, org, err := projects.LoadProjectHandlesForTeam(*maintainersPath, *teamName)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(2)
	}

	// ── Resolve primary GitHub org/repo from project.yaml ────────────────────
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

	primaryOrg, primaryRepo, err := projects.ParsePrimaryRepo(project.Repositories)
	if err != nil {
		// Fall back: use org from maintainers.yaml and slug as repo name.
		if org != "" {
			primaryOrg = org
			primaryRepo = org
			fmt.Fprintf(os.Stderr, "warning: %v; falling back to org=%s repo=%s\n", err, primaryOrg, primaryRepo)
		} else {
			fmt.Fprintf(os.Stderr, "error: %v\n", err)
			os.Exit(2)
		}
	}

	fmt.Fprintf(os.Stderr, "checking drift: project=%s team=%s upstream=%s/%s\n",
		projectID, *teamName, primaryOrg, primaryRepo)

	// ── Fetch upstream handles ────────────────────────────────────────────────
	var upstreamHandles []string
	var sources []string

	if *githubTeamSlug != "" {
		// Use GitHub Teams API as upstream source (requires read:org scope).
		fmt.Fprintf(os.Stderr, "using GitHub Teams API: %s/%s\n", primaryOrg, *githubTeamSlug)
		upstreamHandles, err = projects.FetchGitHubTeamMembers(primaryOrg, *githubTeamSlug, token, client, "")
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: GitHub Teams fetch failed: %v (falling back to governance files)\n", err)
			upstreamHandles, sources, err = projects.FetchUpstreamHandles(primaryOrg, primaryRepo, token, client, "")
			if err != nil {
				fmt.Fprintf(os.Stderr, "warning: governance files fetch also failed: %v\n", err)
			}
		} else {
			sources = []string{fmt.Sprintf("GitHub team: %s/%s", primaryOrg, *githubTeamSlug)}
		}
	} else {
		upstreamHandles, sources, err = projects.FetchUpstreamHandles(primaryOrg, primaryRepo, token, client, "")
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: upstream fetch failed: %v\n", err)
			// Non-fatal: treat as empty upstream — will flag all .project handles as "removed".
			// This is intentionally conservative; the PR body will make the source clear.
		}
	}

	fmt.Fprintf(os.Stderr, "found %d project handle(s), %d upstream handle(s)\n",
		len(projectHandles), len(upstreamHandles))

	// ── Compute drift ─────────────────────────────────────────────────────────
	added, removed := projects.DetectDrift(projectHandles, upstreamHandles)

	// ── Staleness check ───────────────────────────────────────────────────────
	daysSince := *lastUpdatedDays
	if daysSince < 0 {
		// Fall back to file mtime (unreliable in CI but useful locally).
		if fi, statErr := os.Stat(*maintainersPath); statErr == nil {
			daysSince = int(time.Since(fi.ModTime()).Hours() / 24)
		}
	}
	isStale := daysSince >= 0 && daysSince > *stalenessDays

	result := projects.DriftResult{
		ProjectID:              projectID,
		Org:                    org,
		TeamName:               *teamName,
		AddedUpstream:          added,
		RemovedUpstream:        removed,
		HasDrift:               len(added) > 0 || len(removed) > 0,
		IsStale:                isStale,
		DaysSinceUpdate:        daysSince,
		StalenessDaysThreshold: *stalenessDays,
		UpstreamSources:        sources,
		CheckedAt:              time.Now().UTC(),
	}

	hasDrift := result.HasDrift || result.IsStale

	// ── Check-only mode (used by PR/push validation step) ─────────────────────
	if *checkOnly {
		if !hasDrift {
			fmt.Fprintln(os.Stderr, "no drift detected — maintainers are in sync")
			os.Exit(0)
		}
		if len(added) > 0 {
			fmt.Fprintf(os.Stderr, "drift: %d handle(s) added upstream but missing in .project: %v\n", len(added), added)
		}
		if len(removed) > 0 {
			fmt.Fprintf(os.Stderr, "drift: %d handle(s) in .project but gone from upstream: %v\n", len(removed), removed)
		}
		if isStale {
			fmt.Fprintf(os.Stderr, "stale: maintainers.yaml not updated in %d days (threshold: %d)\n",
				daysSince, *stalenessDays)
		}
		os.Exit(1)
	}

	// ── Generate PR body report ───────────────────────────────────────────────
	report := projects.FormatDriftReport(result, primaryOrg, primaryRepo)

	if *reportPath != "" {
		if err := os.WriteFile(*reportPath, []byte(report), 0o644); err != nil {
			fmt.Fprintf(os.Stderr, "error writing report to %s: %v\n", *reportPath, err)
			os.Exit(2)
		}
		fmt.Fprintf(os.Stderr, "PR body written to %s\n", *reportPath)
	}

	// ── Patch maintainers.yaml ────────────────────────────────────────────────
	if *outputPatched != "" {
		if result.HasDrift {
			patched, err := projects.PatchMaintainersYAML(*maintainersPath, *teamName, added, removed)
			if err != nil {
				fmt.Fprintf(os.Stderr, "error patching maintainers.yaml: %v\n", err)
				os.Exit(2)
			}
			if err := os.WriteFile(*outputPatched, patched, 0o644); err != nil {
				fmt.Fprintf(os.Stderr, "error writing patched file to %s: %v\n", *outputPatched, err)
				os.Exit(2)
			}
			fmt.Fprintf(os.Stderr, "patched maintainers.yaml written to %s\n", *outputPatched)
		} else {
			// No handle drift (may still be stale) — copy file unchanged so the
			// workflow can always reference the output-patched path safely.
			data, _ := os.ReadFile(*maintainersPath)
			_ = os.WriteFile(*outputPatched, data, 0o644)
			fmt.Fprintln(os.Stderr, "no handle drift to patch (file copied unchanged)")
		}
	}

	// ── Final exit ────────────────────────────────────────────────────────────
	if hasDrift {
		if len(added) > 0 {
			fmt.Fprintf(os.Stderr, "summary: %d added upstream: %v\n", len(added), added)
		}
		if len(removed) > 0 {
			fmt.Fprintf(os.Stderr, "summary: %d removed from upstream: %v\n", len(removed), removed)
		}
		if isStale {
			fmt.Fprintf(os.Stderr, "summary: stale (%d days since last update)\n", daysSince)
		}
		os.Exit(1)
	}

	fmt.Fprintln(os.Stderr, "no drift detected — maintainers are in sync")
	os.Exit(0)
}
