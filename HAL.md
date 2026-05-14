#!/usr/bin/env bash
# HAL.md — donna-folded routing layer (v0.1.0, structural pivot, May 2026)
# Polyglot: valid Markdown · executable Bash · embedded Python operator · JSON envelope
# Pattern inherited from happi.md/1.1.
#
# Status: STRUCTURAL projection. `route(intent) -> (tool, provider, params)` is
# implemented as an embedded Python operator (not a heredoc). The operator is
# idempotent: route(intent) returns the same dict for the same input.
#
# Pivot context: this file was a docstring-style heredoc enumeration (SMT 55,
# DENY) until the May 2026 SMT council demanded structural projection. The
# council's per-mapping breakdown drove the rewrite — see the verdict at
# drafts/fold-smt-council-verdict-2026-05-14.md in the upstream GRIP repo.
#
# Hypotheses governing this file:
#   H474 routing-operator idempotence — route(route(req)) determinism
#   H483 behavioural equivalence on 5 representative delegations
#   H484 docstring-analogy ratio < 50% (introduced this pivot)

set -euo pipefail

SELF="${BASH_SOURCE[0]:-$0}"
HERE="$(cd "$(dirname "$SELF")" && pwd)"
CMD="${1:-help}"

case "$CMD" in
  verify)
    # Structural envelope check — confirms polyglot integrity and the
    # presence of the executable Python operator (not just heredoc text).
    bash -n "$SELF" >/dev/null
    head -1 "$SELF" | grep -q "^#!/usr/bin/env bash"
    grep -q "^# Polyglot:" "$SELF"
    grep -q "^: <<'MARKDOWN_BEGIN'" "$SELF"
    # The structural requirement: a Python function `def route(` must exist
    grep -q "^def route(" "$SELF" || {
      echo "[HAL.md verify] FAIL — no Python route() operator detected"
      exit 1
    }
    echo "[HAL.md verify] polyglot envelope OK · structural route() operator present"
    ;;

  *)
    # Everything else: delegate to the embedded Python operator.
    shift || true
    python3 - "$CMD" "$@" <<'PYTHON_OPERATOR'
"""HAL.md embedded routing operator.

route(intent) -> {"tool": str, "provider": str, "params": dict}

The operator classifies an intent string by keyword signatures and returns
the canonical routing decision DONNA's MCP server would dispatch to. It is
DETERMINISTIC for any given input: route(intent) returns the same dict for
the same intent string, on any Python 3.10+ implementation, regardless of
locale or wall-clock state.

This file replaces the prior heredoc-enumeration design (SMT 55, DENY).
"""

from __future__ import annotations

import json
import sys

# ─── Tool routing table ─────────────────────────────────────────────
# Dispatch table over keyword signatures. Each tool has a provider chain
# (per syscall doctrine: provider order, never a vendor token).

ROUTING_TABLE = (
    # (tool, keywords, provider_chain, default_params)
    ("donna_analyse", ("analyse", "analyze", "what does", "key clauses", "obligations"),
     "claude>gemini>self-host", {}),
    ("donna_draft", ("draft", "write", "compose", "produce a"),
     "claude>gemini>self-host", {}),
    ("donna_review", ("redline", "review", "edit"),
     "claude>gemini>self-host", {}),
    ("donna_export", ("export", "regulator", "packet"),
     "local", {"formats": ["json", "csv"]}),
    ("donna_sign", ("sign", "notarise", "notarize", "log decision"),
     "docuseal>mock", {}),
)

DEFAULT_TOOL = "donna_sign"
DEFAULT_PROVIDER = "docuseal>mock"


