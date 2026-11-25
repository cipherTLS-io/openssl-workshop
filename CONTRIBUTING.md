# Contributing

Thank you for looking. This page is the whole workflow; nothing is hidden in a wiki.
By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## This repository

Lessons are files. Most contributions never touch Go.

- A lesson lives in `lessons/<module>/<nn>-<slug>/lesson.yaml` and must pass `workshop lesson check`
  on every version it declares. This is the M0 acceptance target; the runner and lesson CI are not implemented yet.
- Every step cites the manual page and section it relies on. A lesson with no citation is not merged.
- A check grades an artifact (a file, a handshake, a config), never a typed string. New checks land in
  `ciphertls-io/core` first; a lesson names them.
- Prose that explains is welcome; prose that grades is not. Grading is a rule in a file.
- Lesson proposals are welcome; runnable lesson contributions depend on the M0 runner.

## Where to start

- **Discussions** for questions, ideas and show-and-tell.
- **Issues** for work with a proving command. Blank issues are off; pick a template.
- Confirm that a labelled issue has a working proving command and satisfied prerequisites before taking it.
  `help wanted` marks work the maintainer would like a hand with.
- Open an issue or a design document (`docs/design/`) before a large change; small fixes can go
  straight to a pull request.

## The gate

One command is the commit gate for this repository and CI runs the same thing:

```
sh hack/ci.sh
```

Requires Go from `go.mod` and Python 3.9 or newer (standard library only). The same command
runs formatting enforcement, vet, Go tests/build, the privacy scrub, acceptance-dispatch tests
and the milestone manifest. Implemented gates must pass. Declared skeletons remain PENDING;
a green commit gate does not certify a product milestone. Manual checks remain pending until run.

Use `python3 hack/acceptance.py --phase M0` to demand actual M0 acceptance; it fails while M0 is
a skeleton. `requires` in the manifest lists host capabilities; dependencies live in PHASES.
The dispatcher validates milestone IDs and gate paths, not the complete YAML schema or remote
repository readiness. Check cross-repository dependency evidence at the pinned consumer revision.
See [agent review instructions](AGENTS.md) and [setup review](docs/setup-review.md).

## Developer Certificate of Origin

Every commit carries a `Signed-off-by` line with a name and a reachable address (`git commit -s`).
The sign-off certifies you wrote the change or have the right to submit it under the licence
([DCO](DCO)). A pull request with an unsigned commit is not merged; CI checks it.

## Commits and pull requests

[Conventional Commits](https://www.conventionalcommits.org/): `type(scope): summary`, imperative,
lowercase, no trailing period, at most 72 characters. Types: `feat`, `fix`, `docs`, `test`,
`refactor`, `perf`, `build`, `ci`, `chore`, `revert`. The scope is the directory you changed, as
`ls` prints it. One commit does one thing; a subject that needs "and" is two commits.

Pull requests are squash-merged, so the PR title follows the same grammar and becomes the commit
on `main`. The PR template's sections (Summary, Gate, Merge preconditions, Review, Ledger,
Checklist) all stay; write "None." rather than deleting one. "Not run (why)" is an honest verdict;
"should pass" is not.

Every claim in a document or a review is verified (the command named), reported (the source
named) or inferred (from what). Every statement about OpenSSL cites the manual page and section
for the release it is about.

## What happens after you open something

A maintainer reads every issue and pull request. If you offer to take an issue and a maintainer
accepts, it is yours for about a week; if no pull request references it by then it returns to the
open queue and you are told so on the issue. Reviews name the fix and the test that fails before
it; they do not ask you to guess.

## Security

Do not open a public issue for a vulnerability. Use the private advisory form in the Security
tab; see [SECURITY.md](SECURITY.md).
