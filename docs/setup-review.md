# Setup review — openssl-workshop

Baseline review: 2026-11-11; scope updated 2026-11-12. Standard: method.programs v1.1.
Reference: [k3sm](https://github.com/k3sm-io/k3sm/tree/8429efe09bf880ac847df6a335db9f51022b8efe),
plus its public site observed 2026-11-11. The pinned phase ledger was rechecked 2026-11-12.

Overall verdict: **baseline replication in progress**. The documentation and commit workflow
have been reworked; the first product journey and audience-accessible release are not demonstrated.

| Baseline responsibility | Project artifact | Evidence / state | Remaining gap |
|---|---|---|---|
| Public first-use path | README, docs/user/README.md | Described; scaffold is prominent | Working installation and first task; rendered public path |
| Design and challenged assumptions | docs/DESIGN.md, core DR-007/evidence contract | Described; numbered sections and review findings recorded | Maintainer resolution and M0 spike results |
| Repository boundaries and contracts | Core docs/program.md; design §6 | Described; products depend independently on core | Exercised consumer API and real revision pin |
| Roadmap → phases → gates | ROADMAP.md, docs/PHASES.md, manifest, hack/ci.sh | Commit workflow exercised separately from product proof | M0 acceptance; full ledger/readiness validation |
| Contributor journey and governance | CONTRIBUTING.md, AGENTS.md, existing governance files | Local gate documented | Fresh-clone contribution walkthrough and runnable first issue |
| Release and documentation consistency | docs/user/README.md; roadmap | Unavailable product explicitly labelled | Tagged usable artifact/preview and captured output |

## Review procedure

Run `sh hack/ci.sh` and record the actual result in the PR. It enforces formatting, vet,
Go tests/build, privacy scan, dispatch regression tests and the manifest. It does not make
pending skeleton or manual gates green. Run `python3 hack/acceptance.py --phase M0` for actual
M0 proof. Full YAML parsing and cross-repository readiness are not certified by the dispatcher.

Trace one claim through public instructions, requirements, design, phase, implementation,
acceptance and the release consumers can obtain. Record revision, environment, inputs and
observed output. A populated file map is insufficient.

## Next proof

DR-008 selects the core/terminal companion first; the following lesson proof remains later scope.

After core M0, exercise a learner submission: untouched exercise fails, correct repair passes, wrong repair fails for the intended reason. Generate the page from that run.
Preserve existing IDs and add evidence when the behavior is observed. This review does not move
any product deliverable to done.

## Local validation recorded in this rework

Verified 2026-11-11 on the working tree: `sh hack/ci.sh` exited 0. Its 11 dispatch regression
cases passed; Go vet/test/build and the tracked-file privacy scan passed. Go product packages
still report no test files. Every product milestone remains a pending skeleton. The result
certifies the commit workflow only; no product acceptance or baseline demonstration is claimed.

## Companion setup validation — 2026-11-12

On the local working tree, `sh hack/ci.sh` exited 0: formatting, Go vet/test/build, tracked-file
privacy scan, 11 dispatch regression cases and manifest dispatch passed. Go product packages
still report no test files. The manifest reports product gates as pending, not completed.

An additional setup check parsed all three YAML ledgers, checked retained phase/deliverable IDs
against HEAD, matched phase IDs to manifests, checked declared cross-repository dependencies for
existence/cycles, resolved local Markdown links and scanned tracked plus untracked project files
for private terms. These checks passed; they do not establish remote dependency readiness.

Explicit `python3 hack/acceptance.py --phase M0` exited 1 because the skeleton remains.
No lesson, rendered site or product release was demonstrated. Changes remain local.

## Parity pass — 2026-11-24

- Moved to `cipherTLS-io/openssl-workshop` per core `DR-009` and updated all cross-repo links and
  `go.mod`.
- Upgraded `hack/ci.sh` to `k3sm` local-gate parity (`ci_done=1` trap, `-race`, `go mod tidy`
  no-diff, local DCO check) and removed `.github/workflows/`.
- Remains parked after `core`/`aitls` M6 per `DR-008`; verdict remains **baseline assembled, not
  yet baseline demonstrated**.
