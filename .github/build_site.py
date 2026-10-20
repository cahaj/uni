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

Styles, scripts and the page template live in the site/ folder next to this
file (style.css, site.js, template.html); see site.js for the keyboard controls.

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

SITE_HOST = os.environ.get("SITE_HOST", "u.ř.xyz")
TOP_LEVEL_EXCLUDES = {".git", ".github", "_site"}
MD_EXTENSIONS = ["fenced_code", "tables", "toc", "sane_lists"]

SITE_DIR = Path(__file__).resolve().parent / "site"


def _load(name: str) -> str:
    path = SITE_DIR / name
    if not path.is_file():
        sys.exit(f"missing {path}: copy the whole .github/site folder")
    return path.read_text(encoding="utf-8")


# Page assets live next to this script in .github/site/:
#   template.html  page skeleton with {{title}}, {{style}}, {{body}}, {{script}}
#   style.css      all styles (colours are the variables in :root)
#   site.js        keyboard navigation and collapsible headings
TEMPLATE = _load("template.html")
STYLE = _load("style.css")
SCRIPT = _load("site.js")


def fill(template: str, **values: str) -> str:
    """Replace {{name}} placeholders in a single pass, so inserted content
    (e.g. markdown that contains "{{style}}") is never substituted again."""
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)


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
    return fill(
        TEMPLATE, title=html.escape(title), style=STYLE, script=SCRIPT, body=body
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
            '<a class="nav-dir" href="./">&larr; Directory</a><span class="meta-sep">-</span>'
            f'<a class="nav-raw" href="{href(md.name)}">raw</a>'
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
