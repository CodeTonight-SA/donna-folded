# LEGAL-PROVENANCE.md — proof you can hand a judge

> *DONNA probat.* The audit chain ([`PROBAT.md`](PROBAT.md)) proves what DONNA
> **decided**. This file is about the other half: proving what DONNA **cited**.

A legal citation is only safe to rely on if the words you attribute to a statute
or a judgment are actually there — and if they actually say what you cite them
for. Those are two different questions, and DONNA answers them with two different
mechanisms, because only one of them is arithmetic.

The open reference implementation of everything below is
**[github.com/CodeTonight-SA/grasp](https://github.com/CodeTonight-SA/grasp)**
(AGPL-3.0) — `cite_verify`, `prove_it`, `legal_receipt`, `idr`. This document is
DONNA's plain-English account of the two layers and the honesty boundary between
them.

---

## The two layers

### Layer 1 — the floor: *is the quote real?*

Deterministic. A quoted passage is in its cited source, or it is not — there is
no "probably". Layer 1 matches every cited quote, verbatim, against the source
document (whitespace and typography are tolerated; words never are). A fabricated
quote renders **NOT FOUND**, and the filing gate refuses: `legal_receipt` exits
non-zero on any not-found citation. *Never file a red.* This is the same
arithmetic as `cite.verify` in [`happi.md`](happi.md) — an open protocol check
any model, on any harness, can reproduce.

Layer 1 catches the error that has already sanctioned lawyers: the
**invented citation** (*Mata v Avianca*, S.D.N.Y. 2023 — six AI-hallucinated
cases in a filed brief). A hallucinated authority cannot earn a green badge,
because its words are not in the record.

### Layer 2 — the council: *does the real quote support the claim?*

Judgement, not arithmetic — so DONNA does not fake it with a number. A citation
can be **100% verbatim-real and still wrong**: a real quote lifted out of
context, cited for a proposition it does not bear, or the exact opposite of what
it says. Layer 2 sends each *(claim, quote)* pair to a panel of **external
models that did not draft the memo** — deliberately independent — each voting on
whether the quote supports the claim, with a separate judge.

Layer 2 is **advisory and monotone toward doubt**: it can flag a real quote as
unsupported for attorney review, but it **never overrides the Layer-1 floor**,
and a not-found quote is never even reviewed (the floor already refused it). If
the external panel is unreachable, it fails open — the receipt still files on the
floor. The panel adds doubt; it cannot manufacture confidence.

---

## The flagship — a real quote, wrong job (*Donoghue v Stevenson* [1932])

We proved Layer 2 on the most famous case in the common law — the snail in the
ginger-beer bottle, the birth of the modern law of negligence — using the real
House of Lords judgment. A memo cites four genuine passages; **every quote is
verbatim-real, so it is SAFE TO FILE on the floor.** But two are misused, and the
external panel caught both:

| Citation | The real, verbatim quote | Cited for the claim… | External panel |
|----------|--------------------------|----------------------|----------------|
| `m1` | Lord Atkin's neighbour principle | …a duty is owed to those closely and directly affected | **supported** ✓ |
| `m2` | Lord Atkin's ratio: a manufacturer owes a duty to take *"reasonable care"* | …liability is **absolute**, independent of negligence | **unsupported** — the words say the opposite |
| `m3` | Lord Macmillan: *"the categories of negligence are never closed"* | …the categories are **fixed and closed** | **unsupported** — cited to mean its own opposite |

Three external, non-Anthropic models (Llama 3.3 70B, Qwen3 32B, Llama 4 Scout,
via [HAL](HAL.md)) independently flagged `m2` and `m3`. The floor still files —
the quotes are all real — but the receipt raises **"attorney review required"**
on the two real citations used for claims they do not bear. That is the second
leg of the moat: a citation machine that catches not only invented law, but real
law used dishonestly.

---

## What it deliberately does NOT do

Stated plainly, because honesty is the product:

- It does **not** prove the source is real, current, or good law — feed it a
  fabricated judgment and a quote from that fabrication still verifies. Source
  authenticity is the lawyer's.
- It does **not** prove the quote is the *best* authority.
- Layer 2 is a fallible second opinion, never a gate.

What the two layers remove is the pair of errors that are invisible in fluent
prose and indefensible in front of a judge: **invented citations** (Layer 1) and
**real citations used for claims they do not support** (Layer 2). The lawyer
keeps the lawyering.

---

## How this sits in DONNA's substrate

The moat is one idea — **cryptographic causation** — with three legs, and DONNA
already carries all three:

| Leg | What it records | Where |
|-----|-----------------|-------|
| **Decision** | what DONNA decided (signed, hash-chained IDRs) | [`PROBAT.md`](PROBAT.md) · [`bin/notarise`](bin/notarise) |
| **Convergence** | the fixed-point kernel every loop reduces to | [`FOLD.md`](FOLD.md) |
| **Citation** | that every quoted authority is real (Layer 1) and reviewed (Layer 2) | this file · reference impl in [GRASP](https://github.com/CodeTonight-SA/grasp) |

`cite.verify` is specified at protocol level in [`happi.md`](happi.md), so the
Layer-1 floor is model-independent — the same un-fakeable check holds whichever
model drafted the words. Provability is a property of the substrate, not of one
model.

---

## Replay it

Do not trust this document. Run the reference implementation:

```bash
# clone the open reference implementation (AGPL-3.0)
git clone https://github.com/CodeTonight-SA/grasp && cd grasp

# Layer 1 — the deterministic floor: a fabricated quote renders NOT FOUND
python3 -m grasp.legal_receipt <spec-with-a-fabrication>.json   # exit 1, DO NOT FILE
```

The floor is arithmetic; you can reproduce it byte-for-byte. Layer 2's verdicts
depend on live external models, so they are recorded with the providers that
voted, at the time they voted — a fallible second opinion, honestly labelled.

> *No claim without a record. No adjective without a measurement.*
