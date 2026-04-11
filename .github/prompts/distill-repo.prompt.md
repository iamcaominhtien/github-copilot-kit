---
name: distill-repo
description: "Full-repo knowledge distillation via project-manager orchestration. Runs the knowledge-distiller and knowledge-keeper across all major topics in sequence, outputting a doc per topic. Use when: onboarding to a new project, producing a comprehensive codebase knowledge base, or building documentation covering coding conventions, business logic, features, architecture, and tech stack."
argument-hint: "Optional: specific topics to focus on, or leave blank for full distillation"
agent: project-manager
---

Work with the `Plan`, `knowledge-distiller`, and `knowledge-keeper` agents to perform a full knowledge distillation of this repository, then export documentation for every topic.

## Goal

Extract and document every significant aspect of this codebase — coding conventions, business logic, features, architecture, tech stack, domain model, and anything else that matters — so that a new engineer could onboard quickly and deeply.

## Distillation Topics

Run one sequential session per topic. Finish and export the doc before moving to the next.

| # | Topic | What to Cover |
|---|---|---|
| 1 | **Tech Stack & Infrastructure** | Languages, frameworks, libraries, deployment setup, CI/CD, external services |
| 2 | **Architecture & Structure** | Directory layout, domain layers, key abstractions, system boundaries |
| 3 | **Domain Model & Business Logic** | Core entities, invariants, bounded contexts, ubiquitous language |
| 4 | **Features & Workflows** | Main features, key user flows, how they are implemented end-to-end |
| 5 | **Coding Conventions** | Naming, patterns, error handling, testing approach, style decisions |
| 6 | **Hidden Knowledge** | Git archaeology findings, deleted code, ADRs, non-obvious decisions |
| 7 | **Soul Document** | Synthesize all topics into a single onboarding page — the essence of the system, written for a new engineer's first day |

## Orchestration Instructions

For **each topic**:
1. Delegate exploration to `knowledge-distiller` — run the relevant distillation phases for the topic scope
2. Once findings are ready, delegate to `knowledge-keeper` to store findings as memory AND export as a doc in `docs/distillation/`
3. Confirm the doc is written before moving to the next topic
4. Do NOT batch topics — run them one at a time, in sequence

## Output

- One doc per topic (topics 1–6), saved to `docs/distillation/<topic-slug>.md`
- A Soul Document at `docs/distillation/soul-document.md` — a single-page synthesis of all 6 topics, written for a new engineer's first day
- A final index doc at `docs/distillation/README.md` listing all produced docs

## Soul Document Instructions

After all 6 topic docs are written, produce `docs/distillation/soul-document.md`:
- **Audience:** a new engineer on day one
- **Length:** one page (500–800 words max)
- **Content:** the core domain model in plain language, the key architectural decisions, the most important conventions, and the one thing that would take months to figure out without this doc
- **Tone:** direct and opinionated — not a summary, but a guide

## Completion Criteria

The distillation is complete when:
- All 6 topic docs exist in `docs/distillation/`
- `docs/distillation/soul-document.md` is written
- The index `README.md` is written
- A new engineer could read the soul document in 10 minutes and understand the codebase better than a week of casual exploration would provide
