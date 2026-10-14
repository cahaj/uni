#!/usr/bin/env python3
"""Build a browsable static copy of a repository for GitHub Pages.

Usage: build_site.py SRC DEST

What it does:
  1. Copies SRC to DEST (skipping .git, .github and DEST itself), so every
     file keeps its exact path: foo/bar/test.c -> DEST/foo/bar/test.c
  2. Renders every *.md file to a sibling *.md.html page; the raw .md file
     is left untouched.
  3. Writes an index.html directory listing into every directory. Markdown
     files get a "(rendered)" link after their name, and a directory's
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
    "%3Crect width='100' height='100' rx='14' fill='%23E7E4DC'/%3E%3Ctext x='50' y='78' "
    "font-family='Courier New,Courier,monospace' font-weight='700' font-size='80' "
    "text-anchor='middle' fill='%2322232A'%3E%C5%98%3C/text%3E%3C/svg%3E"
)

NOISE = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E"
    "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' "
    "stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0.25 0 0 0 0 0.22 0 0 0 0 0.18 "
    "0 0 0 0.07 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E"
    "%3C/svg%3E"
)

STYLE = """
  :root {
    color-scheme: light;
    --paper: #E7E4DC;
    --paper-edge: #CFCBC0;
    --ink: #22232A;
    --ink-faded: #6D6B68;
    --ribbon: #B3372B;
    --font: "Courier Prime", "Courier New", Courier, "Nimbus Mono PS", monospace;
  }

  *, *::before, *::after { box-sizing: border-box; }
  html, body { min-height: 100dvh; margin: 0; }

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

  ::selection { background: var(--ribbon); color: var(--paper); }

  main {
    width: 100%;
    max-width: 760px;
    animation: appear 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  /* ---- links ---- */
  a {
    color: var(--ink);
    text-decoration: underline;
    text-decoration-color: var(--ribbon);
    text-decoration-thickness: 2px;
    text-underline-offset: 0.25em;
    padding: 0 0.15em;
    transition: color 0.15s ease, background-color 0.15s ease;
  }
  a:hover { color: var(--paper); background-color: var(--ribbon); text-decoration: none; }
  a:focus-visible { outline: 2px dashed var(--ribbon); outline-offset: 3px; }

  /* ---- title: i.ř.xyz/current/path/ ---- */
  h1.site-title {
    margin: 0;
    text-align: center;
    font-size: clamp(1.5rem, 6vw, 2.75rem);
    font-weight: 700;
    line-height: 1.25;
    overflow-wrap: anywhere;
    filter: url(#rough);
    text-shadow: 0 0 0.6px rgba(34, 35, 42, 0.55);
  }
  h1.site-title a { color: inherit; text-decoration: none; padding: 0; background: none; }
  h1.site-title a:hover { color: var(--ribbon); background: none; }
  h1.site-title .path,
  h1.site-title .path a,
  h1.site-title .slash { font-weight: 400; color: var(--ink-faded); }
  h1.site-title .path a:hover { color: var(--ribbon); }

  .meta-inline {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.75rem 1rem;
    margin: 1rem 0 0;
    font-size: 0.95rem;
    color: var(--ink-faded);
    text-align: center;
  }
  .meta-sep { color: var(--ink-faded); font-weight: bold; user-select: none; }

  /* ---- double dashed ribbon divider ---- */
  .ribbon-divider {
    width: 100%;
    margin: 1.75rem 0;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  .ribbon-divider::before, .ribbon-divider::after {
    content: "";
    display: block;
    width: 100%;
    height: 2px;
  }
  .ribbon-divider::before {
    background: repeating-linear-gradient(90deg,
      var(--ink-faded) 0px, var(--ink-faded) 8px, transparent 8px, transparent 14px);
  }
  .ribbon-divider::after {
    background: repeating-linear-gradient(90deg,
      var(--ribbon) 0px, var(--ribbon) 8px, transparent 8px, transparent 14px);
    background-position: 5px 0;
  }

  /* ---- directory listing ---- */
  table.files { width: 100%; border-collapse: collapse; font-size: 1.05rem; }
  table.files td {
    padding: 0.45rem 0;
    border-bottom: 1px dashed rgba(109, 107, 104, 0.45);
    vertical-align: baseline;
  }
  table.files td.name { overflow-wrap: anywhere; }
  table.files td.size {
    text-align: right;
    white-space: nowrap;
    padding-left: 1rem;
    color: var(--ink-faded);
    font-size: 0.9rem;
  }
  table.files tr.dir a { font-weight: 700; }
  table.files tr.up a { color: var(--ink-faded); }
  table.files tr.up a:hover { color: var(--paper); }
  table.files a.rendered {
    margin-left: 0.35rem;
    color: var(--ink-faded);
    font-size: 0.85rem;
    text-decoration-thickness: 1px;
  }
  table.files a.rendered:hover { color: var(--paper); }

  .label {
    display: inline-block;
    margin: 0 0 1.25rem;
    padding: 0.15rem 0.5rem;
    border: 1px solid var(--ink-faded);
    border-radius: 2px;
    color: var(--ink-faded);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
  }

  /* ---- rendered markdown ---- */
  .md { font-size: 1.05rem; line-height: 1.75; overflow-wrap: break-word; }
  .md > :first-child { margin-top: 0; }
  .md h1, .md h2, .md h3, .md h4, .md h5, .md h6 {
    margin: 2rem 0 0.75rem; line-height: 1.3; font-weight: 700;
  }
  .md h1 { font-size: 1.9rem; }
  .md h2 { font-size: 1.5rem; padding-bottom: 0.25rem; border-bottom: 1px dashed var(--ink-faded); }
  .md h3 { font-size: 1.25rem; }
  .md h4 { font-size: 1.1rem; }
  .md h5, .md h6 { font-size: 1rem; }
  .md h6 { color: var(--ink-faded); }
  .md p, .md ul, .md ol, .md pre, .md blockquote, .md table, .md details { margin: 0 0 1rem; }
  .md ul, .md ol { padding-left: 1.75rem; }
  .md li > ul, .md li > ol { margin: 0.25rem 0; }
  .md li::marker { color: var(--ribbon); }
  .md code {
    font-family: inherit; font-size: 0.95em;
    padding: 0.1em 0.3em; border-radius: 2px;
    background: rgba(34, 35, 42, 0.07);
  }
  .md pre {
    padding: 0.9rem 1rem; overflow-x: auto; line-height: 1.5;
    border: 1px solid var(--paper-edge); border-radius: 2px;
    background: rgba(34, 35, 42, 0.06);
  }
  .md pre code { padding: 0; background: none; font-size: 0.9rem; }
  .md blockquote {
    margin-left: 0; padding: 0.1rem 1rem;
    border-left: 3px solid var(--ribbon); color: var(--ink-faded);
  }
  .md table { display: block; max-width: 100%; overflow-x: auto; border-collapse: collapse; }
  .md th, .md td { padding: 0.4rem 0.75rem; border: 1px solid var(--paper-edge); }
  .md th { text-align: left; border-bottom: 2px solid var(--ink); }
  .md img { max-width: 100%; height: auto; }
  .md kbd {
    padding: 0.05em 0.4em; border: 1px solid var(--ink-faded); border-radius: 2px;
    font-family: inherit; font-size: 0.9em;
  }
  .md mark { background: rgba(179, 55, 43, 0.2); color: inherit; padding: 0 0.15em; }
  .md summary { cursor: pointer; }
  .md .toc { margin: 1rem 0; padding: 0.25rem 1rem; border-left: 3px solid var(--ribbon); }
  .md .toc ul { margin: 0.25rem 0; padding-left: 1.25rem; }
  .md hr {
    border: 0; height: 7px; margin: 2rem 0;
    background:
      repeating-linear-gradient(90deg,
        var(--ink-faded) 0px, var(--ink-faded) 8px, transparent 8px, transparent 14px)
        0 0 / 100% 2px no-repeat,
      repeating-linear-gradient(90deg,
        var(--ribbon) 0px, var(--ribbon) 8px, transparent 8px, transparent 14px)
        5px 5px / 100% 2px no-repeat;
  }

  @keyframes appear {
    0%   { opacity: 0; transform: translateY(12px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  @media (prefers-reduced-motion: reduce) { main { animation: none; } }
""".replace("__NOISE__", NOISE)

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="theme-color" content="#E7E4DC">
<link rel="icon" href="{favicon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>{style}</style></head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <filter id="rough" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="4" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="1.6" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
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
    out += '<div class="ribbon-divider" role="separator" aria-hidden="true"></div>\n'
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
            '<tr class="up"><td class="name"><a href="../">../</a></td>'
            '<td class="size"></td></tr>'
        )
    for p in dirs:
        rows.append(
            f'<tr class="dir"><td class="name"><a href="{href(p.name)}/">'
            f'{html.escape(p.name)}/</a></td><td class="size"></td></tr>'
        )
    for p in files:
        cell = f'<a href="{href(p.name)}">{html.escape(p.name)}</a>'
        if is_md(p.name) and (p.name + ".html") in names:
            cell += f'<a class="rendered" href="{href(p.name)}.html">(rendered)</a>'
        rows.append(
            f'<tr class="file"><td class="name">{cell}</td>'
            f'<td class="size">{human_size(p.stat().st_size)}</td></tr>'
        )

    parts = d.relative_to(root).parts
    body = header(parts) + f'<table class="files">{"".join(rows)}</table>\n'

    readme = next((p for p in files if p.name.lower() == "readme.md"), None)
    if readme is not None:
        text = readme.read_text(encoding="utf-8", errors="replace")
        body += (
            '<div class="ribbon-divider" role="separator" aria-hidden="true"></div>\n'
            f'<span class="label">{html.escape(readme.name)}</span>\n'
            f'<article class="md">{render_md(text)}</article>\n'
        )

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
