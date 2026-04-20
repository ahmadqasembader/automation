#!/usr/bin/env bash
#
# rollout.sh — Staged rollout of .project repos across CNCF project orgs
#
# Parses the CNCF landscape.yml to discover project orgs, filters by
# maturity level, and provisions .project repos in configurable batches
# using provision.sh.
#
# Usage:
#   ./scripts/rollout.sh --landscape <path> --maturity graduated [options]
#
# Options:
#   --landscape <path>    Path to landscape.yml (required)
#   --maturity <level>    Filter: graduated|incubating|sandbox|all (required)
#   --batch-size <n>      Orgs per batch (default: 50)
#   --batch <n>           Which batch to run, 1-indexed (default: 1)
#   --list                List mode: show orgs + status, no provisioning
#   --dry-run             Pass --dry-run to provision.sh
#   --skip-secrets        Pass --skip-secrets to provision.sh
#   --skip-protection     Pass --skip-protection to provision.sh
#   --provision-bin <p>   Path to provision.sh (default: scripts/provision.sh)
#   --bootstrap-bin <p>   Path to bootstrap binary (passed to provision.sh)
#   --log-dir <path>      Directory for per-org logs (default: /tmp/rollout-logs)
#   --poll-timeout <s>    Max seconds to wait for workflow (default: 300)
#   -h, --help            Show this help
#
set -euo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────────

LANDSCAPE=""
MATURITY=""
BATCH_SIZE=50
BATCH_NUM=1
LIST_MODE=false
DRY_RUN=false
SKIP_SECRETS=false
SKIP_PROTECTION=false
PROVISION_BIN="scripts/provision.sh"
BOOTSTRAP_BIN=""
LOG_DIR="/tmp/rollout-logs"
POLL_TIMEOUT=300

# ── Result Tracking ───────────────────────────────────────────────────────────

RESULT_TOTAL=0
RESULT_SUCCEEDED=0
RESULT_FAILED=0
RESULT_SKIPPED=0
RESULT_SUCCEEDED_ORGS=()
RESULT_FAILED_ORGS=()
RESULT_SKIPPED_ORGS=()

# ── Colours ───────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ── Helpers ───────────────────────────────────────────────────────────────────

die()  { echo -e "${RED}Error: $*${NC}" >&2; exit 1; }
warn() { echo -e "${YELLOW}Warning: $*${NC}" >&2; }
info() { echo -e "${CYAN}$*${NC}" >&2; }
ok()   { echo -e "${GREEN}$*${NC}" >&2; }

usage() {
  sed -n '3,/^$/s/^# \?//p' "$0"
  exit 0
}

# ── CLI Argument Parsing ─────────────────────────────────────────────────────

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --landscape)       LANDSCAPE="$2"; shift 2 ;;
      --maturity)        MATURITY="$2"; shift 2 ;;
      --batch-size)      BATCH_SIZE="$2"; shift 2 ;;
      --batch)           BATCH_NUM="$2"; shift 2 ;;
      --list)            LIST_MODE=true; shift ;;
      --dry-run)         DRY_RUN=true; shift ;;
      --skip-secrets)    SKIP_SECRETS=true; shift ;;
      --skip-protection) SKIP_PROTECTION=true; shift ;;
      --provision-bin)   PROVISION_BIN="$2"; shift 2 ;;
      --bootstrap-bin)   BOOTSTRAP_BIN="$2"; shift 2 ;;
      --log-dir)         LOG_DIR="$2"; shift 2 ;;
      --poll-timeout)    POLL_TIMEOUT="$2"; shift 2 ;;
      -h|--help)         usage ;;
      *)                 die "Unknown option: $1" ;;
    esac
  done

  [[ -n "$LANDSCAPE" ]]  || die "--landscape is required"
  [[ -f "$LANDSCAPE" ]]  || die "Landscape file not found: $LANDSCAPE"
  [[ -n "$MATURITY" ]]   || die "--maturity is required (graduated|incubating|sandbox|all)"
  [[ "$MATURITY" =~ ^(graduated|incubating|sandbox|all)$ ]] \
    || die "Invalid maturity: $MATURITY (must be graduated|incubating|sandbox|all)"
  [[ "$BATCH_SIZE" =~ ^[1-9][0-9]*$ ]] || die "--batch-size must be a positive integer"
  [[ "$BATCH_NUM" =~ ^[1-9][0-9]*$ ]]  || die "--batch must be a positive integer"
}

# ── Prerequisite Checks ──────────────────────────────────────────────────────

