## Summary

<!-- 1-3 sentences: what changed and why. Link the issue if there is one. -->

## Gate

- **Named gate**: `<the exact command that proves this change>`
- **Verdict**: pass | not run (<why>)
- **Evidence**: failing before, passing after (or, for a new test, what it asserts)
- **`sh hack/ci.sh`**: clean | not run (<why>)

## Merge preconditions

<!-- Core revision and dependency evidence; required human/manual review; unresolved requirement decisions. -->
None.

## Review

- **Notes**: <review context, known trade-offs, rejected alternatives>

## Ledger

<!-- Requirement IDs, design/DR references, phase IDs, exact proof. Pending skeletons are not completed milestones. -->
None.

## Checklist

- [ ] Every commit is signed off: `git commit -s` (see [CONTRIBUTING](../CONTRIBUTING.md) and [DCO](../DCO))
- [ ] `sh hack/ci.sh` is clean and CI is green
- [ ] Every claim cites a manual page and section, or a URL
- [ ] Docs updated if behaviour changed
