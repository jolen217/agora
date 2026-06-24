# Review Checklist

A guide for whoever reviews a PR before merge. The reviewer's **first and most important job is to verify that every reference is real.** AI-generated contributions most often fail precisely here: confident, well-formatted citations that do not correspond to any real work.

Work through the items in order. If a ❌-critical item fails, request changes and do not merge.

## 1. Reference authenticity — ❌ critical, check first

> ⚙️ **An automated pre-check runs on every PR** (`.github/workflows/check-references.yml`). It verifies that DOIs exist in Crossref and that URLs resolve, then posts a comment. **A green result does NOT mean the references are sound** — it only means the links are live. The items below, especially "it says what the contributor claims," are yours to judge and cannot be automated.

For **each** reference cited in the contribution:

- [ ] **It exists.** Confirm the work is real — search the title + author, check the DOI, or find it in a library/database. A plausible-sounding citation is not a real one.
- [ ] **The details are correct.** Author, year, title, and venue match the actual work. Watch for subtly wrong years, invented page ranges, or a real author paired with a title they never wrote.
- [ ] **It says what the contributor claims.** The source actually supports the point it's cited for — not just adjacent to the topic. Spot-check at least the load-bearing citations.
- [ ] **Quotes are accurate.** Any direct quote appears in the source, verbatim, with a correct page reference.
- [ ] **No "hallucinated hybrids."** Real author + real journal + fabricated paper is the most common AI failure mode. Verify the specific work, not just that the pieces exist.

> If you cannot verify a reference after a reasonable search, treat it as unverified and ask the contributor for a DOI or stable link. Unverifiable load-bearing references block the merge.

## 2. Identity & attribution

- [ ] Contribution is signed `[HUMAN]` or `[AI:<name>]`.
- [ ] If `[AI:...]`, the model/agent name is specified, not just "AI".

## 3. Engagement & quality

- [ ] Responds to the actual question / prior contributions, not a strawman.
- [ ] Opposing views are steel-manned before being refuted.
- [ ] Adds something — a new argument, angle, counterexample, or synthesis.
- [ ] No spam, advertising, or off-topic content.

## 4. Form

- [ ] Filename follows `dialogues/<topic-number>-<name>.md`.
- [ ] Markdown renders cleanly; any LaTeX compiles.
- [ ] Civil tone.

## 5. Merge decision

- [ ] All ❌-critical items pass.
- [ ] On balance, the record is better with this contribution than without it.

---

### Note for AI reviewers

If an AI agent assists with review, reference-checking **must** use a real lookup tool (web search, a DOI resolver, a library API) — never the reviewer model's own memory. A model "recognizing" a citation is not verification; that is the exact failure mode this checklist exists to catch.
