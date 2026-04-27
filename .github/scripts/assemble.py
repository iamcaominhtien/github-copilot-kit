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

Options:
  --cover <path>   Prepend a cover image (PNG/JPG) as the first page.
                   Path can be absolute or relative to the workspace root.

Dependencies (optional, for HTML/PDF):
  pip install markdown weasyprint

Mermaid diagram rendering (optional, for ```mermaid blocks):
  npm install -g @mermaid-js/mermaid-cli
  (requires Node.js; mmdc must be on PATH)
"""

import hashlib
import re
import subprocess
import sys
import tempfile
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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;1,400&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap" rel="stylesheet">
  <style>
    @page {{ size: letter; margin: 0.75in; @bottom-center {{ content: counter(page); font-family: Georgia, serif; font-size: 11px; color: #888; }} }}
    @page cover {{ size: letter; margin: 0; @bottom-center {{ content: none; }} }}
    @media print {{
      body {{ margin: 0; padding: 0; }}
      .highlight, pre:not(.highlight pre) {{ box-shadow: none !important; }}
    }}
    body {{
      font-family: Lora, Georgia, "Times New Roman", serif;
      font-size: 17px;
      line-height: 1.85;
      color: #1a1a1a;
      background: #fff;
      max-width: 780px;
      margin: 0 auto;
      padding: 0;
      text-align: justify;
      hyphens: auto;
    }}
    h1 {{ font-family: "EB Garamond", Georgia, serif; font-size: 2.4em; font-weight: 700; line-height: 1.2; margin: 0 0 0.3em; text-align: left; }}
    h2 {{ font-family: "EB Garamond", Georgia, serif; font-size: 1.65em; font-weight: 600; margin: 2.2em 0 0.6em; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.25em; text-align: left; break-before: page; }}
    h3 {{ font-family: "EB Garamond", Georgia, serif; font-size: 1.25em; font-weight: 600; margin: 1.8em 0 0.4em; text-align: left; }}
    h4, h5, h6 {{ font-family: "EB Garamond", Georgia, serif; font-size: 1.05em; font-weight: 600; margin: 1.4em 0 0.3em; text-align: left; }}
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
    /* inline code only — light, subtle */
    code {{ font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace; font-size: 0.82em; background: #f0f1f3; color: #c7254e; padding: 0.2em 0.45em; border-radius: 4px; border: 1px solid #dde1e7; white-space: pre-wrap; word-break: break-word; }}
    /* reset inside code blocks so the dark theme takes over */
    pre code, .highlight code {{ background: none !important; color: #abb2bf !important; border: none !important; padding: 0 !important; }}
    /* ── Code card shared base ── */
    .highlight, pre:not(.highlight pre) {{
      position: relative;
      background: #1e2130;
      border: none;
      border-radius: 12px;
      margin: 2em 0;
      page-break-inside: avoid;
      overflow: visible;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      box-shadow:
        0 1px 2px rgba(0,0,0,0.35),
        0 4px 12px rgba(0,0,0,0.30),
        0 12px 32px rgba(0,0,0,0.22);
    }}
    /* ── Faux title-bar: dots + subtle top gradient ── */
    .highlight::before, pre:not(.highlight pre)::before {{
      content: "\\25CF\\00A0\\25CF\\00A0\\25CF";
      display: block;
      padding: 0.6em 1em 0.55em;
      font-size: 0.55em;
      letter-spacing: 0.25em;
      color: #ff5f57;
      text-shadow: 1.4em 0 0 #febc2e, 2.8em 0 0 #28c840;
      background: #272b3b;
      border-bottom: 1px solid #2e3347;
    }}
    /* language badge — top-right via ::after */
    .highlight[data-lang]::after, pre:not(.highlight pre)[data-lang]::after {{
      content: attr(data-lang);
      position: absolute;
      top: 0;
      right: 0;
      padding: 0.42em 0.9em;
      font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
      font-size: 0.65em;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #7c8db5;
      background: transparent;
      line-height: 1.9;
    }}
    /* ── Code area ── */
    .highlight pre {{
      margin: 0;
      padding: 1.1em 1.4em 1.3em;
      overflow-x: auto;
      background: #1e2130 !important;
      text-align: left;
      border: none;
      border-radius: 0;
      box-shadow: none;
      white-space: pre-wrap;
      word-break: break-all;
      overflow-wrap: break-word;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
    }}
    /* WeasyPrint span-boundary fix: spans must inherit wrapping from pre */
    .highlight pre span {{
      display: inline;
      white-space: inherit;
      word-break: inherit;
      overflow-wrap: inherit;
    }}
    .highlight code, pre code {{
      font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
      font-size: 0.87em;
      line-height: 1.75;
      white-space: pre-wrap;
      word-break: break-all;
    }}
    /* plain pre (no Pygments) — code area padding */
    pre:not(.highlight pre) {{ padding: 0; }}
    pre:not(.highlight pre) > code {{
      display: block;
      padding: 1.1em 1.4em 1.3em;
      overflow-x: auto;
    }}
    /* scrollbar */
    .highlight pre::-webkit-scrollbar, pre::-webkit-scrollbar {{ height: 5px; }}
    .highlight pre::-webkit-scrollbar-track, pre::-webkit-scrollbar-track {{ background: #171a26; border-radius: 3px; }}
    .highlight pre::-webkit-scrollbar-thumb, pre::-webkit-scrollbar-thumb {{ background: #3a3f55; border-radius: 3px; }}
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
    /* ── Cover page ── */
    .cover-page {{
      width: 8.5in;
      height: 11in;
      margin-left: calc((780px - 8.5in) / 2);
      page-break-after: always;
      break-after: page;
      padding: 0;
      overflow: hidden;
      page: cover;
    }}
    .cover-img {{
      width: 8.5in;
      height: 11in;
      object-fit: cover;
      object-position: center;
      display: block;
      border-radius: 0;
      box-shadow: none;
    }}
    /* ── Pygments token colors (injected at render time) ── */
    {pygments_css}
  </style>
</head>
<body>
{cover}
{body}
</body>
</html>
"""


def _get_pygments_css() -> str:
    """Generate Pygments token CSS using a dark style. Returns empty string if Pygments is not installed."""
    try:
        from pygments.formatters import HtmlFormatter
        from pygments.styles import get_all_styles
        # Prefer One Dark → Dracula → Monokai (all ship with Pygments ≥ 2.11)
        available = set(get_all_styles())
        for preferred in ("one-dark", "dracula", "monokai"):
            if preferred in available:
                style_name = preferred
                break
        else:
            style_name = "monokai"
        css = HtmlFormatter(style=style_name, cssclass="highlight").get_style_defs(".highlight")
        # Force background to match our card color
        css += "\n.highlight, .highlight pre { background: #1e2130 !important; }"
        return css
    except ImportError:
        return ""


def md_to_html(md_content: str, topic_slug: str, output_dir: Path, cover_path: Path | None = None) -> str:
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

    # Use codehilite (Pygments) when available, fall back to plain fenced_code
    pygments_css = _get_pygments_css()
    if pygments_css:
        extensions = ["tables", "fenced_code", "codehilite", "toc", "nl2br"]
        ext_config = {
            "toc": {"title": "", "toc_depth": "2-4"},
            "codehilite": {"css_class": "highlight", "guess_lang": False},
        }
    else:
        extensions = ["tables", "fenced_code", "toc", "nl2br"]
        ext_config = {"toc": {"title": "", "toc_depth": "2-4"}}

    converter = md_lib.Markdown(extensions=extensions, extension_configs=ext_config)
    body_html = converter.convert(md_resolved)
    body_html = _decorate_code_blocks(body_html, md_resolved)
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

    # Cover page — full-bleed image on its own page before the content
    cover_html = ""
    if cover_path and cover_path.exists():
        # Make path relative to the output HTML file (which lives in research-output/)
        try:
            rel = cover_path.resolve().relative_to(RESEARCH_OUTPUT.resolve())
            cover_src = str(rel)
        except ValueError:
            cover_src = str(cover_path.resolve())
        cover_html = (
            '<div class="cover-page">'
            f'<img src="{cover_src}" alt="Cover" class="cover-img">'
            "</div>"
        )

    return HTML_TEMPLATE.format(title=title, cover=cover_html, body=body_html, pygments_css=pygments_css)


def _decorate_code_blocks(html: str, md_source: str) -> str:
    """
    Add data-lang attributes to code block wrappers for the CSS language badge.

    For Pygments/codehilite output (<div class="highlight">), the language is no
    longer present in the HTML, so we recover it by scanning the original Markdown
    source for fenced block openers and matching them by position.

    For plain fenced_code output (<pre><code class="language-xxx">), we inject
    data-lang directly on the <pre> element.
    """
    # ── Case 1: codehilite .highlight divs ──
    # Collect fenced block languages in source order (``` or ~~~, with or without lang)
    source_langs: list[str | None] = [
        (m.group(2) or None)
        for m in re.finditer(r'(?m)^(```|~~~)(\w[\w.-]*)?', md_source)
    ]

    if source_langs:
        idx: list[int] = [0]

        def _inject_lang(m: re.Match) -> str:
            lang = source_langs[idx[0]] if idx[0] < len(source_langs) else None
            idx[0] += 1
            if lang:
                return m.group(0).replace(
                    '<div class="highlight">',
                    f'<div class="highlight" data-lang="{lang}">',
                    1,
                )
            return m.group(0)

        html = re.sub(r'<div class="highlight">.*?</div>', _inject_lang, html, flags=re.DOTALL)

    # ── Case 2: plain <pre><code class="language-xxx"> (no Pygments) ──
    html = re.sub(
        r'<pre><code class="language-([^"]+)">',
        lambda m: f'<pre data-lang="{m.group(1)}"><code class="language-{m.group(1)}">',
        html,
    )

    return html


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
    """Add toc-h2/h3/h4 classes to <li> elements based on the heading level
    stored in the href anchor by the toc extension.

    The toc extension generates anchors from heading text. We can't reliably
    recover the original heading level from the anchor alone, so we track
    nesting depth via <ul>/<li> but then map depth → heading level correctly:
      depth 1 (top-level <ul>) → toc-h2  (bold section titles)
      depth 2                   → toc-h3
      depth 3+                  → toc-h4
    """
    depth = 0
    parts = re.split(r'(<[^>]+>)', toc_html)
    result = []
    for token in parts:
        if token == '<ul>':
            depth += 1
            result.append(token)
        elif token == '</ul>':
            depth -= 1
            result.append(token)
        elif token == '<li>':
            # depth 1 → h2 (bold), depth 2 → h3, depth 3+ → h4
            level = min(depth + 1, 4)
            result.append(f'<li class="toc-h{level}">')
        else:
            result.append(token)
    return ''.join(result)


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


