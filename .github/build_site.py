#!/usr/bin/env python3
"""Build a browsable static copy of a repository for GitHub Pages.

Usage: build_site.py SRC DEST

What it does:
  1. Copies SRC to DEST (skipping .git, .github and DEST itself), so every
     file keeps its exact path: foo/bar/test.c -> DEST/foo/bar/test.c
  2. Renders every *.md file to a sibling *.md.html page; the raw .md file
     is left untouched.
  3. Writes an index.html directory listing into every directory. Markdown
     files link to the rendered page, with a "(raw)" link after the name, and a directory's
     README.md is rendered below its listing.

All links are relative, so the site works at the domain root, under a
project path (user.github.io/repo/) and on a custom domain.
"""

import html
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

import markdown

SITE_HOST = os.environ.get("SITE_HOST", "i.ř.xyz")
TOP_LEVEL_EXCLUDES = {".git", ".github", "_site"}
MD_EXTENSIONS = ["fenced_code", "tables", "toc", "sane_lists"]

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Crect width='100' height='100' rx='14' fill='%231D1A17'/%3E%3Ctext x='50' y='78' "
    "font-family='Courier New,Courier,monospace' font-weight='700' font-size='80' "
    "text-anchor='middle' fill='%23D6CEBD'%3E%C5%98%3C/text%3E%3C/svg%3E"
)

NOISE = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E"
    "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' "
    "stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0.85 0 0 0 0 0.80 0 0 0 0 0.70 "
    "0 0 0 0.06 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E"
    "%3C/svg%3E"
)

