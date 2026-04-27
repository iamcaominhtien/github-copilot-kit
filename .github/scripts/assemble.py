#!/usr/bin/env python3
"""
assemble.py — Deep Research Report Assembler

Usage (run from any directory):
    python .github/scripts/assemble.py <topic-slug>

Walks research-output/.artifacts/<topic-slug>/sections/ in numeric-prefix order,
reads index.md from each folder, adjusts heading levels by depth,
and concatenates into a single Markdown report.

Heading level rules:
  sections/00-header/          → H1 (kept as-is, root heading)
  sections/01-slug/            → H2
  sections/01-slug/01-sub/     → H3

Asset path resolution:
  ../assets/images/foo.png  →  .artifacts/<slug>/sections/assets/images/foo.png
  https://...               →  preserved as-is

Output:
  research-output/<topic-slug>-<YYYY-MM-DD>.md   ← Markdown
  research-output/<topic-slug>-<YYYY-MM-DD>.html ← HTML (justified text, centered images)
  research-output/<topic-slug>-<YYYY-MM-DD>.pdf  ← PDF (requires: pip install weasyprint)

Dependencies (optional, for HTML/PDF):
  pip install markdown weasyprint
"""

import re
import sys
from datetime import date
from pathlib import Path

# Workspace root = two levels up from this script (.github/scripts/ → root)
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
RESEARCH_OUTPUT = WORKSPACE_ROOT / "research-output"


# ── Helpers ──────────────────────────────────────────────────────────────────

def adjust_headings(content: str, base_level: int) -> str:
    """Shift all headings so that H1 becomes H{base_level}."""
    if base_level == 1:
        return content
    lines = content.split("\n")
    result = []
    for line in lines:
        m = re.match(r"^(#{1,6})(\s+.*)", line)
        if m:
            new_level = min(len(m.group(1)) + base_level - 1, 6)
            line = "#" * new_level + m.group(2)
        result.append(line)
    return "\n".join(result)


def resolve_asset_paths(content: str, topic_slug: str) -> str:
    """
    Replace ../assets/images/ with the path relative to the output file.
    Output lives at research-output/<slug>-<date>.md
    Assets live at research-output/.artifacts/<slug>/sections/assets/images/
    """
    assets_rel = f".artifacts/{topic_slug}/sections/assets/images/"
    return content.replace("../assets/images/", assets_rel)


def get_ordered_subdirs(folder: Path) -> list[Path]:
    """Return direct subfolders sorted by name (numeric prefix drives order)."""
    return sorted(
        [e for e in folder.iterdir() if e.is_dir() and e.name not in {"assets"}],
        key=lambda e: e.name,
    )


def collect_sections(folder: Path, depth: int = 0) -> list[tuple[Path, int]]:
    """
    Recursively collect (index.md path, base_heading_level) in order.

    depth=0  → sections/ root   (no index.md expected here)
    depth=1  → 01-slug/         → base_level 2  (H2)
    depth=2  → 01-slug/01-sub/  → base_level 3  (H3)
    """
    results = []
    for subdir in get_ordered_subdirs(folder):
        index = subdir / "index.md"
        if index.exists():
            base_level = depth + 2
            results.append((index, base_level))
        results.extend(collect_sections(subdir, depth + 1))
    return results


def read_header_block(sections_dir: Path) -> str | None:
    header = sections_dir / "00-header" / "index.md"
    if header.exists():
        return header.read_text(encoding="utf-8").strip()
    return None


# ── Assembler ─────────────────────────────────────────────────────────────────

def assemble(topic_slug: str) -> str:
    sections_dir = RESEARCH_OUTPUT / ".artifacts" / topic_slug / "sections"
    if not sections_dir.exists():
        raise FileNotFoundError(f"Sections folder not found: {sections_dir}")

    parts = []

    # Header block (H1, no level shift)
    header = read_header_block(sections_dir)
    if header:
        parts.append(resolve_asset_paths(header, topic_slug))

    # All other sections in numeric order
    for index_path, base_level in collect_sections(sections_dir):
        if index_path.parent.name == "00-header":
            continue
        content = index_path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        adjusted = adjust_headings(content, base_level)
        adjusted = resolve_asset_paths(adjusted, topic_slug)
        parts.append(adjusted)

    return "\n\n---\n\n".join(parts)


