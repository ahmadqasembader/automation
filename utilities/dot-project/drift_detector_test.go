package projects

import (
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
	"time"
)

// ── LoadProjectHandlesForTeam ─────────────────────────────────────────────────

func TestLoadProjectHandlesForTeam(t *testing.T) {
	const yamlFixture = `
maintainers:
  - project_id: "testproj"
    org: "testorg"
    teams:
      - name: "project-maintainers"
        members:
          - alice
          - "@bob"
          - "  Carol  "
      - name: "reviewers"
        members:
          - dave
`

	dir := t.TempDir()
	path := filepath.Join(dir, "maintainers.yaml")
	if err := os.WriteFile(path, []byte(yamlFixture), 0o644); err != nil {
		t.Fatal(err)
	}

	tests := []struct {
		name        string
		teamName    string
		wantHandles []string
		wantID      string
		wantOrg     string
		wantErr     bool
	}{
		{
			name:        "found team — normalises case and @ prefix",
			teamName:    "project-maintainers",
			wantHandles: []string{"alice", "bob", "carol"},
			wantID:      "testproj",
			wantOrg:     "testorg",
		},
		{
			name:        "second team",
			teamName:    "reviewers",
			wantHandles: []string{"dave"},
			wantID:      "testproj",
			wantOrg:     "testorg",
		},
		{
			name:        "team not found — returns empty slice, no error",
			teamName:    "nonexistent",
			wantHandles: []string{},
			wantID:      "testproj",
			wantOrg:     "testorg",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			handles, id, org, err := LoadProjectHandlesForTeam(path, tt.teamName)
			if (err != nil) != tt.wantErr {
				t.Fatalf("err = %v, wantErr %v", err, tt.wantErr)
			}
			if !reflect.DeepEqual(handles, tt.wantHandles) {
				t.Errorf("handles: got %v, want %v", handles, tt.wantHandles)
			}
			if id != tt.wantID {
				t.Errorf("projectID: got %q, want %q", id, tt.wantID)
			}
			if org != tt.wantOrg {
				t.Errorf("org: got %q, want %q", org, tt.wantOrg)
			}
		})
	}

	t.Run("missing file returns error", func(t *testing.T) {
		_, _, _, err := LoadProjectHandlesForTeam(filepath.Join(dir, "nosuchfile.yaml"), "project-maintainers")
		if err == nil {
			t.Error("expected error for missing file, got nil")
		}
	})

	t.Run("empty maintainers list returns error", func(t *testing.T) {
		empty := filepath.Join(dir, "empty.yaml")
		_ = os.WriteFile(empty, []byte("maintainers: []\n"), 0o644)
		_, _, _, err := LoadProjectHandlesForTeam(empty, "project-maintainers")
		if err == nil {
			t.Error("expected error for empty maintainers, got nil")
		}
	})
}

// ── ParseAllRepos ─────────────────────────────────────────────────────────────

func TestParseAllRepos(t *testing.T) {
	tests := []struct {
		name         string
		repositories []string
		want         []RepoRef
	}{
		{
			name:         "single repo",
			repositories: []string{"https://github.com/kubernetes/kubernetes"},
			want:         []RepoRef{{Org: "kubernetes", Repo: "kubernetes"}},
		},
		{
			name: "multiple repos preserve order",
			repositories: []string{
				"https://github.com/org/first",
				"https://github.com/org/second",
				"https://github.com/org/third",
			},
			want: []RepoRef{
				{Org: "org", Repo: "first"},
				{Org: "org", Repo: "second"},
				{Org: "org", Repo: "third"},
			},
		},
		{
			name: "skips non-github URLs",
			repositories: []string{
				"https://gitlab.com/org/repo",
				"https://github.com/org/repo",
			},
			want: []RepoRef{{Org: "org", Repo: "repo"}},
		},
		{
			name:         "trailing slash stripped",
			repositories: []string{"https://github.com/argoproj/argo-cd/"},
			want:         []RepoRef{{Org: "argoproj", Repo: "argo-cd"}},
		},
		{
			name:         "deep path — only org/repo extracted",
			repositories: []string{"https://github.com/org/repo/tree/main/subdir"},
			want:         []RepoRef{{Org: "org", Repo: "repo"}},
		},
		{
			name:         "empty list",
			repositories: []string{},
			want:         nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := ParseAllRepos(tt.repositories)
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("got %v, want %v", got, tt.want)
			}
		})
	}
}

// ── ParsePrimaryRepo ─────────────────────────────────────────────────────────

