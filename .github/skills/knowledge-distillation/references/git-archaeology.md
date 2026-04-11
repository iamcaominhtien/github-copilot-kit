# Git Archaeology Reference

> *"Every line of code is always documented — in git." — Mislav Marohnić*

Git history is the **hidden documentation of every decision, argument, and mistake** that shaped the codebase. This reference contains the commands and techniques for reading it systematically.

---

## Core Commands

### The Pickaxe — Trace a Concept Through History

Find every commit that introduced or removed a specific string. Use this to trace the origin of a concept or find when a business rule was first encoded.

```bash
# When was "PaymentGateway" first used?
git log -S "PaymentGateway" --oneline

# When did "OrderStatus.PROCESSING" appear?
git log -S "PROCESSING" --oneline --all

# More context around each match
git log -S "PaymentGateway" -p
```

### Blame + Commit Follow

Find who wrote a specific line and then read the full context of that commit.

```bash
# Who wrote this line?
git blame src/payments/gateway.ts

# Read the full commit for a SHA
git show <SHA>

# Follow a file through renames
git log --follow -p src/payments/gateway.ts
```

### Git Churn — Find the Centers of Instability

```bash
# Files changed most frequently in the past 6 months
git log --since='6 months ago' --name-only --format='' | sort | uniq -c | sort -rn | head -20

# Files changed most frequently ever
git log --name-only --format='' | sort | uniq -c | sort -rn | head -20

# Files touched by the most different contributors
git log --format='%H %ae' --name-only | awk 'NF==2{author=$0} NF==1{print $0, author}' | sort | uniq -f1 | cut -d' ' -f1 | uniq -c | sort -rn | head -20
```

### Ownership — Who Knows What

```bash
# Who has committed to a specific file recently?
git log --since='90 days ago' --format='%an' -- src/payments/ | sort | uniq -c | sort -rn

# Most active contributors to the core domain directory
git log --since='6 months ago' --format='%an' -- src/ | sort | uniq -c | sort -rn
```

### Deleted Code — What the Team Removed

Deleted code is often where the most important decisions live. Something was built, then removed — that removal is a decision.

```bash
# Files that were deleted
git log --diff-filter=D --name-only --format=''

# What code was in a deleted file?
git log --all --full-history -- "src/old-module/file.ts"
git show <SHA>:src/old-module/file.ts

# Commits that removed large amounts of code
git log --oneline --diff-filter=D
```

### Searching Commit Messages

```bash
# Commits mentioning "refactor"
git log --oneline --grep="refactor"

# Commits mentioning specific business terms
git log --oneline --grep="payment" --grep="billing" --all-match

# Commits in a date range
git log --oneline --after='2024-01-01' --before='2024-06-01'
```

---

## Spelunking Workflow (Systematic)

When investigating a specific module or concept, run this sequence:

1. **Churn check**: How often has this file changed?
   ```bash
   git log --oneline -- path/to/file.ts | wc -l
   ```

2. **Age check**: When was this file first created?
   ```bash
   git log --follow --format="%ad %s" --date=short -- path/to/file.ts | tail -1
   ```

3. **Blame scan**: Who wrote the key sections?
   ```bash
   git blame path/to/file.ts
   ```

4. **Most significant commits**: What are the most impactful changes?
   ```bash
   git log --oneline -- path/to/file.ts | head -10
   # Then: git show <SHA> for each
   ```

5. **Pickaxe for key concepts**: When did the core concept appear?
   ```bash
   git log -S "CoreConceptName" --oneline -- path/to/file.ts
   ```

---

## Reading a Commit Well

When you `git show <SHA>`, read it in this order:

1. **Title** — what the author claimed they were doing
2. **Body** (if present) — why they did it, what they considered, links to issues/PRs
3. **Files changed** — the scope of the decision
4. **Diff** — what specifically changed

**Warning signals in commit messages:**
- `"fix"` or `"hotfix"` → something broke; what and why?
- `"WIP"` or `"temp"` → unfinished work that was shipped
- `"finally"` or `"at last"` → pain point that resisted solution for a while
- `"hack"` or `"workaround"` → technical debt that was consciously accepted
- No message / "." → the author was in a rush or conflict-averse

---

## GitHub CLI — Reading PR Context

If the project is on GitHub, PR descriptions are the richest source of reasoning. The commit message is the conclusion; the PR is the argument.

```bash
# Install GitHub CLI if needed
brew install gh

# List recent PRs
gh pr list --limit 20 --state all

# Read a specific PR (by number)
gh pr view 123

# PRs that touched a specific file
gh pr list --state all --search "filename:src/payments/gateway.ts"
```

---

## Sources

- Mislav Marohnić, *Every line of code is always documented* — https://mislav.net/2014/02/hidden-documentation/
- Michael Feathers, *Working Effectively with Legacy Code* (2004)
