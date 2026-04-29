# AGENT.md - dot-project Validator

## Project Overview

This is a Go-based utility for validating CNCF project metadata and maintainer rosters. It validates project YAML manifests against structured schema requirements, reconciles maintainer lists against canonical sources, surfaces changes via cached diffs, converts project metadata to CNCF landscape format, checks maintainer data staleness, and audits URL accessibility in project references.

## Repository Structure

```
utilities/dot-project/
├── cmd/
│   ├── validator/              # Main CLI validator tool
│   ├── landscape-updater/      # Tool to convert project.yaml to landscape format
│   ├── staleness-checker/      # Tool to check maintainer data freshness
│   ├── audit-checker/          # Tool to verify referenced URLs are accessible
│   ├── bootstrap/              # Tool to auto-generate project scaffolds from external data
│   └── drift/                  # Maintainer health-check tool (opens GitHub issues for stale maintainers.yaml)
├── template/                   # Template files for new .project repositories
│   ├── project.yaml
│   ├── maintainers.yaml
│   ├── .github/workflows/validate.yaml
│   └── .github/workflows/maintainer-drift.yml  # Scaffolded health-check workflow
├── example/                    # Realistic filled-in example (Kubernetes-like)
│   ├── project.yaml
│   ├── maintainers.yaml
│   ├── .github/workflows/validate.yaml
│   └── maintainer-health-check-issue.md  # Reference rendering of a health-check issue
├── testdata/                   # Test fixtures and sample configs
├── bin/                        # Build output (gitignored)
├── .cache/                     # Validation cache directory (gitignored)
├── types.go                    # Core type definitions (Project, Maintainer, Config, etc.)
├── bootstrap_types.go          # Bootstrap intermediate types (BootstrapResult, API data structs)
├── bootstrap_parsers.go        # CODEOWNERS, OWNERS, MAINTAINERS file parsers
├── bootstrap_sources.go        # Landscape/CLOMonitor/GitHub API clients, fuzzy matching, data merge
├── bootstrap_scaffold.go       # Scaffold generator (project.yaml, maintainers.yaml templates)
├── drift_detector.go           # Issue formatter, sortActivityDesc, formatRepoList
├── drift_sources.go            # GitHub API fetching: multi-repo activity, PR pagination, team members
├── drift_detector_test.go      # Tests for drift detection and formatting
├── validator.go                # Project validation logic
├── maintainers.go              # Maintainer validation logic with LFX integration
├── landscape.go                # Landscape entry conversion and comparison
├── staleness.go                # Maintainer staleness detection
├── audit.go                    # URL accessibility audit
├── validator_test.go           # Core validation tests
├── bootstrap_parsers_test.go   # CODEOWNERS/OWNERS/MAINTAINERS parser tests
├── bootstrap_sources_test.go   # Landscape/CLOMonitor/GitHub client, fuzzy match, merge tests
├── bootstrap_scaffold_test.go  # Scaffold generation and WriteScaffold tests
├── security_test.go            # Security contact email validation tests
├── social_test.go              # Social links URL validation tests
├── landscape_test.go           # Landscape conversion and diff tests
├── staleness_test.go           # Staleness detection tests
├── audit_test.go               # URL audit tests
├── integration_test.go         # YAML fixture integration tests
├── test_helpers_test.go        # Shared test helpers (validBaseProject, etc.)
├── Dockerfile                  # Multi-stage Docker build
├── Makefile                    # Build and development tasks
├── SCHEMA.md                   # Formal schema specification
└── README.md                   # User documentation
```

### Related GitHub Actions (parent repo `.github/`)

```
.github/
├── actions/
│   ├── validate-maintainers/   # Reusable action for maintainer validation
│   └── validate-project/       # Reusable action for project validation
└── workflows/
    ├── project-validator.yml                  # Main CI workflow for this tool
    ├── validate-maintainers.yaml              # Validates maintainers on PR
    └── reusable-validate-maintainers.yaml     # Reusable workflow for external repos
```

## Build and Development

### Prerequisites

- Go 1.24+
- Docker (optional, for containerized builds)

### Build Commands

