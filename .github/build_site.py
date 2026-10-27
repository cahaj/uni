#!/usr/bin/env python3
"""Build a browsable static copy of a repository for GitHub Pages.

Usage: build_site.py SRC DEST

What it does:
  1. Copies SRC to DEST (skipping .git, .github and DEST itself), so every
     file keeps its exact path: foo/bar/test.c -> DEST/foo/bar/test.c
  2. Renders every *.md file to a sibling *.md.html page (markdown is
     pre-generated here); the raw .md file is left untouched.
  3. Gives every other text file a file-viewer page, foo/bar/test.c.html, via
     viewer.py. Those pages only hold a shell; the file is loaded, decoded and
     highlighted in the browser.
  4. Writes an index.html directory listing into every directory. Markdown and
     viewable files link to their page (the raw file is reached from that page,
     through its "raw" link); a directory's README.md is rendered below its
     listing.

Files:
  build_site.py    this script: copying, markdown, directory listings
  common.py        shared page shell, title and helpers
  viewer.py        the file viewer generator (language detection, shells)
  site/            template.html, style.css, site.js, viewer/ (viewer.html/.css/.js
                   and vendor/: the highlight.js files)
  tools/           build_hljs.cjs, which regenerates site/viewer/vendor/

The page title shows SITE_HOST plus the current path, e.g. "u.ř.xyz/foo/bar/"; set
the SITE_HOST environment variable to override the default (see common.py).

All links are relative, so the site works at the domain root, under a project
path (user.github.io/repo/) and on a custom domain.
"""

import html
import os
import re
import shutil
import sys
from pathlib import Path

import markdown

import viewer
from common import header, href, human_size, page, title_text

TOP_LEVEL_EXCLUDES = {".git", ".github", "_site"}
MD_EXTENSIONS = ["fenced_code", "tables", "toc", "sane_lists"]


def is_md(name: str) -> bool:
    return name.lower().endswith(".md")


def render_md(text: str) -> str:
    body = markdown.markdown(text, extensions=MD_EXTENSIONS)

    # Point relative links to other .md files at their rendered pages.
    def fix(m: re.Match) -> str:
        target, rest = m.group(1), m.group(2) or ""
        if target.startswith("//"):  # protocol-relative URL, leave alone
            return m.group(0)
        return f'href="{target}.html{rest}"'

    return re.sub(r'href="([^"#?:]+\.md)([#?][^"]*)?"', fix, body, flags=re.IGNORECASE)


def icon_cell(name: str) -> str:
    return f'<td class="icon"><svg class="ico" aria-hidden="true"><use href="#i-{name}"/></svg></td>'


def copy_repo(src: Path, dest: Path) -> None:
    def ignore(directory: str, names: list) -> set:
        if Path(directory).resolve() == src:
            return {n for n in names if n in TOP_LEVEL_EXCLUDES}
        return {n for n in names if n == ".git"}  # e.g. submodules

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=ignore)
    (dest / ".nojekyll").touch()


def render_all_markdown(dest: Path, md_files: list) -> None:
    for md in md_files:
        parts = md.parent.relative_to(dest).parts
        text = md.read_text(encoding="utf-8", errors="replace")
        body = (
            header(parts, md.name, raw_name=md.name)
            + f'<article class="md">{render_md(text)}</article>\n'
        )
        out = md.with_name(md.name + ".html")
        out.write_text(page(title_text(parts, md.name), body), encoding="utf-8")


def build_listing(d: Path, root: Path, viewable: set) -> bool:
    """Write d/index.html. `viewable` holds the files that have a page next to
    them (X.md.html, X.c.html, ...); those link to the page, and the page itself
    is hidden from the listing."""
    index = d / "index.html"
    if index.exists():
        # A real index.html from the repo: keep it, don't overwrite.
        print(f"note: keeping existing {index.relative_to(root)}", file=sys.stderr)
        return False

    generated = {p.with_name(p.name + ".html") for p in viewable if p.parent == d}
    entries = list(d.iterdir())

    dirs = sorted(
        (p for p in entries if p.is_dir() and not (d == root and p.name == viewer.ASSET_DIR)),
        key=lambda p: p.name.lower(),
    )
    files = sorted(
        (
            p
            for p in entries
            if p.is_file()
            and p not in generated
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
        # the name opens the rendered page / viewer when there is one, else the file
        target = href(p.name) + (".html" if p in viewable else "")
        cell = f'<a href="{target}">{html.escape(p.name)}</a>'
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

    # Snapshot the repository's own files first, so generated pages are never
    # mistaken for them.
    repo_files = [p for p in dest.rglob("*") if p.is_file() and p != dest / ".nojekyll"]
    md_files = [p for p in repo_files if is_md(p.name)]
    other_files = [p for p in repo_files if not is_md(p.name)]

    render_all_markdown(dest, md_files)
    viewable = set(md_files) | viewer.build(dest, other_files)

    directories = [
        Path(p)
        for p, _, _ in os.walk(dest)
        if Path(p) != dest / viewer.ASSET_DIR and (dest / viewer.ASSET_DIR) not in Path(p).parents
    ]
    n_idx = sum(build_listing(d, dest, viewable) for d in directories)

    print(f"Rendered {len(md_files)} markdown file(s), generated {n_idx} directory listing(s) in {dest}")


if __name__ == "__main__":
    main()