def render_mermaid_blocks(md_content: str, topic_slug: str) -> str:
    """
    Find all ```mermaid ... ``` blocks, render each to SVG via mmdc,
    and replace the block with a Markdown image reference.

    SVGs are saved to research-output/.artifacts/<slug>/sections/assets/images/
    so they are co-located with other section assets and picked up by WeasyPrint.

    Skips gracefully if mmdc is not installed.
    """
    import shutil

    mmdc = shutil.which("mmdc")
    if not mmdc:
        print("⚠  Mermaid rendering skipped — install mermaid-cli: npm install -g @mermaid-js/mermaid-cli")
        return md_content

    assets_dir = RESEARCH_OUTPUT / ".artifacts" / topic_slug / "sections" / "assets" / "images"
    assets_dir.mkdir(parents=True, exist_ok=True)
    # This prefix matches the path already resolved by resolve_asset_paths() inside assemble()
    assets_prefix = f".artifacts/{topic_slug}/sections/assets/images/"

    def _render_block(match: re.Match) -> str:
        mermaid_code = match.group(1).strip()
        digest = hashlib.md5(mermaid_code.encode()).hexdigest()[:10]
        png_name = f"mermaid-{digest}.png"
        png_path = assets_dir / png_name

        if not png_path.exists():
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mmd", delete=False, encoding="utf-8"
            ) as f:
                f.write(mermaid_code)
                tmp_mmd = Path(f.name)
            try:
                result = subprocess.run(
                    [mmdc, "-i", str(tmp_mmd), "-o", str(png_path),
                     "--outputFormat", "png", "--backgroundColor", "white", "--scale", "2"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    print(f"⚠  Mermaid render failed: {result.stderr[:300]}")
                    return match.group(0)  # keep original block
            except Exception as exc:
                print(f"⚠  Mermaid render error: {exc}")
                return match.group(0)
            finally:
                tmp_mmd.unlink(missing_ok=True)

        print(f"  Mermaid → {png_name}")
        return f"![diagram]({assets_prefix}{png_name})"

    return re.sub(r"```mermaid\r?\n(.*?)```", _render_block, md_content, flags=re.DOTALL)


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

    # Parse optional --cover <path>
    cover_path: Path | None = None
    args = sys.argv[2:]
    if "--cover" in args:
        idx = args.index("--cover")
        if idx + 1 < len(args):
            raw = args[idx + 1]
            p = Path(raw)
            cover_path = p if p.is_absolute() else (WORKSPACE_ROOT / p).resolve()
            if not cover_path.exists():
                print(f"⚠  Cover image not found: {cover_path} — skipping cover")
                cover_path = None
        else:
            print("⚠  --cover requires a path argument")
    else:
        # Auto-detect cover.png / cover.jpg inside .artifacts/<slug>/
        for ext in ("png", "jpg", "jpeg"):
            candidate = RESEARCH_OUTPUT / ".artifacts" / topic_slug / f"cover.{ext}"
            if candidate.exists():
                cover_path = candidate
                print(f"Auto-detected cover: {candidate}")
                break

    print(f"Assembling: {topic_slug}" + (f" (cover: {cover_path})" if cover_path else ""))

    try:
        content = assemble(topic_slug)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Render Mermaid diagrams to SVG before any output is written
    content = render_mermaid_blocks(content, topic_slug)

    today = date.today().strftime("%Y-%m-%d")
    stem = f"{topic_slug}-{today}"

    # ── Markdown — prepend cover image reference if provided ──
    md_content = inject_md_toc(content)
    if cover_path:
        try:
            rel = cover_path.resolve().relative_to(RESEARCH_OUTPUT.resolve())
            cover_md_src = str(rel)
        except ValueError:
            cover_md_src = str(cover_path.resolve())
        md_content = f"![Cover]({cover_md_src})\n\n" + md_content
    md_path = RESEARCH_OUTPUT / f"{stem}.md"
    md_path.write_text(md_content, encoding="utf-8")
    print(f"Saved → {md_path}")

    # ── HTML ──
    try:
        html_content = md_to_html(content, topic_slug, RESEARCH_OUTPUT, cover_path)
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
