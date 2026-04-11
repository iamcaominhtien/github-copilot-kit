# DDD Concepts Applied to Code Reading

> Domain-Driven Design provides the richest vocabulary for reading a codebase as a **domain model** rather than a collection of functions. You don't need to be practicing DDD to use these concepts — they are tools for understanding.

---

## The Core Vocabulary

### Ubiquitous Language

The **shared vocabulary** between technical and non-technical stakeholders. In a well-designed system, the words used in business conversations appear directly in the code.

**How to find it:**
- List all entity names, event names, method names that express business concepts
- Notice where the language is consistent and where it breaks down
- Look for synonyms: `customer` vs `user` vs `account` in different modules

**What inconsistency reveals:**
- `customer` in one module + `user` in another = the system was built by teams that didn't share a model
- `processData()` everywhere = the domain language never made it into the code (the model lives only in people's heads)
- Frequent comments explaining what a name means = the name is wrong

---

### Bounded Context

A **Bounded Context** is a region of the codebase where a specific Ubiquitous Language applies. Inside the boundary, terms have one precise meaning. At the boundary, translation happens.

**How to identify bounded contexts in code:**
1. Find where the same domain word (`Order`, `Product`, `User`) appears in multiple places with subtly different meanings
2. Look for `Mapper`, `Adapter`, `Translator`, `Converter` classes — these are often at context boundaries
3. Find where imports cross a major architectural seam (e.g., `billing/` importing from `inventory/`)
4. Look for DTO transformations — data being re-shaped as it moves between modules

**Common context boundary patterns:**
- `anti_corruption/`, `adapters/`, `translators/` directories
- Files named `*Mapper.ts`, `*Converter.java`, `*Translator.py`
- Types that exist in two nearly-identical versions in different modules

---

### Aggregate

An **Aggregate** is a cluster of domain objects that are treated as a single unit for the purpose of data changes. The Aggregate Root is the entry point — you can only modify the aggregate through it.

**How to identify aggregates in code:**
- Entity classes that own other entities (have collections or references to other entities)
- Classes that contain business rule validation (all changes go through `placeOrder()`, not directly to `Order.items`)
- Database transactions that group multiple writes together
- Classes that appear at the top of the domain model and are passed around as the main "noun"

**The aggregate root smell:**
- If you see code like `order.items.push(item)` instead of `order.addItem(item)`, the aggregate root is being bypassed — this is a red flag

---

### Domain Event

A **Domain Event** is something significant that happened in the domain — stated in past tense and representing a business fact.

**How to find domain events in code:**
- Classes named `*Event`, `*Happened`, `*Occurred` (well-named systems)
- Method calls that publish to an event bus, message queue, or emit function
- Database records that are append-only (an event log)
- `on*()` handlers, `subscribe*()` methods, Webhook payloads

**Why they matter for distillation:**
Domain events are the **vocabulary of what the system notices**. Each event is a business fact the system considers important enough to record. Together, they define the system's view of the world.

---

### Repository

A **Repository** provides the illusion that domain objects exist in memory (even when they're in a database). It hides the persistence mechanism from the domain model.

**How to identify:**
- Classes named `*Repository`, `*Store`, `*DAO` (Data Access Object)
- Interfaces with methods like `findById()`, `save()`, `findAll()`
- Injected into domain services or use case classes

**What repositories reveal about the domain:**
- The queries that exist reveal what the domain needs to ask about its state
- Missing queries reveal domain questions that aren't yet being asked
- Complex queries (many joins, custom SQL) reveal aggregates that were not modeled correctly

---

## Relationship Patterns Between Contexts

| Pattern | Direction | Description | Code Signal |
|---|---|---|---|
| **Conformist** | One-way, downstream conforms | We adopt upstream's model wholesale | External types used directly in internal code |
| **Anti-Corruption Layer (ACL)** | One-way, with translation | We translate upstream's model into our own | Adapter/mapper classes at the boundary |
| **Shared Kernel** | Bidirectional, shared ownership | Shared model co-owned by two contexts | Shared library, shared types, coordinated changes |
| **Partnership** | Bidirectional, coordinated | Two contexts co-evolve with mutual agreement | Frequent imports between contexts, no clear translator |
| **Published Language** | We expose a stable interface | Others conform to our model | OpenAPI specs, event schemas, stable public API |
| **Separate Ways** | No relationship | Contexts that don't integrate | No imports between directories |

---

## The Whirlpool Process

Eric Evans' **Whirlpool** is an iterative process for exploring a domain model. For onboarding, you run it in reverse — reconstructing the existing model.

```
Scenario exploration
       ↓ ↑
Model brainstorming  ←→  Challenge with scenarios
       ↓ ↑
    Refinement
```

**Applied to onboarding:**
1. **Scenario**: Read a test case (this is your "scenario given to you by the codebase")
2. **Model brainstorming**: What domain model would produce this behavior?
3. **Challenge**: Does the actual code match your model? Where does it diverge?
4. **Refinement**: Update your model and repeat

The Whirlpool is why Scratch Refactoring (Phase 2) is effective — the act of renaming forces you to go through each iteration of this loop for every identifier.

---

## Resources

- Eric Evans, *Domain-Driven Design Reference* (free PDF): https://www.domainlanguage.com/product/domain-driven-design-reference/
- Eric Evans, *Whirlpool Process*: https://www.domainlanguage.com/ddd/whirlpool/
- Alberto Brandolini, *Strategic Domain-Driven Design with Context Mapping*: https://www.infoq.com/articles/ddd-contextmapping/
- Philippe Bourgau, *How to use Event Storming to introduce DDD*: https://philippe.bourgau.net/how-to-use-event-storming-to-introduce-domain-driven-design/
