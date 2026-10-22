"""Static file viewer for any text file (markdown is rendered by build_site.py).

For every text file this writes a small shell page next to it:
    foo/bar/test.c  ->  foo/bar/test.c.html

The shell holds the title, the "<- Directory - raw" line, an info line (language,
lines, size, encoding, line endings) and an empty container. The file itself is not
copied into the page. When the page opens, site/viewer/viewer.js fetches the raw
file, decodes it with the encoding found here, shows it with line numbers, and then
loads the highlighter plus the one language file it needs from _viewer/.

A file gets no viewer (it keeps a plain link to the raw file) when it is binary
(a NUL byte in the first 8 KB, git's rule) or larger than MAX_BYTES.
"""

import html
import re
import shutil
import sys
from pathlib import Path

import common

ASSET_DIR = "_viewer"  # folder inside the site that holds the highlighter files
VENDOR = common.SITE_DIR / "viewer" / "vendor"  # hljs.js, langs/*.js, LICENSE
MAX_BYTES = 2 * 1024 * 1024
SNIFF = 8192

# ---- language detection --------------------------------------------------
# (display label, highlight.js id). The id must match a file in vendor/langs/;
# when it does not, the file is shown without colours. An empty id means plain text.

NAMES = {  # exact (lower-case) file names
    "makefile": ("Makefile", "makefile"), "gnumakefile": ("Makefile", "makefile"),
    "cmakelists.txt": ("CMake", "cmake"),
    "dockerfile": ("Dockerfile", "dockerfile"),
    "nginx.conf": ("Nginx", "nginx"), ".htaccess": ("Apache", "apache"),
    ".gitignore": ("Ignore list", ""), ".dockerignore": ("Ignore list", ""),
    ".gitattributes": ("Git attributes", ""),
    ".gitmodules": ("Git config", "ini"), ".gitconfig": ("Git config", "ini"),
    ".editorconfig": ("EditorConfig", "ini"),
    ".clang-format": ("YAML", "yaml"), ".clang-tidy": ("YAML", "yaml"),
    ".bashrc": ("Shell", "bash"), ".bash_profile": ("Shell", "bash"),
    ".zshrc": ("Shell", "bash"), ".profile": ("Shell", "bash"),
    "gemfile": ("Ruby", "ruby"), "rakefile": ("Ruby", "ruby"), "vagrantfile": ("Ruby", "ruby"),
    "jenkinsfile": ("Groovy", "groovy"),
}

