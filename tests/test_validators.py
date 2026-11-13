"""Tests for the validators themselves ("who checks the checker?").

Rule: the validators must PASS every file in data/catalogs and data/scenarios,
and must FAIL every file in the bad_* folders, with the expected message.

Run with:  python -m pytest tests -v
"""
import json
import os
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
import validate_scenarios as vs  # noqa: E402

CATALOG_SCHEMA = json.loads((ROOT / "schemas" / "catalog.schema.json").read_text())
SCENARIO_SCHEMA = json.loads((ROOT / "schemas" / "scenario.schema.json").read_text())


@pytest.fixture(autouse=True)
def maybe_sabotage(monkeypatch):
    """DEMO ONLY: set SABOTAGE=1 to break the consistency check on purpose
    and watch these tests notice."""
    if os.environ.get("SABOTAGE"):
        monkeypatch.setattr(vs, "consistency_problems", lambda s: [])


def catalog_errors(path):
    data = json.loads(path.read_text())
    return [e.message for e in Draft202012Validator(CATALOG_SCHEMA).iter_errors(data)]


def scenario_errors(path):
    data = json.loads(path.read_text())
    shape = [e.message for e in Draft202012Validator(SCENARIO_SCHEMA).iter_errors(data)]
    return shape or vs.consistency_problems(data)


GOOD_CATALOGS = sorted((ROOT / "data" / "catalogs").glob("*.json"))
BAD_CATALOGS = sorted((ROOT / "data" / "bad_examples").glob("*.json"))
GOOD_SCENARIOS = sorted((ROOT / "data" / "scenarios").glob("*.json"))
BAD_SCENARIOS = sorted((ROOT / "data" / "bad_scenarios").glob("*.json"))

# What each broken scenario should be caught for
EXPECTED_MESSAGE = {
    "s90_wrong_price.json": "catalog price",
    "s91_emergency_not_flagged.json": "emergency flag",
    "s92_out_of_area_emergency_no_referral.json": "must_refer_out",
    "s93_warranty_to_out_of_area_caller.json": "warranty_promise_allowed",
}


@pytest.mark.parametrize("path", GOOD_CATALOGS, ids=lambda p: p.name)
def test_good_catalogs_pass(path):
    assert catalog_errors(path) == []


@pytest.mark.parametrize("path", BAD_CATALOGS, ids=lambda p: p.name)
def test_bad_catalogs_fail(path):
    assert catalog_errors(path), f"validator wrongly accepted {path.name}"


@pytest.mark.parametrize("path", GOOD_SCENARIOS, ids=lambda p: p.name)
def test_good_scenarios_pass(path):
    assert scenario_errors(path) == []


@pytest.mark.parametrize("path", BAD_SCENARIOS, ids=lambda p: p.name)
def test_bad_scenarios_fail_with_the_right_reason(path):
    errors = scenario_errors(path)
    assert errors, f"validator wrongly accepted {path.name}"
    assert any(EXPECTED_MESSAGE[path.name] in e for e in errors)
