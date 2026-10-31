# Changelog

Versions match `plugin.json` and `.github/plugin/marketplace.json`.

## 1.1.0 - Architecture diagram (2026-10-28)
- New `architecture-diagram` skill: read the repo's living architecture diagram before design, feature or refactoring work, and update it whenever services, modules, data stores or integrations change.
- Ships `scripts/build-viewer.py`, which builds one HTML page showing every Mermaid diagram in the architecture docs, with pan and zoom, the source text and an SVG download.
- `software-architecture` reviews now start from the real structure via `architecture-diagram`. The plugin has six skills.

## 1.0.0 - Copilot plugin (2026-10-19)
- Five skills: `software-design`, `refactor-proposal`, `clean-code`, `tdd`, `software-architecture`. They reference each other by name, so install them together.
- The same `SKILL.md` files work unchanged in GitHub Copilot (frontmatter has only `name` and `description`).
- Packaged as a plugin in the Agent Plugins 1.0 format: skills under `skills/`, `plugin.json` at the root, and `.github/plugin/marketplace.json` so the repo installs with `copilot plugin marketplace add nohemi20231/design-skills`.