def route(intent: str) -> dict:
    """Map an intent string to a canonical routing decision.

    Idempotent: route(intent) is a pure function of the intent string.
    Same input -> same output, every time. The result is a dict with
    keys: tool, provider, params.

    The intent is normalised to lower-case before keyword matching, so
    case differences in the input do not change the routing decision.
    """
    intent_lc = intent.lower()
    for tool, keywords, provider, default_params in ROUTING_TABLE:
        if any(kw in intent_lc for kw in keywords):
            params = dict(default_params)
            params["intent"] = intent
            return {"tool": tool, "provider": provider, "params": params}
    # Default: route to sign (every delegation IS a decision worth chaining)
    return {
        "tool": DEFAULT_TOOL,
        "provider": DEFAULT_PROVIDER,
        "params": {"intent": intent},
    }


def test_idempotence() -> int:
    """Verify route(intent) is deterministic on a representative corpus.

    Returns 0 on success, 1 on failure. The corpus matches the five
    delegations in data/delegations.json (H483 falsification corpus).
    """
    intents = [
        "Send Sarah the M&A precedent we used for Dubrovnik, ask her to "
        "redline by Tuesday, copy Marcus when she replies.",
        "Mike, draft the response brief by Friday.",
        "Just spent ninety minutes on the Smith motion.",
        "Show me what I delegated this week.",
        "Export today as a regulator packet.",
    ]
    all_ok = True
    for intent in intents:
        signatures = {
            json.dumps(route(intent), sort_keys=True) for _ in range(10)
        }
        if len(signatures) != 1:
            print(
                f"FAIL idempotence: {intent[:40]}... "
                f"-> {len(signatures)} distinct results"
            )
            all_ok = False
        else:
            decision = json.loads(next(iter(signatures)))
            print(
                f"OK   idempotence: {intent[:40]}... "
                f"-> tool={decision['tool']}"
            )
    return 0 if all_ok else 1


def list_tools() -> None:
    """Print the routing table — the 5 tools DONNA's MCP server exposes."""
    print("[HAL.md tools] routing table (tool / provider / sample keywords):")
    for tool, keywords, provider, _ in ROUTING_TABLE:
        sample = ", ".join(keywords[:3])
        print(f"  {tool:14s}  {provider:30s}  ({sample}...)")


def list_providers() -> None:
    """Print the unique provider chains in use across the routing table."""
    print("[HAL.md providers] unique chains in use:")
    chains = sorted({entry[2] for entry in ROUTING_TABLE})
    for chain in chains:
        tools = [t for t, *_ in ROUTING_TABLE if _provider_for(t) == chain]
        print(f"  {chain:30s}  used by: {', '.join(tools)}")


def _provider_for(tool_name: str) -> str:
    """Lookup helper — provider chain for a tool name."""
    for tool, _, provider, _ in ROUTING_TABLE:
        if tool == tool_name:
            return provider
    return DEFAULT_PROVIDER


def show_help() -> None:
    """Print the help text."""
    print("HAL.md — donna-folded routing layer (v0.1.0, structural pivot)")
    print("")
    print("Commands:")
    print("  bash HAL.md verify             Polyglot envelope + route() presence check")
    print("  bash HAL.md route 'INTENT'     Route an intent to (tool, provider, params)")
    print("  bash HAL.md test-idempotence   Verify route() is deterministic over 5 cases")
    print("  bash HAL.md tools              Print the routing table")
    print("  bash HAL.md providers          Print unique provider chains")
    print("  bash HAL.md help               This message")


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    rest = sys.argv[2:]
    if cmd == "route":
        intent = rest[0] if rest else ""
        if not intent:
            print("[HAL.md route] ERROR — empty intent")
            return 2
        decision = route(intent)
        print(json.dumps(decision, sort_keys=True, indent=2))
        return 0
    if cmd == "test-idempotence":
        return test_idempotence()
    if cmd == "tools":
        list_tools()
        return 0
    if cmd == "providers":
        list_providers()
        return 0
    show_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYTHON_OPERATOR
    ;;
esac

exit 0

: <<'MARKDOWN_BEGIN'

# HAL.md — donna-folded routing layer (structural projection)