check_prerequisites() {
  local missing=()

  command -v python3 >/dev/null 2>&1 || missing+=("python3")
  command -v jq      >/dev/null 2>&1 || missing+=("jq")
  command -v gh      >/dev/null 2>&1 || missing+=("gh")

  if [[ ${#missing[@]} -gt 0 ]]; then
    die "Missing required tools: ${missing[*]}"
  fi

  # Verify PyYAML is available
  python3 -c "import yaml" 2>/dev/null \
    || die "python3 module 'PyYAML' is not installed (pip install pyyaml)"

  # In non-list mode, provision.sh must be executable
  if [[ "$LIST_MODE" == "false" ]]; then
    if [[ ! -x "$PROVISION_BIN" ]]; then
      warn "Provision binary not executable: $PROVISION_BIN (required for non-list mode)"
    fi
  fi
}

# ── Landscape YAML Parser ────────────────────────────────────────────────────

parse_landscape() {
  local landscape_file="$1"

  python3 -c '
import yaml, json, sys
with open(sys.argv[1]) as f:
    data = yaml.safe_load(f)
items = []
for cat in data.get("landscape", []):
    for subcat in cat.get("subcategories", []):
        for item in subcat.get("items", []):
            if item.get("project"):
                items.append({
                    "name": item.get("name", ""),
                    "maturity": item.get("project", ""),
                    "repo_url": item.get("repo_url", ""),
                    "project_org": item.get("project_org", "")
                })
json.dump(items, sys.stdout)
' "$landscape_file" \
  | jq -r '
    .[]
    | select(.maturity != "archived")
    | .org = (
        if .project_org != null and .project_org != ""
        then (.project_org | ltrimstr("https://github.com/") | rtrimstr("/"))
        else (.repo_url   | ltrimstr("https://github.com/") | split("/")[0])
        end
      )
    | "\(.org)|\(.name)|\(.maturity)"
  '
}

# ── Maturity Filter + Org Dedup ──────────────────────────────────────────────

filter_and_dedup() {
  local target_maturity="$1"
  awk -F'|' -v mat="$target_maturity" '{
    org_lower = tolower($1)
    if (mat != "all" && $3 != mat) next
    if (org_lower in seen) next
    seen[org_lower] = 1
    print $0
  }' | sort -t'|' -k1,1 -f
}

# ── Batching Logic ───────────────────────────────────────────────────────────

batch_slice() {
  local batch_size="$1"
  local batch_num="$2"
  local all_lines
  all_lines=$(cat)

  local total
  total=$(printf '%s\n' "$all_lines" | grep -c . || true)

  local total_batches=$(( (total + batch_size - 1) / batch_size ))

  if [[ "$batch_num" -gt "$total_batches" ]]; then
    die "Batch $batch_num requested but only $total_batches batches exist ($total orgs, batch size $batch_size)"
  fi

  local start=$(( (batch_num - 1) * batch_size + 1 ))
  local end=$(( batch_num * batch_size ))

  info "Batch $batch_num of $total_batches ($total orgs total, $batch_size per batch)"
  printf '%s\n' "$all_lines" | sed -n "${start},${end}p"
}

# ── .project Existence Check ──────────────────────────────────────────────────

check_project_exists() {
  local org="$1"
  gh repo view "${org}/.project" --json name >/dev/null 2>&1
}

# ── List Mode ────────────────────────────────────────────────────────────────

list_projects() {
  local batch_lines="$1"

  printf "\n%-4s %-30s %-30s %-12s %-10s\n" "#" "ORG" "PROJECT" "MATURITY" "STATUS"
  printf "%-4s %-30s %-30s %-12s %-10s\n"   "---" "---" "-------" "--------" "------"

  local i=0
  while IFS='|' read -r org name maturity; do
    i=$((i + 1))
    local status
    if check_project_exists "$org"; then
      status="${GREEN}exists${NC}"
    else
      status="${YELLOW}missing${NC}"
    fi
    printf "%-4s %-30s %-30s %-12s %b\n" "$i" "$org" "$name" "$maturity" "$status"
  done <<< "$batch_lines"

  echo ""
  info "Use without --list to provision missing repos"
}

# ── Logging Setup ────────────────────────────────────────────────────────────

setup_logging() {
  mkdir -p "$LOG_DIR"
  info "Logs: $LOG_DIR/"
}

# ── Provision a Single Org ───────────────────────────────────────────────────

provision_org() {
  local org="$1"
  local name="$2"
  local log_file="${LOG_DIR}/${org}.log"

  local -a prov_args=(--org "$org" --name "$name")
  [[ "$DRY_RUN" == true ]]        && prov_args+=(--dry-run)
  [[ "$SKIP_SECRETS" == true ]]    && prov_args+=(--skip-secrets)
  [[ "$SKIP_PROTECTION" == true ]] && prov_args+=(--skip-protection)
  [[ -n "$BOOTSTRAP_BIN" ]]       && prov_args+=(--bootstrap-bin "$BOOTSTRAP_BIN")

  info "[$org] Provisioning .project repo..."

  if "$PROVISION_BIN" "${prov_args[@]}" > "$log_file" 2>&1; then
    ok "[$org] Provisioned successfully"
    return 0
  else
    local exit_code=$?
    warn "[$org] Provisioning failed (exit $exit_code) — see $log_file"
    return 1
  fi
}

# ── Workflow Polling ─────────────────────────────────────────────────────────

poll_workflow() {
  local org="$1"
  local timeout="$2"
  local repo="${org}/.project"
  local deadline=$((SECONDS + timeout))

  sleep 5

  while [[ $SECONDS -lt $deadline ]]; do
    local run_json
    run_json=$(gh api "repos/${repo}/actions/workflows/validate.yaml/runs?per_page=1" 2>/dev/null) || {
      warn "[$org] Could not fetch workflow runs"
      return 1
    }

    local status conclusion
    status=$(echo "$run_json" | jq -r '.workflow_runs[0].status // "none"')
    conclusion=$(echo "$run_json" | jq -r '.workflow_runs[0].conclusion // "none"')

    case "$status" in
      completed)
        if [[ "$conclusion" == "success" ]]; then
          ok "[$org] Validation workflow passed"
          return 0
        else
          warn "[$org] Validation workflow failed: conclusion=$conclusion"
          return 1
        fi
        ;;
      queued|in_progress|waiting)
        sleep 15
        ;;
      none)
        warn "[$org] No workflow runs found"
        return 1
        ;;
      *)
        sleep 15
        ;;
    esac
  done

  warn "[$org] Workflow polling timed out after ${timeout}s"
  return 1
}

