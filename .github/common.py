"""Helpers shared by build_site.py (listings, markdown) and viewer.py (file viewer):
the page assets from site/, the page shell, the site title and small utilities."""

import html
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

SITE_HOST = os.environ.get("SITE_HOST", "u.ř.xyz")
SITE_DIR = Path(__file__).resolve().parent / "site"


def load(name: str) -> str:
    """Read a text asset from the site/ folder (name may include a subfolder)."""
    path = SITE_DIR / name
    if not path.is_file():
        sys.exit(f"missing {path}: copy the whole .github/site folder")
    return path.read_text(encoding="utf-8")


# Page assets live in .github/site/:
#   template.html  page skeleton with {{title}}, {{style}}, {{body}}, {{script}}
#   style.css      styles shared by every page (colours are the variables in :root)
#   site.js        keyboard navigation and collapsible headings
TEMPLATE = load("template.html")
STYLE = load("style.css")
SCRIPT = load("site.js")


def fill(template: str, **values: str) -> str:
    """Replace {{name}} placeholders in a single pass, so inserted content
    (e.g. markdown that contains "{{style}}") is never substituted again."""
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], template)


def page(title: str, body: str, extra_style: str = "", extra_script: str = "") -> str:
    """Wrap a body in the page template. Pages with their own behaviour (the file
    viewer) pass extra CSS/JS that is appended to the shared one."""
    return fill(
        TEMPLATE,
        title=html.escape(title),
        style=STYLE + ("\n" + extra_style if extra_style else ""),
        script=SCRIPT + ("\n" + extra_script if extra_script else ""),
        body=body,
    )


def href(name: str) -> str:
    """URL-quote a single path segment for use in an href attribute."""
    return quote(name)


def human_size(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{int(size)} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{n} B"


def title_text(dir_parts: tuple, filename: str = "") -> str:
    return SITE_HOST + "/" + "".join(p + "/" for p in dir_parts) + filename


def title_html(dir_parts: tuple, filename: str = "") -> str:
    """The <h1> title: host + current path, every directory a link back to it."""
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
    return f'<h1 class="site-title">{"".join(parts)}</h1>\n'


def nav_html(raw_name: str) -> str:
    """The "← Directory - raw" line of pages that belong to one file."""
    return (
        '<p class="meta-inline"><a class="nav-dir" href="./">&larr; Directory</a>'
        '<span class="meta-sep">-</span>'
        f'<a class="nav-raw" href="{href(raw_name)}">raw</a></p>\n'
    )


RULE = '<div class="rule" role="separator" aria-hidden="true"></div>\n'


def header(dir_parts: tuple, filename: str = "", raw_name: str = "") -> str:
    """Title, optional nav line (when raw_name is given) and the divider."""
    return title_html(dir_parts, filename) + (nav_html(raw_name) if raw_name else "") + RULE