_EXT = {  # file extension (without the dot) -> (label, id); several extensions per line
    ("c", "h"): ("C", "c"),
    ("cpp", "cc", "cxx", "c++", "hpp", "hh", "hxx", "h++", "ipp", "tpp"): ("C++", "cpp"),
    ("ino",): ("Arduino", "arduino"),
    ("cs",): ("C#", "csharp"),
    ("java",): ("Java", "java"),
    ("kt", "kts"): ("Kotlin", "kotlin"),
    ("scala", "sc"): ("Scala", "scala"),
    ("groovy", "gvy"): ("Groovy", "groovy"),
    ("gradle",): ("Gradle", "gradle"),
    ("swift",): ("Swift", "swift"),
    ("mm",): ("Objective-C", "objectivec"),
    ("m",): ("MATLAB", "matlab"),
    ("go",): ("Go", "go"),
    ("rs",): ("Rust", "rust"),
    ("d",): ("D", "d"),
    ("dart",): ("Dart", "dart"),
    ("nim",): ("Nim", "nim"),
    ("cr",): ("Crystal", "crystal"),
    ("py", "pyw", "pyi"): ("Python", "python"),
    ("rb",): ("Ruby", "ruby"),
    ("php",): ("PHP", "php"),
    ("pl", "pm"): ("Perl", "perl"),
    ("lua",): ("Lua", "lua"),
    ("r",): ("R", "r"),
    ("jl",): ("Julia", "julia"),
    ("js", "mjs", "cjs", "jsx"): ("JavaScript", "javascript"),
    ("ts", "tsx", "mts", "cts"): ("TypeScript", "typescript"),
    ("coffee",): ("CoffeeScript", "coffeescript"),
    ("json", "jsonc", "geojson", "webmanifest"): ("JSON", "json"),
    ("html", "htm", "xhtml", "vue"): ("HTML", "xml"),
    ("xml", "xsl", "xslt", "svg", "plist", "rss", "atom", "xsd", "csproj"): ("XML", "xml"),
    ("css",): ("CSS", "css"),
    ("scss",): ("SCSS", "scss"),
    ("less",): ("Less", "less"),
    ("styl",): ("Stylus", "stylus"),
    ("hbs", "handlebars", "mustache"): ("Handlebars", "handlebars"),
    ("j2", "jinja", "jinja2", "djhtml"): ("Jinja", "django"),
    ("twig",): ("Twig", "twig"),
    ("erb",): ("ERB", "erb"),
    ("yaml", "yml"): ("YAML", "yaml"),
    ("toml",): ("TOML", "ini"),
    ("ini", "cfg", "conf"): ("INI", "ini"),
    ("properties",): ("Properties", "properties"),
    ("sh", "bash", "zsh", "ksh", "fish"): ("Shell", "bash"),
    ("ps1", "psm1", "psd1"): ("PowerShell", "powershell"),
    ("bat", "cmd"): ("Batch", "dos"),
    ("awk",): ("AWK", "awk"),
    ("tcl",): ("Tcl", "tcl"),
    ("vim",): ("Vim script", "vim"),
    ("sql",): ("SQL", "sql"),
    ("pgsql",): ("PostgreSQL", "pgsql"),
    ("tex", "sty", "cls"): ("LaTeX", "latex"),
    ("diff", "patch"): ("Diff", "diff"),
    ("asm", "nasm", "s"): ("Assembly", "x86asm"),
    ("v", "sv", "svh"): ("Verilog", "verilog"),
    ("vhd", "vhdl"): ("VHDL", "vhdl"),
    ("ll",): ("LLVM IR", "llvm"),
    ("glsl", "vert", "frag"): ("GLSL", "glsl"),
    ("gcode",): ("G-code", "gcode"),
    ("scad",): ("OpenSCAD", "openscad"),
    ("f", "f90", "f95", "f03", "for"): ("Fortran", "fortran"),
    ("pas", "pp", "dpr"): ("Pascal", "delphi"),
    ("bas",): ("BASIC", "basic"),
    ("ada", "adb", "ads"): ("Ada", "ada"),
    ("hs", "lhs"): ("Haskell", "haskell"),
    ("ml", "mli"): ("OCaml", "ocaml"),
    ("fs", "fsx", "fsi"): ("F#", "fsharp"),
    ("lisp", "lsp", "cl", "el"): ("Lisp", "lisp"),
    ("scm", "ss", "rkt"): ("Scheme", "scheme"),
    ("clj", "cljs", "cljc", "edn"): ("Clojure", "clojure"),
    ("erl", "hrl"): ("Erlang", "erlang"),
    ("ex", "exs"): ("Elixir", "elixir"),
    ("elm",): ("Elm", "elm"),
    ("sml",): ("Standard ML", "sml"),
    ("pro", "prolog"): ("Prolog", "prolog"),
    ("hx",): ("Haxe", "haxe"),
    ("st",): ("Smalltalk", "smalltalk"),
    ("vb", "vbnet"): ("VB.NET", "vbnet"),
    ("vbs",): ("VBScript", "vbscript"),
    ("proto",): ("Protocol Buffers", "protobuf"),
    ("thrift",): ("Thrift", "thrift"),
    ("mk", "mak"): ("Makefile", "makefile"),
    ("cmake",): ("CMake", "cmake"),
    ("dockerfile",): ("Dockerfile", "dockerfile"),
    ("nix",): ("Nix", "nix"),
    ("feature",): ("Gherkin", "gherkin"),
    ("abnf",): ("ABNF", "abnf"),
    ("ebnf",): ("EBNF", "ebnf"),
    ("bnf",): ("BNF", "bnf"),
    ("http",): ("HTTP", "http"),
    ("txt", "text", "log", "out"): ("Plain text", ""),
    ("csv",): ("CSV", ""),
    ("tsv",): ("TSV", ""),
    ("rst",): ("reStructuredText", ""),
    ("lock",): ("Lock file", ""),
}
EXTENSIONS = {ext: lang for exts, lang in _EXT.items() for ext in exts}

