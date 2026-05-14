#!/usr/bin/env python3
"""
scripts/capture-baseline.py — capture the upstream IDR signatures for the 5
H483 delegations as the empirical baseline for the fold experiment.

Run once. Appends to data/fold-measurements.jsonl. Uses bin/notarise via
subprocess so the script makes no assumptions about internal call shape.

The captured baseline has wall-clock timestamps (non-deterministic). The
fold-comparison test will need either:
  (a) a future patch to bin/notarise adding --timestamp for determinism, or
  (b) a compare-minus-timestamp criterion at test time.

This script makes the issue concrete by storing the captured timestamps as
data. The decision is V>>'s.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTARISE = REPO_ROOT / "bin" / "notarise"
DELEGATIONS = REPO_ROOT / "data" / "delegations.json"
BASELINE = REPO_ROOT / "data" / "fold-measurements.jsonl"

GENESIS = "0" * 64
DEMO_KEY = "donna-public-demo-key-2026-05-08"
SIGNER = "donna-bot"
CONFIDENCE = "0.92"


def _check_prereqs() -> int:
    if not NOTARISE.exists():
        print(f"ERROR: {NOTARISE} not found", file=sys.stderr)
        return 1
    if not DELEGATIONS.exists():
        print(f"ERROR: {DELEGATIONS} not found", file=sys.stderr)
        return 1
    return 0


def _sign_entry(entry: dict, previous_hash: str, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            str(NOTARISE), "sign",
            "--intent", entry["intent"],
            "--signer", SIGNER,
            "--confidence", CONFIDENCE,
            "--previous-hash", previous_hash,
            "--decision-id", f"fold-{entry['id']}-2026-05",
        ],
        capture_output=True, text=True, env=env, timeout=10,
    )


def _parse_sign_output(entry_id: str, stdout: str) -> tuple[str, dict] | None:
    lines = stdout.split("\n", 1)
    hash_line = lines[0].strip()
    if not hash_line.startswith("hash:"):
        print(f"ERROR: unexpected hash line for {entry_id}: {hash_line!r}")
        return None
    return hash_line.split(":", 1)[1].strip(), json.loads(lines[1])


def _build_baseline_entry(entry: dict, previous_hash: str, record_hash: str, record: dict) -> dict:
    return {
        "id": entry["id"],
        "primitive": entry["primitive"],
        "measurement_kind": "upstream_baseline",
        "environment": "fork main, pre-fold (equivalent to upstream)",
        "previous_hash": previous_hash,
        "record_hash": record_hash,
        "signature": record["signature"],
        "timestamp_wall_clock": record["timestamp"],
        "decision_id": record["decision_id"],
        "signer": SIGNER,
        "confidence": float(CONFIDENCE),
        "notarise_key_id": DEMO_KEY,
        "protocol": record["protocol"],
        "captured_at": "May 2026",
        "note": (
            "timestamp is wall-clock and non-deterministic; "
            "folded-run signatures will differ unless bin/notarise "
            "is patched to accept --timestamp OR the comparison "
            "excludes the timestamp field"
        ),
    }


def _capture_all(corpus: dict, env: dict) -> tuple[list[dict] | None, int]:
    previous_hash = GENESIS
    captured: list[dict] = []
    for entry in corpus["delegations"]:
        result = _sign_entry(entry, previous_hash, env)
        if result.returncode != 0:
            print(f"ERROR signing {entry['id']}: {result.stderr}", file=sys.stderr)
            return None, 2
        parsed = _parse_sign_output(entry["id"], result.stdout)
        if parsed is None:
            return None, 3
        record_hash, record = parsed
        captured.append(_build_baseline_entry(entry, previous_hash, record_hash, record))
        previous_hash = record_hash
    return captured, 0


def _write_and_report(captured: list[dict]) -> None:
    with BASELINE.open("a", encoding="utf-8") as fh:
        for entry in captured:
            fh.write(json.dumps(entry, sort_keys=True) + "\n")
    print(f"Captured {len(captured)} baseline entries to {BASELINE}")
    for e in captured:
        print(
            f"  {e['id']} ({e['primitive']:11s}) "
            f"sig={e['signature'][:16]}... "
            f"hash={e['record_hash'][:16]}..."
        )


def main() -> int:
    rc = _check_prereqs()
    if rc != 0:
        return rc
    corpus = json.loads(DELEGATIONS.read_text(encoding="utf-8"))
    env = os.environ.copy()
    env["DONNA_NOTARISE_KEY"] = DEMO_KEY
    captured, rc = _capture_all(corpus, env)
    if captured is None:
        return rc
    _write_and_report(captured)
    return 0


if __name__ == "__main__":
    sys.exit(main())
