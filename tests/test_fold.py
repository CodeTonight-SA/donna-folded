"""
tests/test_fold.py — Goodhart-proof harness for the six fork-experiment measurements.

Each test maps one-to-one onto a pre-registered hypothesis (H478-H483, deadline
2026-06-13). Tests do not currently execute the full empirical run because:

  - H483 (behavioural equivalence) is gated on V>>'s pick of 5 representative
    DONNA delegations. Until the delegation corpus is locked, the test is
    skipped (not silently passed).
  - H479 (cold-start) needs three test machines and is run via a separate
    smoke-harness shell script (scripts/smoke-harness.sh in the upstream).

The tests that CAN run today verify the structural preconditions:
  - All four polyglot files exist
  - Each polyglot self-check passes (bash X.md verify exits 0)
  - The kernel byte total fits H481's bound
  - The fork wires upstream correctly

Goodhart protection: every assertion checks an observable value, not a call
count. Pass/fail is computable mechanically; the test cannot drift to pass
trivially while the underlying claim is false.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
POLYGLOTS = ["GRIP.md", "HAL.md", "happi.md", "context.md"]


# ─── Structural preconditions ─────────────────────────────────────────


@pytest.mark.parametrize("polyglot", POLYGLOTS)
def test_polyglot_file_exists(polyglot: str) -> None:
    """Each of the four polyglot files must exist at the repo root."""
    path = REPO_ROOT / polyglot
    assert path.exists(), f"{polyglot} missing — the fold is incomplete"


@pytest.mark.parametrize("polyglot", POLYGLOTS)
def test_polyglot_self_check_passes(polyglot: str) -> None:
    """`bash {polyglot} verify` must exit 0 and report 'envelope OK'."""
    path = REPO_ROOT / polyglot
    result = subprocess.run(
        ["bash", str(path), "verify"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, (
        f"{polyglot} verify failed (rc={result.returncode}): "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    assert "OK" in result.stdout, (
        f"{polyglot} verify did not report OK: {result.stdout!r}"
    )


# ─── H481 — kernel byte total ─────────────────────────────────────────


def test_h481_kernel_byte_total_under_100kb() -> None:
    """H481: GRIP.md + HAL.md + context.md combined must be under 100kB.

    happi.md is excluded because it is a transport-shim reference, not a
    kernel layer per the four-doc-fold architecture.
    """
    kernel_files = ["GRIP.md", "HAL.md", "context.md"]
    total = sum((REPO_ROOT / f).stat().st_size for f in kernel_files)
    assert total < 100 * 1024, (
        f"H481 FALSIFIED: kernel total {total} bytes >= 100kB. "
        f"Per-file: " + ", ".join(
            f"{f}={(REPO_ROOT / f).stat().st_size}" for f in kernel_files
        )
    )


# ─── H478 — test-suite pass rate (gated) ──────────────────────────────


@pytest.mark.skipif(
    not (REPO_ROOT / "Makefile").exists(),
    reason="upstream Makefile not present — cannot run baseline pass-rate measurement",
)
def test_h478_test_suite_pass_rate() -> None:
    """H478: the fork's test suite must pass at >=95% rate.

    This test runs the upstream Makefile target and counts passes/failures.
    """
    # Skeleton — full execution gated on the fold being performed
    pytest.skip(
        "H478 measurement gated on the actual fold execution — "
        "currently scaffolding only. See FOLD.md for the schedule."
    )


# ─── H479 — cold-start (external) ─────────────────────────────────────


def test_h479_cold_start_documented() -> None:
    """H479: cold-start measurement is documented in FOLD.md.

    The actual cold-start measurement requires three fresh machines and is
    run via scripts/smoke-harness.sh. This test verifies the methodology
    is documented; the empirical run is external.
    """
    fold_md = REPO_ROOT / "FOLD.md"
    assert fold_md.exists(), "FOLD.md must document the cold-start methodology"
    content = fold_md.read_text(encoding="utf-8")
    assert "H479" in content, "FOLD.md must reference H479 by ID"
    assert "60 seconds" in content or "60s" in content, (
        "FOLD.md must state the H479 threshold of 60 seconds"
    )


# ─── H480 — IDR round-trip (gated on bin/notarise + canonical IDRs) ───


def test_h480_idr_roundtrip_methodology_documented() -> None:
    """H480: IDR sha256-chain round-trip integrity methodology documented."""
    fold_md = REPO_ROOT / "FOLD.md"
    content = fold_md.read_text(encoding="utf-8")
    assert "H480" in content
    assert "round-trip" in content.lower()
    assert "5 representative IDRs" in content or "5 representative" in content


# ─── H482 — load-bearing file reduction (computed at experiment time) ─


def test_h482_methodology_documented() -> None:
    """H482: load-bearing file-count reduction methodology documented."""
    fold_md = REPO_ROOT / "FOLD.md"
    content = fold_md.read_text(encoding="utf-8")
    assert "H482" in content
    assert "load-bearing" in content.lower()
    assert "90%" in content or "0.9" in content


# ─── H483 — behavioural equivalence (gated on V>>'s 5-delegation pick) ─


def test_h483_gated_on_delegation_corpus() -> None:
    """H483: behavioural equivalence — explicitly skipped until corpus locked."""
    delegations = REPO_ROOT / "data" / "delegations.json"
    if not delegations.exists():
        pytest.skip(
            "H483 awaiting V>>'s pick of 5 representative DONNA delegations. "
            "Create data/delegations.json with the corpus to enable this measurement."
        )
    # Full empirical run goes here once the corpus exists
    pytest.fail(
        "H483 corpus present but execution not yet implemented — see FOLD.md"
    )


# ─── Anti-Goodhart: meta-test ─────────────────────────────────────────


def test_no_test_silently_passes_without_assertion() -> None:
    """Meta-test: this file's tests must contain actual assertions.

    Mutation discipline: if a test has only pytest.skip() / pytest.fail()
    without an assert, it is a placeholder. Placeholders are tracked by
    counting. If the count drops, real tests have been deleted.
    """
    this_file = Path(__file__).read_text(encoding="utf-8")
    assert_count = this_file.count("assert ")
    # Lower bound — adjust upward as real measurements are wired in
    assert assert_count >= 10, (
        f"Anti-Goodhart: this file should contain >=10 assertions, "
        f"found {assert_count}. Did someone delete real tests?"
    )
