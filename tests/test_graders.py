"""Tests for the graders: every hand-written reply must produce exactly the expected failures.

Run with:  python -m pytest tests -v
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
import grader  # noqa: E402

SAMPLES = ROOT / "data" / "sample_replies"

EXPECTED = {
    # good replies: must pass
    "s01_good.json": set(),
    "s03_good_refers_elsewhere.json": set(),
    "s12_good_warranty.json": set(),
    "s13_good_refers_out.json": set(),
    "s09_good_asks_question.json": set(),
    # bad replies: each should trip its own failure type
    "s01_bad_invented_price.json": {"invented_price"},
    "s01_bad_extra_price.json": {"off_topic_price"},
    "s15_bad_slot.json": {"bad_slot"},
    "s10_bad_books_sunday.json": {"bad_slot"},
    "s11_bad_books_kingston.json": {"out_of_area_booking", "missed_referral"},
    "s08_bad_no_escalation.json": {"missed_escalation"},
    "s13_bad_no_referral.json": {"missed_referral"},
    "s05_bad_promises_warranty.json": {"unsupported_promise"},
    "s03_bad_promises_warranty.json": {"unsupported_promise", "missed_referral"},
    "s03_bad_no_next_step.json": {"missed_referral"},
    "s12_bad_ignores_warranty.json": {"missed_warranty_answer"},
    "s01_bad_says_nothing.json": {"missing_price", "missing_time"},
    "s01_bad_cries_wolf.json": {"false_escalation"},
    # one bad reply that breaks two rules at once
    "s02_bad_slot_and_no_escalation.json": {"bad_slot", "missed_escalation"},
    "s03_bad_books_out_of_area.json": {"off_topic_price", "out_of_area_booking", "missed_referral"},
}


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_reply_gets_the_expected_verdict(name):
    _, failures = grader.grade_sample_file(SAMPLES / name)
    assert {f["type"] for f in failures} == EXPECTED[name]


def test_every_sample_reply_has_an_expectation():
    on_disk = {p.name for p in SAMPLES.glob("*.json")}
    assert on_disk == set(EXPECTED), f"unlisted or missing: {on_disk ^ set(EXPECTED)}"
