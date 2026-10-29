---
name: architecture-diagram
description: Use at the start of any design, feature, or refactoring work in a repo to read the living architecture diagram, and whenever services, modules, data stores, or integrations change, to update it.
---

# Living Architecture Diagram

Maintain one source-of-truth file, `docs/architecture.md`, that describes the system's structure. Read it for context and keep it current. It works with the `software-architecture` skill.

## Reading (start of a task)
1. Before any design, feature, or refactoring work, read `docs/architecture.md`.
2. Use it to locate where the change belongs and which boundaries and contracts it touches.
3. If the file and the code disagree, trust the code. Flag the drift and fix the file as part of the task.
4. If the file doesn't exist, offer to create it by surveying the codebase, using the build files, package structure, configs, and docker-compose or k8s manifests.

## Updating (end of a task)
Update the file in the same change set whenever any of these change:
- services or modules are added, removed, or renamed
- a dependency between them is added, removed, or renamed
- data stores or data ownership change
- sync or async integrations change: REST, gRPC, topics, or queues
- external systems or the auth flow change

Internal refactors that leave boundaries intact don't need an update. When you update the file, bump `Last updated` and add a one-line entry to the changelog.

## The zoomable HTML viewer
GitHub renders Mermaid small and does not zoom, so every repo also keeps one HTML page that shows
all of its architecture diagrams with pan and zoom: `docs/architecture/diagrams/viewer.html`.
A generator builds it from the markdown; the markdown stays the source of truth.

1. **First time in a repo**: copy `scripts/build-viewer.py` from this skill's folder to
   `docs/architecture/diagrams/build-viewer.py`, so the repo can rebuild the page without the skill.
2. **After every diagram change**, in the same change set as the markdown, run from the repo root:

   ```
   python3 docs/architecture/diagrams/build-viewer.py
   ```

   It scans `docs/architecture.md` and every markdown file under `docs/architecture/`, skipping the
   blueprint's `decomposition-*` proposals (history, not the living design). Pass paths to scan
   something else, `--out` for another output file, `--exclude TEXT` to skip more files.
3. **Check the count it prints** against the number of ```` ```mermaid ```` blocks you expect, then
   open the page in a browser and click through the diagrams you touched. A diagram that Mermaid
   cannot parse shows its error and the source in the page; fix the markdown, not the HTML.
4. Commit the HTML with the markdown. Tell the user the page exists when you first create it.

The page loads Mermaid from jsDelivr, so it needs the network the first time it opens. Each diagram
has a sidebar entry, keyboard navigation, a source pane and an SVG download.

## File structure
The file has these sections, in order:

1. **Overview**: two or three sentences on what the system does.
2. **Context diagram (C4 level 1)**: Mermaid `flowchart` showing users, the system, and external systems.
3. **Container diagram (C4 level 2)**: Mermaid `flowchart` showing services and apps, their databases, and the message broker. Label every edge with its protocol and purpose, for example `REST: create order` or `event: OrderPlaced`.
4. **Components**: for any complex service, a level-3 diagram of its modules, ports, and adapters.
5. **Service catalog**: a table with these columns:
   - service
   - responsibility (one line)
   - owns data
   - exposes APIs
   - publishes events
   - consumes events
6. **Key flows**: Mermaid `sequenceDiagram`s for two to five critical flows.
7. **Decisions**: links to ADRs.
8. **Last updated**: a date, plus a short changelog.

## Rules
- Use Mermaid only, so the diagrams diff cleanly in version control and render on GitHub and GitLab.
- No second colon in a `stateDiagram-v2` transition label (`A --> B : at day 30: purge` breaks the parser). Use a dash or a comma inside the label.
- One fact lives in one place. Keep the diagram and the service catalog consistent with each other.
- Keep each diagram readable, at roughly 15 nodes or fewer. Split by level of detail rather than cramming.
- Use the same names as the code (service names, module names, topic names).
- Describe the system as it is. Put planned changes in a clearly marked **Proposed** section, never mixed into the current state.
