# Public site plan

Program priority (2026-11-12): the first delivery is the core/terminal documentation companion
([DR-008](https://github.com/ciphertls-io/core/blob/main/docs/decisions/DR-008-companion-first.md)).
The learning experience below remains later scope. It is not required to install or use the
companion; its own first lesson still depends on core M0. The first companion preview belongs
to terminal M6; this repository retains the later teaching site.


Status: source plan only. No renderer or published site is implemented. M0 must render a real
first-use path from captured evidence before publication is claimed.

| Route | Source responsibility |
|---|---|
| `/` | Purpose, current availability, Learn/Inspect entry points and source links |
| `/docs/` | User reading order; prerequisites, limitations, troubleshooting |
| `/learn/` | First chain task, objective, required output and observed feedback |
| `/architecture/` | One artifact through core and the two consumer interpretations; links to designs |
| `/releases/` | Actual artifacts, exact dependencies, changes and known limits |
| `/community/` | Contributor routing, local gate, maintainers and security reporting |

Repository user docs own instructions; lesson records and captured results own lesson pages.
Public architecture explains the path while linking the authoritative engineering design.
Do not paste mockup output into a page presented as a verified run. A future preview must state
its revision and maturity. Publication should not link to a product destination the audience
cannot access; describe availability honestly until an accessible artifact exists.

Acceptance: render and inspect the pages, verify local/external routes, complete the first task
from a clean environment, and match displayed outputs to the captured run. Hosting configuration
and publication are still outstanding; `workshop site build` remains a target command.
