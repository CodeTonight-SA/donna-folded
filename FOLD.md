# FOLD.md — The Fork Experiment

> An empirical test of the four-document polyglot fold on production
> legal-tech code. Pre-registered Popperian falsification. May 2026.

## What this fork is

`CodeTonight-SA/donna-folded` is a fork of `chiefofstaff-legal/donna`
created to answer a single question:

> Can a production legal-tech codebase be reconstituted from four
> polyglot Markdown files — GRIP.md, HAL.md, happi.md, context.md —
> while preserving its tests, its audit chain integrity, its
> behavioural shape, and its cold-start time?

If yes, the fold pattern generalises. If no, the falsification is the
deliverable and the lesson preserves the learning. Either outcome is the
scientific method applied to AI infrastructure.

## Six pre-registered hypotheses

Each is a falsifiable claim, registered via the GRIP `lib/hypothesis_engine.py`
on the same day this scaffolding committed. Deadline: 2026-06-13 (30 days).

| ID | Claim | Falsified if |
|---|---|---|
| **H478** | donna-folded preserves DONNA test-suite pass rate ≥ 95% after the four-doc fold | Any version of the fork's `make test` shows < 95% pass rate against the upstream baseline |
| **H479** | Cold-start ≤ 60 seconds on a fresh machine (bash + python3 only) | `time bash GRIP.md run --hal HAL.md --transport happi.md --context context.md` exceeds 60s on three test machines |
| **H480** | IDR sha256-chain round-trip integrity = 1.0 | Any 1 of 5 representative IDRs fails to verify identically through the folded path vs the upstream baseline |
| **H481** | Kernel layers (GRIP.md + HAL.md + context.md) total ≤ 100 kB | `du -b GRIP.md HAL.md context.md \| awk '{s+=$1} END {print s}'` exceeds 102400 |
| **H482** | Load-bearing file reduction ≥ 90% | The fork after fold has ≥ 10% of upstream's load-bearing file count (excluding tests + retained substrate) |
| **H483** | Behavioural equivalence on ≥ 4 of 5 representative DONNA delegations | Folded path produces non-equivalent output (per sigma_tolerance) on ≥ 2 of the 5 delegations |

The 5 representative delegations are gated on V>>'s pick. Until V>> selects
them, the H483 measurement is inert.

## The six observable measurements (mechanical, not interpretive)

```bash
# (1) Test-suite pass rate (H478)
make test 2>&1 | grep -E "passed|failed" | tail -3

# (2) Cold-start time (H479)
time bash GRIP.md run --hal HAL.md --transport happi.md --context context.md

# (3) IDR round-trip integrity (H480)
python3 tests/test_fold.py --measure idr-roundtrip --count 5

# (4) Kernel byte total (H481)
du -b GRIP.md HAL.md context.md | awk '{s+=$1} END {print "kernel_total_kb=" s/1024}'

# (5) Load-bearing file reduction (H482)
python3 tests/test_fold.py --measure file-reduction --baseline upstream/main

# (6) Behavioural equivalence (H483) — gated on V>>'s 5-delegation pick
python3 tests/test_fold.py --measure delegation-equivalence --delegations delegations.json
```

Each measurement emits a single JSON line to `data/fold-measurements.jsonl`.
A passing measurement does not "win" the experiment — it just fails to
falsify the hypothesis. Confirmation accumulates only over the full set.

## Status of this scaffolding

This commit ships the **structural scaffolding** only:

- ✅ Fork created (`CodeTonight-SA/donna-folded`)
- ✅ `feat/four-doc-fold` branch off `main`
- ✅ Four polyglot files (`GRIP.md`, `HAL.md`, `happi.md`, `context.md`) with self-check
- ✅ This document (`FOLD.md`) with hypotheses + methodology
- ✅ Six hypotheses registered upstream (H478–H483, deadline 2026-06-13)
- ⏳ The actual fold (extracting substrate into the polyglots) — multi-session work
- ⏳ V>>'s pick of 5 representative DONNA delegations (gates H483)
- ⏳ The six measurements executed — gated on V>>'s pick + the fold work

## Why this fork rather than a synthesised demo

Synthesised examples are rhetoric. A fork of real production code is the
empirical test. If the fold breaks on `bin/notarise` or `mcp-servers/donna`,
the failure is visible in production-shape tests, not in a contrived demo.
The constraints (tests must pass, IDR chain must verify, cold-start must
hold) are the same constraints a real adopting firm would care about.

This is the principle V>> calls *facta, non verba* — deeds, not words.

## Anti-vendor-lock-in framing

The folded kernel does not import a vendor SDK. Every external boundary
(LLM provider, signing provider, MCP server) is reached through a syscall
shim. Tokens come from OS keychain via `security find-generic-password`
(macOS) or `secret-tool lookup` (Linux). The call site sees a typed dict,
never a raw string starting with `sk_...` or `gho_...`.

That property — *the model is replaceable, the harness is replaceable,
the brain is yours* — is what the four-doc fold preserves. The fork
experiment measures whether that preservation survives compression.

## What happens if the experiment falsifies

If any of H478–H483 falsifies, the deliverable is:

1. A documented falsification (which hypothesis, what evidence, why)
2. A revision to the four-doc architecture (or a clear rejection)
3. A blog post on `donnaoss.com/blog/` explaining what was learned

Falsification is not failure. It is the protocol working as designed.

## Outside scope of this fork

The fork experiment does not attempt to:

- Build a new legal-AI product (DONNA already exists)
- Compete with Mike or Harvey or Legora (these are siblings, not targets)
- Change DONNA's licensing (AGPL-3.0 stands)
- Add features (the experiment is about compression, not expansion)
- Re-litigate the four-doc architecture (the broly council deliberated;
  the verdict was PROCEED at 4/6, confidence 71)

## Pointer to the upstream research

See the GRIP repo at `~/.claude`:

- `drafts/fold-the-kernel-whitepaper-final-2026-05-07.tex`
- `drafts/fold-the-kernel-hypotheses-2026-05-06.md`
- `drafts/four-doc-fold-broly-council-verdict-2026-05-14.md`
- `drafts/cross-vertical-fold-council-verdict-2026-05-14.md`
- `drafts/fold-classification-audit-2026-05-14.md`
- `drafts/the-fold-tonight-2026-05-14.pdf` (Plain Language + ELI5 explanation)

## Operators

The fork is co-architected by V>> (Laurie Scheepers, CodeTonight) and
reviewed by the AI Craftspeople Guild. Craig Miller is the first review
surface for the DONNA-side work; the Guild is the second review surface
for the four-doc generalisation.

External live-run video reviews — in the spirit of the open-source
legal-AI review tradition — are queued for after the foundational
hypotheses (H-FOLD-1 family) return verdicts on 2026-06-01.

---

*facta, non verba.*