SHEBANGS = {  # interpreter name (version digits stripped) -> (label, id)
    "python": ("Python", "python"),
    "bash": ("Shell", "bash"), "sh": ("Shell", "bash"), "zsh": ("Shell", "bash"),
    "dash": ("Shell", "bash"), "ksh": ("Shell", "bash"), "ash": ("Shell", "bash"),
    "fish": ("Shell", "bash"),
    "node": ("JavaScript", "javascript"), "nodejs": ("JavaScript", "javascript"),
    "deno": ("TypeScript", "typescript"),
    "perl": ("Perl", "perl"), "ruby": ("Ruby", "ruby"), "php": ("PHP", "php"),
    "lua": ("Lua", "lua"), "awk": ("AWK", "awk"), "gawk": ("AWK", "awk"),
    "tclsh": ("Tcl", "tcl"), "wish": ("Tcl", "tcl"), "rscript": ("R", "r"),
    "pwsh": ("PowerShell", "powershell"), "make": ("Makefile", "makefile"),
}

# Languages that embed others: also load these so e.g. <script> and <style> in an
# HTML file are coloured too.
DEPENDENCIES = {"xml": ("css", "javascript")}

PLAIN = ("Plain text", "")


def shebang_language(first_line: str):
    """Language from a '#!' line such as '#!/usr/bin/env -S python3 -u'."""
    tokens = first_line[2:].split()
    if not tokens:
        return None
    prog = tokens[0].rsplit("/", 1)[-1]
    if prog == "env":
        prog = next((t for t in tokens[1:] if not t.startswith("-") and "=" not in t), "")
        prog = prog.rsplit("/", 1)[-1]
    m = re.match(r"[A-Za-z]+", prog)
    return SHEBANGS.get(m.group(0).lower()) if m else None


def detect_language(name: str, first_line: str = ""):
    """(label, highlight.js id) from the file name, extension, then '#!' line."""
    low = name.lower()
    if low in NAMES:
        return NAMES[low]
    if low.startswith("dockerfile"):  # Dockerfile.dev, Dockerfile.prod
        return NAMES["dockerfile"]
    suffix = Path(low).suffix.lstrip(".")
    if suffix in EXTENSIONS:
        return EXTENSIONS[suffix]
    if first_line.startswith("#!"):
        return shebang_language(first_line) or PLAIN
    return PLAIN


# ---- reading and classifying a file --------------------------------------

def decode(data: bytes):
    """(text, TextDecoder label, display label), or None for binary data."""
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):  # UTF-16 with a byte order mark
        le = data[:2] == b"\xff\xfe"
        try:
            return data.decode("utf-16"), "utf-16le" if le else "utf-16be", f"UTF-16 {'LE' if le else 'BE'}"
        except UnicodeDecodeError:
            return None
    if b"\x00" in data[:SNIFF]:
        return None
    if data.startswith(b"\xef\xbb\xbf"):
        try:
            return data.decode("utf-8-sig"), "utf-8", "UTF-8 BOM"
        except UnicodeDecodeError:
            pass
    try:
        return data.decode("utf-8"), "utf-8", "UTF-8"
    except UnicodeDecodeError:
        pass
    # Not UTF-8: guess a legacy code page (Central European first, then Western).
    for codec, label, name in (
        ("cp1250", "windows-1250", "Windows-1250"),
        ("cp1252", "windows-1252", "Windows-1252"),
    ):
        try:
            return data.decode(codec), label, f"{name} (guessed)"
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1"), "windows-1252", "Latin-1 (guessed)"


