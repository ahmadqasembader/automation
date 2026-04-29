# Project Validator Makefile

REPO_ROOT := $(abspath ../..)

.PHONY: all build test clean install run help provision

# Default target
all: build

# Build the validator
build:
	@echo "Building project validator..."
	@mkdir -p bin
	go build -o bin/validator ./cmd/validator
	@echo "Building landscape updater..."
	go build -o bin/landscape-updater ./cmd/landscape-updater
	@echo "Building bootstrap tool..."
	go build -o bin/bootstrap ./cmd/bootstrap

# Build the drift health-check binary
build-drift:
	@echo "Building drift binary..."
	@mkdir -p bin
	go build -o bin/drift ./cmd/drift

# Build docker image
docker-build:
	@echo "Building docker image..."
	docker build -t dot-project-validator .

# Run tests
test:
	@echo "Running tests..."
	go test -v ./...

# Run tests excluding slow retry tests (no network needed)
test-short:
	@echo "Running tests (short mode — skips slow retry tests)..."
	go test -short -v ./...

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	go test -v -coverprofile=coverage.out ./...
	go tool cover -func=coverage.out
	go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report generated: coverage.html"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -f validator
	rm -rf bin/
	rm -f coverage.out coverage.html
	rm -rf .cache
	rm -rf .test-cache

# Install dependencies
install:
	@echo "Installing dependencies..."
	go mod download
	go mod tidy

# Run the validator with default settings
run: build
	@echo "Running validator..."
	REPO_ROOT=$(REPO_ROOT) ./bin/validator --config testdata/projectlist.yaml --maintainers testdata/maintainers.yaml --verify-maintainers

# Run the validator and show changes only
run-changes: build
	@echo "Running validator and filtering for changes..."
	REPO_ROOT=$(REPO_ROOT) ./bin/validator --config testdata/projectlist.yaml --maintainers testdata/maintainers.yaml --verify-maintainers | grep -E "(CHANGED|INVALID|Summary)"

# Validate and format Go code
fmt:
	@echo "Formatting Go code..."
	go fmt ./...

# Run linter
lint:
	@echo "Running linter..."
	golangci-lint run

# Check for security issues
security:
	@echo "Running security checks..."
	gosec ./...

# Create a test project list with local files
test-setup:
	@echo "Setting up test environment..."
	@echo "projects:" > testdata/test-projectlist.yaml
	@echo "  - url: \"file://$(PWD)/testdata/test-project.yaml\"" >> testdata/test-projectlist.yaml
	@echo "    id: \"test-project\"" >> testdata/test-projectlist.yaml
	@echo "Test project list created: testdata/test-projectlist.yaml"

# Run validator with test setup
test-run: test-setup build
	REPO_ROOT=$(REPO_ROOT) ./bin/validator --config testdata/test-projectlist.yaml

# ── Drift health-check smoke tests ──────────────────────────────────────────────

# Offline smoke: tests file parsing + the non-stale exit-0 path.
# No GITHUB_TOKEN required — exits before any API call is made.
#
#   -last-updated-days 1  → 1 day since last commit
#   default -staleness-days 180 → 1 < 180, not stale → exit 0
smoke-drift-offline: build-drift
	@echo "Smoke-testing drift (offline, not-stale path)..."
	./bin/drift \
		-project-yaml example/project.yaml \
		-maintainers-yaml example/maintainers.yaml \
		-last-updated-days 1
	@echo "smoke-drift-offline passed (exit 0 as expected)"

# Live smoke: tests the full stale path including GitHub API calls.
# Requires GITHUB_TOKEN with public_repo read access.
#
#   -staleness-days 0     → any age is stale, forces the stale path
#   -last-updated-days 1  → simulate 1-day-old file
#   exit 1 (stale) is the expected outcome — treated as success here.
smoke-drift: build-drift
	@if [ -z "$(GITHUB_TOKEN)" ]; then \
		echo "ERROR: GITHUB_TOKEN is not set. Export a token with public_repo read access."; \
		exit 1; \
	fi
	@echo "Smoke-testing drift (live GitHub API, forced-stale path)..."
	@EXIT=0; \
	GITHUB_TOKEN=$(GITHUB_TOKEN) ./bin/drift \
		-project-yaml example/project.yaml \
		-maintainers-yaml example/maintainers.yaml \
		-last-updated-days 1 \
		-staleness-days 0 \
		-top-contributors 3 \
		|| EXIT=$$?; \
	if [ "$$EXIT" -eq 1 ]; then \
		echo "smoke-drift PASSED (exit 1 = stale path, issue body printed above)"; \
	elif [ "$$EXIT" -eq 0 ]; then \
		echo "smoke-drift WARNING: exit 0 unexpectedly (check -staleness-days flag)"; \
	else \
		echo "smoke-drift FAILED: exit $$EXIT (tool error — check stderr above)"; \
		exit $$EXIT; \
	fi

# Provision a .project repo (prints usage if no args given)
provision: build
	@if [ -z "$(ORG)" ]; then \
		echo "Usage: make provision ORG=<org> NAME=<name> [REPO=<repo>] [DRY_RUN=1]"; \
		echo "       make provision BATCH=<file> [DRY_RUN=1]"; \
		echo ""; \
		echo "Examples:"; \
		echo "  make provision ORG=project-copacetic NAME=Copacetic DRY_RUN=1"; \
		echo "  make provision BATCH=scripts/example-batch.txt DRY_RUN=1"; \
	elif [ -n "$(BATCH)" ]; then \
		./scripts/provision.sh --batch "$(BATCH)" --bootstrap-bin bin/bootstrap $(if $(DRY_RUN),--dry-run); \
	else \
		./scripts/provision.sh --org "$(ORG)" --name "$(NAME)" $(if $(REPO),--repo "$(REPO)") --bootstrap-bin bin/bootstrap $(if $(DRY_RUN),--dry-run); \
	fi

# Show help
help:
	@echo "Available targets:"
	@echo "  build               - Build validator, landscape-updater, and bootstrap binaries"
	@echo "  build-drift         - Build the drift health-check binary"
	@echo "  docker-build        - Build docker image"
	@echo "  test                - Run all tests"
	@echo "  test-short          - Run tests, skipping slow retry tests"
	@echo "  test-coverage       - Run tests with coverage report"
	@echo "  clean               - Clean build artifacts"
	@echo "  install             - Install dependencies"
	@echo "  run                 - Run validator with default settings"
	@echo "  run-changes         - Show only changes and summary"
	@echo "  fmt                 - Format Go code"
	@echo "  lint                - Run linter"
	@echo "  security            - Run security checks"
	@echo "  test-setup          - Create test environment"
	@echo "  test-run            - Run with test setup"
	@echo "  smoke-drift-offline - Smoke-test drift binary (no token, non-stale path)"
	@echo "  smoke-drift         - Smoke-test drift binary against live GitHub API (needs GITHUB_TOKEN)"
	@echo "  provision           - Provision a .project repo (see: make provision)"
	@echo "  help                - Show this help message"
