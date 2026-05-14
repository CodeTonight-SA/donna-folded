#!/usr/bin/env bash
# happi.md — donna-folded transport (reference, May 2026)
# Polyglot: valid Markdown · executable Bash · embedded Python runtime · JSON envelope
#
# This is a thin reference wrapper around the canonical happi.md v1.1 spec at
# https://gist.github.com/architext1/808548dd25cfac5cc47fb6e910b79292
#
# The substantive protocol — IDR envelope, signing, chaining, verification —
# lives in bin/notarise and lib/docuseal.py within this repo. This file
# documents the protocol version, the schema, and the conformance check.

set -euo pipefail

SELF="${BASH_SOURCE[0]:-$0}"
HERE="$(cd "$(dirname "$SELF")" && pwd)"
CMD="${1:-help}"

PROTOCOL_VERSION="happi/1.1"
PROTOCOL_GIST="https://gist.github.com/architext1/808548dd25cfac5cc47fb6e910b79292"

case "$CMD" in
  verify)
    bash -n "$SELF" >/dev/null
    head -1 "$SELF" | grep -q "^#!/usr/bin/env bash"
    grep -q "^# Polyglot:" "$SELF"
    grep -q "^: <<'MARKDOWN_BEGIN'" "$SELF"
    echo "[happi.md verify] polyglot envelope OK · version reference: $PROTOCOL_VERSION"
    ;;

  version)
    echo "$PROTOCOL_VERSION"
    ;;

  spec)
    echo "[happi.md spec] canonical spec: $PROTOCOL_GIST"
    echo "[happi.md spec] local implementation: bin/notarise + lib/docuseal.py"
    ;;

  conformance)
    # Verify bin/notarise speaks happi/1.1
    if [ -x "$HERE/bin/notarise" ]; then
      VER=$("$HERE/bin/notarise" --version 2>&1 | grep -oE "happi/[0-9]+\.[0-9]+" | head -1 || echo "unknown")
      if [ "$VER" = "$PROTOCOL_VERSION" ]; then
        echo "[happi.md conformance] bin/notarise OK · speaks $VER"
      else
        echo "[happi.md conformance] DRIFT · bin/notarise reports $VER, expected $PROTOCOL_VERSION"
        exit 1
      fi
    else
      echo "[happi.md conformance] bin/notarise not executable — conformance not checkable"
      exit 2
    fi
    ;;

  help|*)
    cat <<HELP
happi.md — the donna-folded transport (v1.1 reference, May 2026)

Commands:
  bash happi.md verify        Polyglot envelope self-check
  bash happi.md version       Print the protocol version ($PROTOCOL_VERSION)
  bash happi.md spec          Pointer to the canonical spec gist
  bash happi.md conformance   Check bin/notarise speaks $PROTOCOL_VERSION
  bash happi.md help          This message

The substantive protocol implementation is in:
  bin/notarise           — IDR sign + verify CLI (HMAC-SHA256 chained)
  lib/docuseal.py        — DocuSeal API syscall shim (signing transport)
  lib/docuseal_webhook.py — DocuSeal webhook -> IDR adapter
  PROBAT.md              — the live audit chain at the repo root

Canonical spec: $PROTOCOL_GIST
HELP
    ;;
esac

exit 0

: <<'MARKDOWN_BEGIN'

# happi.md — donna-folded transport (v1.1 reference)

> The receipt. The audit-chain primitive. Every delegated decision becomes
> a signed Intent Decision Record, chained to the previous one, replayable,
> exportable in regulator-ready formats.

This file is a *reference wrapper* around the canonical `happi.md v1.1` spec
(public gist linked above). The substantive protocol implementation lives in
this repository's `bin/notarise` script and `lib/docuseal.py` shim.

## Protocol version

`happi/1.1` — stable since April 2026. Backward-compatible with `happi/1.0`
(see CHANGELOG.md for the migration notes).

## IDR record shape

Every delegated decision produces an Intent Decision Record:

```json
{
  "decision_id": "01H...",
  "protocol_version": "happi/1.1",
  "previous_hash": "<sha256 of the previous IDR or 000...0 for genesis>",
  "intent": "send Sarah the M&A precedent we used for Dubrovnik...",
  "signer": "donna-bot",
  "confidence": 0.92,
  "timestamp_ns": 1715769600000000000,
  "signature_algorithm": "HMAC-SHA256",
  "signature": "<hex>",
  "metadata": { ... matter-specific fields ... }
}
```

The signature is computed over the canonical JSON serialisation
(stable key order, no whitespace). The HMAC key is in the OS keychain
(env `DONNA_NOTARISE_KEY`).

## Chain integrity

Each record's `previous_hash` is the SHA-256 of the previous record's
canonical bytes. Tampering with any record invalidates every record after
it. The chain is the proof.

Verification: `bin/notarise verify --chain PROBAT.md`

## Round-trip equivalence (H480)

The fork experiment registers H480: the IDR chain round-trips through the
fold without loss. Concretely:

1. Take 5 representative IDRs from the upstream `chiefofstaff-legal/donna`
   PROBAT.md chain
2. Verify each with `bin/notarise verify` in the upstream repo (baseline)
3. Apply the four-doc fold to the fork
4. Verify the same 5 IDRs through `bash happi.md conformance` + `bash GRIP.md notarise verify`
5. Compare: every IDR must verify with identical signature output

If any IDR fails to round-trip, H480 is falsified.

## Why this file exists

For self-containment. A fresh machine that has only the four polyglot
files needs to know what protocol version to speak. The full spec is
referenced (gist URL); the version constant and the conformance check
travel with the fold.

MARKDOWN_BEGIN
