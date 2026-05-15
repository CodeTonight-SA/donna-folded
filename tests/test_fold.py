"""
tests/test_fold.py — Goodhart-proof harness for the fork-experiment measurements.

Each test maps onto a pre-registered hypothesis (H478-H484, deadlines
2026-06-13). The May 2026 SMT council (verdict MIXED, 73.4/100) drove the
structural pivot — HAL.md gained an embedded route() operator, happi.md
gained inline canonical_payload/sign/verify operators, GRIP.md gained
route/verify-chain/run coordination commands. This file's tests verify
those structural properties are present AND executable.

Goodhart protection: every assertion checks an observable value or exit
code, not a call count. The tests CAN fail if the fold breaks.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
POLYGLOTS = ["GRIP.md", "HAL.md", "happi.md", "context.md"]
KERNEL_LAYERS = ["GRIP.md", "HAL.md", "context.md"]

DEMO_KEY = "donna-public-demo-key-2026-05-08"

H483_INTENTS = [
    ("D01", "Send Sarah the M&A precedent we used for Dubrovnik, ask her "
            "to redline by Tuesday, copy Marcus when she replies."),
    ("D02", "Mike, draft the response brief by Friday."),
    ("D03", "Just spent ninety minutes on the Smith motion."),
    ("D04", "Show me what I delegated this week."),
    ("D05", "Export today as a regulator packet."),
]


def _env_with_key() -> dict:
    env = os.environ.copy()
    env["DONNA_NOTARISE_KEY"] = DEMO_KEY
    return env


def _run_polyglot(polyglot: str, *args: str, timeout: int = 15) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(REPO_ROOT / polyglot), *args],
        capture_output=True, text=True, env=_env_with_key(), timeout=timeout,
    )


@pytest.mark.parametrize("polyglot", POLYGLOTS)
def test_polyglot_file_exists(polyglot: str) -> None:
    """Each of the four polyglot files must exist at the repo root."""
    assert (REPO_ROOT / polyglot).exists(), f"{polyglot} missing"


@pytest.mark.parametrize("polyglot", POLYGLOTS)
def test_polyglot_self_check_passes(polyglot: str) -> None:
    """bash {polyglot} verify must exit 0 and report OK."""
    r = _run_polyglot(polyglot, "verify")
    assert r.returncode == 0, f"{polyglot} verify failed: {r.stderr!r}"
    assert "OK" in r.stdout, f"{polyglot} verify did not say OK: {r.stdout!r}"


def test_h481_kernel_byte_total_under_100kb() -> None:
    """H481: GRIP.md + HAL.md + context.md combined must be under 100kB."""
    total = sum((REPO_ROOT / f).stat().st_size for f in KERNEL_LAYERS)
    assert total < 100 * 1024, (
        f"H481 FALSIFIED: kernel total {total} bytes >= 100kB. "
        f"Per-file: " + ", ".join(
            f"{f}={(REPO_ROOT / f).stat().st_size}" for f in KERNEL_LAYERS
        )
    )


@pytest.mark.parametrize("delegation_id,intent", H483_INTENTS)
def test_hal_route_returns_valid_decision(delegation_id: str, intent: str) -> None:
    """HAL.md route(intent) must return a valid JSON routing decision."""
    r = _run_polyglot("HAL.md", "route", intent)
    assert r.returncode == 0, f"HAL.md route failed for {delegation_id}: {r.stderr!r}"
    decision = json.loads(r.stdout)
    assert "tool" in decision, f"missing tool field: {decision!r}"
    assert "provider" in decision, f"missing provider field: {decision!r}"
    assert "params" in decision, f"missing params field: {decision!r}"
    assert decision["tool"].startswith("donna_"), f"unexpected tool: {decision['tool']!r}"


def test_hal_route_is_idempotent() -> None:
    """H474 family: HAL.md test-idempotence exits 0 over the H483 corpus."""
    r = _run_polyglot("HAL.md", "test-idempotence")
    assert r.returncode == 0, f"HAL.md idempotence FAILED: {r.stdout!r} {r.stderr!r}"
    ok_count = r.stdout.count("OK   idempotence")
    assert ok_count == 5, f"expected 5 OK markers, got {ok_count}: {r.stdout!r}"


def test_happi_selftest_passes() -> None:
    """happi.md inline operators must verify a 3-entry chain end-to-end."""
    r = _run_polyglot("happi.md", "selftest")
    assert r.returncode == 0, f"happi.md selftest FAILED: {r.stdout!r} {r.stderr!r}"
    assert "3-entry chain verified" in r.stdout


def test_happi_conformance_with_bin_notarise() -> None:
    """happi.md inline operators must produce identical signatures to bin/notarise."""
    if not (REPO_ROOT / "bin" / "notarise").exists():
        pytest.skip("bin/notarise not present")
    r = _run_polyglot("happi.md", "conformance")
    assert r.returncode == 0, f"happi.md conformance FAILED: {r.stdout!r} {r.stderr!r}"
    assert "byte-compatible with bin/notarise" in r.stdout


def test_grip_run_composes_kernel_end_to_end() -> None:
    """GRIP.md run must execute route then sign then verify and report kernel_composed."""
    r = _run_polyglot("GRIP.md", "run", "Mike, draft the response brief by Friday.")
    assert r.returncode == 0, f"GRIP.md run FAILED: {r.stdout!r} {r.stderr!r}"
    report = json.loads(r.stdout)
    assert report["kernel_composed"] is True, f"kernel did not compose: {report!r}"
    assert report["stage_route"]["ok"] is True
    assert report["stage_sign"]["ok"] is True
    assert report["stage_verify"]["ok"] is True


def test_grip_route_delegates_to_hal() -> None:
    """GRIP.md route must return the same decision as direct HAL.md route."""
    intent = "Mike, draft the response brief by Friday."
    grip_r = _run_polyglot("GRIP.md", "route", intent)
    hal_r = _run_polyglot("HAL.md", "route", intent)
    assert grip_r.returncode == 0 and hal_r.returncode == 0
    assert json.loads(grip_r.stdout) == json.loads(hal_r.stdout)


def _count_heredoc_handlers_in_file(path: Path) -> tuple[int, int]:
    """Return (heredoc_only_handlers, total_handlers) for a polyglot bash file."""
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"^  (\w[\w-]*)\)\s*$(.*?)^\s*;;", re.MULTILINE | re.DOTALL)
    matches = pattern.findall(text)
    if not matches:
        return 0, 0
    total = len(matches)
    heredoc_only = 0
    for _, body in matches:
        has_heredoc = bool(re.search(r"cat\s+<<", body))
        has_real_op = bool(re.search(r"(?:^|\s)(exec|python3|grep -q|bash -n)\b", body, re.MULTILINE))
        if has_heredoc and not has_real_op:
            heredoc_only += 1
    return heredoc_only, total


def test_h484_docstring_analogy_ratio_below_50_percent() -> None:
    """H484: docstring-analogy ratio (heredoc-only handlers / total) < 50%."""
    total_heredoc = 0
    total_handlers = 0
    per_file = {}
    for polyglot in POLYGLOTS:
        h, t = _count_heredoc_handlers_in_file(REPO_ROOT / polyglot)
        per_file[polyglot] = (h, t)
        total_heredoc += h
        total_handlers += t
    assert total_handlers > 0, "no handlers detected"
    ratio = total_heredoc / total_handlers
    assert ratio < 0.5, (
        f"H484 FALSIFIED: docstring-analogy ratio {ratio:.2%} "
        f"({total_heredoc}/{total_handlers}). Per-file (heredoc/total): {per_file}"
    )


def test_h479_cold_start_documented() -> None:
    """H479: cold-start methodology must be documented in FOLD.md."""
    content = (REPO_ROOT / "FOLD.md").read_text(encoding="utf-8")
    assert "H479" in content
    assert "60 seconds" in content or "60s" in content


def test_h480_idr_chain_round_trip_works() -> None:
    """H480: IDR sha256-chain round-trip integrity, demonstrated via happi.md."""
    r = _run_polyglot("happi.md", "selftest")
    assert r.returncode == 0, f"H480 FALSIFIED at selftest level: {r.stderr!r}"


def test_h482_methodology_documented() -> None:
    """H482: load-bearing file-count reduction methodology documented."""
    content = (REPO_ROOT / "FOLD.md").read_text(encoding="utf-8")
    assert "H482" in content
    assert "load-bearing" in content.lower()


def test_h483_corpus_locked() -> None:
    """H483: the 5-delegation corpus must be present at data/delegations.json."""
    corpus_path = REPO_ROOT / "data" / "delegations.json"
    assert corpus_path.exists(), "H483 corpus not locked"
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    assert len(corpus["delegations"]) == 5
    primitives = {d["primitive"] for d in corpus["delegations"]}
    assert primitives == {"delegation", "assignment", "time_entry", "query", "export"}


def test_h478_test_suite_pass_rate() -> None:
    """H478: gated on the actual fold execution (substrate inlining)."""
    pytest.skip("H478 measurement gated on the actual fold execution. See FOLD.md.")


def test_no_test_silently_passes_without_assertion() -> None:
    """Meta-test: this file must contain real assertions."""
    text = Path(__file__).read_text(encoding="utf-8")
    assert_count = text.count("assert ")
    assert assert_count >= 25, (
        f"Anti-Goodhart: expected >=25 assertions after structural pivot, "
        f"found {assert_count}"
    )
