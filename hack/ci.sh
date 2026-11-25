#!/bin/sh
# Local commit gate — the single proof of record (k3sm / method.programs v1.1).
# No GitHub Actions workflows run in this repository; this script enforces Go
# checks, local DCO sign-off, privacy scrub, and acceptance manifest honesty.
set -eu
cd "$(dirname "$0")/.."

ci_done=0
ci_tmp="$(mktemp -d)"
cleanup() {
  rc=$?
  rm -rf "$ci_tmp"
  if [ "$ci_done" -ne 1 ]; then
    echo "FAIL: hack/ci.sh aborted before completion (exit $rc)" >&2
    exit 1
  fi
}
trap cleanup EXIT

echo "==> gofmt"
unformatted="$(gofmt -l .)"
if [ -n "$unformatted" ]; then
  printf 'Formatting required:\n%s\n' "$unformatted" >&2
  exit 1
fi

echo "==> go list (fail-closed)"
if ! go_pkgs="$(GOWORK=off go list ./... 2>"$ci_tmp/golist.err")"; then
  echo "FAIL: go list ./... failed — refusing to skip vet/test/build:" >&2
  cat "$ci_tmp/golist.err" >&2
  exit 1
fi

if [ -n "$go_pkgs" ]; then
  echo "==> go vet"
  GOWORK=off go vet ./...
  echo "==> go test -race"
  GOWORK=off go test -race -count=1 ./...
  echo "==> go build"
  GOWORK=off go build ./...
fi

echo "==> go mod tidy (no-diff)"
before_mod="$(cat go.mod)"
before_sum=""
[ -f go.sum ] && before_sum="$(cat go.sum)"
GOWORK=off go mod tidy
after_mod="$(cat go.mod)"
after_sum=""
[ -f go.sum ] && after_sum="$(cat go.sum)"
if [ "$before_mod" != "$after_mod" ] || [ "$before_sum" != "$after_sum" ]; then
  echo "FAIL: go.mod or go.sum changed after 'go mod tidy'" >&2
  exit 1
fi

echo "==> DCO sign-off (local commit history)"
python3 -B -c '
import subprocess, sys
out = subprocess.check_output(
    ["git", "log", "--format=%H%x1f%s%x1f%(trailers:key=Signed-off-by,valueonly)%x1e"],
    text=True,
)
missing = []
for rec in out.split("\x1e"):
    rec = rec.strip()
    if not rec:
        continue
    sha, subj, trailers = rec.split("\x1f", 2)
    if not trailers.strip():
        missing.append(f"{sha[:7]} {subj}")
if missing:
    print("FAIL: commits missing Signed-off-by trailer (use git commit -s):", file=sys.stderr)
    for m in missing:
        print(" ", m, file=sys.stderr)
    sys.exit(1)
'

echo "==> privacy scrub"
sh hack/check.sh

echo "==> acceptance dispatcher tests"
python3 -B -m unittest discover -s hack/tests -p 'test_*.py'

echo "==> acceptance manifest"
python3 -B hack/acceptance.py

ci_done=1
echo "ci: commit checks passed; see pending acceptance above"
