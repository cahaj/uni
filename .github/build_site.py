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

TOP_LEVEL_EXCLUDES = {".git", ".github", "_site"}
MD_EXTENSIONS = ["fenced_code", "tables", "toc", "sane_lists"]

STYLE = """
  :root { color-scheme: light dark; }
  body { max-width: 860px; margin: 2rem auto; padding: 0 1rem;
         font: 16px/1.6 system-ui, sans-serif; }
  a { color: #0969da; text-decoration: none; }
  a:hover { text-decoration: underline; }
  pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; }
  code { background: #f6f8fa; padding: .1em .3em; border-radius: 4px; }
  pre code { padding: 0; background: none; }
  table { border-collapse: collapse; }
  td, th { border: 1px solid #d0d7de; padding: .3rem .6rem; }
  img { max-width: 100%; }
  blockquote { margin-left: 0; padding-left: 1rem; border-left: 4px solid #d0d7de; color: #57606a; }
  .nav { color: #57606a; }
  table.files { width: 100%; border: none; }
  table.files td { border: none; border-bottom: 1px solid #eaeef2; }
  table.files td.size { text-align: right; color: #57606a; white-space: nowrap; }
  .readme { margin-top: 2rem; border: 1px solid #d0d7de; border-radius: 6px; padding: 0 1.5rem 1rem; }
  .readme > h2.readme-title { font-size: 1rem; border-bottom: 1px solid #d0d7de;
         margin: 0 -1.5rem 1rem; padding: .6rem 1.5rem; }
  @media (prefers-color-scheme: dark) {
    body { background: #0d1117; color: #e6edf3; }
    a { color: #58a6ff; }
    pre, code { background: #161b22; }
    td, th, .readme, .readme > h2.readme-title, blockquote { border-color: #30363d; }
    table.files td { border-bottom-color: #21262d; }
    .nav, .size, blockquote { color: #8b949e; }
  }
"""

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{style}</style></head>
<body>
{body}
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
        text = md.read_text(encoding="utf-8", errors="replace")
        body = (
            '<p class="nav"><a href="./">&larr; Directory</a> &middot; '
            f'<a href="{href(md.name)}">raw</a></p>\n' + render_md(text)
        )
        out = md.with_name(md.name + ".html")
        out.write_text(
            PAGE.format(title=html.escape(md.name), style=STYLE, body=body),
            encoding="utf-8",
        )
    return len(md_files)


def breadcrumbs(rel_parts: tuple) -> str:
    depth = len(rel_parts)
    crumbs = [f'<a href="{"../" * depth or "./"}">/</a>']
    for i, part in enumerate(rel_parts):
        up = depth - i - 1
        crumbs.append(f'<a href="{"../" * up or "./"}">{html.escape(part)}</a>/')
    return "".join(crumbs)


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
        rows.append('<tr><td><a href="../">../</a></td><td class="size"></td></tr>')
    for p in dirs:
        rows.append(
            f'<tr><td><a href="{href(p.name)}/">{html.escape(p.name)}/</a></td>'
            '<td class="size"></td></tr>'
        )
    for p in files:
        cell = f'<a href="{href(p.name)}">{html.escape(p.name)}</a>'
        if is_md(p.name) and (p.name + ".html") in names:
            cell += f' <a href="{href(p.name)}.html">(rendered)</a>'
        rows.append(
            f"<tr><td>{cell}</td>"
            f'<td class="size">{human_size(p.stat().st_size)}</td></tr>'
        )

    rel = d.relative_to(root)
    rel_parts = rel.parts
    shown = "/" + "/".join(rel_parts) + ("/" if rel_parts else "")
    body = (
        f"<h1>Index of {html.escape(shown)}</h1>\n"
        f'<p class="nav">{breadcrumbs(rel_parts)}</p>\n'
        f'<table class="files">{"".join(rows)}</table>\n'
    )

    readme = next((p for p in files if p.name.lower() == "readme.md"), None)
    if readme is not None:
        text = readme.read_text(encoding="utf-8", errors="replace")
        body += (
            '<section class="readme">'
            f'<h2 class="readme-title">{html.escape(readme.name)}</h2>\n'
            f"{render_md(text)}</section>\n"
        )

    index.write_text(
        PAGE.format(title=f"Index of {html.escape(shown)}", style=STYLE, body=body),
        encoding="utf-8",
    )
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
