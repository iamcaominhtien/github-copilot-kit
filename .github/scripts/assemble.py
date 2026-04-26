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
  research-output/<topic-slug>-<YYYY-MM-DD>.md
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
    output_path = RESEARCH_OUTPUT / f"{topic_slug}-{today}.md"
    output_path.write_text(content, encoding="utf-8")
    print(f"Saved → {output_path}")


if __name__ == "__main__":
    main()
