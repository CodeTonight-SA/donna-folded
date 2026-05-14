#!/usr/bin/env bash
# GRIP.md — donna-folded substrate (skeleton, v0.0.1, May 2026)
# Polyglot: valid Markdown · executable Bash · embedded Python runtime · JSON envelope
# Pattern inherited from happi.md/1.1 (chiefofstaff-legal/donna · public spec).
#
# Status: SKELETON for the fork-experiment scaffolding. The full fold of DONNA's
# substrate (bin/notarise + donna-skill/SKILL.md + dispatch table + skills/) into
# this single polyglot file is the experimental work this scaffolding gates.
#
# Hypotheses governing the fork experiment (registered May 2026, deadline 2026-06-13):
#   H478 — donna-folded preserves DONNA test-suite pass rate (>=0.95)
#   H479 — cold-start <=60s on a fresh machine (bash + python3 only)
#   H480 — preserves IDR sha256-chain round-trip integrity (=1.0)
#   H481 — kernel layers (GRIP+HAL+context) total <=100kB
#   H482 — load-bearing file count reduction >=90%
#   H483 — behavioural equivalence on >=4 of 5 representative delegations

set -euo pipefail

SELF="${BASH_SOURCE[0]:-$0}"
HERE="$(cd "$(dirname "$SELF")" && pwd)"
CMD="${1:-help}"

case "$CMD" in
  verify)
    # Polyglot envelope self-check
    bash -n "$SELF" >/dev/null
    head -1 "$SELF" | grep -q "^#!/usr/bin/env bash"
    grep -q "^# Polyglot:" "$SELF"
    grep -q "^: <<'MARKDOWN_BEGIN'" "$SELF"
    echo "[GRIP.md verify] polyglot envelope OK · bash parseable · markdown frontmatter intact"
    ;;

  notarise)
    # The substrate verb. Delegates to bin/notarise (the upstream primitive).
    if [ -x "$HERE/bin/notarise" ]; then
      shift || true
      exec "$HERE/bin/notarise" "$@"
    else
      echo "[GRIP.md notarise] bin/notarise not present — falling back to skeleton response"
      echo "Target: GRIP.md notarise --intent '...' --signer '...' --previous-hash <sha>"
      exit 2
    fi
    ;;

  skill)
    # Inventory the substrate skills folded into this kernel.
    echo "[GRIP.md skill] folded surfaces (upstream sources):"
    [ -f "$HERE/donna-skill/SKILL.md" ] && echo "  · donna-skill/SKILL.md ($(wc -l < "$HERE/donna-skill/SKILL.md") lines)"
    [ -d "$HERE/skills/donna" ] && echo "  · skills/donna/ ($(find "$HERE/skills/donna" -type f | wc -l | tr -d ' ') files)"
    [ -f "$HERE/PROBAT.md" ] && echo "  · PROBAT.md (the live IDR chain demonstration)"
    ;;

  bootstrap)
    # SKELETON — full bootstrap will fold the substrate into self-contained Python
    echo "[GRIP.md bootstrap] SKELETON — substrate fold not yet performed"
    echo "[GRIP.md bootstrap] Target: <=60s cold start on bash + python3 only (H479)"
    echo "[GRIP.md bootstrap] See FOLD.md for the experiment plan + measurement methodology"
    ;;

  run)
    # SKELETON — runtime composition with HAL.md + happi.md + context.md
    echo "[GRIP.md run] SKELETON — composition with HAL.md + happi.md + context.md not yet wired"
    echo "[GRIP.md run] Target: bash GRIP.md run --hal HAL.md --transport happi.md --context context.md"
    ;;

  help|*)
    cat <<'HELP'
GRIP.md — the donna-folded substrate (v0.0.1 skeleton)

Commands:
  bash GRIP.md verify       Polyglot envelope self-check
  bash GRIP.md notarise     Delegate to bin/notarise (the IDR primitive)
  bash GRIP.md skill        Inventory the substrate skills folded in
  bash GRIP.md bootstrap    Load the folded substrate (not yet implemented)
  bash GRIP.md run          Compose with HAL.md + happi.md + context.md
  bash GRIP.md help         This message

