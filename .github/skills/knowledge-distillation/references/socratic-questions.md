# Socratic Question Bank

> *Surface-level: "What does this do?" — Distillation: "Why does this exist? What would break without it?"*

This question bank provides a structured set of Socratic questions organized by the level of analysis. Use these to probe your own understanding and to interrogate the AI when exploring a codebase.

---

## Question Hierarchy

| Level | Surface Question | Socratic Question |
|---|---|---|
| **Function** | What does this function do? | *Why does this function exist? What would break without it? Who calls this, and why do they need it?* |
| **Module** | What does this module contain? | *What concept is this module protecting? What does it deliberately NOT know about? What is its one reason to change?* |
| **Dependency** | What does A depend on B for? | *Why does A depend on B? What assumption does that encode? What would need to change in the domain to reverse this dependency?* |
| **Architecture** | How is the system structured? | *What problem is this structure solving? What problem does it create? What alternatives were ruled out, and why?* |
| **History** | When was this added? | *What changed in the business or domain that made this code necessary? What did it replace?* |
| **Tests** | What does this test verify? | *What failure was the author afraid of? What production incident might have prompted this? What is the system's most dangerous edge?* |
| **Error handling** | What errors are caught? | *What does the system treat as unrecoverable? What does it treat as transient? Why?* |
| **Naming** | What is this called? | *Does the name reflect the domain or the implementation? What would a non-technical stakeholder think this does? Is the name lying?* |

---

## Questions by Exploration Goal

### To Understand Purpose

- *What would a non-technical stakeholder need this module/service to do, in plain language?*
- *If this were deleted, what is the first visible symptom the user would see?*
- *What guarantee does this code make to the rest of the system?*
- *What rule is this enforcing? What happens if that rule is broken?*

### To Understand Architecture

- *Why is this a separate module/service/class rather than being part of X?*
- *What cohesion principle guides what belongs here?*
- *Where is the boundary of this thing's responsibility — and why there?*
- *Is this architecture solving an existing problem, or preventing a hypothetical one?*
- *What would need to change in the domain for this architectural decision to become wrong?*

### To Understand Dependencies

- *Why does A know about B? Who decided this, and when?*
- *What would it take to decouple A from B? Is there a seam here?*
- *Is this dependency an accident (happened to be convenient) or a decision (encodes domain relationship)?*
- *Does the direction of this dependency make domain sense — is A really "in charge of" B?*

### To Understand History

- *This code exists. What stopped existing when it was created?*
- *What was the previous approach, and why was it abandoned?*
- *Is this code young (rapidly changing) or mature (stable because trusted or stable because feared)?*
- *Who built this, and are they still here? (Do I have access to the human teacher signal?)*

### To Understand Complexity

- *Is this complexity solving a real domain problem, or is it accidental (technical debt)?*
- *What would the simplest version of this look like? What would we lose?*
- *What's the most common reason this code has to change? Is it business change or technical change?*
- *If I had to explain this to a senior engineer in 60 seconds, what would I say?*

### To Understand Risk

- *What is the most dangerous assumption this code makes?*
- *What external change (business rule, API contract, infra behavior) would break this silently?*
- *Where might a new engineer most likely introduce a bug? Why?*
- *What is protected by tests? What is only protected by convention?*

---

## Prompts for the AI

Use these prompts when exploring with GitHub Copilot or another AI assistant:

```
"Read [file/module] and tell me: What was the author most worried about? 
What invariants does this protect? What business rule is encoded here?"
```

```
"I think [module X] is responsible for [Y]. What evidence in the code 
supports or contradicts this hypothesis?"
```

```
"Given this code, what are the 3 most important questions a new engineer 
should ask before making any changes?"
```

```
"Look at the test file for [feature]. What failure was the author afraid of? 
What business rules are encoded in the specific values used?"
```

```
"What does [module X] deliberately NOT know about? What is it isolated from, 
and why might that isolation be intentional?"
```

```
"If [module X] were deleted, what is the first visible symptom? 
Trace the failure path."
```

```
"What are the 3 most dangerous assumptions this codebase makes about 
the outside world? Are any of them currently being violated?"
```

---

## Posture Reminder

> *"Approach the code as a shared intellectual object to be understood, not judged."*
> — Gerald Weinberg, Egoless Programming (1971)

Socratic questioning in onboarding is never about critique. It is about **reconstructing the reasoning** of the people who built the system. Even code that seems wrong had reasons for being written that way — those reasons are part of the teacher signal.
