---
name: knowledge-distillation
description: "Deep project onboarding skill using the knowledge distillation metaphor. Use when: joining a new project, understanding an unfamiliar codebase, going beyond surface-level Q&A to grasp the 'soul' of a system — its domain model, architectural decisions, hidden tensions, and core invariants. Triggers: 'distill this project', 'help me understand this codebase deeply', 'I'm onboarding to a new project', 'explain the soul of this system', 'what is the essence of this codebase', 'deep codebase exploration', 'understand this project like an expert'."
argument-hint: "Name of the project or repo to distill (optional). Omit to distill the current workspace."
---

# Knowledge Distillation

> *Inspired by the AI technique of knowledge distillation — where a smaller "student" model learns the compressed, high-fidelity essence of a large "teacher" model, not just its raw outputs.*

In a codebase, the teacher is the **accumulated knowledge of everyone who ever built it**: embedded in tests, git history, domain naming, architectural seams, and invariants. Surface-level reading captures only the hard labels (what the code *does*). Distillation extracts the **soft labels** — what the authors *believed*, *feared*, *decided*, and *rejected*.

---

## The 5-Phase Distillation Protocol

| Phase | Name | Goal | Time Estimate |
|---|---|---|---|
| 1 | [Terrain Mapping](./phases/01-terrain-mapping.md) | Orient yourself — find the landscape before walking it | 30–60 min |
| 2 | [Signal Extraction](./phases/02-signal-extraction.md) | Extract the rich hidden signals: tests, git, naming | 1–3 hours |
| 3 | [Model Reconstruction](./phases/03-model-reconstruction.md) | Rebuild the domain model the authors had in their heads | 1–2 hours |
| 4 | [Socratic Validation](./phases/04-socratic-validation.md) | Stress-test your understanding with Socratic questions | 1 hour |
| 5 | [Knowledge Compression](./phases/05-knowledge-compression.md) | Compress everything into permanent, shareable artifacts | 30–60 min |

---

## Quick Start

If you have 30 minutes, run **Phase 1** only. It will give you enough orientation to ask better questions and avoid the most common onboarding mistakes.

If you have a full day, run all 5 phases in order. The output is a **Soul Document** — a one-page compressed model of the codebase that an experienced engineer would agree captures its essence.

---

## Core Concepts

| Term | Meaning |
|---|---|
| **Teacher signal** | The accumulated knowledge embedded in the codebase (tests, git, ADRs, naming) |
| **Soft-target reading** | Reading tests to understand *what the author believed*, not just what the code does |
| **Domain signal mining** | Extracting the ubiquitous language — the shared vocabulary that is the soul of the system |
| **Fault-line detection** | Finding the seams between bounded contexts — where domain words change meaning |
| **Spelunking** | Git archaeology: tracing decisions through commit history, blame, and changeset analysis |
| **Soul Document** | The final deliverable — the compressed model of the system in plain language |

---

## Templates

- [Soul Document template](./templates/soul-document.md)
- [New Engineer Briefing template](./templates/new-engineer-briefing.md)
- [ADR template for discovered decisions](./templates/adr-template.md)

## Reference Materials

- [Git Archaeology commands](./references/git-archaeology.md)
- [Socratic Question Bank](./references/socratic-questions.md)
- [DDD Concepts Applied to Code Reading](./references/ddd-concepts.md)