# ── Provisioning Loop ────────────────────────────────────────────────────────

run_provisioning() {
  local batch_lines="$1"

  setup_logging

  local succeeded=0 failed=0 skipped=0 total=0
  local -a succeeded_orgs=() failed_orgs=() skipped_orgs=()

  while IFS='|' read -r org name maturity; do
    total=$((total + 1))

    if check_project_exists "$org"; then
      info "[$org] .project repo already exists — skipping"
      skipped=$((skipped + 1))
      skipped_orgs+=("$org")
      continue
    fi

    if provision_org "$org" "$name"; then
      if [[ "$DRY_RUN" == false ]]; then
        if poll_workflow "$org" "$POLL_TIMEOUT"; then
          succeeded=$((succeeded + 1))
          succeeded_orgs+=("$org")
        else
          failed=$((failed + 1))
          failed_orgs+=("$org")
        fi
      else
        succeeded=$((succeeded + 1))
        succeeded_orgs+=("$org")
      fi
    else
      failed=$((failed + 1))
      failed_orgs+=("$org")
    fi

    sleep 2
  done <<< "$batch_lines"

  RESULT_TOTAL=$total
  RESULT_SUCCEEDED=$succeeded
  RESULT_FAILED=$failed
  RESULT_SKIPPED=$skipped
  RESULT_SUCCEEDED_ORGS=("${succeeded_orgs[@]+"${succeeded_orgs[@]}"}")
  RESULT_FAILED_ORGS=("${failed_orgs[@]+"${failed_orgs[@]}"}")
  # shellcheck disable=SC2034  # Available for future summary enhancements
  RESULT_SKIPPED_ORGS=("${skipped_orgs[@]+"${skipped_orgs[@]}"}")
}

# ── Summary Report ───────────────────────────────────────────────────────────

print_summary() {
  local summary_file="${LOG_DIR}/summary.txt"

  cat <<SUMMARY | tee "$summary_file"

════════════════════════════════════════════════════
  ROLLOUT SUMMARY
  Maturity: ${MATURITY}
  Batch: ${BATCH_NUM} (size: ${BATCH_SIZE})
  Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
════════════════════════════════════════════════════
  Total:    ${RESULT_TOTAL}
  Skipped:  ${RESULT_SKIPPED}  (already provisioned)
  Success:  ${RESULT_SUCCEEDED}
  Failed:   ${RESULT_FAILED}
════════════════════════════════════════════════════
SUMMARY

  if [[ ${RESULT_FAILED} -gt 0 ]]; then
    echo "" | tee -a "$summary_file"
    echo "Failed orgs:" | tee -a "$summary_file"
    for org in "${RESULT_FAILED_ORGS[@]}"; do
      echo "  - $org (log: ${LOG_DIR}/${org}.log)" | tee -a "$summary_file"
    done
  fi

  if [[ ${RESULT_SUCCEEDED} -gt 0 ]]; then
    echo "" | tee -a "$summary_file"
    echo "Succeeded orgs:" | tee -a "$summary_file"
    for org in "${RESULT_SUCCEEDED_ORGS[@]}"; do
      echo "  - https://github.com/${org}/.project" | tee -a "$summary_file"
    done
  fi

  echo "" | tee -a "$summary_file"
  echo "Full logs: ${LOG_DIR}/" | tee -a "$summary_file"

  if [[ ${RESULT_FAILED} -gt 0 ]]; then
    return 1
  fi
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
  parse_args "$@"
  check_prerequisites

  local project_list
  project_list=$(parse_landscape "$LANDSCAPE" | filter_and_dedup "$MATURITY")

  local batch
  batch=$(echo "$project_list" | batch_slice "$BATCH_SIZE" "$BATCH_NUM")

  if [[ -z "$batch" ]]; then
    info "No projects found for maturity=$MATURITY"
    exit 0
  fi

  if [[ "$LIST_MODE" == true ]]; then
    list_projects "$batch"
    exit 0
  fi

  run_provisioning "$batch"
  print_summary
}

main "$@"
