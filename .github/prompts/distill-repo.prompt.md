---
name: distill-repo
description: "Full-repo knowledge distillation via project-manager orchestration. Runs the knowledge-distiller and knowledge-keeper across all major topics in sequence, outputting a doc per topic. Use when: onboarding to a new project, producing a comprehensive codebase knowledge base, or building documentation covering coding conventions, business logic, features, architecture, and tech stack."
argument-hint: "Optional: specific topics to focus on, or leave blank for full distillation"
agent: project-manager
---

Work with the `Plan`, `knowledge-distiller`, and `knowledge-keeper` agents to distill this repository and export documentation for every topic.

## What I Need

I want to understand every significant aspect of this codebase — coding conventions, business logic, features, architecture, tech stack, domain model, and anything else that matters — so a new engineer could onboard quickly and deeply.

## Suggested Approach

To work efficiently, run **one topic at a time, sequentially** — finish and export the doc before moving to the next. Let `knowledge-distiller` explore each topic deeply, then `knowledge-keeper` store the findings and export the doc.

Suggested topics to cover (adapt based on what the repo actually contains — add, remove, or split as needed):

- Tech stack & infrastructure
- Architecture & structure
- Domain model & business logic
- Features & workflows
- Coding conventions
- Hidden knowledge (git history, deleted code, non-obvious decisions, ADRs)

End with a **Soul Document** — a single-page synthesis of everything, written for a new engineer's first day. Direct and opinionated, not a summary.

## Output

- One doc per topic in `docs/distillation/`
- Soul Document at `docs/distillation/soul-document.md`
- Index at `docs/distillation/README.md`
- The index `README.md` is written
- A new engineer could read the soul document in 10 minutes and understand the codebase better than a week of casual exploration would provide
