#!/usr/bin/env python3
"""Build the TIDEMARK reading site from manuscript/*.md into _site/.

No external dependencies. The manuscript files use a small, fixed subset of
Markdown (## headings, --- rules, *italic*, **bold**, blank-line paragraphs),
so a tiny purpose-built converter is enough and keeps CI dependency-free.

ch00.md is the front matter and becomes the landing page intro. Every other
chNN.md becomes its own page with prev/next navigation.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT = ROOT / "manuscript"
OUT = ROOT / "_site"

BOOK_TITLE = "TIDEMARK"
TAGLINE = "A serialized novel, written one chapter at a time."


# ---------------------------------------------------------------------------
# Tiny Markdown -> HTML converter (only what the manuscript actually uses)
# ---------------------------------------------------------------------------

def render_inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def md_to_html(md: str, drop_first_h1: bool = False) -> str:
    out = []
    para: list[str] = []
    dropped = False

    def flush():
        if para:
            out.append("<p>" + render_inline(" ".join(para)) + "</p>")
            para.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        if line.strip() == "---":
            flush()
            out.append('<hr class="break">')
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            flush()
            level = len(m.group(1))
            if level == 1 and drop_first_h1 and not dropped:
                dropped = True
                continue
            out.append(f"<h{level}>{render_inline(m.group(2))}</h{level}>")
            continue
        para.append(line.strip())
    flush()
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Chapter model
# ---------------------------------------------------------------------------

class Chapter:
    def __init__(self, path: Path):
        self.path = path
        self.num = int(re.search(r"ch(\d+)\.md$", path.name).group(1))
        self.text = path.read_text(encoding="utf-8")
        self.title, self.kicker = self._parse_title()
        self.slug = "index" if self.num == 0 else f"ch{self.num:02d}"

    def _parse_title(self):
        m = re.search(r"^##\s+Chapter\s+\d+\s+[—-]\s+(.*)$", self.text, re.M)
        if m:
            return m.group(1).strip(), f"Chapter {self.num}"
        return "Front matter", ""


def discover() -> list[Chapter]:
    chapters = [Chapter(p) for p in sorted(MANUSCRIPT.glob("ch*.md"))]
    return sorted(chapters, key=lambda c: c.num)


# ---------------------------------------------------------------------------
# Page templates
# ---------------------------------------------------------------------------

STYLE = """
:root {
  --bg: #faf8f4; --fg: #1f1c18; --muted: #8a8178; --rule: #e3ddd2;
  --accent: #9a3b2e; --link: #6b4a2f;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Times New Roman", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #16140f; --fg: #e9e3d6; --muted: #968d7e; --rule: #322d24;
    --accent: #d98a6a; --link: #cdb38a;
  }
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: var(--serif); font-size: 1.16rem; line-height: 1.7;
}
.wrap { max-width: 38rem; margin: 0 auto; padding: 4.5rem 1.4rem 6rem; }
.topbar {
  font-family: var(--sans); font-size: .8rem; letter-spacing: .08em;
  text-transform: uppercase; color: var(--muted);
  display: flex; justify-content: space-between; margin-bottom: 3rem;
}
.topbar a { color: var(--muted); text-decoration: none; }
.topbar a:hover { color: var(--accent); }
a { color: var(--link); }
.kicker {
  font-family: var(--sans); font-size: .8rem; letter-spacing: .16em;
  text-transform: uppercase; color: var(--accent); margin: 0 0 .4rem;
}
h1.title { font-size: 2.1rem; line-height: 1.15; margin: 0 0 2.6rem; font-weight: 600; }
h2 { font-size: 1.5rem; margin: 2.4rem 0 1rem; font-weight: 600; }
h3 { font-size: 1.2rem; margin: 2rem 0 .8rem; }
p { margin: 0 0 1.25rem; }
hr.break {
  border: 0; text-align: center; margin: 2.2rem 0;
}
hr.break::before { content: "\\00a7"; color: var(--muted); font-size: 1rem; letter-spacing: .4em; }
.cover-title {
  font-size: 3.4rem; letter-spacing: .02em; margin: 0 0 .5rem; font-weight: 600;
}
.cover-tag { color: var(--muted); font-style: italic; margin: 0 0 3rem; }
.toc { list-style: none; padding: 0; margin: 2.5rem 0 0; }
.toc li { border-top: 1px solid var(--rule); }
.toc li:last-child { border-bottom: 1px solid var(--rule); }
.toc a {
  display: flex; gap: 1rem; align-items: baseline;
  padding: .85rem .2rem; text-decoration: none; color: var(--fg);
}
.toc a:hover { color: var(--accent); }
.toc .n {
  font-family: var(--sans); font-size: .82rem; color: var(--muted);
  min-width: 2.2rem; font-variant-numeric: tabular-nums;
}
.toc .t { flex: 1; }
.nav {
  display: flex; justify-content: space-between; gap: 1rem;
  margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--rule);
  font-family: var(--sans); font-size: .9rem;
}
.nav a { text-decoration: none; color: var(--link); }
.nav a:hover { color: var(--accent); }
.nav .spacer { flex: 1; }
.end { color: var(--muted); font-style: italic; text-align: center; margin-top: 2.5rem; }
"""


def page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{STYLE}</style>
</head>
<body>
<div class="wrap">
{body}
</div>
</body>
</html>
"""