```bash
# Build validator binary (outputs to bin/)
make build

# Run tests
make test

# Run tests with coverage
make test-coverage

# Format code
make fmt

# Run linter (requires golangci-lint)
make lint

# Build Docker image
docker build -t dot-project-validator .

# Clean build artifacts
make clean
```

Note: The Makefile `build` target builds the `validator`, `landscape-updater`, and `bootstrap` binaries. The other CLI tools (`staleness-checker`, `audit-checker`, `drift`) must be built manually:

```bash
go build -o bin/landscape-updater ./cmd/landscape-updater
go build -o bin/staleness-checker ./cmd/staleness-checker
go build -o bin/audit-checker ./cmd/audit-checker
go build -o bin/drift ./cmd/drift
```

### Running the Validator

```bash
# Default run (validates projects and maintainers)
make run

# Or directly:
./bin/validator --config testdata/projectlist.yaml --maintainers testdata/maintainers.yaml

# Skip maintainer validation
./bin/validator --config testdata/projectlist.yaml --maintainers ""

# With external verification enabled
./bin/validator --verify-maintainers

# Diff validation (only verify new/changed maintainers)
./bin/validator --maintainers maintainers.yaml --base-maintainers previous-maintainers.yaml

# Output formats: text (default), json, yaml
./bin/validator --config testdata/projectlist.yaml --output json
```

### Running the Landscape Updater

Converts a `project.yaml` to CNCF landscape entry format. Validates the project first, then outputs the landscape entry.

```bash
./bin/landscape-updater --project path/to/project.yaml

# With landscape file for comparison (comparison not yet fully implemented)
./bin/landscape-updater --project project.yaml --landscape landscape.yml

# Output formats: text (default), json, yaml
./bin/landscape-updater --project project.yaml --output yaml

# Dry run is on by default
./bin/landscape-updater --project project.yaml --dry-run=false
```

### Running the Bootstrap Tool

Auto-generates `project.yaml` and `maintainers.yaml` scaffolds by fetching data from CLOMonitor, GitHub API, and the CNCF landscape. Discovers maintainer handles from CODEOWNERS, OWNERS, and MAINTAINERS files.

```bash
# Dry run: preview generated YAML
./bin/bootstrap -name "My Project" -github-org my-org -dry-run

# Generate scaffold in current directory
./bin/bootstrap -name "My Project" -github-org my-org -github-repo my-repo

# Generate into a specific directory
./bin/bootstrap -name "Envoy" -github-org envoyproxy -github-repo envoy -output-dir /tmp/envoy

# Skip landscape fetch (CLOMonitor + GitHub only)
./bin/bootstrap -name "My Project" -github-org my-org -skip-landscape

# Skip CLOMonitor (landscape + GitHub only)
./bin/bootstrap -github-org my-org -skip-clomonitor

# With GitHub token for higher rate limits
GITHUB_TOKEN=ghp_xxx ./bin/bootstrap -name "My Project" -github-org my-org
```

**bootstrap** (`cmd/bootstrap/main.go`):
- `-name` - Project display name to search for
- `-github-org` - GitHub organization
- `-github-repo` - Primary repository name (defaults to org name)
- `-github-token` - GitHub token (or set `GITHUB_TOKEN` env)
- `-output-dir` - Directory for scaffold output (default: `.`)
- `-skip-landscape` - Skip CNCF landscape YAML lookup (default: false)
- `-skip-clomonitor` - Skip CLOMonitor API lookup (default: false)
- `-skip-github` - Skip GitHub API lookup (default: false)
- `-dry-run` - Print generated YAML without writing files (default: false)

### Running the Staleness Checker

Checks if a project's maintainer data has become stale based on a configurable threshold.

```bash
./bin/staleness-checker --project path/to/project.yaml

# Custom threshold (default: 180 days)
./bin/staleness-checker --project project.yaml --threshold 90

# Override last update date instead of using file modification time
./bin/staleness-checker --project project.yaml --last-update 2025-01-15

# Output formats: text (default), json, yaml
./bin/staleness-checker --project project.yaml --output json
```

Exit code 1 if the project is stale.

