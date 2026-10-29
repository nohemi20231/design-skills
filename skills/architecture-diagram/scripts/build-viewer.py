#!/usr/bin/env python3
"""Build one HTML page that shows every Mermaid diagram in the architecture docs,
with pan and zoom, a sidebar, the source text and an SVG download.

Run from the repo root:

    python3 docs/architecture/diagrams/build-viewer.py
    python3 docs/architecture/diagrams/build-viewer.py --out docs/diagrams.html
    python3 docs/architecture/diagrams/build-viewer.py docs/architecture.md docs/architecture/services

With no paths it reads docs/architecture.md and every markdown file under
docs/architecture/, in path order, skipping files whose name contains one of
the --exclude strings (default: the blueprint's decomposition proposals, which
are history, not the living design). Then open the HTML in a browser; it loads
Mermaid from jsDelivr, so it needs the network once.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

DEFAULT_OUT = Path("docs/architecture/diagrams/viewer.html")
DEFAULT_EXCLUDE = ("decomposition-",)

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def extract(path: Path, root: Path) -> dict:
    """Return {"title", "path", "diagrams": [{"title", "line", "source"}]}."""
    lines = path.read_text(encoding="utf-8").splitlines()
    file_title = path.stem
    heading = file_title
    diagrams = []
    in_block = False
    block: list[str] = []
    start = 0
    for number, line in enumerate(lines, start=1):
        if in_block:
            if line.strip().startswith("```"):
                diagrams.append({"title": heading, "line": start, "source": "\n".join(block)})
                in_block, block = False, []
            else:
                block.append(line)
            continue
        match = HEADING.match(line)
        if match:
            text = match.group(2)
            if match.group(1) == "#" and file_title == path.stem:
                file_title = text
            heading = text
        elif line.strip() == "```mermaid":
            in_block, block, start = True, [], number
    return {"title": file_title, "path": str(path.resolve().relative_to(root.resolve())), "diagrams": diagrams}


def discover(root: Path, paths: list[str], exclude: tuple[str, ...]) -> list[Path]:
    """Markdown files to scan, in reading order."""
    if paths:
        candidates: list[Path] = []
        for given in paths:
            path = Path(given)
            candidates += sorted(path.rglob("*.md")) if path.is_dir() else [path]
    else:
        top = root / "docs" / "architecture.md"
        candidates = ([top] if top.exists() else []) + sorted((root / "docs" / "architecture").rglob("*.md"))
    return [path for path in candidates if not any(part in path.name for part in exclude)]


def build(root: Path, out: Path, paths: list[str], exclude: tuple[str, ...]) -> None:
    groups = [extract(path, root) for path in discover(root, paths, exclude)]
    groups = [group for group in groups if group["diagrams"]]
    count = sum(len(group["diagrams"]) for group in groups)
    data = json.dumps(groups, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", data).replace("__DATE__", date.today().isoformat())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}: {count} diagrams from {len(groups)} files")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Answerplate diagrams</title>
<style>
  :root {
    --bg: #f6f7f9; --panel: #ffffff; --ink: #1c1f24; --muted: #6b7280;
    --line: #e2e5ea; --accent: #2563eb; --accent-ink: #ffffff; --hover: #eef2f7;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #15171b; --panel: #1e2126; --ink: #e8eaed; --muted: #9aa3ad;
      --line: #30343b; --accent: #60a5fa; --accent-ink: #0b1220; --hover: #272b32;
    }
  }
  :root[data-theme="dark"] {
    --bg: #15171b; --panel: #1e2126; --ink: #e8eaed; --muted: #9aa3ad;
    --line: #30343b; --accent: #60a5fa; --accent-ink: #0b1220; --hover: #272b32;
  }
  * { box-sizing: border-box; }
  html, body { height: 100%; margin: 0; }
  body {
    background: var(--bg); color: var(--ink);
    font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    display: grid; grid-template-columns: 300px 1fr; grid-template-rows: 100%;
  }
  nav {
    background: var(--panel); border-right: 1px solid var(--line); overflow-y: auto; padding: 12px 0 24px;
  }
  nav h1 { font-size: 15px; margin: 4px 16px 12px; }
  nav h1 small { display: block; font-weight: normal; color: var(--muted); font-size: 12px; }
  nav .group { margin: 10px 0 2px; }
  nav .group-title {
    font-size: 11px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted);
    padding: 6px 16px 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  nav button {
    display: block; width: 100%; text-align: left; background: none; border: 0; color: var(--ink);
    font: inherit; padding: 6px 16px 6px 24px; cursor: pointer; border-left: 3px solid transparent;
  }
  nav button:hover { background: var(--hover); }
  nav button.active { border-left-color: var(--accent); background: var(--hover); font-weight: 600; }
  main { display: grid; grid-template-rows: auto 1fr; min-width: 0; min-height: 0; }
  header {
    display: flex; flex-wrap: wrap; align-items: center; gap: 8px; padding: 10px 16px;
    border-bottom: 1px solid var(--line); background: var(--panel);
  }
  header .title { font-weight: 600; margin-right: auto; min-width: 0; }
  header .title small { display: block; font-weight: normal; color: var(--muted); font-size: 12px; }
  header button, header label {
    font: inherit; padding: 5px 10px; border-radius: 6px; border: 1px solid var(--line);
    background: var(--panel); color: var(--ink); cursor: pointer;
  }
  header button:hover { background: var(--hover); }
  header .zoom { min-width: 54px; text-align: center; color: var(--muted); }
  #stage {
    position: relative; overflow: hidden; cursor: grab; touch-action: none; min-height: 0;
    background-image: radial-gradient(var(--line) 1px, transparent 1px); background-size: 24px 24px;
  }
  #stage.dragging { cursor: grabbing; }
  #canvas { position: absolute; left: 0; top: 0; transform-origin: 0 0; will-change: transform; }
  #canvas svg { display: block; max-width: none !important; }
  #source {
    display: none; position: absolute; right: 0; top: 0; bottom: 0; width: min(560px, 60%);
    overflow: auto; margin: 0; padding: 14px 16px; background: var(--panel); border-left: 1px solid var(--line);
    font: 12px/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; white-space: pre; color: var(--ink);
  }
  #stage.show-source #source { display: block; }
  .error {
    margin: 24px; padding: 12px 16px; max-width: 720px; border-radius: 8px; white-space: pre-wrap;
    background: #fde8e8; color: #7f1d1d; border: 1px solid #f5b5b5;
    font: 12px/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  }
  .hint { position: absolute; left: 12px; bottom: 10px; color: var(--muted); font-size: 12px; pointer-events: none; }
  @media (max-width: 760px) {
    body { grid-template-columns: 1fr; grid-template-rows: auto 1fr; }
    nav { max-height: 32vh; border-right: 0; border-bottom: 1px solid var(--line); }
    #source { width: 100%; }
  }
</style>
</head>
<body>
<nav id="nav">
  <h1>Answerplate diagrams <small>Built __DATE__ from the markdown in docs/</small></h1>
</nav>
<main>
  <header>
    <div class="title"><span id="title"></span><small id="subtitle"></small></div>
    <button id="prev" title="Previous (←)">◀</button>
    <button id="next" title="Next (→)">▶</button>
    <button id="zoom-out" title="Zoom out (-)">−</button>
    <span class="zoom" id="zoom-level">100%</span>
    <button id="zoom-in" title="Zoom in (+)">+</button>
    <button id="fit" title="Fit to window (F)">Fit</button>
    <button id="reset" title="Actual size (1)">1:1</button>
    <button id="toggle-source" title="Show the Mermaid source (S)">Source</button>
    <button id="download" title="Download this diagram as SVG">SVG</button>
    <button id="theme" title="Switch light / dark">Theme</button>
  </header>
  <div id="stage">
    <div id="canvas"></div>
    <pre id="source"></pre>
    <div class="hint">Scroll to zoom, drag to pan. Keys: ← → + − F 1 S</div>
  </div>
</main>

<script id="data" type="application/json">__DATA__</script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
<script>
(function () {
  var groups = JSON.parse(document.getElementById('data').textContent);
  var items = [];
  groups.forEach(function (group) {
    group.diagrams.forEach(function (diagram) {
      items.push({ group: group, diagram: diagram });
    });
  });

  var nav = document.getElementById('nav');
  var stage = document.getElementById('stage');
  var canvas = document.getElementById('canvas');
  var sourceBox = document.getElementById('source');
  var zoomLabel = document.getElementById('zoom-level');
  var current = -1;
  var scale = 1, tx = 0, ty = 0;
  var svgText = '';

  function isDark() {
    var forced = document.documentElement.getAttribute('data-theme');
    if (forced) return forced === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function configureMermaid() {
    mermaid.initialize({ startOnLoad: false, theme: isDark() ? 'dark' : 'default', securityLevel: 'loose',
      sequence: { useMaxWidth: false }, flowchart: { useMaxWidth: false }, class: { useMaxWidth: false },
      state: { useMaxWidth: false } });
  }

  function buildNav() {
    groups.forEach(function (group, g) {
      var box = document.createElement('div');
      box.className = 'group';
      var title = document.createElement('div');
      title.className = 'group-title';
      title.textContent = group.title;
      title.title = group.path;
      box.appendChild(title);
      group.diagrams.forEach(function (diagram) {
        var button = document.createElement('button');
        button.textContent = diagram.title;
        var index = items.findIndex(function (item) { return item.diagram === diagram; });
        button.dataset.index = index;
        button.addEventListener('click', function () { show(index); });
        box.appendChild(button);
      });
      nav.appendChild(box);
    });
  }

  function apply() {
    canvas.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + scale + ')';
    zoomLabel.textContent = Math.round(scale * 100) + '%';
  }
  function diagramSize() {
    var svg = canvas.querySelector('svg');
    if (!svg) return { w: 0, h: 0 };
    return { w: svg.getBoundingClientRect().width / scale, h: svg.getBoundingClientRect().height / scale };
  }
  function fit() {
    var size = diagramSize();
    if (!size.w || !size.h) return;
    var pad = 32;
    var visibleWidth = stage.clientWidth - (stage.classList.contains('show-source') ? sourceBox.offsetWidth : 0);
    scale = Math.min((visibleWidth - pad) / size.w, (stage.clientHeight - pad) / size.h, 4);
    tx = (visibleWidth - size.w * scale) / 2;
    ty = (stage.clientHeight - size.h * scale) / 2;
    apply();
  }
  function actualSize() {
    scale = 1; tx = 24; ty = 24; apply();
  }
  function zoomAt(factor, cx, cy) {
    var next = Math.min(Math.max(scale * factor, 0.1), 12);
    factor = next / scale;
    tx = cx - (cx - tx) * factor;
    ty = cy - (cy - ty) * factor;
    scale = next;
    apply();
  }
  function zoomCenter(factor) {
    zoomAt(factor, stage.clientWidth / 2, stage.clientHeight / 2);
  }

  function show(index) {
    if (index < 0 || index >= items.length) return;
    current = index;
    var item = items[index];
    location.hash = '#' + index;
    document.getElementById('title').textContent = item.diagram.title;
    document.getElementById('subtitle').textContent = item.group.title + ' · ' + item.group.path + ':' + item.diagram.line;
    sourceBox.textContent = item.diagram.source;
    nav.querySelectorAll('button').forEach(function (button) {
      button.classList.toggle('active', Number(button.dataset.index) === index);
    });
    canvas.innerHTML = '';
    svgText = '';
    mermaid.render('d' + index + '-' + Date.now(), item.diagram.source).then(function (result) {
      if (current !== index) return;
      canvas.innerHTML = result.svg;
      var svg = canvas.querySelector('svg');
      var box = svg.viewBox && svg.viewBox.baseVal;
      if (box && box.width && box.height) {
        svg.setAttribute('width', box.width);
        svg.setAttribute('height', box.height);
        svg.style.width = box.width + 'px';
        svg.style.height = box.height + 'px';
      }
      svg.removeAttribute('style');
      svgText = svg.outerHTML;
      if (result.bindFunctions) result.bindFunctions(canvas);
      fit();
    }).catch(function (error) {
      canvas.innerHTML = '';
      var pre = document.createElement('div');
      pre.className = 'error';
      pre.textContent = 'Mermaid could not render this diagram.\n\n' + (error && error.message ? error.message : error);
      canvas.appendChild(pre);
      scale = 1; tx = 0; ty = 0; apply();
    });
  }

  // Pan with the pointer.
  var dragging = null;
  stage.addEventListener('pointerdown', function (event) {
    if (event.button !== 0 || sourceBox.contains(event.target)) return;
    dragging = { x: event.clientX, y: event.clientY, tx: tx, ty: ty };
    stage.classList.add('dragging');
    stage.setPointerCapture(event.pointerId);
  });
  stage.addEventListener('pointermove', function (event) {
    if (!dragging) return;
    tx = dragging.tx + (event.clientX - dragging.x);
    ty = dragging.ty + (event.clientY - dragging.y);
    apply();
  });
  function endDrag() { dragging = null; stage.classList.remove('dragging'); }
  stage.addEventListener('pointerup', endDrag);
  stage.addEventListener('pointercancel', endDrag);

  // Zoom with the wheel (trackpad pinch arrives as ctrlKey + wheel).
  stage.addEventListener('wheel', function (event) {
    if (sourceBox.contains(event.target)) return;
    event.preventDefault();
    var rect = stage.getBoundingClientRect();
    var factor = Math.exp(-event.deltaY * (event.ctrlKey ? 0.01 : 0.002));
    zoomAt(factor, event.clientX - rect.left, event.clientY - rect.top);
  }, { passive: false });

  document.getElementById('zoom-in').addEventListener('click', function () { zoomCenter(1.25); });
  document.getElementById('zoom-out').addEventListener('click', function () { zoomCenter(0.8); });
  document.getElementById('fit').addEventListener('click', fit);
  document.getElementById('reset').addEventListener('click', actualSize);
  document.getElementById('prev').addEventListener('click', function () { show(current - 1); });
  document.getElementById('next').addEventListener('click', function () { show(current + 1); });
  document.getElementById('toggle-source').addEventListener('click', function () {
    stage.classList.toggle('show-source');
  });
  document.getElementById('download').addEventListener('click', function () {
    if (!svgText) return;
    var blob = new Blob([svgText], { type: 'image/svg+xml' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = items[current].diagram.title.replace(/[^a-z0-9]+/gi, '-').toLowerCase() + '.svg';
    link.click();
    URL.revokeObjectURL(link.href);
  });
  document.getElementById('theme').addEventListener('click', function () {
    document.documentElement.setAttribute('data-theme', isDark() ? 'light' : 'dark');
    configureMermaid();
    show(current);
  });
  document.addEventListener('keydown', function (event) {
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') return;
    switch (event.key) {
      case 'ArrowLeft': show(current - 1); break;
      case 'ArrowRight': show(current + 1); break;
      case '+': case '=': zoomCenter(1.25); break;
      case '-': case '_': zoomCenter(0.8); break;
      case 'f': case 'F': fit(); break;
      case '1': actualSize(); break;
      case 's': case 'S': stage.classList.toggle('show-source'); break;
      default: return;
    }
    event.preventDefault();
  });
  window.addEventListener('resize', fit);

  configureMermaid();
  buildNav();
  var start = parseInt(location.hash.slice(1), 10);
  show(isNaN(start) ? 0 : Math.min(Math.max(start, 0), items.length - 1));
})();
</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", help="markdown files or folders to scan (default: docs/architecture)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"HTML file to write (default: {DEFAULT_OUT})")
    parser.add_argument("--exclude", action="append", default=None, metavar="TEXT",
                        help="skip files whose name contains TEXT (repeatable; default: decomposition-)")
    args = parser.parse_args()
    exclude = tuple(args.exclude) if args.exclude is not None else DEFAULT_EXCLUDE
    build(Path.cwd(), args.out, args.paths, exclude)


if __name__ == "__main__":
    main()
