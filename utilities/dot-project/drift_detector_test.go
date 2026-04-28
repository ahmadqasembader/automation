package projects

import (
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

// ── DetectDrift ───────────────────────────────────────────────────────────────

func TestDetectDrift(t *testing.T) {
	tests := []struct {
		name            string
		projectHandles  []string
		upstreamHandles []string
		wantAdded       []string
		wantRemoved     []string
	}{
		{
			name:            "no drift — identical sets",
			projectHandles:  []string{"alice", "bob"},
			upstreamHandles: []string{"alice", "bob"},
			wantAdded:       nil,
			wantRemoved:     nil,
		},
		{
			name:            "upstream adds a handle",
			projectHandles:  []string{"alice"},
			upstreamHandles: []string{"alice", "carol"},
			wantAdded:       []string{"carol"},
			wantRemoved:     nil,
		},
		{
			name:            "upstream removes a handle",
			projectHandles:  []string{"alice", "bob"},
			upstreamHandles: []string{"alice"},
			wantAdded:       nil,
			wantRemoved:     []string{"bob"},
		},
		{
			name:            "both added and removed",
			projectHandles:  []string{"alice", "bob"},
			upstreamHandles: []string{"alice", "carol"},
			wantAdded:       []string{"carol"},
			wantRemoved:     []string{"bob"},
		},
		{
			name:            "case-insensitive comparison",
			projectHandles:  []string{"Alice", "BOB"},
			upstreamHandles: []string{"alice", "bob"},
			wantAdded:       nil,
			wantRemoved:     nil,
		},
		{
			name:            "empty upstream — all project handles flagged removed",
			projectHandles:  []string{"alice", "bob"},
			upstreamHandles: []string{},
			wantAdded:       nil,
			wantRemoved:     []string{"alice", "bob"},
		},
		{
			name:            "empty project — all upstream handles flagged added",
			projectHandles:  []string{},
			upstreamHandles: []string{"alice", "bob"},
			wantAdded:       []string{"alice", "bob"},
			wantRemoved:     nil,
		},
		{
			name:            "both empty — no drift",
			projectHandles:  []string{},
			upstreamHandles: []string{},
			wantAdded:       nil,
			wantRemoved:     nil,
		},
		{
			name:            "results are sorted",
			projectHandles:  []string{"zebra", "apple"},
			upstreamHandles: []string{"mango", "apple"},
			wantAdded:       []string{"mango"},
			wantRemoved:     []string{"zebra"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			added, removed := DetectDrift(tt.projectHandles, tt.upstreamHandles)
			if !reflect.DeepEqual(added, tt.wantAdded) {
				t.Errorf("added: got %v, want %v", added, tt.wantAdded)
			}
			if !reflect.DeepEqual(removed, tt.wantRemoved) {
				t.Errorf("removed: got %v, want %v", removed, tt.wantRemoved)
			}
		})
	}
}

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

// ── PatchMaintainersYAML ─────────────────────────────────────────────────────

func TestPatchMaintainersYAML(t *testing.T) {
	const original = `# Header comment
# second line

maintainers:
  - project_id: "proj"
    org: "myorg"
    teams:
      - name: "project-maintainers"
        members:
          - alice
          - bob
      - name: "reviewers"
        members:
          - dave
`

	dir := t.TempDir()
	write := func(content string) string {
		p := filepath.Join(dir, "maintainers.yaml")
		_ = os.WriteFile(p, []byte(content), 0o644)
		return p
	}

	t.Run("removes a handle", func(t *testing.T) {
		p := write(original)
		out, err := PatchMaintainersYAML(p, "project-maintainers", nil, []string{"bob"})
		if err != nil {
			t.Fatal(err)
		}
		s := string(out)
		if contains(s, "bob") {
			t.Error("expected bob to be removed")
		}
		if !contains(s, "alice") {
			t.Error("expected alice to be retained")
		}
		// Other teams untouched
		if !contains(s, "dave") {
			t.Error("expected dave (reviewers team) to be retained")
		}
	})

	t.Run("adds a handle", func(t *testing.T) {
		p := write(original)
		out, err := PatchMaintainersYAML(p, "project-maintainers", []string{"carol"}, nil)
		if err != nil {
			t.Fatal(err)
		}
		s := string(out)
		if !contains(s, "carol") {
			t.Error("expected carol to be added")
		}
		if !contains(s, "alice") || !contains(s, "bob") {
			t.Error("expected existing members to be retained")
		}
	})

	t.Run("add and remove in one pass", func(t *testing.T) {
		p := write(original)
		out, err := PatchMaintainersYAML(p, "project-maintainers", []string{"carol"}, []string{"bob"})
		if err != nil {
			t.Fatal(err)
		}
		s := string(out)
		if contains(s, "bob") {
			t.Error("expected bob to be removed")
		}
		if !contains(s, "carol") {
			t.Error("expected carol to be added")
		}
	})

	t.Run("no-op preserves all members", func(t *testing.T) {
		p := write(original)
		out, err := PatchMaintainersYAML(p, "project-maintainers", nil, nil)
		if err != nil {
			t.Fatal(err)
		}
		s := string(out)
		if !contains(s, "alice") || !contains(s, "bob") {
			t.Error("expected no members to be removed on no-op")
		}
	})

	t.Run("header comments are preserved", func(t *testing.T) {
		p := write(original)
		out, err := PatchMaintainersYAML(p, "project-maintainers", nil, nil)
		if err != nil {
			t.Fatal(err)
		}
		s := string(out)
		if !contains(s, "# Header comment") {
			t.Error("expected header comment to be preserved")
		}
	})

	t.Run("output uses 2-space indentation", func(t *testing.T) {
		p := write(original)
		out, err := PatchMaintainersYAML(p, "project-maintainers", []string{"carol"}, nil)
		if err != nil {
			t.Fatal(err)
		}
		// The YAML body should NOT contain 4-space-indented list items.
		if contains(string(out), "    - project_id") {
			t.Error("expected 2-space indentation, got 4-space")
		}
	})

	t.Run("add is idempotent — no duplicate on re-add", func(t *testing.T) {
		p := write(original)
		out, err := PatchMaintainersYAML(p, "project-maintainers", []string{"alice"}, nil)
		if err != nil {
			t.Fatal(err)
		}
		count := countOccurrences(string(out), "alice")
		if count != 1 {
			t.Errorf("expected alice to appear exactly once, got %d", count)
		}
	})
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

// ── helpers ───────────────────────────────────────────────────────────────────

func contains(s, substr string) bool {
	return len(s) > 0 && len(substr) > 0 &&
		(s == substr || len(s) >= len(substr) &&
			func() bool {
				for i := 0; i <= len(s)-len(substr); i++ {
					if s[i:i+len(substr)] == substr {
						return true
					}
				}
				return false
			}())
}

func countOccurrences(s, substr string) int {
	count := 0
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			count++
		}
	}
	return count
}
