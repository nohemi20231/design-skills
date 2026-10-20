# Design Skills

Claude Code skills for reasoning about software design, from a single function up to service boundaries. One folder per skill, each with a `SKILL.md`.

| Skill | Use it when |
|---|---|
| `software-design/` | Deciding how to design a change before writing it, reviewing a PR for design quality, or judging whether a design is "good": just-in-time design, economics of change, minimalism vs. extensibility, cohesion and coupling, readability, non-functional requirements. |
| `refactor-proposal/` | Planning, writing, or reviewing a refactor: the ask, the benefits, what changes; whether a new requirement needs a refactor first; duplicated code and payloads, flags and hard-coded values, centralized error handling, judging a refactor PR by its tests. |
| `clean-code/` | Writing, refactoring, or reviewing code at the function, class, and module level: naming, function design, SOLID, error handling, tests, code smells. |
| `tdd/` | Implementing a feature or fixing a bug test-first: red-green-refactor, choosing the next test, test doubles, testing levels. |
| `software-architecture/` | Designing or reviewing system structure: layering, module and service boundaries, microservices, data ownership, integration patterns, ADRs. |

## How they fit together

`software-design` is the reasoning layer: it decides *whether* a design is good and *why*. `clean-code` gives the rules below the class level and `software-architecture` the rules above it. `refactor-proposal` turns a concrete new ask into a justified set of changes, leaning on `clean-code` for the smell catalog and on `tdd` to keep behavior pinned while structure changes. The skills reference each other by name, so install them together.

## Install

Personal (available in every project):

```sh
git clone https://github.com/nohemi20231/design-skills.git
cp -R design-skills/*/ ~/.claude/skills/
```

Per project (shared with the team through git):

```sh
cp -R design-skills/*/ your-project/.claude/skills/
```

Claude Code picks up any folder under `.claude/skills/` that contains a `SKILL.md`. Invoke a skill with `/software-design`, `/refactor-proposal`, and so on, or let Claude load it when the description matches the task.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
