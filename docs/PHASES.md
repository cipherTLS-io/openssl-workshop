---
repo: openssl-workshop
schema: phases/v1
current_phase: M0
updated: 2026-11-11
updated_by: veronaimars
phases:
  - id: M0
    title: "Walking skeleton — one lesson, two versions, graded in CI, published, the retired module pointing here (design §7)"
    status: todo
    depends_on: ["core:M0"]
    subphases:
      - id: M0.0
        title: "Spike — run one lesson through the core's check runner by hand (design §4, §5.1)"
        status: todo
        deliverables:
          - id: M0.0-d1
            done: false
            desc: "docs/findings-m0.md records the lesson-to-check mapping, what the core API must expose, and the page shape"
      - id: M0.1
        title: "One lesson, graded (design §2, §5.1)"
        status: todo
        deliverables:
          - id: M0.1-d1
            done: false
            desc: "lessons/pki-basics/03-chain passes `workshop lesson check` on 3.5 and 4.1; the check runs real OpenSSL in the core's image and reads the artifacts"
          - id: M0.1-d2
            done: false
            desc: "CI runs every lesson on every declared version on each pull request"
        acceptance:
          - id: M0.1-a1
            met: false
            check: "On both exact releases, author validation passes; untouched and wrong learner submissions fail; a correct submitted intermediate bundle passes; missing input/runtime failure is not mistaken for the intended negative case"
            method: e2e
      - id: M0.2
        title: "Published (design §4, §5.2)"
        status: todo
        deliverables:
          - id: M0.2-d1
            done: false
            desc: "`workshop site build` renders the lesson with the output captured in CI; GitHub Pages serves it"
          - id: M0.2-d2
            done: false
            desc: "the retired module's repository README points at the published page, not only at this repository"
      - id: M0.3
        title: "gate"
        status: todo
        deliverables:
          - id: M0.3-d1
            done: false
            desc: "hack/acceptance/m0.sh replaces the skeleton; phases.json flips skeleton to false in the same change"
  - id: M1
    title: "PKI basics module"
    status: todo
    depends_on: [M0]
    subphases:
      - id: M1.1
        title: "Key, request, chain, verify, revocation, with current commands (design §5.0 pki-basics)"
        status: todo
        deliverables:
          - id: M1.1-d1
            done: false
            desc: "five lessons use genpkey, an algorithm-agnostic key match, and a chain check that fails when the intermediate is missing; all pass on 3.5 and 4.1"
      - id: M1.2
        title: "The your-stack module (design §5.0)"
        status: todo
        deliverables:
          - id: M1.2-d1
            done: false
            desc: "three lessons read the learner's own host probe from the core: which openssl is on PATH and what it is, what their Python, Node and curl link, what OPENSSL_CONF would change; the checks grade the probe output so the lesson is true on every machine"
      - id: M1.3
        title: "gate"
        status: todo
        deliverables:
          - id: M1.3-d1
            done: false
            desc: "hack/acceptance/m1.sh replaces the skeleton"
  - id: M2
    title: "Drift"
    status: todo
    depends_on: [M1, "core:M1"]
    subphases:
      - id: M2.1
        title: "Re-run the lessons that cite a changed section (design §4 drift)"
        status: todo
        deliverables:
          - id: M2.1-d1
            done: false
            desc: "a nightly workflow takes the core release-snapshot change list, re-runs affected lessons, marks explanations for content review even if checks pass, and deduplicates issues by lesson/source change; a controlled fixture proves unrelated lessons stay untouched"
      - id: M2.2
        title: "gate"
        status: todo
        deliverables:
          - id: M2.2-d1
            done: false
            desc: "hack/acceptance/m2.sh replaces the skeleton"
  - id: M3
    title: "The generator"
    status: todo
    depends_on: [M2]
    subphases:
      - id: M3.1
        title: "Draft a lesson from a manual section (design §4 generator)"
        status: todo
        deliverables:
          - id: M3.1-d1
            done: false
            desc: "`workshop lesson draft openssl-req` writes a lesson.yaml from the page's DESCRIPTION, OPTIONS and EXAMPLES with every step cited; it is a pull request a person confirms, never published on its own"
      - id: M3.2
        title: "gate"
        status: todo
        deliverables:
          - id: M3.2-d1
            done: false
            desc: "hack/acceptance/m3.sh replaces the skeleton"
---

# Phases

The YAML frontmatter is authoritative; the prose after it is a mirror for reading. One command per
phase proves it: `hack/acceptance/phases.json` maps each gate to the script whose exit 0 means
met. A gate that does not exist yet ships as an always-red skeleton so nothing is green by
accident.

Phases are `M<N>`, sub-phases `M<N>.<k>`; `.0` is a spike whose findings are written back as
`docs/findings-m<N>.md`, the middle numbers are deliverables, the last is the gate that swaps the
skeleton for the real acceptance script. Deliverable ids are `M<N>.<k>-d<j>`, acceptance ids
`M<N>.<k>-a<j>`. Status: ✅ done, 🟡 in progress, ⛔ blocked, ⬜ todo. Completion dates and proof are added only when the behavior is demonstrated.


## Mirror

- **M0** proves the whole loop once: one lesson graded on two releases by the core's checks, a page
  people can open, the retired module pointing at it.
- **M1** rebuilds the earlier module's path with commands that are right today, then teaches the stack
  the learner actually has.
- **M2** is the reason the project exists: released-source changes select the affected lessons
  for re-testing and content review; branch monitoring is separate scope.
- **M3** lets the manuals write the first draft of a lesson; a person still confirms.
