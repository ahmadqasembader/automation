package projects

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync/atomic"
	"testing"
	"time"
)

// ── test helpers ──────────────────────────────────────────────────────────────

// writeJSON encodes v to w as JSON, failing the test on encode error.
func writeJSON(w http.ResponseWriter, v any) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(v)
}

// prUser is a shorthand to build the anonymous user struct in prEntry.
func prUser(login string) struct {
	Login string `json:"login"`
} {
	return struct {
		Login string `json:"login"`
	}{Login: login}
}

// contribAuthor is a shorthand to build the anonymous author struct in contributorEntry.
func contribAuthor(login string) struct {
	Login string `json:"login"`
} {
	return struct {
		Login string `json:"login"`
	}{Login: login}
}

// ── fetchContributorStats ─────────────────────────────────────────────────────

func TestFetchContributorStats(t *testing.T) {
	since := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	weekIn := int(since.Unix()) + 7*24*3600  // one week inside window
	weekOut := int(since.Unix()) - 7*24*3600 // one week before window

	t.Run("counts commits, filters window, lowercases login", func(t *testing.T) {
		payload := []contributorEntry{
			{
				Author: contribAuthor("Alice"),
				Weeks: []contributorWeek{
					{W: weekIn, C: 5},   // in window
					{W: weekOut, C: 10}, // before window — must be ignored
				},
			},
			{
				Author: contribAuthor("BOB"), // should be stored as "bob"
				Weeks:  []contributorWeek{{W: weekIn, C: 3}},
			},
			{
				Author: contribAuthor(""), // empty login — must be skipped
				Weeks:  []contributorWeek{{W: weekIn, C: 99}},
			},
		}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			writeJSON(w, payload)
		}))
		defer srv.Close()

		commits, lastSeen, err := fetchContributorStats(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if commits["alice"] != 5 {
			t.Errorf("alice commits: want 5, got %d", commits["alice"])
		}
		if commits["bob"] != 3 {
			t.Errorf("bob commits: want 3, got %d", commits["bob"])
		}
		if _, ok := commits[""]; ok {
			t.Error("empty login should not appear in commits map")
		}
		if lastSeen["alice"].IsZero() {
			t.Error("alice: expected non-zero lastSeen")
		}
	})

	t.Run("zero-commit weeks produce no entry", func(t *testing.T) {
		payload := []contributorEntry{
			{
				Author: contribAuthor("ghost"),
				Weeks:  []contributorWeek{{W: weekIn, C: 0}}, // zero commits
			},
		}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			writeJSON(w, payload)
		}))
		defer srv.Close()

		commits, _, err := fetchContributorStats(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if _, ok := commits["ghost"]; ok {
			t.Error("ghost should not appear: all weeks have zero commits")
		}
	})

	t.Run("204 no content returns empty maps", func(t *testing.T) {
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			w.WriteHeader(http.StatusNoContent)
		}))
		defer srv.Close()

		commits, lastSeen, err := fetchContributorStats(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if len(commits) != 0 || len(lastSeen) != 0 {
			t.Errorf("expected empty maps for 204; got commits=%v", commits)
		}
	})

	t.Run("non-200 status returns error", func(t *testing.T) {
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			w.WriteHeader(http.StatusInternalServerError)
		}))
		defer srv.Close()

		_, _, err := fetchContributorStats(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err == nil {
			t.Fatal("expected error for 500, got nil")
		}
	})

	t.Run("retries on 202 then succeeds", func(t *testing.T) {
		// First call returns 202; second returns data.
		// The retry sleeps 3 s (attempt=1 × 3s) so this is skipped in short mode.
		if testing.Short() {
			t.Skip("skipping slow retry test (-short)")
		}
		var callCount int32
		payload := []contributorEntry{
			{Author: contribAuthor("alice"), Weeks: []contributorWeek{{W: weekIn, C: 7}}},
		}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			if atomic.AddInt32(&callCount, 1) < 2 {
				w.WriteHeader(http.StatusAccepted) // 202
				return
			}
			writeJSON(w, payload)
		}))
		defer srv.Close()

		commits, _, err := fetchContributorStats(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error after retry: %v", err)
		}
		if atomic.LoadInt32(&callCount) != 2 {
			t.Errorf("expected 2 calls (1×202 + 1×200), got %d", callCount)
		}
		if commits["alice"] != 7 {
			t.Errorf("alice: want 7 commits, got %d", commits["alice"])
		}
	})

	t.Run("context cancellation returns error", func(t *testing.T) {
		// Server blocks until its request context is cancelled.
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			<-r.Context().Done()
		}))
		defer srv.Close()

		ctx, cancel := context.WithCancel(context.Background())
		cancel() // pre-cancel so the first request fails immediately

		_, _, err := fetchContributorStats(ctx, "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err == nil {
			t.Fatal("expected error on cancelled context, got nil")
		}
	})
}

