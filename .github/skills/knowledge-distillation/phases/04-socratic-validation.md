# Phase 4 — Socratic Validation

> *"I know that I know nothing." — Socrates*
> *"I know what I think I know. Let me prove it." — The distilling engineer*

**Goal**: Stress-test your understanding. You have built a model of the system — now you must challenge it with Socratic questioning before you trust it. A model you can't defend is not yet a model.

---

## The Socratic Method Applied to Code

Surface-level understanding answers: *"What does this do?"*  
Distilled understanding answers: *"Why does this exist? What would break without it? What did the authors decide NOT to do here?"*

See the full [Socratic Question Bank](../references/socratic-questions.md) for the complete question set.

---

## Step 1 — Module-by-Module Socratic Interrogation

For each of the 5 most important modules identified in Phase 1, ask these questions:

**Existence questions:**
- Why does this module exist as a separate module? What would happen if it were merged into another?
- What concept is this module protecting? What does it deliberately NOT know about?
- If this module were deleted, what is the first visible symptom the user would see?

**Dependency questions:**
- Why does this module depend on X? What assumption does that encode?
- What would need to change in the domain for this dependency to be removed?
- Is there any circular reasoning in the dependencies? (A needs B to understand itself)

**Naming questions:**
- Is the name of this module accurate? Does it match what it actually does?
- What would a domain expert (non-technical stakeholder) think this module does, based purely on the name?

---

## Step 2 — Gotcha Scenario Tracing

Generate 3 "gotcha" scenarios — edge cases or unusual situations that test the boundaries of your model — and trace through the code manually.

**How to generate good scenarios:**

Ask the AI:
> "Given my understanding of this system's domain, what are the 3 most dangerous edge cases — situations where the behavior is least obvious, most likely to surprise a new engineer, or most likely to cause a bug?"

Then:
1. Write down your **predicted behavior** before tracing
2. Trace through the actual code path
3. Compare result to prediction
4. Any gap between prediction and reality = a gap in your distilled model

**Good scenario types:**
- Concurrency: what happens if two users do X at the same time?
- Failure recovery: what happens if step 3 of a 5-step workflow fails?
- Boundary values: what happens at exactly the min and max of a quantity?
- Permission edge cases: what happens if the actor is partially authorized?
- Data transformation: what happens if the input is in an unexpected format?

---

## Step 3 — Challenge Your Own Model

Take the model you've constructed (Context Map, Event Storming, invariants) and actively try to break it.

**Self-interrogation prompts:**
- If I had to change [X] in the business domain, what would need to change in the code? Does that make sense?
- Where in the code would a new engineer most likely make a mistake? Is my model of why that is correct?
- What does the code assume about the world outside itself? Are those assumptions documented anywhere?
- What is the most fragile part of this system? Does my model explain why?

**Ask the AI:**
> "I think this system works as follows: [your summary of the model]. What evidence in the codebase supports or contradicts this hypothesis? What corner cases does my model not account for?"

---

## Step 4 — Identify Your Remaining Fog

After Phases 1–4, there will still be areas of uncertainty — parts of the codebase that remain opaque. This step is about **naming your fog explicitly** rather than ignoring it.

Create a list of:
- **Known unknowns**: things you know you don't understand yet
- **Assumed truths**: things you've assumed without verifying
- **Contradictions**: places where your model says one thing but the code suggests another

This list is not a failure — it is a map of where future exploration should focus. It is also the most honest documentation you can give to future engineers.

---

## Deliverable

By the end of Phase 4, you should have:
- [ ] Socratic interrogation notes for the 5 most important modules
- [ ] 3 traced gotcha scenarios, with gaps between predicted and actual behavior documented
- [ ] A list of at least 5 challenges you posed to your own model (and the answers)
- [ ] A "Remaining Fog" list: known unknowns, assumed truths, and contradictions

---

**Prev**: [Phase 3 — Model Reconstruction](./03-model-reconstruction.md) | **Next**: [Phase 5 — Knowledge Compression](./05-knowledge-compression.md)