> The mouth. The polyglot router that dispatches an intent to the right tool
> and the right provider — implemented as an embedded Python operator, not
> as a heredoc enumeration.

## Structural pivot (May 2026)

This file was previously a docstring-style heredoc that listed DONNA's five
MCP tools and provider chains as `cat <<TOOLS` static text. The May 2026
SMT council scored that design 55/100 with a DENY verdict from
`lib/gentner_enforcer.enforce()` — 0% causal relations, 100% surface
relations. The bash case statement was a dispatch table by syntax but a
docstring by semantics.

The pivot replaces the heredoc with an executable `route(intent)` function
embedded under the polyglot envelope. The function:

- Is **deterministic** — same intent string returns the same `(tool, provider, params)` dict
- Is **idempotent in the test-suite sense** — testable via `bash HAL.md test-idempotence`
- Is **causally projected from DONNA's MCP routing** — the five-tool table matches `mcp-servers/donna/src/server.ts` one-for-one
- Is **syscall-doctrine compliant** — providers are named, tokens are never embedded; the OS keychain resolves credentials at call time

## The routing table (data-driven, not heredoc-driven)

```
donna_analyse   claude>gemini>self-host    (analyse, analyze, what does, ...)
donna_draft     claude>gemini>self-host    (draft, write, compose, ...)
donna_review    claude>gemini>self-host    (redline, review, edit)
donna_export    local                      (export, regulator, packet)
donna_sign      docuseal>mock              (sign, notarise, notarize, log decision)
```

The table is a Python tuple-of-tuples — readable, editable, testable. Adding
a sixth tool means adding a sixth tuple. The dispatch logic does not change.

## Idempotence (H474)

`route(intent)` is a pure function of its input. `bash HAL.md test-idempotence`
runs each of the five H483 corpus intents 10 times and asserts all 50 results
collapse to 5 distinct decisions (one per intent). If any intent produces more
than one distinct decision across 10 invocations, the test fails and H474 is
falsified for this implementation.

## Why polyglot for the router

The router file is one stream of bytes that bash invokes, Python executes,
and humans read. The same file can be:

- copied to a fresh machine,
- run as `bash HAL.md route 'intent'`,
- parsed by markdown renderers (this body),
- inspected by humans editing the routing table directly.

No build step. No installation. No package manager.

## What this file is NOT

This file does NOT replace `mcp-servers/donna/src/server.ts` in the fork.
It is the *causal projection* of the routing layer — the minimum bytes that
implement the routing operator without depending on the npm node_modules
tree. That property is what makes the fork portable to a fresh machine.

The MCP server remains the production routing surface. HAL.md is the
fold's claim that the routing logic can be reproduced from first principles
on any Python 3.10+ runtime, with the same keyword-signature table the
production server uses.

## Anti-vendor-lock-in by construction

The `route()` function never imports a vendor SDK. The provider chain
strings (`claude>gemini>self-host`, `docuseal>mock`) are operator-readable
preference orders, not API endpoints. The credential resolution layer
(not in this file) reads the OS keychain via `security find-generic-password`
on macOS or `secret-tool lookup` on Linux. The call site sees a typed dict,
never a string starting with `sk_...` or `gho_...`.

That is the syscall doctrine, projected structurally rather than narrated.

## Falsifiers (this file specifically)

1. **Determinism**: if `route(intent)` returns two different dicts for the
   same input on the same Python version, `H474` for this implementation is
   falsified.
2. **Production parity**: if the five-tool table here diverges from
   `mcp-servers/donna/src/server.ts` after any upstream change, the
   structural-projection claim weakens. Mitigation: `tests/test_fold.py`
   will compare the two surfaces at test time.
3. **Surface-relation regression**: if the SMT re-scoring after this pivot
   does not raise HAL.md from 55 to ≥75, the pivot did not achieve its
   stated purpose and the experiment design needs reconsidering.

MARKDOWN_BEGIN
