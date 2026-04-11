# Soul Document

**Project**: [Project Name]  
**Distilled by**: [Your Name]  
**Date**: [YYYY-MM-DD]  
**Time invested in distillation**: [X hours]

---

## 1. What Problem Does This System Solve?

*(2–3 sentences, no tech jargon. If a non-technical stakeholder read this, they should nod.)*

---

## 2. The Core Domain Model

*(The 3–5 concepts that everything else is built around. These are the "load-bearing walls" of the system's understanding of the world.)*

| Concept | What It Is | Why It's Central |
|---|---|---|
| `[ConceptName]` | | |
| `[ConceptName]` | | |
| `[ConceptName]` | | |

---

## 3. The Most Important Invariants

*(The rules that, if violated, break the system or the business fundamentally. Not the most common rules — the most critical.)*

1. **[Invariant name]**: [Plain-language description]. If violated: [what breaks].
2. **[Invariant name]**: [Plain-language description]. If violated: [what breaks].
3. **[Invariant name]**: [Plain-language description]. If violated: [what breaks].

---

## 4. The Fault Lines

*(Where the bounded contexts meet, where domain words change meaning, where the most bugs happen and where the most confusion lives.)*

| Fault Line | Left Side | Right Side | Translation Risk |
|---|---|---|---|
| Between [A] and [B] | [what A means here] | [what B means here] | [what gets lost in translation] |

---

## 5. What This System Intentionally Does NOT Do

*(Scope boundaries — equal in importance to what the system does. Often the reason for a separate service or module.)*

- **Not responsible for**: [X] — [which system is]
- **Explicitly excludes**: [Y] — [why it was carved out]
- **Delegates to**: [Z service/module] — [contract]

---

## 6. The Biggest Source of Complexity

*(Honest answer. Which complexity is essential — inherent in the domain? Which is accidental — technical debt, historical decisions, wrong abstractions?)*

**Essential complexity** (must be carried):  
[Describe the genuinely hard part of the domain]

**Accidental complexity** (should be addressed):  
[Describe the technical debt or structural issues that make the code harder than the domain requires]

---

## 7. What a New Engineer Must Never Touch Without Caution

*(The load-bearing walls. Changing these without deep understanding causes cascading, non-obvious failures.)*

| File / Module / Pattern | Why It's Dangerous | Who to Ask Before Changing |
|---|---|---|
| `[path/to/thing]` | | |
| `[concept or pattern]` | | |

---

## 8. The Remaining Fog

*(Known unknowns — what you couldn't fully understand through distillation alone. Be honest. This is the map of where future exploration should go.)*

- [ ] **[Thing I don't understand]**: [Why it's unclear. What I'd need to figure it out.]
- [ ] **[Assumption I made]**: [What I assumed. How I'd verify it.]
- [ ] **[Contradiction I noticed]**: [What the code says vs. what my model predicts.]

---

## 9. Questions for Domain Experts

*(The residual unknowns that require human input — people who were there when decisions were made.)*

1. [Hypothesis-first question: "I concluded X because Y. Is that correct? What am I missing?"]
2. [...]

---

*This Soul Document was produced using the [Knowledge Distillation skill](../../.github/skills/knowledge-distillation/SKILL.md).*
