#!/usr/bin/env python3
"""Build the Calmer Bills static HTML site from docs/ Markdown.

Local-first: no network, no accounts, no dependencies beyond Python 3 and
the `markdown` package. Run `python3 build.py` and open site/index.html.

Education only — never legal advice.
Copyright (c) 2026 Asdale Dynamics, LLC
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

import markdown

REPO_ROOT = Path(__file__).resolve().parent

TITLE = "Calmer Bills — The Ring-Binder of Discount-Call Scripts"

# Display order for the sidebar, by path relative to docs/.
SIDEBAR = [
    ("Start here", [
        ("docs/index.md", "Calmer Bills — start here"),
        ("docs/how-to-use.md", "How to use this binder"),
        ("docs/walk-away-math.md", "Walk-away math"),
        ("docs/glossary.md", "Glossary"),
    ]),
    ("The five scripts", [
        ("docs/scripts/internet.md", "Internet provider"),
        ("docs/scripts/phone.md", "Phone carrier"),
        ("docs/insurance-call.md", "Insurance claim"),
        ("docs/scripts/card-interest.md", "Card interest"),
        ("docs/scripts/medical-bill.md", "Medical bill"),
    ]),
    ("Keep it honest, keep it warm", [
        ("docs/promise-tracker.md", "The promise tracker"),
        ("docs/saying-no.md", "Saying no kindly"),
        ("docs/escalation-ladder.md", "The escalation ladder"),
    ]),
]

CSS = """
:root {
  --bg: #fbf7f0;
  --paper: #fffdf9;
  --ink: #2c2a26;
  --muted: #6d675d;
  --accent: #9a5b2e;
  --accent-soft: #f3e4d5;
  --line: #e5dccd;
  --green: #3f6f4f;
}
* { box-sizing: border-box; }
html { font-size: 17px; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: Charter, Georgia, Cambria, "Times New Roman", serif;
  line-height: 1.65;
}
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 3px; }
a:hover { color: #7c4520; }
.layout { display: flex; min-height: 100vh; max-width: 1220px; margin: 0 auto; }
nav.toc {
  flex: 0 0 250px;
  padding: 2rem 1.2rem;
  border-right: 1px solid var(--line);
}
nav.toc h2 { font-size: 1rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin: 1.4rem 0 0.4rem; }
nav.toc h2:first-of-type { margin-top: 0; }
nav.toc ul { list-style: none; margin: 0; padding: 0; }
nav.toc li a { display: block; padding: 0.22rem 0.55rem; border-radius: 6px; text-decoration: none; font-size: 0.95rem; }
nav.toc li a:hover { background: var(--accent-soft); }
nav.toc li a.active { background: var(--accent-soft); font-weight: bold; color: #6b3d1c; }
main { flex: 1; min-width: 0; padding: 2.4rem 3rem 5rem; max-width: 52rem; }
.skip { position: absolute; left: -999px; }
.skip:focus { left: 1rem; top: 1rem; background: var(--paper); padding: 0.4rem 0.8rem; border-radius: 6px; }
.banner {
  background: var(--accent-soft);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 0.7rem 1.1rem;
  margin: 0 0 2rem;
  font-size: 0.92rem;
  color: #70543a;
}
.banner strong { color: #5d3a1c; }
h1 { font-size: 2rem; line-height: 1.25; margin: 0 0 1.2rem; }
h2 { font-size: 1.35rem; margin-top: 2.2rem; border-bottom: 1px solid var(--line); padding-bottom: 0.25rem; }
h3 { font-size: 1.1rem; margin-top: 1.7rem; }
blockquote {
  margin: 1.2rem 0;
  padding: 0.15rem 1.1rem;
  border-left: 4px solid var(--accent);
  background: var(--paper);
  border-radius: 0 8px 8px 0;
}
blockquote p { margin: 0.7rem 0; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.94rem; }
th, td { border: 1px solid var(--line); padding: 0.45rem 0.7rem; text-align: left; vertical-align: top; }
th { background: var(--accent-soft); }
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.86em;
  background: var(--accent-soft);
  padding: 0.1em 0.35em;
  border-radius: 5px;
}
pre { background: var(--paper); border: 1px solid var(--line); border-radius: 10px; padding: 1rem 1.2rem; overflow-x: auto; }
pre code { background: none; padding: 0; font-size: 0.86em; }
hr { border: 0; border-top: 1px solid var(--line); margin: 2.4rem 0; }
footer.site {
  border-top: 1px solid var(--line);
  margin-top: 3rem;
  padding-top: 1rem;
  font-size: 0.88rem;
  color: var(--muted);
}
.pager { display: flex; justify-content: space-between; gap: 1rem; margin-top: 2.5rem; font-size: 0.95rem; }
.pager a { text-decoration: none; }
.pager .next { margin-left: auto; text-align: right; }
input#navtoggle, label.navtoggle { display: none; }
@media (max-width: 900px) {
  .layout { display: block; }
  nav.toc { border-right: 0; padding: 1rem 1.2rem 0; }
  label.navtoggle { display: inline-block; cursor: pointer; border: 1px solid var(--line); border-radius: 8px; padding: 0.35rem 0.9rem; background: var(--paper); }
  nav.toc ul, nav.toc h2 { display: none; }
  input#navtoggle:checked ~ * ul, input#navtoggle:checked ~ * h2 { display: block; }
  input#navtoggle:checked ~ ul, input#navtoggle:checked ~ h2 { display: block; }
  main { padding: 1.6rem 1.2rem 4rem; }
}
@media print {
  nav.toc, .banner, .pager { display: none; }
  body { background: white; }
  main { max-width: none; }
}
""".strip()

BANNER = (
    "<div class=\"banner\" role=\"note\"><strong>Education only — never "
    "legal, financial, or medical advice.</strong> This binder explains how "
    "conversations usually go; it doesn't replace reading your own "
    "statements or consulting a licensed professional for your situation."
    "</div>"
)

FOOTER = (
    "<footer class=\"site\">Calmer Bills · “like a friend would” guides by "
    "Asdale Dynamics, LLC · MIT licensed · works offline · no tracking · "
    "education only, never legal advice</footer>"
)


def md_to_html(text: str, base_dir: Path, page_dir: Path = Path("")) -> str:
    """Convert Markdown to HTML and rewrite local .md links to .html.

    `page_dir` is the built page's directory relative to the site root;
    rewritten links become relative to that directory so they resolve from
    any depth.
    """

    def href_repl(match: re.Match) -> str:
        target = match.group(2)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        url_part, _, frag = target.partition("#")
        resolved = (base_dir / url_part).resolve()
        docs = (REPO_ROOT / "docs").resolve()
        if resolved.suffix == ".md" and str(resolved).startswith(str(docs)):
            site_rel = resolved.relative_to(docs).with_suffix(".html")
            new = Path(os.path.relpath(Path(site_rel), page_dir)).as_posix()
        else:
            return match.group(0)
        if frag:
            new += "#" + frag
        return f'{match.group(1)}="{new}"'

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    html = md.reset().convert(text)
    return re.sub(r'(href)="([^"]+)"', href_repl, html)


def page_shell(title: str, active_rel: str, body: str, page_dir: Path = Path("")) -> str:
    toc = ['<input type="checkbox" id="navtoggle" class="skip">',
           '<label class="navtoggle" for="navtoggle">☰ Tabs</label>']
    for section, entries in SIDEBAR:
        toc.append(f"<h2>{section}</h2><ul>")
        for path, label in entries:
            target = path[len("docs/") :][:-3] + ".html"
            href = Path(os.path.relpath(Path(target), page_dir)).as_posix()
            act = ' class="active"' if path == active_rel else ""
            toc.append(f'<li><a href="{href}"{act}>{label}</a></li>')
        toc.append("</ul>")
    nav = "".join(toc)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Calmer Bills</title>
<meta name="description" content="Kind, honest phone scripts for internet, phone, insurance, card-interest and medical-bill discount calls. Education only, never legal advice. Asdale Dynamics, LLC.">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="layout">
<nav class="toc" aria-label="Binder tabs">{nav}</nav>
<main id="content">{BANNER}
<h1>{title}</h1>
{body}
<div class="pager">{pager_html(active_rel, page_dir)}</div>
{FOOTER}
</main>
</div>
</body>
</html>
"""


def flat_pages() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for _, entries in SIDEBAR:
        for path, _label in entries:
            out.append((path, path[len("docs/") :][:-3] + ".html"))
    return out


def pager_html(active_rel: str, page_dir: Path = Path("")) -> str:
    pages = flat_pages()
    pages_with_labels = [(p, l) for _, entries in SIDEBAR for p, l in entries]
    label_map = dict(pages_with_labels)
    idx = next((i for i, (p, _) in enumerate(pages) if p == active_rel), None)
    if idx is None:
        return ""
    prev_link = ""
    if idx > 0:
        p, h = pages[idx - 1]
        href = Path(os.path.relpath(Path(h), page_dir)).as_posix()
        prev_link = f'<a class="prev" href="{href}">← {label_map[p]}</a>'
    next_link = ""
    if idx < len(pages) - 1:
        p, h = pages[idx + 1]
        href = Path(os.path.relpath(Path(h), page_dir)).as_posix()
        next_link = f'<a class="next" href="{href}">{label_map[p]} →</a>'
    return prev_link + next_link


def collect_doc_files(docs: Path) -> list[Path]:
    return sorted(p for p in docs.rglob("*.md") if p.is_file())


def build(docs_dir: Path, out_dir: Path) -> dict:
    docs = docs_dir.resolve()
    out_dir = out_dir.resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    pages, md_links = [], 0
    for md_path in collect_doc_files(docs):
        rel = md_path.relative_to(docs)
        text = md_path.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", text, flags=re.M)
        title = m.group(1).strip() if m else md_path.stem
        out_rel = rel.with_suffix(".html")
        page_dir = out_rel.parent
        html_body = md_to_html(text, md_path.parent, page_dir)
        # The shell renders the page title as the single <h1>; drop the
        # markdown-generated duplicate.
        html_body = re.sub(r"^\s*<h1>.*?</h1>\s*", "", html_body, count=1)
        md_links += html_body.count('href="')  # rough count for the report
        out_rel = rel.with_suffix(".html")
        dest = out_dir / out_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        active = "docs/" + rel.as_posix()
        dest.write_text(
            page_shell(title, active, html_body, page_dir), encoding="utf-8"
        )
        pages.append(str(out_rel.as_posix()))
    return {"pages": len(pages), "html_links": md_links, "out": str(out_dir)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--docs", type=Path, default=REPO_ROOT / "docs")
    ap.add_argument("--out", type=Path, default=REPO_ROOT / "site")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    stats = build(args.docs, args.out)
    if not args.quiet:
        print(f"Built {stats['pages']} pages into {stats['out']}")
        print("Open site/index.html in your browser. Education only — "
              "never legal advice.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
