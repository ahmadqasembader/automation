package projects

import (
	"fmt"
	"os"
	"sort"
	"strings"

	"gopkg.in/yaml.v3"
)

// LoadProjectHandlesForTeam reads maintainers.yaml and returns the GitHub handles
// for the named team (e.g., "project-maintainers"), plus the project_id and org.
//
// If the team is not found, it returns an empty slice (not an error) so the
// caller can decide whether to treat that as noteworthy.
func LoadProjectHandlesForTeam(path, teamName string) (handles []string, projectID, org string, err error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, "", "", fmt.Errorf("reading %s: %w", path, err)
	}

	var config MaintainersConfig
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, "", "", fmt.Errorf("parsing %s: %w", path, err)
	}

	if len(config.Maintainers) == 0 {
		return nil, "", "", fmt.Errorf("%s has no maintainer entries", path)
	}

	// Each org/.project repo contains exactly one MaintainerEntry (one project
	// per repo).  We read only [0]; if someone mistakenly adds a second entry
	// it is silently ignored — the validator will catch that separately.
	entry := config.Maintainers[0]
	projectID = entry.ProjectID
	org = entry.Org

	for _, team := range entry.Teams {
		if team.Name != teamName {
			continue
		}
		for _, m := range team.Members {
			m = strings.TrimSpace(m)
			m = strings.TrimPrefix(m, "@")
			if m != "" {
				handles = append(handles, strings.ToLower(m))
			}
		}
		return handles, projectID, org, nil
	}

	// Team not found; return empty slice so caller can reason about it.
	return []string{}, projectID, org, nil
}

// FormatActivityIssue renders the Markdown body for the maintainer
// health-check GitHub issue from a HealthCheckResult.
func FormatActivityIssue(result HealthCheckResult) string {
	var b strings.Builder

	b.WriteString(fmt.Sprintf("## Maintainer List Health Check — `%s`\n\n", result.ProjectID))

	// Greet up to 3 maintainers by @mention, mirroring the onboarding issue pattern.
	if len(result.MentionHandles) > 0 {
		var mentions []string
		for _, h := range result.MentionHandles {
			mentions = append(mentions, "@"+h)
		}
		b.WriteString(fmt.Sprintf("Hi %s 👋\n\n", strings.Join(mentions, " ")))
	}

	b.WriteString(fmt.Sprintf(
		"`maintainers.yaml` has not been updated in **%d days** (threshold: %d days).\n"+
			"Please confirm the list below still reflects your project's governance model.\n\n",
		result.DaysSinceUpdate, result.StalenessDaysThreshold,
	))
	b.WriteString(fmt.Sprintf("🕒 **Checked:** %s  \n",
		result.CheckedAt.UTC().Format("2006-01-02 15:04 UTC")))
	b.WriteString(fmt.Sprintf("📅 **Activity window:** last %d months\n\n",
		DefaultActivityWindowMonths))

	// ── Current maintainers ──────────────────────────────────────────────────
	b.WriteString("### Current Maintainers — Activity\n\n")
	if len(result.MaintainerActivity) == 0 {
		b.WriteString("_No maintainers found in the `" + result.TeamName + "` team._\n\n")
	} else {
		b.WriteString("| Maintainer | Commits | Merged PRs | Active repos | Last seen |\n")
		b.WriteString("|---|---|---|---|---|\n")
		for _, a := range result.MaintainerActivity {
			lastSeen := "—"
			if !a.LastSeen.IsZero() {
				lastSeen = a.LastSeen.UTC().Format("2006-01-02")
			}
			b.WriteString(fmt.Sprintf("| `@%s` | %d | %d | %s | %s |\n",
				a.Handle, a.Commits, a.MergedPRs, formatRepoList(a.ReposTouched), lastSeen))
		}
		b.WriteString("\n")
	}

	// ── Active contributors not yet in the maintainer list ───────────────────
	if len(result.TopNewContributors) > 0 {
		b.WriteString("### Active Contributors Not Yet in Maintainer List\n\n")
		b.WriteString(fmt.Sprintf(
			"These contributors have been active across project repos in the last %d months "+
				"but do not appear in `maintainers.yaml`. "+
				"Consider whether any should be nominated per your governance process.\n\n",
			DefaultActivityWindowMonths,
		))
		b.WriteString("| Handle | Commits | Merged PRs | Active repos |\n")
		b.WriteString("|---|---|---|---|\n")
		for _, a := range result.TopNewContributors {
			b.WriteString(fmt.Sprintf("| `@%s` | %d | %d | %s |\n",
				a.Handle, a.Commits, a.MergedPRs, formatRepoList(a.ReposTouched)))
		}
		b.WriteString("\n")
	}

	b.WriteString("---\n")
	b.WriteString("> **No changes are required automatically.** " +
		"Please update `maintainers.yaml` if this no longer reflects your governance, " +
		"or close this issue to confirm it is still accurate. " +
		"This issue was opened by [cncf/automation](https://github.com/cncf/automation) " +
		"maintainer health-check tooling.\n")

	return b.String()
}

// sortActivityDesc sorts an ActivitySummary slice by total activity
// (commits + merged PRs) descending, with handle as a stable tiebreaker.
func sortActivityDesc(summaries []ActivitySummary) {
	sort.Slice(summaries, func(i, j int) bool {
		ti := summaries[i].Commits + summaries[i].MergedPRs
		tj := summaries[j].Commits + summaries[j].MergedPRs
		if ti != tj {
			return ti > tj
		}
		return summaries[i].Handle < summaries[j].Handle
	})
}

// formatRepoList renders a repo list for a Markdown table cell.
// Up to repoInlineMax repos are shown by name; any remainder is shown as
// "+N more" so the table cell stays readable even for Kubernetes-scale maintainers.
func formatRepoList(repos []string) string {
	const repoInlineMax = 3
	if len(repos) == 0 {
		return "—"
	}
	if len(repos) <= repoInlineMax {
		return strings.Join(repos, ", ")
	}
	visible := strings.Join(repos[:repoInlineMax], ", ")
	return fmt.Sprintf("%s +%d more", visible, len(repos)-repoInlineMax)
}