STYLE = """
  :root {
    color-scheme: dark;
    --paper: #1D1A17;        /* warm charcoal-brown page */
    --paper-edge: #100E0C;   /* vignette at the page edges */
    --ink: #D6CEBD;          /* soft cream text */
    --ink-faded: #918878;    /* warm grey for secondary text */
    --accent: #D9724F;       /* muted terracotta: links, hover, markers */
    --rule: rgba(145, 136, 120, 0.35);
    --rule-soft: rgba(145, 136, 120, 0.22);
    --tint: rgba(255, 240, 215, 0.07);   /* inline code background */
    --inset: rgba(0, 0, 0, 0.28);        /* code block background */
    --font: "Courier Prime", "Courier New", Courier, "Nimbus Mono PS", monospace;
  }

  *, *::before, *::after { box-sizing: border-box; }
  html, body { min-height: 100dvh; margin: 0; }
  html { scrollbar-color: #4A443B #1D1A17; }

  body {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: var(--ink);
    font-family: var(--font);
    -webkit-font-smoothing: antialiased;
    background-color: var(--paper);
    background-image:
      url("__NOISE__"),
      radial-gradient(ellipse at 50% 45%, transparent 55%, var(--paper-edge) 130%);
    background-attachment: fixed;
    padding:
      calc(2rem + env(safe-area-inset-top, 0px))
      calc(1.5rem + env(safe-area-inset-right, 0px))
      calc(2rem + env(safe-area-inset-bottom, 0px))
      calc(1.5rem + env(safe-area-inset-left, 0px));
  }

  ::selection { background: var(--accent); color: var(--paper); }

  main {
    width: 100%;
    max-width: 760px;
  }

  /* ---- links ---- */
  a {
    color: var(--ink);
    text-decoration: underline;
    text-decoration-color: var(--accent);
    text-decoration-thickness: 2px;
    text-underline-offset: 0.25em;
    padding: 0 0.15em;
    transition: color 0.15s ease, background-color 0.15s ease;
  }
  a:hover { color: var(--paper); background-color: var(--accent); text-decoration: none; }
  a:focus-visible { outline: 2px dashed var(--accent); outline-offset: 3px; }

  /* ---- title: i.ř.xyz/current/path/ ---- */
  h1.site-title {
    margin: 0;
    text-align: left;
    font-size: clamp(0.95rem, 3.4vw, 1.2rem);
    font-weight: 700;
    line-height: 1.5;
    overflow-wrap: anywhere;
  }
  h1.site-title a { color: inherit; text-decoration: none; padding: 0; background: none; }
  h1.site-title a:hover { color: var(--accent); background: none; }
  h1.site-title .path,
  h1.site-title .path a,
  h1.site-title .slash { font-weight: 400; color: var(--ink-faded); }
  h1.site-title .path a:hover { color: var(--accent); }

  .meta-inline {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: flex-start;
    gap: 0.5rem 0.75rem;
    margin: 0.5rem 0 0;
    font-size: 0.9rem;
    color: var(--ink-faded);
  }
  .meta-sep { color: var(--ink-faded); user-select: none; }
  .meta-inline a { text-decoration: none; padding: 0; }
  .meta-inline a:hover { color: var(--accent); background: none; }

  /* ---- plain thin rule ---- */
  .rule {
    height: 0;
    margin: 1.25rem 0;
    border: 0;
    border-top: 1px solid var(--rule);
  }

  /* ---- directory listing ---- */
  table.files { width: 100%; border-collapse: collapse; font-size: 1.05rem; }
  table.files td {
    padding: 0.4rem 0;
    border-bottom: 1px solid var(--rule-soft);
    vertical-align: baseline;
  }
  table.files td.icon { width: 1.75rem; color: var(--ink-faded); }
  svg.ico {
    width: 1.1em; height: 1.1em; vertical-align: -0.2em;
    fill: none; stroke: currentColor; stroke-width: 1.6;
    stroke-linecap: round; stroke-linejoin: round;
  }
  table.files td.name { overflow-wrap: anywhere; }
  table.files tr.up td.name { color: var(--ink-faded); }
  table.files a { color: inherit; text-decoration: none; padding: 0; }
  table.files a:hover { color: var(--accent); background: none; }
  table.files td.size {
    text-align: right;
    white-space: nowrap;
    padding-left: 1rem;
    color: var(--ink-faded);
    font-size: 0.9rem;
  }
  table.files a.raw {
    margin: 0 0 0 0.5rem;
    color: var(--ink-faded);
    font-size: 0.85rem;
  }
  table.files a.raw:hover { color: var(--accent); }

  table.files + .md { margin-top: 2rem; }

  /* ---- rendered markdown ---- */
  .md { font-size: 1.05rem; line-height: 1.75; overflow-wrap: break-word; }
  .md > :first-child { margin-top: 0; }
  .md h1, .md h2, .md h3, .md h4, .md h5, .md h6 {
    margin: 2rem 0 0.75rem; line-height: 1.3; font-weight: 700;
  }
  .md h1 { font-size: 1.9rem; }
  .md h2 { font-size: 1.5rem; padding-bottom: 0.25rem; border-bottom: 1px solid var(--rule); }
  .md h3 { font-size: 1.25rem; }
  .md h4 { font-size: 1.1rem; }
  .md h5, .md h6 { font-size: 1rem; }
  .md h6 { color: var(--ink-faded); }
  .md p, .md ul, .md ol, .md pre, .md blockquote, .md table, .md details { margin: 0 0 1rem; }
  .md ul, .md ol { padding-left: 1.75rem; }
  .md li > ul, .md li > ol { margin: 0.25rem 0; }
  .md li::marker { color: var(--accent); }
  .md code {
    font-family: inherit; font-size: 0.95em;
    padding: 0.1em 0.3em; border-radius: 2px;
    background: var(--tint);
  }
  .md pre {
    padding: 0.9rem 1rem; overflow-x: auto; line-height: 1.5;
    border: 1px solid var(--rule-soft); border-radius: 2px;
    background: var(--inset);
  }
  .md pre code { padding: 0; background: none; font-size: 0.9rem; }
  .md blockquote {
    margin-left: 0; padding: 0.1rem 1rem;
    border-left: 3px solid var(--accent); color: var(--ink-faded);
  }
  .md table { display: block; max-width: 100%; overflow-x: auto; border-collapse: collapse; }
  .md th, .md td { padding: 0.4rem 0.75rem; border: 1px solid var(--rule); }
  .md th { text-align: left; border-bottom: 2px solid var(--ink); }
  .md img { max-width: 100%; height: auto; }
  .md kbd {
    padding: 0.05em 0.4em; border: 1px solid var(--ink-faded); border-radius: 2px;
    font-family: inherit; font-size: 0.9em;
  }
  .md mark { background: rgba(217, 114, 79, 0.28); color: inherit; padding: 0 0.15em; }
  .md summary { cursor: pointer; }
  .md .toc { margin: 1rem 0; padding: 0.25rem 1rem; border-left: 3px solid var(--accent); }
  .md .toc ul { margin: 0.25rem 0; padding-left: 1.25rem; }
  .md hr {
    height: 0; margin: 2rem 0; border: 0;
    border-top: 1px solid var(--rule);
  }
""".replace("__NOISE__", NOISE)

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="theme-color" content="#1D1A17">
<link rel="icon" href="{favicon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>{style}</style></head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="i-folder" viewBox="0 0 24 24"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></symbol>
  <symbol id="i-file" viewBox="0 0 24 24"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/></symbol>
  <symbol id="i-up" viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></symbol>
