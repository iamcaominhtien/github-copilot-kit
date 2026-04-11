# Phase 3 — Model Reconstruction

> *"Instead of brainstorming new domain models, you are reconstructing the one the authors had in their heads."*

**Goal**: Build a rich, structured understanding of the domain model — the invisible blueprint that the code was written to express. You are doing **reverse engineering of intent**, not just code.

---

## Step 1 — Solo Reverse Event Storming

Event Storming (Alberto Brandolini) is a collaborative workshop technique for mapping a domain as a timeline of business events. In onboarding, you run it **solo, in reverse** — reconstructing the events the system processes rather than designing new ones.

**The core vocabulary:**

| Color | Element | Example |
|---|---|---|
| 🟠 **Orange** | Domain Event (past tense, always) | `OrderPlaced`, `PaymentFailed`, `UserRegistered` |
| 🔵 **Blue** | Command (imperative — what triggered it) | `PlaceOrder`, `ProcessPayment`, `RegisterUser` |
| 🟡 **Yellow** | Actor (who/what issues the command) | `Customer`, `Scheduler`, `PaymentGateway` |
| 🟨 **Yellow (light)** | Aggregate (enforces business rules) | `Order`, `Account`, `Inventory` |
| 🩷 **Pink** | Policy / Business Rule | `"Cannot place order if payment failed"` |
| 🔴 **Red** | Hotspot / Problem Area | Unknown, confusing, or contested concepts |

**How to run it solo:**

1. Start from the **write paths** in the codebase (methods that save/update state)
2. For each write path, ask: *"What business event does this represent?"* → write an 🟠 Orange sticky
3. Work backward: *"What command triggered this event?"* → 🔵 Blue
4. Ask: *"Who can issue this command and under what conditions?"* → 🟡 Yellow, 🩷 Pink
5. Ask: *"What aggregate enforces the rules?"* → 🟨 light Yellow
6. Mark anything you can't answer confidently → 🔴 Red

Use a [FigJam](https://www.figma.com/figjam/), whiteboard, or even a plain markdown list. The format matters less than the act of forcing yourself to name the events.

---

## Step 2 — Identify the Primary Invariants

**Invariants are the business rules that can never be violated** — they represent the core constraints the system was built to protect.

Ask the AI:
> "What are the invariants in this codebase? Look for: validation logic that throws exceptions, database constraints, transaction boundaries that wrap multiple operations, and any code that checks a pre-condition before proceeding."

**Classification of invariants:**
- **Hard invariants**: enforced in code (throws, DB constraints, assertions)
- **Soft invariants**: enforced by convention (naming, comments, agreed-upon patterns that aren't technically enforced)
- **Assumed invariants**: not enforced anywhere — the system just assumes they're true (the most dangerous)

For each invariant found, ask: *"What business disaster would happen if this invariant were violated?"* — that question reveals exactly why it exists.

---

## Step 3 — Map Upstream / Downstream Dependencies

Every system exists in a larger ecosystem. Understanding **what the system conforms to** (upstream dependencies) and **what the system controls** (downstream) reveals its role in the wider domain.

**Ask the AI:**
> "What external systems, APIs, or services does this codebase integrate with? Which of these is upstream (we conform to their model) vs. downstream (they conform to ours)?"

**Patterns to identify:**

| Pattern | Description | What to look for |
|---|---|---|
| **Anti-Corruption Layer** | Translation between two models | Adapter/mapper classes, DTO translation |
| **Conformist** | We adopt their model wholesale | Direct use of external types throughout internal code |
| **Partnership** | Bidirectional, co-evolving | Shared types, frequent sync needed |
| **Published Language** | We expose a stable public interface | API contracts, OpenAPI specs, event schemas |

---

## Step 4 — Finalize the Context Map

With the Event Storming and dependency mapping complete, update the rough Context Map you drew in Phase 1.

A complete Context Map shows:
1. The **bounded contexts** — named domain areas with their own ubiquitous language
2. The **relationships** between contexts (Conformist, ACL, Partnership, etc.)
3. The **translation points** — where domain terms change meaning as data crosses boundaries

**Ask the AI:**
> "Based on everything we've analyzed, draw a text-based Context Map of this system. Label each bounded context with its domain language and show the relationships between them."

---

## Deliverable

By the end of Phase 3, you should have:
- [ ] A completed (even rough) Event Storming board for the core workflows
- [ ] A list of the 5–10 primary invariants with their business justification
- [ ] A map of upstream/downstream dependencies with relationship types
- [ ] A finalized Context Map

---

**Prev**: [Phase 2 — Signal Extraction](./02-signal-extraction.md) | **Next**: [Phase 4 — Socratic Validation](./04-socratic-validation.md)
