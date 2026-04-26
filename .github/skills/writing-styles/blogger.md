# Writing Style: Blogger

Source: Paul Graham essays, NN/g UX research, UNC Writing Center, swyx.io.

---

## Core Philosophy

Great blog writing feels like a smart person thinking in public. Not summarizing consensus — *disagreeing with it, testing it, being surprised by it*.

The "human" feel comes from:
1. **Specificity** — real scenes, real trade-offs, real numbers, real failures
2. **Stance** — a non-obvious opinion held with honest confidence
3. **Asymmetry** — some ideas emphasized, others dismissed; not false balance

**The one test for everything:** *"Could this paragraph be about any topic by swapping the nouns?"*
If yes → generic AI filler. Rewrite.

---

## Opening — Front-Load Value, No Throat-Clearing

First 1–3 sentences must do one of:

**A. Contrarian claim:**
> *"Most startup advice on writing is upside down: clarity beats cleverness almost every time."*

**B. Sharp puzzle:**
> *"Why do smart teams ship unreadable docs?"*

**C. Micro-scene:**
> *"I watched a staff engineer scroll past three paragraphs before finding the one line she needed."*

**Banned openers:**
- "In today's fast-paced world..."
- "X is an important topic that many people are thinking about..."
- Any sentence that could open a Wikipedia article

---

## Voice — Sound Like a Person With Skin in the Game

| Weak (AI-generic) | Strong (human opinion) |
|---|---|
| "There are many factors to consider." | "I think most productivity programs fail because they optimize dashboards, not decision latency." |
| "Organizations should evaluate their options carefully." | "Pick the boring tool. You'll thank yourself in year 3." |
| "This approach has both advantages and disadvantages." | "This works — but only until your data grows past 10GB. Then it falls apart fast." |

**"I think" is honest. Use it when uncertainty is real. Never fake certainty. Never fake balance.**

**Paul Graham's 4 requirements for useful writing:**
1. Correct — actually true
2. Novel — not obvious consensus
3. Important — matters to the reader
4. Strength — stated with conviction

---

## Explaining Complex Ideas — Beat the Curse of Knowledge

For every technical term: **Keep** (audience knows it) / **Replace** (simpler is clearer) / **Pair** with plain language in parentheses.

**Before:** "Use event-sourced CQRS with eventual consistency guarantees."
**After:** "Split reads from writes (CQRS), keep a replayable event log, and accept short-lived lag between update and display."

Write for the smart non-specialist. If a 20-year veteran reads faster AND a junior engineer actually understands — you've won.

---

## Personal Anecdote — Use as Evidence, Not Autobiography

**Pattern:**
1. Short scene (1–3 sentences)
2. Generalizable lesson extracted immediately
3. Move on

**Example:**
> *"Last quarter I rewrote our onboarding doc three times and support tickets still rose. The issue wasn't detail — it was sequencing. So now I lead with a 7-line 'what to do first' block."*

Rules: one anecdote per major section max; must reveal a decision, failure, or changed belief.

---

## Humor — Release Tension, Don't Perform

**Irony:** state the gap between intent and reality:
> *"Our 'simple' workflow had 14 required clicks."*

**Self-deprecation:** show you've made the mistake too:
> *"I named the script `final_final_v7`, so you know this was rigorous."*

**Bathos:** lofty claim, mundane punchline:
> *"We deployed a microservices architecture. It solved the latency problem. It created 11 new ones."*

**Callback:** reuse an earlier phrase near the end for payoff.

Rules: humor releases cognitive tension, not performance; one beat per ~500 words; if a joke needs explaining, cut it.

---

## Structure — Two Tracks

**Skim lane** (headers, bullets, bold):
- 3–6 bullet BLUF summary at the top
- Section headers that carry the insight: ❌ "Performance Results" → ✅ "It ran 4× faster, but only in one scenario"
- Bold the key sentence per section

**Deep lane** (prose):
- One idea per paragraph
- After every claim, show the evidence or example
- Short sentence to land each major point. Like this.

---

## Endings — Close the Loop, Then Open a Door

1. **Decision rule:** *"If a paragraph can't survive as a bullet, it's probably still thinking, not writing."*
2. **Loop closure:** return to opening scene, show what changed
3. **Reader challenge:** *"What belief in your team survives mostly because nobody has written against it clearly?"*

Never: summary ending / new point in last paragraph / unearned CTA.

---

## Pre-Publish Humanity Checklist

**Human signals (need ≥4):**
- [ ] Takes a non-obvious stance
- [ ] Shows concrete experience or trade-off
- [ ] Uses precise nouns/verbs — not "robust," "seamless," "leveraging"
- [ ] Admits uncertainty in at least one specific place
- [ ] Some ideas emphasized; others dismissed — not false balance
- [ ] At least one real example, failure, or changed-mind moment

**AI-generic red flags (need 0):**
- [ ] Generic opener ("In today's world...", "X is important because...")
- [ ] Empty intensifiers without mechanism
- [ ] No cost, no downside, no trade-off anywhere
- [ ] Every claim balanced "on the other hand" — no actual take
- [ ] Could be about any topic by swapping the nouns

---

## Hot-Take Box Format

```markdown
> 🔥 **Hot take**: [Non-obvious opinion, stated with conviction]
> 💡 **What actually works**: [Specific, concrete alternative]
> ⚠️ **The thing nobody says**: [The uncomfortable truth]
```

Max one per ~600 words. These should feel earned, not decorative.
