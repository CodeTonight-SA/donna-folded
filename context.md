#!/usr/bin/env bash
# context.md — donna-folded operator state (schema-only, May 2026)
# Polyglot: valid Markdown · executable Bash · embedded Python runtime · JSON envelope
#
# Status: SCHEMA ONLY. This file documents the shape of operator-specific
# state — firm config, matter context, signer identity. Real values live in
# an encrypted blob (git-crypt / age / OS keychain — operator decision).
#
# THIS FILE NEVER CONTAINS REAL OPERATOR VALUES IN PLAINTEXT.

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
    # Confirm no obvious operator values landed in this file
    if grep -qE "(@[a-z]+\.(com|org|net|co\.[a-z]{2})|sk_[A-Za-z0-9]{30,}|gho_[A-Za-z0-9]{20,})" "$SELF"; then
      echo "[context.md verify] FAIL — operator values detected in plaintext"
      exit 1
    fi
    echo "[context.md verify] polyglot envelope OK · schema-only · no operator values present"
    ;;

  schema)
    cat <<'SCHEMA'
context.md operator-state schema (the shape, never the values):

  firm:
    name:        "{firm name}"
    jurisdiction: "{jurisdiction code, e.g. UK · US-NY · CH · ZA}"
    bar_number:  "{practising-certificate identifier — never logged}"
    house_style: "{path to firm's style guide}"
    risk_profile: "{path to firm's risk profile JSON}"

  signer:
    name:        "{full name}"
    role:        "{partner | associate | counsel | trainee}"
    signature:   "{operator signature, e.g. V>>}"
    notarise_key_keychain: "{keychain entry name — never the value}"

  matter:
    default_path:  "{filesystem path or storage URL for matter folders}"
    archive_after: "{retention period in days}"
    privilege_default: "{strict | standard | none}"

  preferences:
    voice:       "{terse | warm | formal}"
    register:    "{technical | plain}"
    language:    "{en-GB | en-US | de-CH | ...}"

  providers:
    analytical:  "{provider preference order, e.g. claude > gemini > self-host}"
    signing:     "{docuseal | adobe-sign | other}"
SCHEMA
    ;;

  example)
    cat <<'EXAMPLE'
[context.md example] — placeholder values only, never check this in for real

  firm:
    name: "EXAMPLE Solicitors LLP"
    jurisdiction: "UK"
    bar_number: "<redacted>"
    house_style: "config/firm-style.md"
    risk_profile: "config/firm-risk.json"

  signer:
    name: "Example Partner"
    role: "partner"
    signature: "E>>"
    notarise_key_keychain: "donna-notarise-example"

  matter:
    default_path: "/data/matters"
    archive_after: 2555
    privilege_default: "strict"

  preferences:
    voice: "terse"
    register: "technical"
    language: "en-GB"

  providers:
    analytical: "claude > gemini > self-host"
    signing: "docuseal"
EXAMPLE
    ;;

  help|*)
    cat <<'HELP'
context.md — the donna-folded operator state (schema-only, v0.0.1)

Commands:
  bash context.md verify   Polyglot envelope self-check + plaintext-value scan
  bash context.md schema   Print the operator-state schema (the shape)
  bash context.md example  Print a placeholder example (never real values)
  bash context.md help     This message

NEVER commit real firm/signer/matter values to this file. The encryption
story (git-crypt / age / sealed-box / external keychain) is an operator
decision that gates real deployment — see FOLD.md for the open question
the fork experiment cannot answer alone.
HELP
    ;;
esac

exit 0

: <<'MARKDOWN_BEGIN'

# context.md — donna-folded operator state

> The mount. The schema for operator-specific state — which firm, which
> signer, which matter conventions, which preferences. The fold's most
> sensitive surface, and the only one that is fundamentally *per-operator*.

## What lives here (schema only)

| Section | Purpose | Sensitivity |
|---------|---------|-------------|
| `firm` | Firm name, jurisdiction, bar number, house style | HIGH — never plaintext |
| `signer` | Operator identity, role, signature, keychain pointer | HIGH — keychain refs only |
| `matter` | Default matter path, retention period, privilege default | MEDIUM |
| `preferences` | Voice, register, language | LOW — but per-operator |
| `providers` | Provider preference order | LOW |

## Encryption open question

This skeleton does NOT yet pick an encryption story. The operator decides:

- `git-crypt` — symmetric encryption pinned to .gitattributes patterns
- `age` — Curve25519 + ChaCha20-Poly1305, modern, simple
- `sealed-box` — libsodium, asymmetric
- External keychain only — file holds keychain entry names, no values at all

The fork experiment registers no hypothesis on this dimension because the
trade-off is operator-specific. The empirical fork run uses placeholder
values (`bash context.md example`) and does NOT touch real firm data.

## What this file is NOT

This file is NOT a credentials store. It is NOT a secrets vault. It is the
*shape* of operator state — a typed contract that downstream substrate
(GRIP.md, HAL.md) can rely on without hard-coding firm-specific assumptions.

If real firm data ever lands here in plaintext, `bash context.md verify`
catches it (the regex scan) and refuses to pass. That refusal is the
load-bearing safety primitive.

## Why per-operator matters

Two solicitors at different firms may share the same GRIP + HAL + happi
fold, but their context.md files differ on every line. The fold operator
treats `context.md` as a parameter, not a constant. That property is what
makes the fork portable to many firms without re-engineering the kernel.

MARKDOWN_BEGIN
