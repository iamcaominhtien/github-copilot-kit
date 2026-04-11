# Phase 1 — Terrain Mapping

> *"Do not read a single line of feature code until you understand the landscape."*

**Goal**: Orient yourself structurally. Build a coarse map of the codebase — where domain layers live, what the bounded contexts are, and **where uncertainty is concentrated**. Think like a cartographer, not a tourist.

---

## Step 1 — Scan the Directory Structure (Domain-First)

Do NOT interpret the structure as a tech stack. Interpret it as **where domain concerns live**.

Ask the AI:
> "Look at the directory structure and identify the primary domain concepts — not technical layers. Which directories seem to encode business logic vs. infrastructure concerns? Where are the most important decisions likely to be?"

Flag any directories that:
- Use generic tech names (`utils/`, `helpers/`, `common/`) — these are often where domain confusion hides
- Have unexpectedly deep nesting — may indicate growing complexity or historical scar tissue
- Have unexpected names relative to the domain — naming mismatches reveal domain debt

---

## Step 2 — Run Git Churn Analysis

Git churn tells you **where the system is uncertain** — files that change most frequently are either buggy, overloaded with responsibility, or sit at unstable domain boundaries.

```bash
# Top 20 most-changed files in the past 6 months
git log --since='6 months ago' --name-only --format='' | sort | uniq -c | sort -rn | head -20

# Files changed by the most contributors (team hotspots)
git log --since='6 months ago' --format='%an' --name-only | awk 'NF' | sort | uniq -c | sort -rn | head -20
```

**Interpret results:**
- High churn + single owner → high bus factor risk
- High churn + many contributors → crossing of concerns or unclear responsibility
- High churn + test files → tests are being written reactively (pain zone)
- Low churn but central to architecture → likely stable and well-understood (or never touched out of fear)

---

## Step 3 — Draw a Rough Context Map

Before reading any feature code, sketch a **Context Map** — a high-level diagram of the bounded contexts in the system.

Ask the AI:
> "Based on the directory structure and any README or architecture docs, can you sketch the bounded contexts in this system? Where do the same domain words (like 'user', 'account', 'order') appear in different parts of the codebase with potentially different meanings?"

Look for:
- **Anti-Corruption Layers** (ACL): translation code between two domain models
- **Shared Kernels**: code shared between multiple contexts with shared ownership
- **Conformist** relationships: places where this system simply adopts an upstream model

You don't need to be accurate yet. The goal is to have a **hypothesis map** that you'll refine in Phase 3.

---

## Step 4 — Identify the "Centers of Gravity"

Every codebase has a few files or modules that everything else orbits. These are the centers of gravity — not necessarily the largest files, but the most **load-bearing** ones.

Ask the AI:
> "Which files or modules does the rest of the codebase depend on most? Which abstractions or types appear throughout the codebase? What would break first if I made a mistake?"

Also look at:
- What types/interfaces are imported in many files
- What services or classes are instantiated at the top level
- What files are referenced in the main configuration or entry point

---

## Deliverable

By the end of Phase 1, you should be able to answer:
- [ ] What are the 3–5 main domain areas of this system?
- [ ] Which 5 files are the most load-bearing?
- [ ] Where are the areas of highest churn (instability)?
- [ ] What is my initial hypothesis for the bounded contexts?

If you cannot answer these, spend more time in Phase 1 before proceeding.

---

**Next**: [Phase 2 — Signal Extraction](./02-signal-extraction.md)
