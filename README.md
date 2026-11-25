# openssl-workshop

Program priority (2026-11-12): the first delivery is the core/terminal documentation companion
([DR-008](https://github.com/ciphertls-io/core/blob/main/docs/decisions/DR-008-companion-first.md)).
The learning experience below remains later scope. It is not required to install or use the
companion; its own first lesson still depends on core M0. The first companion preview belongs
to terminal M6; this repository retains the later teaching site.


**Availability: scaffold; no working product release is claimed.** The examples below illustrate
planned behavior. Start with the [current quickstart](docs/user/README.md),
[setup gaps](docs/setup-review.md) and [design](docs/DESIGN.md).

Lessons generated from OpenSSL's own documentation for the version you pick, graded on the real
artifacts you make, planned to re-test when its cited release snapshot changes, published as a site.

Title: **OpenSSL Workshop**. Maintainer: veronaimars. Apache-2.0. A workshop built as a tribute to OpenSSL,
on OpenSSL's own documentation, maintained independently.

## Intended behavior

- You pick an OpenSSL release. Every lesson step cites the manual section for that release.
- You run the real `openssl` in a sandbox and make real keys, requests, certificates and chains.
- The grader checks the artifact you made, not the text you typed, and tells you which section
  explains the result.
- The planned drift workflow detects changes between cited release snapshots, re-runs affected
  lessons and marks their explanations for review.
- The site shows every command with the output captured by the run that graded it.

Lessons are files anyone can read and propose changes to. The model drafts and explains; the
checks grade; a person confirms.

## A look (mockup of the M0 target)

```text
$ workshop lesson run pki-basics/03-chain --version 4.1
OpenSSL 4.1.0 (pinned image)          PKI basics · lesson 3 of 5 · the chain

  Goal   Verify leaf.pem against root.pem, supplying the intermediate.
  Files  root.pem  int.pem  leaf.pem
  Read   openssl-verify(1) OPTIONS: -CAfile, -untrusted

sandbox$ openssl verify -CAfile root.pem leaf.pem
CN = leaf
error 20 at 0 depth lookup: unable to get local issuer certificate
error leaf.pem: verification failed

  ✘ Not yet. The verifier found leaf.pem but nothing that signed it;
    root.pem signed int.pem, not leaf.pem.
    openssl-verify(1) OPTIONS -untrusted: "A file of untrusted certificates …
    used to build the chain".

sandbox$ openssl verify -CAfile root.pem -untrusted int.pem leaf.pem
leaf.pem: OK

  ✔ check 1  the chain verifies with the intermediate supplied
  ✔ check 2  it fails without the intermediate (run for you)
  Lesson 3 passed on 4.1.0. Also passes on 3.5.9. Cited: openssl-verify(1) OPTIONS.
```

The grader read the files you made and ran the real `openssl` on them. The explanation quotes the manual
for the release you chose.

## Completion that knows your release (mockup of the M4 shell tutor)

```text
sandbox$ openssl req -new -key leaf.key -<TAB>
 -subj <arg>          Set or modify the subject of the request          openssl-req(1) OPTIONS
 -addext <ext>        Additional extension, key=value                    openssl-req(1) OPTIONS
 -not_before <date>   Validity start                                     new in 4.0
 -not_after <date>    Validity end                                       new in 4.0
 -x509                Output a certificate instead of a request          openssl-req(1) OPTIONS
 -keygen_engine <id>  not in 4.1.0: removed with ENGINE support          last seen in 3.x
```

The shell completes `openssl` itself, with one line per option taken from the manual for the release
you are running, and tells you when an option you remember is gone.

## Why

The earlier public teaching module taught an end-of-life release, a chain check that passed with
a missing intermediate, and a key match that only worked for RSA, and nobody noticed for a year. Its site is
down and its repository is archived; this is where it moved.
Material that cites a versioned source and is re-tested against the real binary cannot go stale
quietly.

## Status

Scaffold. Nothing runs yet. Delivery state: `docs/PHASES.md`, proven by `hack/acceptance/`.
Direction: `ROADMAP.md`. Design: `docs/DESIGN.md`. Decisions: `docs/decisions/`.

## Layout

| Path | What |
|---|---|
| `cmd/workshop/` | the CLI (`lesson check`, `lesson draft`, `site build`, later `ask`) |
| `internal/` | lesson runner, generator, site renderer (created in M0) |
| `lessons/` | lessons as files; see `lessons/README.md` |
| `site/` | templates for the static site; output is published, never committed |
| `docs/` | design, phases, decisions |
| `hack/` | `check.sh` (scrub) and the acceptance gates |

The corpus, the release images and the checks come from
[ciphertls-io/core](https://github.com/ciphertls-io/core), imported as a Go module
and pinned to a release.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): the gate, the DCO sign-off (`git commit -s`), the commit
grammar, and what happens after you open an issue or a pull request. Governance is in
[GOVERNANCE.md](GOVERNANCE.md) and [MAINTAINERS.md](MAINTAINERS.md); security reports go through
[SECURITY.md](SECURITY.md). Check the issue prerequisites: lesson and product tasks depend on the unfinished M0 runner.

## Licence

Apache-2.0 (`LICENSE`). Third-party material, if any, is listed in `NOTICE`.