func TestParsePrimaryRepo(t *testing.T) {
	tests := []struct {
		name         string
		repositories []string
		wantOrg      string
		wantRepo     string
		wantErr      bool
	}{
		{
			name:         "simple github URL",
			repositories: []string{"https://github.com/kubernetes/kubernetes"},
			wantOrg:      "kubernetes",
			wantRepo:     "kubernetes",
		},
		{
			name:         "trailing slash stripped",
			repositories: []string{"https://github.com/argoproj/argo-cd/"},
			wantOrg:      "argoproj",
			wantRepo:     "argo-cd",
		},
		{
			name:         "picks first github URL and ignores rest",
			repositories: []string{"https://github.com/org/first", "https://github.com/org/second"},
			wantOrg:      "org",
			wantRepo:     "first",
		},
		{
			name:         "skips non-github URLs",
			repositories: []string{"https://gitlab.com/org/repo", "https://github.com/org/repo"},
			wantOrg:      "org",
			wantRepo:     "repo",
		},
		{
			name:         "deep path — only org/repo extracted",
			repositories: []string{"https://github.com/org/repo/tree/main/subdir"},
			wantOrg:      "org",
			wantRepo:     "repo",
		},
		{
			name:         "no github URLs — error",
			repositories: []string{"https://gitlab.com/org/repo"},
			wantErr:      true,
		},
		{
			name:         "empty list — error",
			repositories: []string{},
			wantErr:      true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			org, repo, err := ParsePrimaryRepo(tt.repositories)
			if (err != nil) != tt.wantErr {
				t.Fatalf("err = %v, wantErr %v", err, tt.wantErr)
			}
			if err != nil {
				return
			}
			if org != tt.wantOrg {
				t.Errorf("org: got %q, want %q", org, tt.wantOrg)
			}
			if repo != tt.wantRepo {
				t.Errorf("repo: got %q, want %q", repo, tt.wantRepo)
			}
		})
	}
}

// ── BuildHealthCheckActivityLists ────────────────────────────────────────────

func TestBuildHealthCheckActivityLists(t *testing.T) {
	t0 := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	activity := map[string]*ActivitySummary{
		"alice": {Handle: "alice", Commits: 50, MergedPRs: 10, ReposTouched: []string{"repo"}, LastSeen: t0},
		"bob":   {Handle: "bob", Commits: 5, MergedPRs: 1, ReposTouched: []string{"repo"}, LastSeen: t0},
		"dave":  {Handle: "dave", Commits: 30, MergedPRs: 8, ReposTouched: []string{"repo"}, LastSeen: t0},
		"eve":   {Handle: "eve", Commits: 20, MergedPRs: 5, ReposTouched: []string{"repo"}, LastSeen: t0},
	}

	t.Run("maintainers sorted by activity desc", func(t *testing.T) {
		maintainers, _ := BuildHealthCheckActivityLists(activity, []string{"alice", "bob"}, 10)
		if len(maintainers) != 2 {
			t.Fatalf("got %d maintainers, want 2", len(maintainers))
		}
		if maintainers[0].Handle != "alice" {
			t.Errorf("expected alice first (most active), got %s", maintainers[0].Handle)
		}
	})

	t.Run("inactive maintainer still shown with zero activity", func(t *testing.T) {
		maintainers, _ := BuildHealthCheckActivityLists(activity, []string{"alice", "carol"}, 10)
		found := false
		for _, m := range maintainers {
			if m.Handle == "carol" && m.Commits == 0 && m.MergedPRs == 0 {
				found = true
			}
		}
		if !found {
			t.Error("expected carol with zero activity to appear in maintainer list")
		}
	})

	t.Run("top contributors excludes maintainers", func(t *testing.T) {
		_, top := BuildHealthCheckActivityLists(activity, []string{"alice", "bob"}, 10)
		for _, c := range top {
			if c.Handle == "alice" || c.Handle == "bob" {
				t.Errorf("maintainer %s should not appear in top contributors", c.Handle)
			}
		}
	})

	t.Run("top contributors capped at topN", func(t *testing.T) {
		_, top := BuildHealthCheckActivityLists(activity, []string{"alice"}, 1)
		if len(top) > 1 {
			t.Errorf("expected at most 1 top contributor, got %d", len(top))
		}
	})

	t.Run("top contributors sorted by activity desc", func(t *testing.T) {
		_, top := BuildHealthCheckActivityLists(activity, []string{"alice"}, 10)
		for i := 1; i < len(top); i++ {
			prev := top[i-1].Commits + top[i-1].MergedPRs
			curr := top[i].Commits + top[i].MergedPRs
			if curr > prev {
				t.Errorf("top contributors not sorted: %s(%d) before %s(%d)",
					top[i-1].Handle, prev, top[i].Handle, curr)
			}
		}
	})

	t.Run("team slugs excluded from top contributors", func(t *testing.T) {
		actWithSlug := map[string]*ActivitySummary{
			"alice":         {Handle: "alice", Commits: 5, MergedPRs: 1},
			"sig-approvers": {Handle: "sig-approvers", Commits: 100, MergedPRs: 50},
		}
		_, top := BuildHealthCheckActivityLists(actWithSlug, []string{}, 10)
		for _, c := range top {
			if c.Handle == "sig-approvers" {
				t.Error("team slug sig-approvers should be excluded from top contributors")
			}
		}
	})
}

// ── FormatActivityIssue ───────────────────────────────────────────────────────

