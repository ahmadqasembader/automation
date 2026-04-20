#!/usr/bin/env bash
#
# Integration tests for rollout.sh
#
# These tests verify the landscape parsing, filtering, deduplication,
# and batching logic by invoking rollout.sh --list against the real
# landscape.yml file. No repos are created or modified.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROLLOUT="${SCRIPT_DIR}/rollout.sh"
LANDSCAPE="${SCRIPT_DIR}/../../audit_project_lifecycle_across_tools/datasources/landscape.yml"

# ── Counters ──────────────────────────────────────────────────────────────────
PASS=0
FAIL=0
ERRORS=()

# ── Helpers ───────────────────────────────────────────────────────────────────
pass() { PASS=$((PASS + 1)); echo "  PASS: $1"; }
fail() { FAIL=$((FAIL + 1)); ERRORS+=("$1"); echo "  FAIL: $1"; }

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    pass "$label (expected=$expected)"
  else
    fail "$label (expected=$expected, got=$actual)"
  fi
}

assert_exit() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    pass "$label (exit=$expected)"
  else
    fail "$label (expected exit=$expected, got=$actual)"
  fi
}

assert_contains() {
  local label="$1" needle="$2" haystack="$3"
  if echo "$haystack" | grep -q "$needle"; then
    pass "$label (contains '$needle')"
  else
    fail "$label (expected to contain '$needle')"
  fi
}

# ── Preflight ─────────────────────────────────────────────────────────────────
echo "=== Preflight ==="
if [[ ! -x "$ROLLOUT" ]]; then
  echo "ERROR: rollout.sh not found or not executable at $ROLLOUT"
  exit 1
fi
if [[ ! -f "$LANDSCAPE" ]]; then
  echo "ERROR: landscape.yml not found at $LANDSCAPE"
  exit 1
fi
echo "  rollout.sh: $ROLLOUT"
echo "  landscape:  $LANDSCAPE"
echo ""

# ── Test 1: --help exits cleanly ─────────────────────────────────────────────
echo "=== Test 1: --help ==="
output=$("$ROLLOUT" --help 2>&1) || true
assert_contains "help-shows-usage" "landscape" "$output"
assert_contains "help-shows-maturity" "maturity" "$output"
echo ""

# ── Test 2: Missing required args ─────────────────────────────────────────────
echo "=== Test 2: Missing required arguments ==="
set +e
output=$("$ROLLOUT" 2>&1); rc=$?
set -e
assert_exit "no-args-fails" 1 "$rc"
assert_contains "no-args-error" "required" "$output"
echo ""

# ── Test 3: Invalid maturity ──────────────────────────────────────────────────
echo "=== Test 3: Invalid maturity ==="
set +e
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity bogus 2>&1); rc=$?
set -e
assert_exit "invalid-maturity-fails" 1 "$rc"
assert_contains "invalid-maturity-error" "Invalid maturity" "$output"
echo ""

# ── Test 4: Graduated list count ─────────────────────────────────────────────
echo "=== Test 4: Graduated --list count ==="
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity graduated --batch-size 999 --list 2>&1)
# Count data rows (skip header, separator, and info lines)
count=$(echo "$output" | grep -cE '^\s*[0-9]+\s' || true)
assert_eq "graduated-count" 33 "$count"
echo ""

# ── Test 5: Incubating list count ─────────────────────────────────────────────
echo "=== Test 5: Incubating --list count ==="
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity incubating --batch-size 999 --list 2>&1)
count=$(echo "$output" | grep -cE '^\s*[0-9]+\s' || true)
assert_eq "incubating-count" 37 "$count"
echo ""

# ── Test 6: Sandbox list count ────────────────────────────────────────────────
echo "=== Test 6: Sandbox --list count ==="
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity sandbox --batch-size 999 --list 2>&1)
count=$(echo "$output" | grep -cE '^\s*[0-9]+\s' || true)
assert_eq "sandbox-count" 144 "$count"
echo ""

# ── Test 7: All (unique orgs) ────────────────────────────────────────────────
echo "=== Test 7: All --list count ==="
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity all --batch-size 999 --list 2>&1)
count=$(echo "$output" | grep -cE '^\s*[0-9]+\s' || true)
assert_eq "all-count" 214 "$count"
echo ""

# ── Test 8: Batching — batch 1 of graduated (batch-size 10) ──────────────────
echo "=== Test 8: Batch slicing ==="
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity graduated --batch-size 10 --batch 1 --list 2>&1)
count=$(echo "$output" | grep -cE '^\s*[0-9]+\s' || true)
assert_eq "batch-1-size-10" 10 "$count"
echo ""

# ── Test 9: Batching — last batch of graduated ────────────────────────────────
echo "=== Test 9: Last batch (partial) ==="
# 33 graduated / 10 per batch = 4 batches (10+10+10+3)
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity graduated --batch-size 10 --batch 4 --list 2>&1)
count=$(echo "$output" | grep -cE '^\s*[0-9]+\s' || true)
assert_eq "batch-4-size-10-remainder" 3 "$count"
echo ""

# ── Test 10: Batch out of range ───────────────────────────────────────────────
echo "=== Test 10: Batch out of range ==="
set +e
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity graduated --batch-size 10 --batch 99 --list 2>&1); rc=$?
set -e
assert_exit "batch-out-of-range-fails" 1 "$rc"
assert_contains "batch-out-of-range-error" "Batch 99" "$output"
echo ""

# ── Test 11: Alphabetical sort (first and last) ──────────────────────────────
echo "=== Test 11: Alphabetical sort ==="
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity graduated --batch-size 999 --list 2>&1)
first_org=$(echo "$output" | grep -E '^\s*1\s' | awk '{print $2}')
last_org=$(echo "$output" | grep -E '^\s*33\s' | awk '{print $2}')
# argoproj should be first alphabetically, vitessio last
assert_eq "first-org-alpha" "argoproj" "$first_org"
assert_eq "last-org-alpha" "vitessio" "$last_org"
echo ""

# ── Test 12: Dedup — spiffe should appear only once ──────────────────────────
echo "=== Test 12: Org deduplication ==="
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity graduated --batch-size 999 --list 2>&1)
spiffe_count=$(echo "$output" | grep -c 'spiffe' || true)
assert_eq "spiffe-dedup" 1 "$spiffe_count"
echo ""

# ── Test 13: No archived projects in output ──────────────────────────────────
echo "=== Test 13: No archived in output ==="
output=$("$ROLLOUT" --landscape "$LANDSCAPE" --maturity all --batch-size 999 --list 2>&1)
archived_count=$(echo "$output" | grep -c 'archived' || true)
assert_eq "no-archived" 0 "$archived_count"
echo ""

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════"
echo "  Results: $PASS passed, $FAIL failed"
echo "════════════════════════════════════════"

if [[ $FAIL -gt 0 ]]; then
  echo ""
  echo "Failures:"
  for err in "${ERRORS[@]}"; do
    echo "  - $err"
  done
  exit 1
fi

echo "All tests passed."
exit 0
