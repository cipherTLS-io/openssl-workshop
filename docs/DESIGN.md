# openssl-workshop — design

**Direction update, 2026-11-12:** [DR-008](https://github.com/ciphertls-io/core/blob/main/docs/decisions/DR-008-companion-first.md) selects the documentation companion
and one read-only expiry task first (core/terminal M6); NL is an optional M7 experiment.
The earlier chain/learning/workbench designs below remain later scope. Contracts and gates are
acceptance targets, not implemented behavior; historical measurements retain their original dates.


> **OpenSSL Workshop**: lessons generated from OpenSSL's own manuals for the release you pick, graded on the
> real artifacts you make, revalidated when cited release snapshots change, published as a site. One Go binary `workshop`;
> lessons are files. The corpus, the release images, the checks and the host probe come from
> [`ciphertls-io/core`](https://github.com/ciphertls-io/core); its `docs/DESIGN.md` is the
> reference for every shared piece and is cited here by section.
>
> **Status: v1.1 (2026-11-11), pre-spike; contract revision proposed.** ⬜ marks a claim the M0 spike confirms.

## 1. Context

The maintainer's 2025 module for cybersecurity students (archived) taught OpenSSL 1.1.1 (end of life
2023-09-11), a chain check that passes with a missing intermediate, and an RSA-only key match, behind a fake
terminal. Its site was taken down in 2026-11 and its repository, archived, points here. The workshop is independently maintained and uses the current manuals as its source. Verified facts about the manuals and their rate of change: core design §1.

The gap this closes is the one between what is taught and what operators meet: a learner is told "run
`openssl`" on a Mac whose `/usr/bin/openssl` is LibreSSL while Python, Node and curl each link something else
(core design §2). Teaching one command in one version, from a fixed binary, and then showing the learner the
stack they actually have, is the whole idea.

## 2. The core constraint

**A lesson is only as correct as the release it names, and only as honest as the binary that graded it.**

- Every step cites a page and section in the corpus for the releases the lesson declares. A step with no
  citation is not merged (`CONTRIBUTING.md`).
- Every check grades an artifact the learner made by running the real `openssl` in the pinned image for each
  declared release (core §5.3). The grader never reads what the learner typed.
- The page shows the output captured by the run that graded it, never a pasted transcript.
- M2 consumes changed-section records between immutable release snapshots. Affected lessons are re-run
  and their explanations marked for review, even when commands still pass. Development-branch monitoring
  is separate future scope; this is not a promise to detect every upstream edit overnight.
- The model drafts and explains; the checks grade; a person confirms before anything is published (M3).

## 3. Review findings and revisions

2026-11-12 scope review: the maintainer selected a smaller first task to test maintenance value.
A documentation companion must prove applicable sources and accurate output before adding NL.
DR-008 changes delivery order, preserves historical phase IDs, and removes the workshop from
the first companion dependency path. No runtime result or market validation is claimed.

Design review, 2026-11-11: the prior outlines did not consistently distinguish execution errors,
cryptographic outcomes and learner assessment; product dependencies and explanation context also
needed reconciliation. The first shared journey now references the core evidence contract and
DR-007 (proposed; maintainer review pending). No product acceptance or external review is claimed.

Section migration: old §3 architecture → §4; old §4 platform model → §5.0; §5.1 onward and
§6–§9 retain their IDs. §10 now includes prerequisites. References in this repository were migrated
with the change; old revisions retain the original map.

## 4. Architecture

```text
lessons/<module>/<nn>-<slug>/lesson.yaml ──▶ workshop lesson check ──▶ core pkg/check (sandbox, pinned image) ──▶ findings
                                           └──▶ workshop site build ──(findings + captured output)──▶ site/ ──▶ GitHub Pages
core index.json ──▶ workshop lesson draft <page> ──(model drafts, cites)──▶ pull request ──(person confirms)──▶ lessons/
core nightly changed-section list ──▶ workshop drift ──▶ re-run lessons that cite it ──▶ one issue per failure
core host probe ──▶ the "stack you actually have" module (lessons that read the learner's own machine)
workshop ask / shell completion ──▶ core index for the release `openssl version` reports ──▶ cited answer
```

### Components

| Component | Responsibility | Path |
|---|---|---|
| CLI | `lesson check\|run\|draft`, `site build`, `drift`, `ask`, `completion` | `cmd/workshop/` |
| Lesson | schema for `lesson.yaml`; map steps to core checks; declared versions | `internal/lesson/`, `lessons/` |
| Runner | run a lesson's checks through the core for each version; collect findings | `internal/runner/` |
| Site | render lessons with captured output to static pages | `internal/site/`, `site/` |
| Generator | draft a lesson from a page's DESCRIPTION, OPTIONS, EXAMPLES; every step cited | `internal/draft/` |
| Drift | take the core's changed-section list; find citing lessons; re-run; open issues | `internal/drift/`, `.github/workflows/nightly.yml` |
| Tutor | release-aware completion for `openssl` itself; `ask` answering from the index with the section | `internal/tutor/` |

## 5. Subsystem designs

### 5.0. Platform realities and the modules that teach them

The workshop grades in the core's pinned images, so a lesson's result never depends on the learner's
machine (core design §2). The learner's machine is still the point: core design §5.0 measured five TLS stacks
on one Mac, and that gap between what is taught and what runs is what the second module teaches from.

Lessons are grouped in modules. The first two:

- **`pki-basics`**: key (`genpkey`, `pkey`), request (`req`), chain (`x509`, `verify -untrusted`), revocation
  (`ca`, `crl`, `verify -crl_check`), server (`s_client`). Each lesson's artifact and checks are in its issue.
- **`your-stack`** (answers the conflation between what is taught and what runs): the learner runs the core's
  host probe on their own machine and the lesson reads the result. Which `openssl` is on `PATH`; what their
  Python, Node and curl actually link; what `OPENSSL_CONF` would change; why `/usr/bin/openssl` on a Mac is not
  OpenSSL. The checks grade the probe output, so the lesson is true for every learner's machine.


### 5.1 Lesson

The draft [lesson schema](../lessons/README.md) separates supplied fixtures, the learner task and
submission, a reference solution for author validation, and assessment of the actual submission.
The chain task produces `submission/intermediates.pem`; setup never creates that output.
Doing nothing, submitting the wrong chain and submitting the correct chain must be distinguishable.

Lessons reference core rule IDs with named input bindings. Reusable verification commands are not
copied into lessons. The author-validation runner creates a fresh exercise, applies the reference
solution and checks it; the learner-assessment runner checks the learner workspace without applying
that solution. Missing submission is unmet assessment, not a successful negative verification.

Record prerequisites, objective, misconceptions, feedback and a transfer task. Passing technical
lesson checks is not evidence of educational effectiveness. See core's evidence contract and DR-007.

### 5.2 Page data

`workshop site build` writes one JSON per lesson per version beside the HTML, from the core's findings (core
§5.4) plus the lesson's prose. The page is a function of that file; nothing on it is hand-written after grading.