func TestFormatActivityIssue(t *testing.T) {
	result := HealthCheckResult{
		ProjectID:              "myproject",
		Org:                    "myorg",
		TeamName:               "project-maintainers",
		IsStale:                true,
		DaysSinceUpdate:        200,
		StalenessDaysThreshold: 180,
		MentionHandles:         []string{"alice", "bob"},
		MaintainerActivity: []ActivitySummary{
			{Handle: "alice", Commits: 10, MergedPRs: 2, ReposTouched: []string{"myproject"},
				LastSeen: time.Date(2026, 1, 15, 0, 0, 0, 0, time.UTC)},
			{Handle: "bob", Commits: 0, MergedPRs: 0}, // zero LastSeen → "—"
		},
		TopNewContributors: []ActivitySummary{
			{Handle: "carol", Commits: 8, MergedPRs: 3, ReposTouched: []string{"myproject-sdk"}},
		},
		CheckedAt: time.Date(2026, 4, 29, 8, 0, 0, 0, time.UTC),
	}

	body := FormatActivityIssue(result)

	checks := []struct {
		desc     string
		mustHave string
	}{
		{"project ID in heading", "myproject"},
		{"mention alice in greeting", "@alice"},
		{"mention bob in greeting", "@bob"},
		{"greeting emoji", "👋"},
		{"staleness days", "200 days"},
		{"threshold days", "180 days"},
		{"maintainer alice in table", "| `@alice`"},
		{"maintainer bob (zero activity)", "| `@bob`"},
		{"alice last seen date", "2026-01-15"},
		{"bob last seen dash", "| — |"},
		{"top contributor carol", "@carol"},
		{"no auto-changes note", "No changes are required automatically"},
		{"activity window", "6 months"},
	}

	for _, c := range checks {
		t.Run(c.desc, func(t *testing.T) {
			if !strings.Contains(body, c.mustHave) {
				t.Errorf("issue body missing %q", c.mustHave)
			}
		})
	}
}

// ── isLikelyTeamSlug ─────────────────────────────────────────────────────────

func TestIsLikelyTeamSlug(t *testing.T) {
	tests := []struct {
		handle string
		want   bool
	}{
		// Should be filtered (team slugs)
		{"sig-release", true},
		{"sig-contributor-experience-approvers", true},
		{"wg-security", true},
		{"committee-steering", true},
		{"toc-bootstrap", true},
		{"tag-security", true},
		{"cncf-ambassador", true},
		{"k8s-infra-owners", true},
		{"core-approvers", true},
		{"repo-reviewers", true},
		{"project-maintainers", true},
		{"team-leads", true},
		{"org-members", true},
		{"cluster-admins", true},
		{"foo-bar-baz-qux", true}, // 4 segments
		// Should NOT be filtered (real usernames)
		{"alice", false},
		{"bob-smith", false}, // 2 segments — could be a username
		{"john-doe", false},  // common hyphenated username
		{"alice-bot", false}, // 2 segments, does not match any suffix
		{"thockin", false},
		{"liggitt", false},
	}

	for _, tt := range tests {
		t.Run(tt.handle, func(t *testing.T) {
			got := isLikelyTeamSlug(tt.handle)
			if got != tt.want {
				t.Errorf("isLikelyTeamSlug(%q) = %v, want %v", tt.handle, got, tt.want)
			}
		})
	}
}

// ── parseLinkNext ─────────────────────────────────────────────────────────────

func TestParseLinkNext(t *testing.T) {
	tests := []struct {
		name   string
		header string
		want   string
	}{
		{
			name:   "no header",
			header: "",
			want:   "",
		},
		{
			name:   "single next link",
			header: `<https://api.github.com/orgs/o/teams/t/members?page=2>; rel="next"`,
			want:   "https://api.github.com/orgs/o/teams/t/members?page=2",
		},
		{
			name:   "next and last links",
			header: `<https://api.github.com/page=2>; rel="next", <https://api.github.com/page=5>; rel="last"`,
			want:   "https://api.github.com/page=2",
		},
		{
			name:   "last page — no next",
			header: `<https://api.github.com/page=5>; rel="last"`,
			want:   "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := parseLinkNext(tt.header)
			if got != tt.want {
				t.Errorf("got %q, want %q", got, tt.want)
			}
		})
	}
}

// ── sortActivityDesc ──────────────────────────────────────────────────────────

func TestSortActivityDesc(t *testing.T) {
	summaries := []ActivitySummary{
		{Handle: "z", Commits: 1, MergedPRs: 0},
		{Handle: "a", Commits: 10, MergedPRs: 5},
		{Handle: "m", Commits: 5, MergedPRs: 5},
	}
	sortActivityDesc(summaries)

	if summaries[0].Handle != "a" {
		t.Errorf("expected 'a' first (total=15), got %s", summaries[0].Handle)
	}
	if summaries[1].Handle != "m" {
		t.Errorf("expected 'm' second (total=10), got %s", summaries[1].Handle)
	}

	// Tiebreaker: alphabetical handle
	tied := []ActivitySummary{
		{Handle: "zebra", Commits: 5, MergedPRs: 0},
		{Handle: "apple", Commits: 5, MergedPRs: 0},
	}
	sortActivityDesc(tied)
	if tied[0].Handle != "apple" {
		t.Errorf("expected alphabetical tiebreaker, got %s first", tied[0].Handle)
	}
}
