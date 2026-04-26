# Writing Style: TL;DR

Source: NNGroup (n=51, 124% usability improvement), Google Technical Writing, HBR military BLUF, UW-Madison Writing Center.

---

## Core Philosophy

**Bottom Line Up Front. Always.**

The reader should stop after the first sentence and still understand the verdict. Every sentence after that is optional context.

NNGroup: concise + scannable + objective writing improves usability by **124%**.

**The one test:** *"Can the first sentence be forwarded to a VP with no other context?"* If not — rewrite it.

---

## Structure: Inverted Pyramid, Always

```
[VERDICT — the answer, decision, or key finding]
         ↓
[Supporting facts — who/what/when/how much]
         ↓
[Background — only for those who need it]
```

**BLUF tags** (open every section with type + verdict):
```
ACTION:   Approve vendor migration by Friday.
INFO:     Deployment complete. Zero downtime.
DECISION: Choose between Option A and B by EOD Thursday.
FINDING:  Mobile conversion dropped 18% — cause identified.
```

---

## Opening Rewrites

> ❌ "Over the past quarter we examined user behavior across three platforms. After extensive analysis, we concluded that mobile conversion has dropped significantly."
> ✅ "Mobile conversion dropped 18% this quarter. Cause: checkout form fails on iOS 17. Fix: in progress, ETA Friday."

> ❌ "After a lengthy period of deliberation involving multiple stakeholders..."
> ✅ "Stakeholders approved the migration."

---

## Bloat Phrases — Delete on Sight

| Verbose | Concise |
|---|---|
| at this point in time | now |
| in order to | to |
| due to the fact that | because |
| it is important to note that | *(delete)* |
| is able to | can |
| in the event that | if |
| for the purpose of | for / to |

---

## Bullet Writing Rules

**1. Parallel structure (non-negotiable)** — first bullet sets the grammar contract; every bullet must honor it.

**2. Verb-first for action items** — *Download, Configure, Deploy, Approve*. Not "The app should be downloaded..."

**3. No orphan bullets** — fewer than 3 items? Embed in a sentence.
> ❌ `- Restart the server` / `- Clear the cache`
> ✅ "Restart the server and clear the cache."

**4. One idea per bullet** — "and" linking two distinct actions → split into two bullets.

**5. Similar line lengths** — one 3-word and one 40-word bullet = unfinished editing.

---

## Headers That Summarize, Not Label

| Label ❌ | Summary ✅ |
|---|---|
| Background | Company was profitable in Q3 |
| Results | Conversion dropped 18% |
| Architecture | System uses event sourcing, not REST |
| Next Steps | Engineer X must deploy by Friday |

**Rules:** front-load keywords · works out of context · no hype · ~6 words · answers "so what?"

---

## Tables vs. Bullets

Ask: does the reader need to **compare** or just **enumerate**?

| Need | Use |
|---|---|
| Compare options across multiple attributes | Table |
| Sequential steps | Numbered list |
| Homogeneous items, no comparison | Bullets |
| Error codes + meanings | Table |

---

## One Idea Per Sentence

**Test:** Does the subordinate clause introduce a *new idea* or just *qualify* the main idea?
- New idea → its own sentence
- Qualifies → can stay

> ❌ "The late 1950s was a key era for programming languages because IBM introduced Fortran in 1957 and John McCarthy introduced Lisp the following year, which gave programmers both an iterative and a recursive approach."
> ✅ "The late 1950s was a key era for programming languages. IBM introduced Fortran in 1957. McCarthy invented Lisp the following year. Programmers could then solve problems iteratively or recursively."

**Legitimate exceptions:** causal chain where both halves are the point · contrast requiring both halves · restrictive clause defining the claim.

---

## Section Format Minimum

Every section needs at least one visual:

**Stat callout:**
```markdown
> ⚡ **Bottom line**: Mobile conversion dropped 18%. Cause identified. Fix ETA: Friday.
```

**Before/After table:**
| Before | After |
|---|---|
| 14-step workflow | 3-step workflow |
| 8-second load | 1.2-second load |

Use `> ⚡ Bottom line:` max once per section — it should feel like a landing, not a habit.

---

## Pre-Publish Checklist

- [ ] First sentence states the verdict (not context, not background)?
- [ ] All bloat phrases deleted?
- [ ] Bullets: parallel structure, verb-first, ≥3 items?
- [ ] Headers: summary sentences, ≤6 words, keyword-first?
- [ ] Tables for comparison; bullets for enumeration?
- [ ] One idea per sentence (subordinate clause test done)?
- [ ] Every section has at least one visual element?
- [ ] Zero filler openers: "In today's world," "As we can see," "It is important to note"?
- [ ] First sentence passes the VP forwarding test?