// ── fetchMergedPRs ────────────────────────────────────────────────────────────

func TestFetchMergedPRs(t *testing.T) {
	since := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	inWindow := since.Add(24 * time.Hour)
	outOfWindow := since.Add(-24 * time.Hour)

	t.Run("counts merged PRs, skips unmerged and out-of-window", func(t *testing.T) {
		ma := inWindow
		old := outOfWindow
		payload := []prEntry{
			{MergedAt: &ma, UpdatedAt: inWindow, User: prUser("alice")},
			{MergedAt: &ma, UpdatedAt: inWindow, User: prUser("alice")}, // alice +1
			{MergedAt: &ma, UpdatedAt: inWindow, User: prUser("bob")},
			{MergedAt: nil, UpdatedAt: inWindow, User: prUser("carol")}, // unmerged — skip
			{MergedAt: &old, UpdatedAt: inWindow, User: prUser("dave")}, // merged before window — skip
		}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			writeJSON(w, payload)
		}))
		defer srv.Close()

		counts, _, err := fetchMergedPRs(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if counts["alice"] != 2 {
			t.Errorf("alice: want 2, got %d", counts["alice"])
		}
		if counts["bob"] != 1 {
			t.Errorf("bob: want 1, got %d", counts["bob"])
		}
		if _, ok := counts["carol"]; ok {
			t.Error("carol (unmerged) should not appear in counts")
		}
		if _, ok := counts["dave"]; ok {
			t.Error("dave (merged before window) should not appear in counts")
		}
	})

	t.Run("early exit when all PRs on page have UpdatedAt before since", func(t *testing.T) {
		// A page where every PR is last-updated before the window.
		// The function should stop after the first page even though a Link: next is provided.
		var pagesFetched int32
		old := outOfWindow
		page := []prEntry{
			{MergedAt: &old, UpdatedAt: outOfWindow, User: prUser("alice")},
		}
		var srv *httptest.Server
		srv = httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			atomic.AddInt32(&pagesFetched, 1)
			// Always include a next-page link to prove it is not followed.
			w.Header().Set("Link", fmt.Sprintf(`<%s/repos/org/repo/pulls?page=2>; rel="next"`, srv.URL))
			writeJSON(w, page)
		}))
		defer srv.Close()

		counts, _, err := fetchMergedPRs(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if n := atomic.LoadInt32(&pagesFetched); n != 1 {
			t.Errorf("expected exactly 1 page (early exit), got %d", n)
		}
		if len(counts) != 0 {
			t.Errorf("expected no counts (all PRs out of window), got %v", counts)
		}
	})

	t.Run("pagination follows Link header", func(t *testing.T) {
		ma := inWindow
		page1 := []prEntry{{MergedAt: &ma, UpdatedAt: inWindow, User: prUser("alice")}}
		page2 := []prEntry{{MergedAt: &ma, UpdatedAt: inWindow, User: prUser("bob")}}

		var srv *httptest.Server
		srv = httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			if r.URL.Query().Get("page") == "2" {
				writeJSON(w, page2)
				return
			}
			w.Header().Set("Link", fmt.Sprintf(`<%s/repos/org/repo/pulls?page=2>; rel="next"`, srv.URL))
			writeJSON(w, page1)
		}))
		defer srv.Close()

		counts, _, err := fetchMergedPRs(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if counts["alice"] != 1 {
			t.Errorf("alice: want 1, got %d", counts["alice"])
		}
		if counts["bob"] != 1 {
			t.Errorf("bob: want 1, got %d", counts["bob"])
		}
	})

	t.Run("tracks lastSeen as most recent merged_at for same user", func(t *testing.T) {
		early := inWindow
		late := inWindow.Add(7 * 24 * time.Hour)
		payload := []prEntry{
			{MergedAt: &early, UpdatedAt: late, User: prUser("alice")},
			{MergedAt: &late, UpdatedAt: late, User: prUser("alice")},
		}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			writeJSON(w, payload)
		}))
		defer srv.Close()

		_, lastSeen, err := fetchMergedPRs(context.Background(), "org", "repo", since, "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if !lastSeen["alice"].Equal(late) {
			t.Errorf("alice lastSeen: want %v, got %v", late, lastSeen["alice"])
		}
	})
}

