# Current quickstart and limitations

Program priority (2026-11-12): the first delivery is the core/terminal documentation companion
([DR-008](https://github.com/ciphertls-io/core/blob/main/docs/decisions/DR-008-companion-first.md)).
The learning experience below remains later scope. It is not required to install or use the
companion; its own first lesson still depends on core M0. The first companion preview belongs
to terminal M6; this repository retains the later teaching site.


Status: scaffold, checked 2026-11-11. The `workshop` entry point is a placeholder. The product
commands illustrated in the README and design are targets, not a usable release.

## What can be checked today

Install Go matching `go.mod` and Python 3.9 or newer, clone this repository and run:

```sh
sh hack/ci.sh
python3 hack/acceptance.py --phase M0
```

The first command checks the development baseline. The second must fail while M0 remains a
skeleton. Its failure is an honest availability signal; it is not an installation fix.

## First usable path being built

Learn why a server's intermediate certificates differ from a trusted root. Use the supplied leaf, root and intermediate to create `submission/intermediates.pem`. The future assessment verifies that submitted artifact through the core; leaving the submission absent must fail. A reference solution validates the lesson separately from a learner's submission.

See [design](../DESIGN.md), [phases](../PHASES.md) and [setup review](../setup-review.md).
The release must provide exact dependencies, installation, expected outputs and a tested clean
checkout before this becomes a runnable tutorial.

## Limits

No completed M0, working product release or learner/operator validation is claimed. Container
execution, exact release images and consumer integration remain unproved. Use disposable fixtures
during development. Current documentation does not establish production suitability.
