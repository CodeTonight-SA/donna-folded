#!/usr/bin/env bash
# HAL.md — donna-folded routing layer (skeleton, v0.0.1, May 2026)
# Polyglot: valid Markdown · executable Bash · embedded Python runtime · JSON envelope
# Pattern inherited from happi.md/1.1.
#
# Status: SKELETON for the fork-experiment scaffolding. The full routing layer
# (MCP server dispatch + provider chain) sources from mcp-servers/donna/src/server.ts
# and lib/docuseal.py — both already syscall-doctrine compliant.

set -euo pipefail

SELF="${BASH_SOURCE[0]:-$0}"
HERE="$(cd "$(dirname "$SELF")" && pwd)"
CMD="${1:-help}"

case "$CMD" in
  verify)
    bash -n "$SELF" >/dev/null
    head -1 "$SELF" | grep -q "^#!/usr/bin/env bash"
    grep -q "^# Polyglot:" "$SELF"
    grep -q "^: <<'MARKDOWN_BEGIN'" "$SELF"
    echo "[HAL.md verify] polyglot envelope OK · routing layer skeleton intact"
    ;;

  tools)
    # The MCP routing surface — five tools.
    cat <<'TOOLS'
[HAL.md tools] DONNA's MCP routing surface (sourced from mcp-servers/donna/src/server.ts):
  donna_analyse   Analyse a legal document — clauses, risks, obligations
  donna_draft     Draft a response, motion, brief, redline
  donna_review    Review a draft against the firm's house style + risk profile
  donna_export    Export an IDR chain segment to regulator-ready JSON / CSV
  donna_sign      Sign an IDR via DocuSeal + emit an HMAC-SHA256 chain entry

  Transport: streamable HTTP MCP, port DONNA_PORT (default 3102)
  Auth: bearer token (DONNA_AUTH_TOKEN env var)
TOOLS
    ;;

  providers)
    # The provider chain for the analysis/draft/review path
    cat <<'PROVIDERS'
[HAL.md providers] Provider chain for the analytical tools:
  Cloud:   Anthropic Claude · OpenAI GPT · Google Gemini · xAI Grok
  Self:    Ollama (qwen2.5, llama3.1) · vLLM (production self-host)
  Routing: HAL Council multi-model verification for high-confidence decisions

  Signing-path provider (donna_sign):
  Primary:  DocuSeal (lib/docuseal.py syscall shim — keychain entry grip-docuseal)
  Fallback: mock_provider (lib/mock_provider.py — test mode only)
PROVIDERS
    ;;

  route)
    # SKELETON — full routing delegates to mcp-servers/donna/src/server.ts via MCP
    echo "[HAL.md route] SKELETON — intent → provider routing not yet wired here"
    echo "[HAL.md route] Target: route(intent) → (tool, provider, params) tuple"
    echo "[HAL.md route] Idempotence: route(route(intent)) == route(intent) per H474 pattern"
    ;;

  mcp)
    # Start the MCP server if the upstream node module is installed
    if [ -d "$HERE/mcp-servers/donna" ] && [ -f "$HERE/mcp-servers/donna/package.json" ]; then
      echo "[HAL.md mcp] MCP server present at mcp-servers/donna/"
      echo "[HAL.md mcp] Start with: cd mcp-servers/donna && npm install && npm start"
    else
      echo "[HAL.md mcp] MCP server not installed locally yet"
    fi
    ;;

  help|*)
    cat <<'HELP'
HAL.md — the donna-folded routing layer (v0.0.1 skeleton)

Commands:
  bash HAL.md verify        Polyglot envelope self-check
  bash HAL.md tools         List DONNA's five MCP tools
  bash HAL.md providers     List provider chain (analytical + signing)
  bash HAL.md route         Dispatch intent to tool/provider (skeleton)
  bash HAL.md mcp           Start the MCP server (if installed)
  bash HAL.md help          This message

Sibling files (the four-doc fold):
  GRIP.md     — substrate (the notarise verb, the donna skill)
  happi.md    — transport (IDR protocol at v1.1)
  context.md  — operator state (firm + matter + signer)

See FOLD.md for the experiment plan and the six pre-registered hypotheses.
HELP
    ;;
esac

exit 0

: <<'MARKDOWN_BEGIN'

# HAL.md — donna-folded routing layer

> The mouth. The polyglot router that dispatches an intent to the right tool,
> the right provider, the right model — and never lets the call site see a
> provider token.

## The routing surface

DONNA exposes five MCP tools, mapped one-to-one onto the verbs an attorney
would use during a working day:

| Tool | What it does | Provider chain |
|------|-------------|----------------|
| `donna_analyse` | Read a legal document, surface clauses + risks + obligations | Cloud (Claude / Gemini / GPT) → self-host Ollama |
| `donna_draft` | Produce a draft response / motion / brief / redline | Cloud → self-host |
| `donna_review` | Review a draft against the firm's house style + risk profile | Cloud → self-host |
| `donna_export` | Export an IDR chain segment in regulator-ready JSON or CSV | local (no model needed) |
| `donna_sign` | Sign an IDR through DocuSeal + emit a chained HMAC-SHA256 entry | DocuSeal API (lib/docuseal.py shim) |

The MCP server (`mcp-servers/donna/src/server.ts`) is the call-site
boundary. Every external surface (Anthropic, OpenAI, Google, DocuSeal, the
firm's filesystem, the firm's calendar) sits behind one of these tools.

## Why polyglot for the router

A router file that's also Markdown means the routing table can be edited
by humans without breaking the bash entry point. The same bytes are
operator-readable, machine-runnable, and machine-parseable.

## Hypothesis registration

Per the upstream four-doc-fold council's H474 family — the routing operator
must be idempotent under identical input and identical sentinel state. The
donna-folded routing operator is tested for this property in
`tests/test_fold.py::test_route_idempotence` (skeleton — awaiting V>>'s
5-delegation pick).

## What this file is NOT

This file does NOT replace `mcp-servers/donna/src/server.ts` in the fork.
It is the *kernel projection* of the routing layer — the minimum bytes that
expose DONNA's tool surface without depending on the npm node_modules tree.
That property is what makes the fork portable to a fresh machine.

## Anti-vendor-lock-in by construction

The routing operator never references a vendor token directly. Tokens come
from the OS keychain via `security find-generic-password` (macOS) or
`secret-tool lookup` (Linux). The call site sees a typed dict, never a
string starting with `sk_...` or `gho_...`. That is the syscall doctrine in
practice.

MARKDOWN_BEGIN