def count_lines(text: str) -> int:
    """Number of lines; the same rule viewer.js uses to split (CRLF, LF or CR)."""
    parts = re.split(r"\r\n|\n|\r", text)
    if parts and parts[-1] == "":
        parts.pop()
    return len(parts)


def line_endings(text: str) -> str:
    crlf = text.count("\r\n")
    kinds = [
        (n, label)
        for n, label in ((text.count("\n") - crlf, "LF"), (crlf, "CRLF"), (text.count("\r") - crlf, "CR"))
        if n
    ]
    if not kinds:
        return ""
    if len(kinds) == 1:
        return kinds[0][1]
    return "mixed (" + "+".join(label for _, label in kinds) + ")"


# ---- building ------------------------------------------------------------

def shell_body(dest: Path, path: Path, info: str, enc: str, lang: str, deps: str, size: int, lines: int) -> str:
    parts = path.parent.relative_to(dest).parts
    fragment = common.load("viewer/viewer.html")
    return (
        common.title_html(parts, path.name)
        + common.nav_html(path.name)
        + common.fill(
            fragment,
            info=html.escape(info),
            src=html.escape(common.href(path.name)),
            enc=enc,
            lang=lang,
            deps=deps,
            root=html.escape("../" * len(parts)),
            size=str(size),
            lines=str(lines),
        )
    )


def build(dest: Path, files: list) -> set:
    """Write a viewer shell next to every viewable text file in `files`.

    Returns the set of files that got one. The highlighter is copied to
    DEST/_viewer/ (or skipped, with a warning, when vendor/ is empty: files are
    then still shown, just without colours)."""
    css = common.load("viewer/viewer.css")
    js = common.load("viewer/viewer.js")

    assets = dest / ASSET_DIR
    if assets.exists():
        sys.exit(f"the repository has a '{ASSET_DIR}' folder, which the file viewer needs for itself")
    langs = set()
    if (VENDOR / "hljs.js").is_file():
        shutil.copytree(VENDOR, assets)
        langs = {p.stem for p in (assets / "langs").glob("*.js")}
    else:
        print(f"warning: {VENDOR} is missing, files will be shown without syntax colours", file=sys.stderr)

    viewable, binary, large, clashes = set(), 0, 0, 0
    for path in files:
        shell = path.with_name(path.name + ".html")
        if shell.exists():  # the repository has its own X.ext.html: keep it
            clashes += 1
            print(f"note: {shell.relative_to(dest)} already exists, no viewer for {path.name}", file=sys.stderr)
            continue
        size = path.stat().st_size
        if size > MAX_BYTES:
            large += 1
            continue
        decoded = decode(path.read_bytes())
        if decoded is None:
            binary += 1
            continue
        text, enc, enc_label = decoded

        label, lang = detect_language(path.name, text[:200].split("\n", 1)[0].lstrip("\ufeff"))
        if lang not in langs:
            lang = ""
        deps = " ".join(d for d in DEPENDENCIES.get(lang, ()) if d in langs)

        lines = count_lines(text)
        info = [label, f"{lines:,} line" + ("" if lines == 1 else "s"), common.human_size(size), enc_label]
        eol = line_endings(text)
        if eol:
            info.append(eol)

        parts = path.parent.relative_to(dest).parts
        body = shell_body(dest, path, " \u00b7 ".join(info), enc, lang, deps, size, lines)
        shell.write_text(
            common.page(common.title_text(parts, path.name), body, css, js), encoding="utf-8"
        )
        viewable.add(path)

    print(
        f"File viewer: {len(viewable)} file(s); skipped {binary} binary, {large} over "
        f"{common.human_size(MAX_BYTES)}, {clashes} name clash(es)"
    )
    return viewable