### Running the Audit Checker

Verifies that all URLs referenced in a project (website, artwork, repositories, audit reports, security/governance/documentation paths) are accessible via HTTP HEAD requests.

```bash
./bin/audit-checker --project path/to/project.yaml

# Custom HTTP timeout (default: 10 seconds)
./bin/audit-checker --project project.yaml --timeout 30

# Output formats: text (default), json, yaml
./bin/audit-checker --project project.yaml --output json
```

Exit code 1 if any URL check fails.

### Running the Maintainer Health-Check (drift)

Fires when `maintainers.yaml` has not been updated in more than the configured number of days. Fetches contributor activity across all repos in `project.yaml` and writes a Markdown issue body.

```bash
# Check staleness and print issue body to stdout
./bin/drift \
  -project-yaml project.yaml \
  -maintainers-yaml maintainers.yaml \
  -last-updated-days 194

# Write issue body to a file (used by the GitHub Actions workflow)
./bin/drift \
  -project-yaml project.yaml \
  -maintainers-yaml maintainers.yaml \
  -last-updated-days 194 \
  -report /tmp/health-report.md

# Custom staleness threshold (default: 180 days)
./bin/drift -last-updated-days 200 -staleness-days 90

# Adjust activity window and concurrency
./bin/drift -activity-months 3 -concurrency 5 -top-contributors 10
```

**drift** (`cmd/drift/main.go`):
- `-project-yaml` — Path to `project.yaml` (default: `project.yaml`)
- `-maintainers-yaml` — Path to `maintainers.yaml` (default: `maintainers.yaml`)
- `-github-token` — GitHub PAT (or set `GITHUB_TOKEN` env var)
- `-team` — Team name in `maintainers.yaml` to read (default: `project-maintainers`)
- `-report` — Write Markdown issue body to this file path (default: stdout)
- `-staleness-days` — Days without update before the health-check fires (default: `180`)
- `-last-updated-days` — Days since `maintainers.yaml` was last git-committed (`-1` = use file mtime)
- `-activity-months` — How many months back to look for contributor activity (default: `6`)
- `-concurrency` — Max parallel GitHub API repo fetches (default: `10`)
- `-top-contributors` — How many non-maintainer contributors to surface (default: `5`)

Exit codes: `0` = not stale; `1` = stale (issue body written); `2` = fatal error.

## Testing

### Test Commands

```bash
# Run all tests
go test -v

# Run specific test
go test -v -run TestValidator

# Run with coverage
go test -v -coverprofile=coverage.out
go tool cover -html=coverage.out -o coverage.html
```

### Test Files

- `validator_test.go` - Core validation tests (project structure, maturity log, repositories, hashing)
- `security_test.go` - Security contact email validation tests
- `social_test.go` - Social links URL validation tests
- `landscape_test.go` - Landscape entry conversion and diff comparison tests
- `staleness_test.go` - Staleness detection threshold tests
- `audit_test.go` - URL accessibility audit tests
- `integration_test.go` - YAML fixture integration tests (loads files from `testdata/` and `example/`)
- `test_helpers_test.go` - Shared test helpers (`validBaseProject()` factory function)

### Test Patterns

Tests use table-driven patterns with `validBaseProject()` as a baseline. Tests modify only the fields relevant to their case:

```go
func TestSomething(t *testing.T) {
    project := validBaseProject()
    project.Name = "" // override to trigger validation error

    errors := ValidateProjectStruct(project)
    expectedErrors := []string{
        "expected error message",
    }

    for _, expectedError := range expectedErrors {
        found := false
        for _, err := range errors {
            if err == expectedError {
                found = true
                break
            }
        }
        if !found {
            t.Errorf("Expected error '%s' not found in: %v", expectedError, errors)
        }
    }
}
```

## Code Style and Conventions

### Go Conventions

- Package name: `projects`
- Go version: 1.24+ (see `go.mod`)
- Use standard Go formatting (`go fmt`)
- Error messages should be lowercase and descriptive
- Use `fmt.Errorf` with `%w` for error wrapping
- Struct tags include both `json` and `yaml` for serialization
- YAML decoding uses `decoder.KnownFields(true)` to reject unknown fields