</svg>
<main>
{body}
</main>
</body></html>
"""


def is_md(name: str) -> bool:
    return name.lower().endswith(".md")


def href(name: str) -> str:
    """URL-quote a single path segment for use in an href attribute."""
    return quote(name)


def render_md(text: str) -> str:
    body = markdown.markdown(text, extensions=MD_EXTENSIONS)

    # Point relative links to other .md files at their rendered pages.
    def fix(m: re.Match) -> str:
        target, rest = m.group(1), m.group(2) or ""
        if target.startswith("//"):  # protocol-relative URL, leave alone
            return m.group(0)
        return f'href="{target}.html{rest}"'

    return re.sub(r'href="([^"#?:]+\.md)([#?][^"]*)?"', fix, body, flags=re.IGNORECASE)


def human_size(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{int(size)} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{n} B"


def page(title: str, body: str) -> str:
    return PAGE.format(
        title=html.escape(title), favicon=FAVICON, style=STYLE, body=body
    )


def icon_cell(name: str) -> str:
    return f'<td class="icon"><svg class="ico" aria-hidden="true"><use href="#i-{name}"/></svg></td>'


def title_text(dir_parts: tuple, filename: str = "") -> str:
    return SITE_HOST + "/" + "".join(p + "/" for p in dir_parts) + filename


def header(dir_parts: tuple, filename: str = "", nav: str = "") -> str:
    """Site title (host + current path, each directory clickable) and divider."""
    depth = len(dir_parts)
    parts = [
        f'<a class="host" href="{"../" * depth or "./"}">{html.escape(SITE_HOST)}</a>'
        '<span class="path"><span class="slash">/</span>'
    ]
    for i, part in enumerate(dir_parts):
        up = depth - i - 1
        parts.append(
            f'<a href="{"../" * up or "./"}">{html.escape(part)}</a>'
            '<span class="slash">/</span>'
        )
    parts.append(html.escape(filename))
    parts.append("</span>")

    out = f'<h1 class="site-title">{"".join(parts)}</h1>\n'
    if nav:
        out += f'<p class="meta-inline">{nav}</p>\n'
    out += '<div class="rule" role="separator" aria-hidden="true"></div>\n'
    return out


def copy_repo(src: Path, dest: Path) -> None:
    def ignore(directory: str, names: list) -> set:
        if Path(directory).resolve() == src:
            return {n for n in names if n in TOP_LEVEL_EXCLUDES}
        return {n for n in names if n == ".git"}  # e.g. submodules

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=ignore)
    (dest / ".nojekyll").touch()


def render_all_markdown(dest: Path) -> int:
    md_files = [p for p in dest.rglob("*") if p.is_file() and is_md(p.name)]
    for md in md_files:
        parts = md.parent.relative_to(dest).parts
        text = md.read_text(encoding="utf-8", errors="replace")
        nav = (
            '<a href="./">&larr; Directory</a><span class="meta-sep">-</span>'
            f'<a href="{href(md.name)}">raw</a>'
        )
        body = (
            header(parts, md.name, nav)
            + f'<article class="md">{render_md(text)}</article>\n'
        )
        out = md.with_name(md.name + ".html")
        out.write_text(page(title_text(parts, md.name), body), encoding="utf-8")
    return len(md_files)


def build_listing(d: Path, root: Path) -> bool:
    index = d / "index.html"
    if index.exists():
        # A real index.html from the repo: keep it, don't overwrite.
        print(f"note: keeping existing {index.relative_to(root)}", file=sys.stderr)
        return False

    entries = list(d.iterdir())
    names = {p.name for p in entries}

    def is_generated(p: Path) -> bool:
        # hide X.md.html when X.md exists next to it
        return p.name.endswith(".md.html") and p.name[:-5] in names

    dirs = sorted((p for p in entries if p.is_dir()), key=lambda p: p.name.lower())
    files = sorted(
        (
            p
            for p in entries
            if p.is_file()
            and not is_generated(p)
            and not (d == root and p.name == ".nojekyll")
        ),
        key=lambda p: p.name.lower(),
    )

    rows = []
    if d != root:
        rows.append(
            '<tr class="up">' + icon_cell("up")
            + '<td class="name"><a href="../">../</a></td><td class="size"></td></tr>'
        )
    for p in dirs:
        rows.append(
            '<tr class="dir">' + icon_cell("folder")
            + f'<td class="name"><a href="{href(p.name)}/">{html.escape(p.name)}/</a></td>'
            '<td class="size"></td></tr>'
        )
    for p in files:
        if is_md(p.name) and (p.name + ".html") in names:
            # markdown: the name opens the rendered page, "(raw)" opens the source
            cell = (
                f'<a href="{href(p.name)}.html">{html.escape(p.name)}</a>'
                f'<a class="raw" href="{href(p.name)}">(raw)</a>'
            )
        else:
            cell = f'<a href="{href(p.name)}">{html.escape(p.name)}</a>'
        rows.append(
            '<tr class="file">' + icon_cell("file")
            + f'<td class="name">{cell}</td>'
            f'<td class="size">{human_size(p.stat().st_size)}</td></tr>'
        )

    parts = d.relative_to(root).parts
    body = header(parts) + f'<table class="files">{"".join(rows)}</table>\n'

    readme = next((p for p in files if p.name.lower() == "readme.md"), None)
    if readme is not None:
        text = readme.read_text(encoding="utf-8", errors="replace")
        body += f'<article class="md">{render_md(text)}</article>\n'

    index.write_text(page(title_text(parts), body), encoding="utf-8")
    return True


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} SRC DEST")
    src = Path(sys.argv[1]).resolve()
    dest = Path(sys.argv[2]).resolve()

    copy_repo(src, dest)
    n_md = render_all_markdown(dest)

    directories = [Path(p) for p, _, _ in os.walk(dest)]
    n_idx = sum(build_listing(d, dest) for d in directories)

    print(f"Rendered {n_md} markdown file(s), generated {n_idx} directory listing(s) in {dest}")


if __name__ == "__main__":
    main()