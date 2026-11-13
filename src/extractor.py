"""Extractor: read an agent's reply (plain words) and fill in the six-box facts form.

This is the "AI extracts, code verifies" step. For the MOCK agents we use simple
pattern rules (no AI needed). For a REAL agent with free-form wording, the same
form (schemas/agent_facts.schema.json) would be filled in by an LLM with a strict
JSON output, and the graders stay exactly the same.

Limits of this rule-based version: it only understands the phrasings the mock agents
use, plus a few common variants. Unusual wording can fool it.
"""
import re

DAY_ABBR = {"monday": "Mon", "tuesday": "Tue", "wednesday": "Wed", "thursday": "Thu",
            "friday": "Fri", "saturday": "Sat", "sunday": "Sun"}

PRICE = re.compile(r"\$\s?(\d+(?:\.\d+)?)")
TIME = re.compile(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b\s+at\s+(\d{1,2}):(\d{2})", re.I)
# Confirmed booking. A question like "Want me to book it?" or an offer like "I can book you" does NOT count.
BOOKED = re.compile(r"\bi(?:'ve| have) booked\b|\byou(?:'re| are) booked\b|\bbooked you\b|\bi'll book\b", re.I)
URGENT = re.compile(r"\burgent\b|\balerting\b|\bright away\b|\bimmediately\b", re.I)
REFERRAL = re.compile(r"emergency services|\b(?:try|call|contact) (?:a |an )?(?:local|another|different)\b|"
                      r"\banother provider\b|\blocal provider\b", re.I)
WARRANTY = re.compile(r"guarantee|warrant|stand behind", re.I)
NEGATION = re.compile(r"\b(?:don't|doesn't|do not|does not|can't|cannot|isn't|aren't|not|no)\b", re.I)


def _number(text):
    value = float(text)
    return int(value) if value.is_integer() else value


def _unique(items):
    seen, out = set(), []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def extract_facts(reply_text):
    t = reply_text.replace("\u2019", "'")
    prices = _unique(_number(p) for p in PRICE.findall(t))
    times = _unique(f"{DAY_ABBR[d.lower()]} {int(h):02d}:{m}" for d, h, m in TIME.findall(t))

    # A warranty promise needs a warranty word in a clause with no negation.
    # Clauses are split on punctuation and " but ", so "We don't serve X, but it's guaranteed"
    # is read as two clauses and the promise is still found.
    clauses = re.split(r"[.!?;,]| but ", t)
    promised = any(WARRANTY.search(c) and not NEGATION.search(c) for c in clauses)

    return {
        "prices_quoted": prices,
        "times_offered": times,
        "booked": bool(BOOKED.search(t)),
        "escalated": bool(URGENT.search(t)),
        "referred_out": bool(REFERRAL.search(t)),
        "promised_warranty": promised,
    }