## 6. Repositories

Core design §6. This repository imports the core as a Go module and pins a release; it never holds a copy of
the manuals.

## 7. Build roadmap as slices

- **M0** one lesson on two exact releases through the core; untouched/wrong submissions fail and a
  correct repair passes; author validation is separate from assessment; the page uses captured output.
  The retired repository points to the replacement; core DR-004 records the existing signpost
  decision and removes the obsolete HTTP redirect requirement.
- **M1** the `pki-basics` module, five lessons.
- **M2** drift: nightly re-run of lessons that cite a changed section; one issue per failure.
- **M3** the generator: `lesson draft <page>` opens a pull request a person confirms.
- **M4** the tutor: release-aware completion for `openssl` itself, then `ask`.
- **M5** the browser sandbox (OpenSSL compiled to WebAssembly); **M6** practice targets.
- `your-stack` module: after M0 and the core's host probe land; its own issue set.

## 8. Risks and mitigations

| Risk | Verified how | Mitigation |
|---|---|---|
| A lesson passes on one release and fails on another | ✅ the chain-check case (core §8) | every lesson lists versions; CI runs each; the page shows each |
| Learners have no container runtime | ⚠️ inferred for students on managed laptops | the site shows captured output for reading; M5 removes the need |
| People still hold the old module's URL | ✅ the site answers 404 since 2026-11-08 | the retired repository's README names this project; the page, once it exists, is what that README links |
| Generated lessons are fluent and wrong | ⬜ M3 measures the confirm-rate | a draft is a pull request; the checks must pass before a person reads it; nothing publishes on its own |

## 9. Verification

```sh
workshop lesson check lessons/pki-basics/03-chain --version 3.5 --version 4.1   # planned author validation; also test untouched/wrong learner submissions
workshop site build && test -f site/out/pki-basics/03-chain/index.html
hack/acceptance/m0.sh
```

## 10. Prerequisites and decisions

DR-008 selects companion-first delivery. Exact executable/source mapping, bounded bridge behavior
and actual consumer evidence remain prerequisites for core/terminal M6. No model or external
source service is required. The following prerequisites describe the later chain journey.

Implementation prerequisites: an exercised core interface, exact release/image/source identities,
and evidence for the first shared journey. These are pending. DR-007 in core proposes the
reconciled contract; design text is a pre-implementation plan, not a runtime claim.


- DR-001 independent, clean-room, open source; sole maintainer.
- DR-002 one Go binary; lessons as files; the core does the cryptography.
- DR-003 three repositories, one program; this one carries OpenSSL's name as a dedicated workshop.