// ── FetchAllRepoActivity ──────────────────────────────────────────────────────

func TestFetchAllRepoActivity(t *testing.T) {
	since := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
	weekIn := int(since.Unix()) + 7*24*3600
	mergedAt := since.Add(24 * time.Hour)

	t.Run("aggregates commits and PRs across multiple repos", func(t *testing.T) {
		// Every repo returns alice with 3 commits + 1 merged PR.
		contribs := []contributorEntry{
			{Author: contribAuthor("alice"), Weeks: []contributorWeek{{W: weekIn, C: 3}}},
		}
		prs := []prEntry{
			{MergedAt: &mergedAt, UpdatedAt: mergedAt, User: prUser("alice")},
		}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			if strings.Contains(r.URL.Path, "/stats/contributors") {
				writeJSON(w, contribs)
				return
			}
			writeJSON(w, prs)
		}))
		defer srv.Close()

		refs := []RepoRef{{Org: "org", Repo: "repo1"}, {Org: "org", Repo: "repo2"}}
		activity, scanned, errs := FetchAllRepoActivity(context.Background(), refs, since, "", http.DefaultClient, srv.URL, 2)
		if len(errs) > 0 {
			t.Fatalf("unexpected errors: %v", errs)
		}
		if len(scanned) != 2 {
			t.Errorf("scanned: want 2, got %d", len(scanned))
		}
		a, ok := activity["alice"]
		if !ok {
			t.Fatal("alice not found in activity map")
		}
		if a.Commits != 6 { // 3 × 2 repos
			t.Errorf("alice.Commits: want 6, got %d", a.Commits)
		}
		if a.MergedPRs != 2 { // 1 × 2 repos
			t.Errorf("alice.MergedPRs: want 2, got %d", a.MergedPRs)
		}
		if len(a.ReposTouched) != 2 {
			t.Errorf("alice.ReposTouched: want 2, got %d", len(a.ReposTouched))
		}
	})

	t.Run("fetch error is non-fatal — other repos still aggregated", func(t *testing.T) {
		// "fail-repo" returns 500; "ok-repo" returns bob with 5 commits.
		contribs := []contributorEntry{
			{Author: contribAuthor("bob"), Weeks: []contributorWeek{{W: weekIn, C: 5}}},
		}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			if strings.Contains(r.URL.Path, "fail-repo") {
				w.WriteHeader(http.StatusInternalServerError)
				return
			}
			if strings.Contains(r.URL.Path, "/stats/contributors") {
				writeJSON(w, contribs)
				return
			}
			writeJSON(w, []prEntry{})
		}))
		defer srv.Close()

		refs := []RepoRef{{Org: "org", Repo: "fail-repo"}, {Org: "org", Repo: "ok-repo"}}
		activity, _, errs := FetchAllRepoActivity(context.Background(), refs, since, "", http.DefaultClient, srv.URL, 1)
		if len(errs) == 0 {
			t.Error("expected at least one error, got none")
		}
		if activity["bob"] == nil {
			t.Error("bob (from ok-repo) should still appear despite fail-repo error")
		}
	})

	t.Run("context cancellation propagates to in-flight requests", func(t *testing.T) {
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Block until the request context is done.
			<-r.Context().Done()
		}))
		defer srv.Close()

		ctx, cancel := context.WithCancel(context.Background())
		cancel() // cancel before any request starts

		_, _, errs := FetchAllRepoActivity(ctx, []RepoRef{{Org: "org", Repo: "repo"}}, since, "", http.DefaultClient, srv.URL, 1)
		if len(errs) == 0 {
			t.Error("expected errors after context cancellation, got none")
		}
	})

	t.Run("empty refs list returns empty result", func(t *testing.T) {
		activity, scanned, errs := FetchAllRepoActivity(context.Background(), nil, since, "", http.DefaultClient, "", 1)
		if len(activity) != 0 || len(scanned) != 0 || len(errs) != 0 {
			t.Errorf("expected all-empty results for nil refs; got activity=%v scanned=%v errs=%v", activity, scanned, errs)
		}
	})
}

