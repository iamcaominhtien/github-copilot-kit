# Scripts

Utility scripts for the GitHub Copilot Kit workspace. Run all scripts from the **workspace root**.

---

## assemble.py — Deep Research Report Assembler

Assembles a final Markdown report from section files produced by the `deep-research` prompt.

### Usage

```bash
python .github/scripts/assemble.py <topic-slug>
```

### What it does

The `deep-research` prompt writes each report section into its own `index.md` file under a numbered folder. This script walks those folders in order and joins them into one coherent Markdown file.

```
research-output/.artifacts/<topic-slug>/sections/
  00-header/index.md        → H1  (title + metadata)
  01-opening/index.md       → H2
  02-findings/index.md      → H2
    01-subtopic/index.md    → H3
    02-subtopic/index.md    → H3
  03-implications/index.md  → H2
  ...
```

Output: `research-output/<topic-slug>-<YYYY-MM-DD>.md`

### Heading rules

| Folder depth | Rendered as |
|---|---|
| `sections/00-header/` | H1 (unchanged) |
| `sections/01-slug/` | H2 |
| `sections/01-slug/01-sub/` | H3 |

The script reads `# Heading` from the first line of each `index.md` and adjusts the level automatically. Folder names are for ordering only.

### Asset paths

Images placed in `sections/assets/images/` are referenced in section files as:

```markdown
![caption](../assets/images/filename.png)
```

The assembler rewrites these to the correct relative path in the output file. Direct `https://` URLs are preserved as-is.

### Requirements

Python 3.10+ (uses `str | None` union syntax). No external dependencies.
