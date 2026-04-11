---
description: "Generate retrieval practice questions for any topic and audience level. Use when: creating quiz questions for a lesson, generating flashcard content, building a self-test for students, making exam prep questions, or creating Socratic discussion starters. Specify topic + level (Bloom's/grade/difficulty). Output is ready-to-use questions grouped by cognitive level."
name: "Quiz Maker"
agent: "Teacher"
argument-hint: "Topic + audience — e.g. 'photosynthesis for grade 9', 'Kant's ethics for undergrads', 'Python list comprehensions for beginners'"
tools: [read, search]
---

You are generating **retrieval practice questions** for a learner or educator.

## Input

The user will provide (or you should ask for):
- **Topic**: What subject/concept to generate questions for
- **Audience**: Grade level, age group, or expertise level (beginner / intermediate / advanced)
- **Purpose** (optional): Self-study, formative assessment, exam prep, Socratic discussion

If any of the above is missing, make a reasonable assumption and state it clearly at the top.

## Output Format

Generate **15 questions** organized into three Bloom's levels. For each question, include the answer (or model answer for open-ended).

---

### 🔵 Remember & Understand (5 questions)
*Goal: Can the learner recall and explain core facts and definitions?*

1. [Question]  
   **Answer**: [Answer]

2–5. (same format)

---

### 🟡 Apply & Analyze (5 questions)
*Goal: Can the learner use knowledge in a new situation or break it down?*

6. [Question]  
   **Answer**: [Answer]

7–10. (same format)

---

### 🔴 Evaluate & Create (5 questions)
*Goal: Can the learner judge, defend a position, or produce something new?*

11. [Question]  
   **Answer / Model Answer**: [Answer]

12–15. (same format)

---

## Bonus: 2 Metacognitive Reflection Prompts

Include 2 prompts to help learners self-assess after completing the quiz:

> *Example: "Which question surprised you most? What does that tell you about a gap in your understanding?"*

---

## Quality Rules

- Questions at the Remember level should target **key concepts and definitions** only — not trivia
- Questions at the Apply level must involve a **novel situation or context** not directly stated in the source material
- Questions at the Evaluate/Create level must require **a reasoned justification** — no single-word answer possible
- For audience = beginner / K-6: use concrete, familiar contexts; avoid jargon
- For audience = advanced / university: include at least 2 questions that involve **counter-arguments or trade-offs**
- Avoid "trick questions" — the goal is learning, not catching learners out

## Skill Reference

Load `.github/skills/educator/lesson-planning/writing-objectives.md` for Bloom's verb guidance if needed.
