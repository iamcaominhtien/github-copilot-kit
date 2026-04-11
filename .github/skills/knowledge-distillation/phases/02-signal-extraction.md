# Phase 2 — Signal Extraction

> *"The teacher's knowledge is hidden in the soft labels — not what the code does, but what the authors believed, feared, and protected."*

**Goal**: Extract the rich hidden signals that encode deep authorial intent. These are the **soft targets** of the codebase — the test suite, git history, naming decisions, and error handling patterns that reveal what the team actually cared about.

---

## Step 1 — Read Tests as Domain Documentation (Soft-Target Reading)

**Tests are the closest thing to the authors' mental model.** They encode intended behavior far more richly than comments or docs, because they were written when the authors were actively reasoning about correctness.

**What to look for:**

| Test Pattern | What It Reveals |
|---|---|
| Tests with very specific numeric/string values | Business rules encoded as pure knowledge |
| Tests for edge cases that seem unlikely | Painful bugs that already happened in production |
| Tests marked as `skip` or `pending` | Known unknowns — territory the team hasn't fully mapped |
| Tests with very long setup (many mocks/fixtures) | Highly coupled code, or domain state that is hard to construct |
| Integration tests that span many modules | The most important workflows — the "happy paths" that must always work |
| Tests for error messages | The system's vocabulary for failure — often rich with domain meaning |

**Ask the AI:**
> "Read the test files for [module X] and tell me: What did the author seem most worried about? What invariants do the tests protect? What business rules are encoded in the specific values used?"

---

## Step 2 — Git Archaeology (Spelunking)

Git history is the **hidden documentation of every decision, argument, and mistake** that shaped the codebase. Most engineers never read it. Distillation requires reading it.

See the full [Git Archaeology Reference](../references/git-archaeology.md) for commands.

**Key techniques:**

```bash
# The Pickaxe — find commits that introduced or removed a specific concept
git log -S "PaymentGateway" --oneline

# Blame + follow — understand why a line exists
git blame <file>
# Then: git show <commit-SHA> to read the full context

# Follow a concept across renames
git log --follow -p src/payments/gateway.ts

# Who owns what (last 90 days)
git log --since='90 days ago' --format='%an' -- src/ | sort | uniq -c | sort -rn
```

**What to mine:**

1. **The 5 most important files** (from Phase 1 centers of gravity) — read the blame and last 10 commits for each
2. **Any file with "refactor" or "restructure" in surrounding commits** — these are decision points
3. **Deleted code** — find what was removed and why (`git log --diff-filter=D --name-only`)
4. **PR descriptions** (if accessible via GitHub CLI) — the richest single source of reasoning

---

## Step 3 — Scratch Refactoring the Opaque Module

Pick the **most opaque module** — the one you least understand from Phase 1. Then:

1. **Check out a temporary branch**: `git checkout -b distillation/scratch`
2. **Rename everything** in the module to what you think it means: rename variables, extract functions, simplify conditionals
3. **Run the tests** — if they pass, your understanding is roughly correct; if they fail, revise
4. **Discard everything**: `git checkout . && git branch -D distillation/scratch`

You are not shipping this code. You are using editing as a reading tool. The goal is to force yourself into a position where you must assign meaning to every name and every structure.

This technique is known as **Scratch Refactoring** (Michael Feathers, "Working Effectively with Legacy Code").

---

## Step 4 — Mine the Ubiquitous Language

The **Ubiquitous Language** is the shared vocabulary of the domain — the terms that should appear both in conversations with stakeholders and in the code. Finding where the language is consistent, and where it breaks down, reveals the soul and the scars of the system.

**Extract the vocabulary:**

Ask the AI:
> "Scan the codebase and list all the key domain terms — entity names, method names that express business concepts, event names, error message language. Which terms appear consistently? Which terms seem to have multiple synonyms or conflicting meanings in different parts of the code?"

**Red flags to look for:**
- `processData()`, `handleStuff()`, `doThing()` — no domain meaning, pure tech speak
- The same concept named `customer` in one module and `user` in another — domain split
- Terms from the domain that appear nowhere in the code — means the business model isn't in the code at all (common in older systems)

---

## Step 5 — Identify the Error Handling Patterns

**Error handling reveals what the system treats as unrecoverable** — the dark edges of the domain model.

Look for:
- Broad `catch-all` error handlers → the team gave up modeling failure
- Custom error types (`PaymentDeclinedError`, `InventoryExhaustedError`) → these are **domain events that failed**; each one encodes a business rule
- Silent failures (`catch (e) { /* ignore */ }`) → danger zones; these are either tech debt or deliberate but unexplained decisions
- Retry logic → reveals what the team considers transient vs. permanent failure

---

## Deliverable

By the end of Phase 2, you should have:
- [ ] A list of the top 5 business rules encoded in tests
- [ ] The 3–5 most interesting commits in git history (with your notes on why they matter)
- [ ] A completed scratch refactoring of at least one opaque module
- [ ] A draft vocabulary list — domain terms and where they are consistent/inconsistent
- [ ] A map of the custom error types and what they represent

---

**Prev**: [Phase 1 — Terrain Mapping](./01-terrain-mapping.md) | **Next**: [Phase 3 — Model Reconstruction](./03-model-reconstruction.md)
