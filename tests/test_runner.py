"""Tests for the runner, including the most important one:
every known bug we can inject into a mock agent must be CAUGHT by the kit.

Run with:  python -m pytest tests -v
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
import run_eval  # noqa: E402
from mock_agents import ALL_FLAWS, DEFAULT_FLAWED, MockAgent  # noqa: E402

# For each injected bug: the failure type it MUST trigger, and the types it is allowed to trigger.
MUST_CATCH = {
    "invents_price": ("invented_price", {"invented_price"}),
    "adds_extra_price": ("off_topic_price", {"off_topic_price"}),
    "bad_slot": ("bad_slot", {"bad_slot"}),
    "books_out_of_area": ("out_of_area_booking",
                          {"out_of_area_booking", "off_topic_price", "missed_escalation", "missed_referral"}),
    "never_escalates": ("missed_escalation", {"missed_escalation", "missed_referral"}),
    "no_referral": ("missed_referral", {"missed_referral"}),
    "promises_warranty": ("unsupported_promise", {"unsupported_promise"}),
    "cries_wolf": ("false_escalation", {"false_escalation"}),
    "says_nothing": ("missing_price", {"missing_price", "missing_time", "missed_escalation",
                                       "missed_referral", "missed_warranty_answer"}),
    "ignores_warranty_question": ("missed_warranty_answer", {"missed_warranty_answer"}),
}


def types_found(results):
    return {f["type"] for r in results for f in r["failures"]}


def test_every_flaw_has_a_catch_rule():
    assert set(MUST_CATCH) == ALL_FLAWS


def test_good_agent_passes_every_scenario():
    results = run_eval.run_agent(MockAgent())
    assert all(not r["failures"] for r in results)
    assert len(results) == 15


@pytest.mark.parametrize("flaw", sorted(ALL_FLAWS))
def test_each_injected_bug_is_caught(flaw):
    must, allowed = MUST_CATCH[flaw]
    found = types_found(run_eval.run_agent(MockAgent({flaw})))
    assert must in found, f"the kit MISSED the bug '{flaw}'"
    assert found <= allowed, f"unexpected failure types for '{flaw}': {found - allowed}"


def test_runs_are_reproducible():
    a = run_eval.run_agent(MockAgent(DEFAULT_FLAWED))
    b = run_eval.run_agent(MockAgent(DEFAULT_FLAWED))
    assert a == b


def test_compare_shows_fixed_and_newly_broken():
    v1 = run_eval.run_agent(MockAgent(DEFAULT_FLAWED))
    v2 = run_eval.run_agent(MockAgent({"invents_price", "bad_slot", "promises_warranty", "adds_extra_price"}))
    text = run_eval.format_compare("v1", v1, "v2", v2)
    assert "Fixed" in text and "Newly broken" in text
    assert "missed_escalation" in text and "off_topic_price" in text
