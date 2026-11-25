# Agent instructions — openssl-workshop

Selected priority (2026-11-12): [DR-008](https://github.com/ciphertls-io/core/blob/main/docs/decisions/DR-008-companion-first.md) and [companion contract](https://github.com/ciphertls-io/core/blob/main/docs/design/companion.md). Workshop chain lessons remain later work after core M0; the first companion does not depend on this repository or NL.


Read `CLAUDE.md`, `README.md`, `docs/setup-review.md`, `docs/DESIGN.md`,
`docs/PHASES.md`, `CONTRIBUTING.md` and the acceptance manifest before changing behavior.
Shared authorities: [program map](https://github.com/ciphertls-io/core/blob/main/docs/program.md), [PRD](https://github.com/ciphertls-io/core/blob/main/docs/PRD.md), [evidence contract](https://github.com/ciphertls-io/core/blob/main/docs/design/evidence-contract.md). When reviewing a consumer, use its actual pinned core revision;
main-branch links are navigation, not a compatibility pin.

## Work and evidence

- Select an existing deliverable and verify its dependencies. Cross-repository IDs name the
  owning repository; inspect its evidence at the consumed revision. No automated ready-work
  command is installed yet.
- Cite the relevant requirement IDs, design sections and decision records in the PR. DR-008 selects companion-first delivery; its implementation remains unproved. DR-007
  remains a proposed later chain contract, with first-delivery priority superseded by DR-008.
- Preserve requirement, decision and phase IDs. A new implementation choice updates design and
  its decision record before it becomes an instruction to other contributors.
- Run `sh hack/ci.sh`. To prove a milestone, also run
  `python3 hack/acceptance.py --phase M0` (substitute the milestone).
- Record command, commit, environment, input identities and actual outcome. A skeleton reported
  PENDING is unfinished work even when the commit gate passes. Do not mark a row complete without
  its specific evidence and satisfied dependencies.
- A code or runtime contract change needs discriminating tests. Documentation corrections do not
  complete product phases. Site examples come from captured runs once those exist.

## PR and merge review

Check requirement → design/DR → diff → tests → acceptance → public claim. Validate the core pin
and affected consumer contract together. Report manual checks, inaccessible dependencies and
unresolved decisions explicitly. Preserve the existing PR template and DCO requirements.

Private coordination can supply priority and release context; it must not create hidden technical
acceptance criteria. Public comments cite public requirements and reproducible evidence. If a
private constraint changes public behavior, request a public requirement/decision revision before
judging implementation against it. Do not copy private planning or links into public changes.

Read access and successful checks do not authorize merging, publishing or changing visibility.
Follow the maintainer's existing authorization for those actions. If a required decision remains
open, identify it rather than fabricating approval.
