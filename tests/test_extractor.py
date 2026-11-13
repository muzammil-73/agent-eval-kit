"""Tests for the extractor.

1. For every hand-written sample reply, the extractor must produce the SAME form
   that we filled in by hand.
2. Extra checks on tricky wording.
3. The output must always satisfy the agent_facts schema.
"""
import json
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
from extractor import extract_facts  # noqa: E402

SCHEMA = json.loads((ROOT / "schemas" / "agent_facts.schema.json").read_text())
SAMPLES = sorted((ROOT / "data" / "sample_replies").glob("*.json"))


@pytest.mark.parametrize("path", SAMPLES, ids=lambda p: p.name)
def test_extractor_matches_the_hand_filled_form(path):
    sample = json.loads(path.read_text())
    assert extract_facts(sample["reply_text"]) == sample["facts"]


@pytest.mark.parametrize("path", SAMPLES, ids=lambda p: p.name)
def test_extractor_output_fits_the_schema(path):
    sample = json.loads(path.read_text())
    errors = list(Draft202012Validator(SCHEMA).iter_errors(extract_facts(sample["reply_text"])))
    assert errors == []


@pytest.mark.parametrize("text,expected", [
    ("We don't offer a warranty on that.", False),
    ("Everything we do is fully guaranteed.", True),
    ("We don't serve Toronto, but everything is guaranteed.", True),
    ("I can't promise a guarantee.", False),
])
def test_warranty_wording(text, expected):
    assert extract_facts(text)["promised_warranty"] is expected


@pytest.mark.parametrize("text,expected", [
    ("Want me to book it?", False),
    ("I can book you for Friday at 09:00.", False),
    ("I've booked you in for Friday at 09:00!", True),
    ("I'll book it now!", True),
])
def test_booking_wording(text, expected):
    assert extract_facts(text)["booked"] is expected


def test_times_are_zero_padded_and_abbreviated():
    assert extract_facts("I have Friday at 9:00 open.")["times_offered"] == ["Fri 09:00"]


def test_prices_are_numbers_and_deduplicated():
    assert extract_facts("It is $150. Again, $150.")["prices_quoted"] == [150]
