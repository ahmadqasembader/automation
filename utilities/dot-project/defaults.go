package projects

import "time"

// Centralized runtime config defaults for the dot-project tooling.

const (
	// DefaultHTTPTimeout is the timeout applied to all outbound HTTP
	// clients (validator, bootstrap sources, etc.).
	DefaultHTTPTimeout = 30 * time.Second

	// DefaultStalenessThresholdDays is the number of days after which a
	// project's maintainer data is considered stale.
	DefaultStalenessThresholdDays = 180

	// DefaultActivityWindowMonths is how far back (in months) the maintainer
	// health check looks when measuring contributor activity.
	DefaultActivityWindowMonths = 6

	// DefaultConcurrency is the maximum number of GitHub API repo fetches
	// that the maintainer health check runs in parallel.  Keeps total
	// inflight requests well inside GitHub's 5 000 req/hr REST limit even
	// for very large projects (Kubernetes-scale).
	DefaultConcurrency = 10

	// DefaultTopContributors is how many non-maintainer contributors to
	// surface in the health-check issue body.
	DefaultTopContributors = 5

	// DefaultDCOCommitSampleSize is how many recent commits we fetch when
	// detecting whether a repo uses DCO (Signed-off-by).
	DefaultDCOCommitSampleSize = 20

	// DefaultDCOSignedRatio is the minimum ratio of Signed-off-by commits
	// to total sampled commits before we consider DCO "enabled".
	DefaultDCOSignedRatio = 0.5

	// DefaultFuzzyMatchWeight is the weight applied to partial word-match
	// scores when fuzzy-matching project names against landscape entries.
	DefaultFuzzyMatchWeight = 0.5

	// defaultGitHubAPIURL is the base URL for the GitHub REST API.
	// It is kept unexported because callers pass it as an override parameter;
	// "" (empty string) is the idiomatic "use the default" sentinel.
	defaultGitHubAPIURL = "https://api.github.com"
)