### Type Definitions

All core types are defined in `types.go`:
- `Project` - Main project metadata structure with nested config types
- `SecurityConfig`, `GovernanceConfig`, `LegalConfig`, `DocumentationConfig` - Nested project config sections
- `LandscapeConfig` - CNCF landscape category/subcategory mapping
- `PathRef` - Reusable path reference (used by security, governance, documentation configs)
- `MaturityEntry` - Phase, date, and issue URL for maturity log entries
- `Audit` - Security audit record (date, type, URL)
- `MaintainerEntry` / `MaintainersConfig` - Maintainer definitions with teams
- `Team` - GitHub team name and member handles
- `ValidationResult` / `MaintainerValidationResult` - Validation output types
- `Config`, `Cache`, `CacheEntry` - Configuration and caching types
- `ProjectValidator` - Main validator struct (wraps config, cache, HTTP client)
- `ProjectListEntry` / `ProjectListConfig` - Project list configuration

Additional types in domain-specific files:
- `LandscapeEntry`, `LandscapeDiff`, `LandscapeChange` - in `landscape.go`
- `StalenessResult` - in `staleness.go`
- `AuditResult`, `AuditCheck` - in `audit.go`
- `BootstrapConfig`, `BootstrapResult`, `CLOMonitorProject`, `CLOMonitorRepo`, `CLOMonitorReport`, `CLOMonitorScore` - in `bootstrap_types.go`
- `GitHubRepoData`, `GitHubOrgData`, `GitHubCommunityProfile`, `GitHubContentEntry` - in `bootstrap_types.go`
- `GitHubData`, `LandscapeData` - in `bootstrap_sources.go`

### Validation Logic

- `validator.go` contains project validation (`ValidateProjectStruct`) and the `ProjectValidator` type with `ValidateAll`, `FormatResults`, `NewValidator`
- `maintainers.go` contains maintainer validation with optional LFX integration and handle normalization
- `landscape.go` contains `ProjectToLandscapeEntry`, `CompareLandscapeEntries`, `LoadProjectFromFile`
- `staleness.go` contains `CheckStaleness` and `FormatStalenessResults`
- `audit.go` contains `AuditProject` and `FormatAuditResult`
- Handle normalization strips whitespace and leading `@` symbols
- All URLs are validated for proper format
- Email addresses use `net/mail.ParseAddress` for validation

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `REPO_ROOT` | Repository root for resolving relative `file://` paths in project list config |
| `LFX_AUTH_TOKEN` | Token for LFX API maintainer verification |
| `MAINTAINER_API_ENDPOINT` | External maintainer verification endpoint URL |
| `MAINTAINER_API_STUB` | Set to "fail" to simulate verification failures in testing |

### CLI Flags

**validator** (`cmd/validator/main.go`):
- `--config` - Path to project list configuration file (default: `testdata/projectlist.yaml`)
- `--cache` - Directory to store cached validation results (default: `.cache`)
- `--maintainers` - Path to maintainers file, set empty to skip (default: `testdata/maintainers.yaml`)
- `--base-maintainers` - Path to base maintainers file for diff validation
- `--verify-maintainers` - Verify maintainer handles via external service (default: false)
- `--output` - Output format: text, json, yaml (default: `text`)

**landscape-updater** (`cmd/landscape-updater/main.go`):
- `--project` - Path to project.yaml file (required)
- `--landscape` - Path to landscape.yml for comparison (optional)
- `--output` - Output format: text, json, yaml (default: `text`)
- `--dry-run` - Show changes without applying (default: true)

**staleness-checker** (`cmd/staleness-checker/main.go`):
- `--project` - Path to project.yaml file (required)
- `--threshold` - Days before considering maintainers stale (default: 180)
- `--last-update` - Override last update date (YYYY-MM-DD format)
- `--output` - Output format: text, json, yaml (default: `text`)

**audit-checker** (`cmd/audit-checker/main.go`):
- `--project` - Path to project.yaml file (required)
- `--output` - Output format: text, json, yaml (default: `text`)
- `--timeout` - HTTP request timeout in seconds (default: 10)