Sibling files (the four-doc fold):
  HAL.md      — routing layer (MCP server contract + provider dispatch)
  happi.md    — transport shim (the IDR protocol at v1.1)
  context.md  — operator state (firm config + matter context + signer identity)

See FOLD.md for the fork-experiment plan, six observable measurements,
and the six pre-registered falsification hypotheses (H478-H483).
HELP
    ;;
esac

exit 0

: <<'MARKDOWN_BEGIN'

# GRIP.md — donna-folded substrate

> The discipline. The polyglot kernel that compresses DONNA's substrate
> primitives — the `notarise` verb, the `donna` skill, the IDR audit chain,
> the dispatch tables — into one self-contained executable Markdown file.

## What folds in

DONNA's substrate is already strikingly compact because the codebase was
designed with the syscall doctrine in mind. Four primitives carry the
discipline:

| Upstream source | Role | Folded into |
|-----------------|------|-------------|
| `bin/notarise` | IDR sign/verify CLI (HMAC-SHA256, chained) | GRIP.md command dispatch |
| `donna-skill/SKILL.md` | The /donna skill spec (delegation, time-entry, query, export) | GRIP.md skill section |
| `PROBAT.md` | Live IDR chain demonstration at the repo root | Referenced as proof |
| `tests/test_notarise.py` + `test_donna_skill_scaffold.py` | The regression harness | tests/test_fold.py extension |

Per H481, the folded GRIP.md target size is under 50kB. The current
skeleton sits well under that — the actual fold happens when the substrate
primitives are inlined as Python heredocs and the dispatch table is
compressed.

## Why polyglot

A polyglot file is one stream of bytes that multiple parsers can read
without conflict. This file is:

- a valid **Markdown** document (this body is in a heredoc terminator)
- an executable **Bash** script (the top section)
- an embedded **Python** runtime can be added under the same envelope
- a **JSON** envelope of its own metadata (planned `bash GRIP.md json`)

That property is the empirical claim being measured: the same bytes work
across four parsers, and the file is self-bootstrappable on any machine
with bash + python3.

## Self-check

Run `bash GRIP.md verify`. Three checks must pass:

1. `bash -n` parses the bash script without error
2. The shebang is `#!/usr/bin/env bash`
3. The polyglot marker comment is present
4. The markdown heredoc terminator is intact

If any check fails, the fold has corrupted the envelope and the experiment
is falsified for this file (H478 sub-clause).

## Banach fixed-point property

The fold operator `ℱ` is a contraction mapping in the syntactic sense:
running the compactor on an already-folded GRIP.md returns the same bytes.
`ℱ(ℱ(x)) = ℱ(x)`. The Banach fixed-point theorem guarantees convergence
when iterating from any starting state — the same property `fold_search.py`
demonstrates at the discovery layer.

## What this is NOT

This file does NOT replace `bin/notarise` or `donna-skill/SKILL.md` in the
fork. It is the *kernel projection* of those primitives — the minimal set
of bytes that, plus the remote substrate (chiefofstaff-legal/donna), can
reconstitute the operating system of DONNA on a fresh machine.

The experiment measures whether that reconstitution preserves the six
observables (H478-H483). If it does, the fold pattern generalises beyond
GRIP itself and into legal-tech production code. If it doesn't, the
falsification is the deliverable and the lesson is preserved.

## Pointer to the canonical fold research

See the upstream GRIP repo:
- `drafts/fold-the-kernel-whitepaper-final-2026-05-07.tex` — full whitepaper
- `drafts/fold-the-kernel-hypotheses-2026-05-06.md` — H-FOLD-1..H-FOLD-11
- `drafts/four-doc-fold-broly-council-verdict-2026-05-14.md` — PROCEED verdict
- `drafts/fold-classification-audit-2026-05-14.md` — 99.6% surface reduction

MARKDOWN_BEGIN