def build_index(front: Chapter | None, chapters: list[Chapter]) -> str:
    toc = ['<ul class="toc">']
    for c in chapters:
        toc.append(
            f'<li><a href="{c.slug}.html">'
            f'<span class="n">{c.num:02d}</span>'
            f'<span class="t">{html.escape(c.title)}</span></a></li>'
        )
    toc.append("</ul>")

    intro = ""
    if front is not None:
        intro = md_to_html(front.text, drop_first_h1=True)

    body = f"""<div class="topbar"><span>{html.escape(BOOK_TITLE)}</span><span></span></div>
<h1 class="cover-title">{html.escape(BOOK_TITLE)}</h1>
<p class="cover-tag">{html.escape(TAGLINE)}</p>
{intro}
<h2>Chapters</h2>
{"".join(toc)}
"""
    return page(BOOK_TITLE, body)


def build_chapter(c: Chapter, prev: Chapter | None, nxt: Chapter | None) -> str:
    body_md = md_to_html(c.text, drop_first_h1=False)
    # Promote the chapter's "## Chapter N — Title" into a styled header.
    body_md = re.sub(
        r"<h2>Chapter \d+ [—-] (.*?)</h2>",
        f'<p class="kicker">{html.escape(c.kicker)}</p>'
        f'<h1 class="title">{html.escape(c.title)}</h1>',
        body_md,
        count=1,
    )

    nav = ['<div class="nav">']
    if prev is not None:
        nav.append(f'<a href="{prev.slug}.html">← {html.escape(prev.title)}</a>')
    else:
        nav.append('<a href="index.html">← Cover</a>')
    nav.append('<span class="spacer"></span>')
    nav.append('<a href="index.html">Contents</a>')
    nav.append('<span class="spacer"></span>')
    if nxt is not None:
        nav.append(f'<a href="{nxt.slug}.html">{html.escape(nxt.title)} →</a>')
    nav.append("</div>")

    body = f"""<div class="topbar">
<a href="index.html">{html.escape(BOOK_TITLE)}</a>
<span>Chapter {c.num}</span>
</div>
{body_md}
{"".join(nav)}
"""
    return page(f"{c.title} — {BOOK_TITLE}", body)


def main():
    chapters = discover()
    front = next((c for c in chapters if c.num == 0), None)
    body_chapters = [c for c in chapters if c.num != 0]

    OUT.mkdir(exist_ok=True)
    (OUT / ".nojekyll").write_text("")
    (OUT / "index.html").write_text(build_index(front, body_chapters), encoding="utf-8")

    for i, c in enumerate(body_chapters):
        prev = body_chapters[i - 1] if i > 0 else None
        nxt = body_chapters[i + 1] if i + 1 < len(body_chapters) else None
        (OUT / f"{c.slug}.html").write_text(build_chapter(c, prev, nxt), encoding="utf-8")

    print(f"Built {len(body_chapters)} chapters + index into {OUT}")


if __name__ == "__main__":
    main()
