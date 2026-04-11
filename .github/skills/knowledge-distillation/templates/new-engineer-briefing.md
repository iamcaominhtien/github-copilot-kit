# New Engineer Briefing

**Project**: [Project Name]  
**Written by**: [Your Name]  
**Date**: [YYYY-MM-DD]

> This briefing contains the 5 things you must know before making your first change to this codebase. Everything here was non-obvious and was learned through systematic distillation, not casual reading.

---

## 1. The Core Abstraction Everything Depends On

**What it is**: [Name of the abstraction — class, interface, concept]

**Where to find it**: `[path/to/file]`

**Why it matters**: [1–2 sentences on why this is the load-bearing center of the codebase. What would break if you got this wrong.]

**Common mistake**: [The thing people do when they don't understand this abstraction]

---

## 2. The Most Non-Obvious Naming Decision

**The name**: `[ClassName / methodName / directoryName]`

**What it actually means**: [Plain-language explanation — not what the name suggests, but what it actually does]

**Why the name is misleading / unusual**: [Historical reason, or domain reason that's not obvious from the outside]

**Where the confusion bites**: [Where you would make a bug if you misunderstood the name]

---

## 3. The Most Dangerous File or Module

**Location**: `[path/to/dangerous/module]`

**Why it's dangerous**: [What makes this module high-risk. Complexity? Lack of tests? Many callers? Critical invariant? Concurrency issues?]

**Warning signal**: [The sign that you're about to make a mistake here]

**Protocol before changing**: [What to do before touching this — ask X, read Y, verify Z]

---

## 4. The Pattern That Catches Experienced Engineers Too

**The pattern**: [Describe the trap — an anti-pattern, a non-obvious convention, an exception to a rule]

**Why it's easy to get wrong**: [Why even experienced engineers fall for this]

**How to avoid it**: [The safe approach]

**Example**: [Optional: a concrete case where this pattern caused a problem]

---

## 5. The Invariant That Breaks Silently

**The invariant**: [The business rule]

**Where it's enforced**: `[path/to/enforcement]`

**Where it's NOT enforced** (but assumed): [The places that assume the invariant holds without checking]

**What failure looks like**: [The symptom of violation — note that this may be delayed, data corruption, or appear in an unrelated part of the system]

**How to protect it**: [The safe pattern for code that touches this area]

---

## Quick-Reference Contacts

| Question | Who to Ask |
|---|---|
| Business domain / requirements | [Name / channel] |
| Architecture decisions | [Name / channel] |
| [Specific module] | [Name / channel] |
| Deployment / infra | [Name / channel] |

---

*Produced via the [Knowledge Distillation skill](../../.github/skills/knowledge-distillation/SKILL.md). Read the [Soul Document](./soul-document.md) for deeper context.*
