# Design Skills

Skills for Claude Code and GitHub Copilot that cover reasoning about software design, from a single function up to service boundaries. One folder per skill under `skills/`, each with a `SKILL.md`.

| Skill | Use it when |
|---|---|
| `skills/software-design/` | Deciding how to design a change before writing it, reviewing a PR for design quality, or judging whether a design is "good": just-in-time design, economics of change, minimalism vs. extensibility, cohesion and coupling, readability, non-functional requirements. |
| `skills/refactor-proposal/` | Planning, writing, or reviewing a refactor: the ask, the benefits, what changes; whether a new requirement needs a refactor first; duplicated code and payloads, flags and hard-coded values, centralized error handling, judging a refactor PR by its tests. |
| `skills/clean-code/` | Writing, refactoring, or reviewing code at the function, class, and module level: naming, function design, SOLID, error handling, tests, code smells. |
| `skills/tdd/` | Implementing a feature or fixing a bug test-first: red-green-refactor, choosing the next test, test doubles, testing levels. |
| `skills/software-architecture/` | Designing or reviewing system structure: layering, module and service boundaries, microservices, data ownership, integration patterns, ADRs. |
| `skills/architecture-diagram/` | Starting any design, feature, or refactoring work in a repo: read the living architecture diagram first, and update it whenever services, modules, data stores, or integrations change. Ships `scripts/build-viewer.py` to render it. |

## How they fit together

`software-design` is the reasoning layer: it decides *whether* a design is good and *why*. `clean-code` gives the rules below the class level and `software-architecture` the rules above it. `refactor-proposal` turns a concrete new ask into a justified set of changes, leaning on `clean-code` for the smell catalog and on `tdd` to keep behavior pinned while structure changes. `architecture-diagram` keeps the repo's living diagram current so `software-architecture` reviews start from the real structure. The skills reference each other by name, so install them together.

## Install

With the [`skills`](https://github.com/vercel-labs/skills) CLI (Node.js 22.20+). It asks which skills and agents to install; pick all six, since they reference each other:

```sh
npx skills add nohemi20231/design-skills      # this project
npx skills add nohemi20231/design-skills -g   # every project
```

Or by hand.

Personal (available in every project):

```sh
git clone https://github.com/nohemi20231/design-skills.git
cp -R design-skills/skills/* ~/.claude/skills/
```

Per project (shared with the team through git):

```sh
cp -R design-skills/skills/* your-project/.claude/skills/
```

Claude Code picks up any folder under `.claude/skills/` that contains a `SKILL.md`. Invoke a skill with `/software-design`, `/refactor-proposal`, `/architecture-diagram`, and so on, or let Claude load it when the description matches the task.

### GitHub Copilot

The same files work unchanged. Each skill is a folder with a `SKILL.md` whose frontmatter has only `name` and `description`, which is the shared Agent Skills format Copilot reads.

As a plugin, in a terminal with the GitHub Copilot CLI:

```sh
copilot plugin marketplace add nohemi20231/design-skills
copilot plugin install design-skills@design-skills
```

To update, run the install command again. See [`CHANGELOG.md`](CHANGELOG.md) for what changed in each version. The repo is a plugin in the Agent Plugins 1.0 format: `plugin.json` at the root and the skills under `skills/`.

Or copy the folders by hand. In a project, Copilot loads skills from `.github/skills/` and also from `.claude/skills/`, so one copy serves both tools. For personal skills, copy the folders into `~/.copilot/skills/`.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
