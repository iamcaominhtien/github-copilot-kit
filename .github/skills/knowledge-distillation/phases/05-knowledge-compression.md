# Phase 5 — Knowledge Compression

> *"Intelligence is not the accumulation of information, but the compression of it into understanding."*

**Goal**: Compress everything you've learned into permanent, shareable artifacts. These artifacts serve two purposes: (1) they force you to synthesize rather than just accumulate, and (2) they become the teacher signal for the next engineer who joins after you.

---

## Step 1 — Write the Soul Document

The **Soul Document** is a single-page (400–600 word) description of the essence of the system. Not what it does. What it *is* — its purpose, its constraints, its core model, and what makes it hard.

Use the [Soul Document template](../templates/soul-document.md).

**The Soul Document must answer:**
1. **What problem does this system solve?** (in 2–3 sentences, no tech jargon)
2. **What is the core domain model?** (the 3–5 concepts that everything else is built around)
3. **What are the 3 most important invariants?** (the rules that, if violated, break the system catastrophically)
4. **What are the fault lines?** (where the bounded contexts meet, where the most bugs happen, where the most confusion lives)
5. **What does this system intentionally NOT do?** (scope boundaries — often encoded in git history and deleted code)
6. **What is the biggest source of complexity?** (honest answer — accidental complexity vs. essential complexity)
7. **What should a new engineer NEVER touch without extreme caution?** (the load-bearing walls)

---

## Step 2 — Write ADRs for Discovered Decisions

An **Architecture Decision Record (ADR)** is a short document that captures an architectural decision: what was decided, why, and what alternatives were considered.

Use the [ADR template](../templates/adr-template.md).

Write an ADR for the **top 3 structural decisions you discovered** through your distillation:
- A decision visible in the directory structure (why is it organized this way?)
- A decision visible in git history (a significant refactoring or approach change)
- A decision visible in the domain model (why is X a separate bounded context from Y?)

ADRs transform discovered knowledge into permanent, searchable records. The next engineer won't have to re-discover these decisions.

---

## Step 3 — Write the New Engineer Briefing

The **New Engineer Briefing** is a 5-point cheat sheet — the 5 things every new engineer *must* know before making their first change.

Use the [New Engineer Briefing template](../templates/new-engineer-briefing.md).

**Good "must-know" items include:**
- A non-obvious invariant that causes bugs when violated
- The most counterintuitive naming decision and what it actually means
- The most dangerous file/module and why
- A common mistake that experienced engineers also make
- The "center of gravity" — the abstraction that everything else depends on

---

## Step 4 — Identify Questions for Domain Experts

After all this independent distillation, you will have a clear list of questions that can only be answered by talking to someone who was there. These are the **residual unknowns** — things the code cannot tell you on its own.

Compile these into a list and schedule a conversation with the team lead, architect, or longest-tenured engineer. You will get far more value from this conversation now (after distillation) than you would have gotten if you'd started with it.

**Frame your questions as Socratic challenges:**
- Instead of: *"Why is the payment module separate?"*
- Ask: *"I reconstructed the domain model and concluded that payments were separated because of X. Is that correct? What am I missing?"*

This framing signals that you've done serious work and gets you exponentially richer responses.

---

## Step 5 — Place Artifacts in the Right Location

| Artifact | Recommended Location |
|---|---|
| Soul Document | `docs/soul-document.md` or `docs/architecture/soul.md` |
| ADRs | `docs/decisions/adr-NNN-title.md` (use sequential numbering) |
| New Engineer Briefing | `docs/onboarding/briefing.md` or top-level `ONBOARDING.md` |
| Remaining Fog list | Personal notes — not committed, but not forgotten |
| Event Storming board | `docs/domain/event-storming.md` or a FigJam link |
| Context Map | `docs/domain/context-map.md` or embedded in architecture docs |

---

## Deliverable

At the end of Phase 5, you should have produced:
- [ ] A Soul Document (400–600 words)
- [ ] 3 ADRs for discovered decisions
- [ ] A New Engineer Briefing (5 key must-know items)
- [ ] A question list for domain expert conversations
- [ ] All artifacts committed to the repo in appropriate locations

---

**You have completed the Knowledge Distillation protocol.** The system that was once behind a fog is now legible — not just to you, but to every engineer who comes after.

---

**Prev**: [Phase 4 — Socratic Validation](./04-socratic-validation.md) | **Back to**: [SKILL.md](../SKILL.md)