**drift** (`cmd/drift/main.go`): see [Running the Maintainer Health-Check](#running-the-maintainer-health-check-drift) above.

## Docker

### Build

```bash
docker build -t dot-project-validator .
```

### Run

```bash
# Run validator
docker run --rm -v $(pwd)/testdata:/app/testdata dot-project-validator --config /app/testdata/projectlist.yaml
```

The Dockerfile uses a multi-stage build:
1. `golang:1.24-alpine` builder stage (builds only the `validator` binary)
2. `alpine:3.20` runtime with `git` and `ca-certificates`

Note: The Docker image includes `validator` and `landscape-updater` binaries. The other CLI tools (bootstrap, staleness-checker, audit-checker, etc.) are not built in the Dockerfile.

## Configuration Files

### Project List (`testdata/projectlist.yaml`)

```yaml
projects:
  - url: "https://raw.githubusercontent.com/org/repo/main/project.yaml"
    id: "project-id"
  - url: "file://${REPO_ROOT}/path/to/project.yaml"
    id: "local-project"
```

### Maintainers (`testdata/maintainers.yaml`)

```yaml
maintainers:
  - project_id: "project-id"
    org: "github-org"  # optional
    teams:
      - name: "project-maintainers"  # required team
        members:
          - alice
          - bob
      - name: "other-team"
        members:
          - carol
```

### Project Schema (`project.yaml`)

```yaml
schema_version: "1.0.0"
slug: "project-name"
name: "Project Name"
description: "Project description"
project_lead: "github-handle"
cncf_slack_channel: "#project-name"
maturity_log:
  - phase: "incubating"
    date: 2024-01-15
    issue: "https://github.com/cncf/toc/issues/123"
repositories:
  - "https://github.com/org/repo"
website: "https://project.io"
artwork: "https://project.io/artwork"
social:
  twitter: "https://twitter.com/project"
  slack: "https://slack.project.io"
security:
  policy:
    path: "SECURITY.md"
  contact: "security@project.io"
governance:
  contributing:
    path: "CONTRIBUTING.md"
  governance_doc:
    path: "GOVERNANCE.md"
documentation:
  readme:
    path: "README.md"
landscape:
  category: "App Definition and Development"
  subcategory: "Database"
audits:
  - date: 2023-12-01
    type: "security"
    url: "https://project.io/audit.pdf"
```

### Template Files (`template/`)

The `template/` directory contains starter files for new `.project` repositories:
- `project.yaml` - Example project metadata
- `maintainers.yaml` - Example maintainers configuration
- `.github/workflows/validate.yaml` - CI workflow to validate project files

## Common Tasks

### Adding a New Validation Rule

1. Add error check in `ValidateProjectStruct()` in `validator.go`
2. Add corresponding test case in `validator_test.go`
3. Update type definition in `types.go` if adding new fields

### Adding a New Maintainer Validation

1. Add check in `validateMaintainerEntry()` in `maintainers.go`
2. Handle normalization in `normalizeHandles()` if needed
3. Add test cases

### Modifying CLI Flags

Edit the corresponding `cmd/*/main.go` file. All CLIs use the standard `flag` package.

### Adding a New CLI Tool

1. Create `cmd/<tool-name>/main.go` with a `package main` and `main()` function
2. Import `"projects"` to use library functions from the package root
3. Use `flag` for argument parsing
4. Support `--output` with text/json/yaml formats for consistency

## Testing the Maintainer Health-Check Feature

The cron trigger fires once a month and only once `maintainers.yaml` is 180 days old, so the feature needs to be tested via four complementary layers:

### Layer 1 — Unit tests (no network, always fast)

`go test -short ./...` runs all unit tests. The relevant files are:

| File | What it covers |
|------|----------------|
| `drift_detector_test.go` | `FormatActivityIssue` rendering, `BuildHealthCheckActivityLists` sorting/filtering, `ParseAllRepos`, `sortActivityDesc`, `isLikelyTeamSlug`, `parseLinkNext`, `LoadProjectHandlesForTeam` |
| `drift_sources_test.go` | HTTP API layer — uses `httptest.NewServer` mocks (no real network calls). Covers: contributor-stats window filtering, 204 no-content, 202 retry logic (skipped with `-short`), non-200 errors, PR merged/unmerged/out-of-window filtering, early-exit pagination, multi-repo fan-out, non-fatal fetch errors, context cancellation, team-members pagination, 403/404 error messages |

```bash
# Fast: all unit tests, skips the 3-second 202-retry test
make test-short

# Full: includes the 202-retry slow path
make test
```

### Layer 2 — Offline smoke test (no token needed)

Tests file parsing + staleness detection without touching the GitHub API. Because `-last-updated-days 1` (1 day) is less than the default 180-day threshold, the binary exits `0` ("not stale") before making any network requests.

```bash
make smoke-drift-offline
# Equivalent:
./bin/drift \
  -project-yaml example/project.yaml \
  -maintainers-yaml example/maintainers.yaml \
  -last-updated-days 1
```

To test the staleness-detection logic specifically (the `daysSince > stalenessDays` gate):

```bash
# Should exit 0 — 1 day < 180-day threshold
./bin/drift -last-updated-days 1   -staleness-days 180

# Should exit 0 — equal is NOT stale (strict greater-than)
./bin/drift -last-updated-days 180 -staleness-days 180

# Should exit 1 — 181 > 180, stale, BUT will also call GitHub API
# (use make smoke-drift for this, which needs GITHUB_TOKEN)
./bin/drift -last-updated-days 181 -staleness-days 180
```

### Layer 3 — Live smoke test (needs `GITHUB_TOKEN`)

Uses `-staleness-days 0` to force the stale path regardless of file age, then runs the full pipeline against the real GitHub API using the Kubernetes example fixtures. Exit code `1` is the expected ("stale") outcome.

```bash
export GITHUB_TOKEN=ghp_...
make smoke-drift

# Or manually, writing the issue body to a file for inspection:
GITHUB_TOKEN=$GITHUB_TOKEN ./bin/drift \
  -project-yaml  example/project.yaml \
  -maintainers-yaml example/maintainers.yaml \
  -last-updated-days 1 \
  -staleness-days 0 \
  -top-contributors 3 \
  -report /tmp/health-report.md \
  ; echo "exit: $?"
cat /tmp/health-report.md
```

### Layer 4 — GitHub Actions workflow (needs a real `.project` repo)

The scaffolded `template/.github/workflows/maintainer-drift.yml` has a `workflow_dispatch` trigger so the workflow can be triggered manually at any time without waiting for the cron schedule.

```bash
# Trigger manually from your .project repo's Actions tab, or via CLI:
gh workflow run maintainer-drift.yml \
  --repo <org>/<project>.project \
  --field ref=main
```

**To test the full issue-open/update path without a real repo**, use the `act` local runner:

```bash
brew install act        # macOS / Linux
act workflow_dispatch \
  --secret GITHUB_TOKEN="$GITHUB_TOKEN" \
  --workflows .github/workflows/maintainer-drift.yml
```

### Cheat-sheet: what each layer covers

| Layer | Network | Token | What it proves |
|-------|---------|-------|----------------|
| `make test-short` | ✗ | ✗ | All logic paths via mocks — fast, runs in CI |
| `make test` | ✗ | ✗ | Same + 202-retry backoff path |
| `make smoke-drift-offline` | ✗ | ✗ | Binary builds, parses real YAML, exits 0 correctly |
| `make smoke-drift` | ✓ | ✓ | Real GitHub API, full issue body rendered |
| `workflow_dispatch` / `act` | ✓ | ✓ | Full GitHub Actions workflow, issue create/edit |



| Code | Meaning |
|------|---------|
| `0` | All checks passed / not stale — no action needed |
| `1` | One or more checks failed (validation errors, stale data, failed URL checks) **or** `drift`: `maintainers.yaml` is stale — issue body written to `-report` |
| `2` | `drift` only: fatal error (bad flags, unreadable file, GitHub API failure) — do **not** open an issue |
| Non-zero | Other errors (file not found, parse errors, etc.) |
