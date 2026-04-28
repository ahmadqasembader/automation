package projects

import (
	"bytes"
	"fmt"
	"os"
	"sort"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

// LoadProjectHandlesForTeam reads maintainers.yaml and returns the GitHub handles
// for the named team (e.g., "project-maintainers"), plus the project_id and org.
// If the team is not found, it returns an empty slice (not an error) so the caller
// can decide whether to treat that as drift.
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

// DetectDrift compares two handle sets (case-insensitive) and returns:
//   - added:   handles present upstream but missing from .project
//   - removed: handles present in .project but gone from upstream
//
// Both slices are sorted and lowercase.
func DetectDrift(projectHandles, upstreamHandles []string) (added, removed []string) {
	projectSet := make(map[string]bool, len(projectHandles))
	for _, h := range projectHandles {
		projectSet[strings.ToLower(h)] = true
	}

	upstreamSet := make(map[string]bool, len(upstreamHandles))
	for _, h := range upstreamHandles {
		upstreamSet[strings.ToLower(h)] = true
	}

	for h := range upstreamSet {
		if !projectSet[h] {
			added = append(added, h)
		}
	}
	for h := range projectSet {
		if !upstreamSet[h] {
			removed = append(removed, h)
		}
	}

	sort.Strings(added)
	sort.Strings(removed)
	return added, removed
}

// PatchMaintainersYAML applies a drift result to maintainers.yaml, returning
// the updated file content.  Added handles are appended to the named team;
// removed handles are deleted from it.
//
// Header comment lines (lines starting with '#') that appear before the first
// YAML key are preserved verbatim.  A one-line drift annotation is inserted
// after the original header so reviewers know the file was auto-patched.
func PatchMaintainersYAML(path, teamName string, added, removed []string) ([]byte, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("reading %s: %w", path, err)
	}

	// Collect header comment lines (everything before the first non-comment,
	// non-blank line).
	var headerLines []string
	for _, line := range strings.Split(string(data), "\n") {
		if strings.HasPrefix(line, "#") || strings.TrimSpace(line) == "" {
			headerLines = append(headerLines, line)
		} else {
			break
		}
	}

	var config MaintainersConfig
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, fmt.Errorf("parsing %s: %w", path, err)
	}

	removedSet := make(map[string]bool, len(removed))
	for _, h := range removed {
		removedSet[strings.ToLower(h)] = true
	}

	for i := range config.Maintainers {
		for j := range config.Maintainers[i].Teams {
			if config.Maintainers[i].Teams[j].Name != teamName {
				continue
			}

			// Drop removed handles.
			var kept []string
			for _, m := range config.Maintainers[i].Teams[j].Members {
				normalized := strings.ToLower(strings.TrimPrefix(strings.TrimSpace(m), "@"))
				if !removedSet[normalized] {
					kept = append(kept, m)
				}
			}

			// Append added handles (skip duplicates).
			existing := make(map[string]bool, len(kept))
			for _, m := range kept {
				existing[strings.ToLower(strings.TrimPrefix(strings.TrimSpace(m), "@"))] = true
			}
			for _, h := range added {
				if !existing[strings.ToLower(h)] {
					kept = append(kept, h)
				}
			}

			config.Maintainers[i].Teams[j].Members = kept
		}
	}

	body, err := marshalYAML2Indent(config)
	if err != nil {
		return nil, fmt.Errorf("marshalling patched config: %w", err)
	}

	// Rebuild: original header + drift annotation + marshalled body.
	header := strings.Join(headerLines, "\n")
	annotation := fmt.Sprintf("# Auto-patched by cncf/automation drift detector on %s\n",
		time.Now().UTC().Format("2006-01-02"))

	var out strings.Builder
	out.WriteString(strings.TrimRight(header, "\n"))
	out.WriteString("\n")
	out.WriteString(annotation)
	out.WriteString(string(body))

	return []byte(out.String()), nil
}

// FormatDriftReport renders a human-readable Markdown PR body from a DriftResult.
func FormatDriftReport(result DriftResult, primaryOrg, primaryRepo string) string {
	var b strings.Builder

	b.WriteString(fmt.Sprintf("## Maintainer Drift Detected — `%s`\n\n", result.ProjectID))
	b.WriteString(fmt.Sprintf(
		"Automated comparison between **`%s/.project/maintainers.yaml`** (team: `%s`) "+
			"and upstream governance files in **`%s/%s`**.\n\n",
		primaryOrg, result.TeamName, primaryOrg, primaryRepo,
	))
	b.WriteString(fmt.Sprintf("🕒 **Checked:** %s\n\n", result.CheckedAt.UTC().Format("2006-01-02 15:04 UTC")))

	if len(result.UpstreamSources) > 0 {
		b.WriteString(fmt.Sprintf("📂 **Sources searched:** %s\n\n", strings.Join(result.UpstreamSources, ", ")))
	}

	if len(result.AddedUpstream) > 0 {
		b.WriteString("### ➕ Added upstream — not yet in `.project`\n\n")
		b.WriteString("These handles appear in upstream governance files but are missing from `maintainers.yaml`.\n\n")
		b.WriteString("| Handle | Suggested action |\n")
		b.WriteString("|--------|------------------|\n")
		for _, h := range result.AddedUpstream {
			b.WriteString(fmt.Sprintf("| `@%s` | Add to `%s` team |\n", h, result.TeamName))
		}
		b.WriteString("\n")
	}

	if len(result.RemovedUpstream) > 0 {
		b.WriteString("### ➖ Removed from upstream — still in `.project`\n\n")
		b.WriteString("These handles are in `maintainers.yaml` but no longer appear in upstream governance files.\n\n")
		b.WriteString("| Handle | Suggested action |\n")
		b.WriteString("|--------|------------------|\n")
		for _, h := range result.RemovedUpstream {
			b.WriteString(fmt.Sprintf("| `@%s` | Remove from `%s` team (or move to emeritus) |\n", h, result.TeamName))
		}
		b.WriteString("\n")
	}

	if result.IsStale {
		threshold := result.StalenessDaysThreshold
		if threshold <= 0 {
			threshold = 90 // safe fallback if caller forgot to set it
		}
		b.WriteString("### ⏰ Staleness Warning\n\n")
		b.WriteString(fmt.Sprintf(
			"`maintainers.yaml` has not been updated in **%d days** (threshold: %d days). "+
				"Please review and confirm the maintainer list is still current, even if no "+
				"handle changes are needed.\n\n",
			result.DaysSinceUpdate, threshold,
		))
	}

	b.WriteString("---\n")
	b.WriteString("> **Note:** This PR was auto-generated by [cncf/automation](https://github.com/cncf/automation) " +
		"drift detection. The patch applies only to the `" + result.TeamName + "` team. " +
		"Please review carefully — automated handle matching may produce false positives " +
		"if upstream governance files are incomplete or use a non-standard format. " +
		"YAML comments in the original file are not preserved by the auto-patcher.\n")

	return b.String()
}

// marshalYAML2Indent marshals v to YAML using 2-space indentation, matching
// the indentation style used throughout the .project scaffold templates.
// gopkg.in/yaml.v3's Marshal default is 4-space; we override via NewEncoder.
func marshalYAML2Indent(v any) ([]byte, error) {
	var buf bytes.Buffer
	enc := yaml.NewEncoder(&buf)
	enc.SetIndent(2)
	if err := enc.Encode(v); err != nil {
		return nil, err
	}
	if err := enc.Close(); err != nil {
		return nil, err
	}
	return buf.Bytes(), nil
}
