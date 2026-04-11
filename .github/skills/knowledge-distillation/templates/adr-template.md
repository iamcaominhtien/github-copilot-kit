# ADR — Architecture Decision Record

> ADR format based on Michael Nygard's original template (2011).  
> Use this to document architectural decisions you **discovered** during distillation — decisions the original authors made but never wrote down.

---

**ADR Number**: [NNN]  
**Title**: [Short noun phrase describing the decision, e.g., "Use Event Sourcing for Order State"]  
**Date**: [YYYY-MM-DD]  
**Status**: [Accepted | Superseded by ADR-NNN | Deprecated]  
**Discovered by**: [Your name] during knowledge distillation  
**Original decision approximately**: [Year or date range, if discoverable from git history]

---

## Context

*(What situation, business requirement, or technical constraint required a decision? What forces were at play? Be specific about the domain context.)*

---

## Decision

*(What was decided? State it clearly in active voice: "We will use X" or "The system uses X because...")*

---

## Evidence of This Decision in the Codebase

*(This section is unique to discovered ADRs — cite where you found evidence of this decision.)*

| Evidence Type | Location | What It Shows |
|---|---|---|
| Code structure | `[path]` | [Why this path/pattern reveals the decision] |
| Git commit | `[SHA]` | [What the commit message / diff shows] |
| Test pattern | `[path]` | [What the tests assume about the decision] |
| Naming choice | `[class/method]` | [How the naming encodes the decision] |

---

## Alternatives That Were Rejected

*(If discoverable from git history, deleted code, or PR comments — what alternatives did the team consider? If not findable, state your hypothesis about what alternatives existed.)*

| Alternative | Why It Was Likely Rejected |
|---|---|
| [Alternative approach] | [Reasoning, if discoverable. Otherwise: hypothesis] |

---

## Consequences

*(What became easier or harder as a result of this decision? These are often visible as recurring patterns in the codebase, or as hotspots in git churn.)*

**Positive:**
- [What this decision makes easy or safe]

**Negative / Trade-offs:**
- [What this decision makes harder, or what it costs]
- [What technical debt this decision creates or inherited]

**Open questions:**
- [Things this document couldn't determine — questions for domain experts]

---

## Related Decisions

- [ADR-NNN: related decision]
- [Any system or architectural diagram that shows this decision]

---

*Discovered during knowledge distillation of [Project Name] using the [Knowledge Distillation skill](../../.github/skills/knowledge-distillation/SKILL.md).*
