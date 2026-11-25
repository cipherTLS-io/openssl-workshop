# Lessons

Status: draft M0 schema; lesson execution and grading are not implemented.

One directory per lesson: `lessons/<module>/<nn>-<slug>/lesson.yaml` and its disposable fixtures.
See [the chain example](pki-basics/03-chain/lesson.yaml) and [design](../docs/DESIGN.md).

| Field | Responsibility |
|---|---|
| `id`, `versions`, `cites` | Stable lesson identity, release selection and source references |
| `prerequisites`, `objective` | Prior knowledge and observable learning objective |
| `setup` | Reviewed fixture preparation; never creates the completed learner output |
| `learner.task`, `learner.outputs` | What the learner must do and the artifact assessment reads |
| `reference_solution` | Author-validation solution; never executed by learner assessment |
| `assessment` | Core rule IDs with bindings to the actual submission and supplied fixtures |
| `feedback`, `transfer` | Misconception feedback and a different artifact for transfer practice |

Author validation creates a fresh exercise, applies the reference solution and runs its assessment
on every declared exact release. Learner assessment reads the existing submission and never applies
that solution. An untouched workspace must fail. Correct alternative solutions should pass; wrong
submissions and infrastructure errors must be distinguished.

Reusable verification commands belong in core. An expected failure must match the intended
cryptographic reason; a missing file or failed container is not proof of that reason. The parser
must reject unsupported fields and unresolved bindings. Generated lessons use this same contract
and remain drafts until checked and reviewed.

Passing a reference exercise demonstrates technical consistency. Learning claims additionally
need observed users, feedback and a transfer task. Use disposable fixture keys only.