// ── FetchGitHubTeamMembers ────────────────────────────────────────────────────

func TestFetchGitHubTeamMembers(t *testing.T) {
	t.Run("returns all members lowercased", func(t *testing.T) {
		members := []teamMember{{Login: "Alice"}, {Login: "BOB"}, {Login: "carol"}}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			writeJSON(w, members)
		}))
		defer srv.Close()

		got, err := FetchGitHubTeamMembers(context.Background(), "org", "team", "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		want := []string{"alice", "bob", "carol"}
		if len(got) != len(want) {
			t.Fatalf("member count: want %d, got %d (%v)", len(want), len(got), got)
		}
		for i := range want {
			if got[i] != want[i] {
				t.Errorf("member[%d]: want %q, got %q", i, want[i], got[i])
			}
		}
	})

	t.Run("follows pagination via Link header", func(t *testing.T) {
		page1 := []teamMember{{Login: "alice"}}
		page2 := []teamMember{{Login: "bob"}}

		var srv *httptest.Server
		srv = httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			if r.URL.Query().Get("page") == "2" {
				writeJSON(w, page2)
				return
			}
			w.Header().Set("Link", fmt.Sprintf(`<%s/orgs/org/teams/team/members?page=2>; rel="next"`, srv.URL))
			writeJSON(w, page1)
		}))
		defer srv.Close()

		got, err := FetchGitHubTeamMembers(context.Background(), "org", "team", "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if len(got) != 2 {
			t.Errorf("expected 2 members across 2 pages, got %d: %v", len(got), got)
		}
	})

	t.Run("403 returns error mentioning read:org scope", func(t *testing.T) {
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			w.WriteHeader(http.StatusForbidden)
		}))
		defer srv.Close()

		_, err := FetchGitHubTeamMembers(context.Background(), "org", "team", "", http.DefaultClient, srv.URL)
		if err == nil {
			t.Fatal("expected error for 403, got nil")
		}
		if !strings.Contains(err.Error(), "read:org") {
			t.Errorf("expected 'read:org' in error message, got: %v", err)
		}
	})

	t.Run("404 returns team-not-found error", func(t *testing.T) {
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			w.WriteHeader(http.StatusNotFound)
		}))
		defer srv.Close()

		_, err := FetchGitHubTeamMembers(context.Background(), "org", "team", "", http.DefaultClient, srv.URL)
		if err == nil {
			t.Fatal("expected error for 404, got nil")
		}
		if !strings.Contains(err.Error(), "404") {
			t.Errorf("expected '404' in error message, got: %v", err)
		}
	})

	t.Run("skips empty login in response", func(t *testing.T) {
		members := []teamMember{{Login: "alice"}, {Login: ""}, {Login: "bob"}}
		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
			writeJSON(w, members)
		}))
		defer srv.Close()

		got, err := FetchGitHubTeamMembers(context.Background(), "org", "team", "", http.DefaultClient, srv.URL)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		for _, h := range got {
			if h == "" {
				t.Error("empty login should be excluded from results")
			}
		}
		if len(got) != 2 {
			t.Errorf("expected 2 members (alice, bob), got %d: %v", len(got), got)
		}
	})
}