# ── Entry point ───────────────────────────────────────────────────────────────

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    @page {{ size: letter; margin: 0.75in; @bottom-center {{ content: counter(page); font-family: Georgia, serif; font-size: 11px; color: #888; }} }}
    @media print {{ body {{ margin: 0; padding: 0; }} }}
    body {{
      font-family: Georgia, "Times New Roman", serif;
      font-size: 17px;
      line-height: 1.8;
      color: #1a1a1a;
      background: #fff;
      max-width: 780px;
      margin: 0 auto;
      padding: 0;
      text-align: justify;
      hyphens: auto;
    }}
    h1 {{ font-size: 2.2em; line-height: 1.25; margin: 0 0 0.3em; text-align: left; }}
    h2 {{ font-size: 1.55em; margin: 2.2em 0 0.6em; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.25em; text-align: left; break-before: page; }}
    h3 {{ font-size: 1.2em; margin: 1.8em 0 0.4em; text-align: left; }}
    h4, h5, h6 {{ font-size: 1em; margin: 1.4em 0 0.3em; text-align: left; }}
    p {{ margin: 0 0 1.1em; }}
    a {{ color: #1a56db; }}
    blockquote {{
      border-left: 3px solid #ccc;
      margin: 1.4em 0;
      padding: 0.6em 1.2em;
      color: #444;
      font-style: italic;
      text-align: left;
    }}
    code {{ font-family: "SFMono-Regular", Consolas, monospace; font-size: 0.88em; background: #f4f4f4; padding: 0.15em 0.35em; border-radius: 3px; }}
    pre {{ background: #f4f4f4; padding: 1em 1.2em; border-radius: 5px; overflow-x: auto; text-align: left; }}
    pre code {{ background: none; padding: 0; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1.4em 0; font-size: 0.95em; text-align: left; }}
    th, td {{ border: 1px solid #ddd; padding: 0.55em 0.9em; }}
    th {{ background: #f0f0f0; font-weight: 600; }}
    tr:nth-child(even) {{ background: #fafafa; }}
    hr {{ border: none; border-top: 1px solid #e0e0e0; margin: 2.5em 0; }}
    figure {{
      display: block;
      text-align: center;
      margin: 2em auto;
    }}
    figure img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 0 auto;
      border-radius: 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }}
    figcaption {{
      text-align: center;
      font-size: 0.88em;
      color: #666;
      margin-top: 0.5em;
      font-style: italic;
    }}
    /* ── Table of Contents ── */
    .toc-wrapper {{
      border: 1px solid #e0e0e0;
      border-radius: 6px;
      padding: 1.2em 1.5em;
      margin: 1.8em 0 2.4em;
      page-break-after: avoid;
    }}
    .toc-title {{
      font-size: 1em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #555;
      margin: 0 0 0.8em;
    }}
    .toc ul {{ list-style: none; margin: 0; padding: 0; }}
    .toc li {{ margin: 0.2em 0; }}
    .toc li.toc-h2 {{ padding-left: 0; font-weight: 700; }}
    .toc li.toc-h3 {{ padding-left: 1.4em; font-size: 0.95em; font-weight: normal; }}
    .toc li.toc-h4 {{ padding-left: 2.8em; font-size: 0.9em; font-weight: normal; }}
    .toc a {{
      text-decoration: none;
      color: #1a1a1a;
      display: inline;
    }}
    /* Page numbers via WeasyPrint CSS target-counter */
    .toc a::after {{
      content: leader(dotted) target-counter(attr(href url), page);
      font-style: normal;
      color: #888;
      font-weight: normal;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def md_to_html(md_content: str, topic_slug: str, output_dir: Path) -> str:
    """Convert Markdown to a full HTML string with justified text and centered figures."""
    try:
        import markdown as md_lib
    except ImportError:
        raise ImportError("Run: pip install markdown")

    # Resolve asset paths to be relative to the HTML output file location
    assets_rel = f".artifacts/{topic_slug}/sections/assets/images/"
    md_resolved = md_content.replace(
        f".artifacts/{topic_slug}/sections/assets/images/", assets_rel
    )

    converter = md_lib.Markdown(
        extensions=["tables", "fenced_code", "toc", "nl2br"],
        extension_configs={"toc": {"title": ""}},
    )
    body_html = converter.convert(md_resolved)
    body_html = _wrap_images_in_figures(body_html)

    # Build TOC block and inject it after the first H1
    toc_html = _build_toc_html(converter.toc)
    body_html = re.sub(
        r"(<h1[^>]*>.*?</h1>)",
        r"\1" + toc_html,
        body_html,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Extract title from first H1
    title_m = re.search(r"<h1[^>]*>(.*?)</h1>", body_html, re.IGNORECASE | re.DOTALL)
    title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else topic_slug

    return HTML_TEMPLATE.format(title=title, body=body_html)


def _build_toc_html(toc_raw: str) -> str:
    """Wrap the markdown toc extension output in a styled container."""
    if not toc_raw or not toc_raw.strip():
        return ""
    # Add CSS classes to li elements by depth (toc extension nests <ul> for depth)
    toc_with_classes = _add_toc_depth_classes(toc_raw)
    return (
        '\n<div class="toc-wrapper">'
        '\n  <p class="toc-title">Contents</p>'
        f'\n  <nav class="toc">{toc_with_classes}</nav>'
        "\n</div>\n"
    )


def _add_toc_depth_classes(toc_html: str) -> str:
    """Add toc-h2/h3/h4 classes to <li> elements based on nesting depth."""
    depth = 1
    result = []
    for line in toc_html.splitlines():
        stripped = line.strip()
        if stripped.startswith("<ul>"):
            depth += 1
        elif stripped.startswith("</ul>"):
            depth -= 1
        elif stripped.startswith("<li>"):
            css_class = f"toc-h{min(depth + 1, 4)}"
            line = line.replace("<li>", f'<li class="{css_class}">', 1)
        result.append(line)
    return "\n".join(result)


def _wrap_images_in_figures(html: str) -> str:
    """
    Convert <img> tags into <figure><img><figcaption> blocks.

    Handles two patterns produced by the markdown library:
      1. <p><img ...><br><em>Figure N: ...</em></p>  (no blank line between img and caption)
      2. <p><img ...></p>\n<p><em>Figure N: ...</em></p>  (blank line between)

    In both cases the <em> text becomes the figcaption and the surrounding <p> is removed.
    For bare images with no following caption, the alt text is used as figcaption.
    """
    # Pattern 1: img + <br> + <em>caption</em> inside same <p>
    html = re.sub(
        r"<p>\s*(<img[^>]+>)\s*<br\s*/?>\s*<em>(.*?)</em>\s*</p>",
        lambda m: _figure(m.group(1), m.group(2)),
        html,
        flags=re.DOTALL,
    )
    # Pattern 2: img in its own <p>, followed immediately by <p><em>caption</em></p>
    html = re.sub(
        r"<p>\s*(<img[^>]+>)\s*</p>\s*<p>\s*<em>(.*?)</em>\s*</p>",
        lambda m: _figure(m.group(1), m.group(2)),
        html,
        flags=re.DOTALL,
    )
    # Pattern 3: bare <img> still inside a <p> — use alt as caption
    html = re.sub(
        r"<p>\s*(<img[^>]+>)\s*</p>",
        lambda m: _figure(m.group(1), _extract_alt(m.group(1))),
        html,
    )
    return html


def _figure(img_tag: str, caption: str) -> str:
    cap = caption.strip()
    figcap = f"\n  <figcaption>{cap}</figcaption>" if cap else ""
    return f"<figure>\n  {img_tag}{figcap}\n</figure>"


def _extract_alt(img_tag: str) -> str:
    m = re.search(r'alt="([^"]*)"', img_tag)
    return m.group(1) if m else ""


def _heading_to_anchor(text: str) -> str:
    """Convert heading text to a GitHub-style markdown anchor slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s]+", "-", text)


def build_md_toc(md_content: str) -> str:
    """Generate a markdown TOC block from all H2/H3/H4 headings."""
    lines = []
    for line in md_content.splitlines():
        m = re.match(r"^(#{2,4})\s+(.*)", line)
        if not m:
            continue
        level = len(m.group(1))  # 2, 3, or 4
        text = m.group(2).strip()
        anchor = _heading_to_anchor(text)
        indent = "  " * (level - 2)
        lines.append(f"{indent}- [{text}](#{anchor})")
    if not lines:
        return ""
    return "## Contents\n\n" + "\n".join(lines)


def inject_md_toc(md_content: str) -> str:
    """Inject the TOC block into the markdown content right after the first H1."""
    toc = build_md_toc(md_content)
    if not toc:
        return md_content
    # Insert after the first H1 line (and any immediately following blank lines)
    return re.sub(
        r"(^#\s+[^\n]+\n+)",
        r"\1" + toc + "\n\n---\n\n",
        md_content,
        count=1,
        flags=re.MULTILINE,
    )


def save_pdf(html_path: Path, pdf_path: Path) -> None:
    """Render HTML to PDF using weasyprint."""
    # On macOS with Homebrew, Pango/GLib libs live in /opt/homebrew/lib.
    # Ensure that path is on DYLD_LIBRARY_PATH so cffi can find libgobject.
    import os, sys
    homebrew_lib = "/opt/homebrew/lib"
    if sys.platform == "darwin" and os.path.isdir(homebrew_lib):
        current = os.environ.get("DYLD_LIBRARY_PATH", "")
        if homebrew_lib not in current.split(":"):
            os.environ["DYLD_LIBRARY_PATH"] = f"{homebrew_lib}:{current}".strip(":")
    try:
        from weasyprint import HTML as WP_HTML
    except ImportError:
        print("⚠  PDF skipped — run: pip install weasyprint")
        return
    WP_HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    print(f"Saved → {pdf_path}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    topic_slug = sys.argv[1]
    print(f"Assembling: {topic_slug}")

    try:
        content = assemble(topic_slug)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    today = date.today().strftime("%Y-%m-%d")
    stem = f"{topic_slug}-{today}"

    # ── Markdown ──
    md_path = RESEARCH_OUTPUT / f"{stem}.md"
    md_path.write_text(inject_md_toc(content), encoding="utf-8")
    print(f"Saved → {md_path}")

    # ── HTML ──
    try:
        html_content = md_to_html(content, topic_slug, RESEARCH_OUTPUT)
        html_path = RESEARCH_OUTPUT / f"{stem}.html"
        html_path.write_text(html_content, encoding="utf-8")
        print(f"Saved → {html_path}")
    except ImportError as e:
        print(f"⚠  HTML skipped — {e}")
        return

    # ── PDF ──
    pdf_path = RESEARCH_OUTPUT / f"{stem}.pdf"
    save_pdf(html_path, pdf_path)


if __name__ == "__main__":
    main()
