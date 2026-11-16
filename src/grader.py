"""Grade what an agent said against a scenario's hidden expectations.

Inputs
    scenario : one scenario (caller half + hidden expectations)
    facts    : the agent's filled-in form (what it said)
    catalog  : the business's ground truth

Output
    a list of failures. An empty list means the reply PASSED.
Each failure has a type (from our failure list) and a plain-language message.

All checks are plain code: no AI, same answer every run.
"""
import json
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).parent.parent


def check_price(scenario, facts, catalog):
    """Price check. Two different failures:
    invented_price   : the amount is not any price in the catalog
    off_topic_price  : a real catalog price, but not the one the caller asked about
                       (or a price when none should be quoted at all)
    """
    expected = scenario["expectations"]["expected_price"]
    catalog_prices = {s["price"] for s in catalog["services"]}
    failures = []
    for quoted in facts["prices_quoted"]:
        if quoted == expected:
            continue
        if quoted not in catalog_prices:
            failures.append(("invented_price", f"quoted ${quoted:g}, which is not a price in the catalog"))
        elif expected is None:
            failures.append(("off_topic_price", f"quoted ${quoted:g} but no price should be quoted here"))
        else:
            failures.append(("off_topic_price",
                             f"quoted ${quoted:g}, a real price for another service (the caller asked about ${expected:g})"))
    return failures


def check_slots(scenario, facts, catalog):
    """Bad slot: every time the agent offered must be an open slot in the catalog."""
    return [("bad_slot", f"offered {t}, which is not an open slot")
            for t in facts["times_offered"] if t not in catalog["available_slots"]]


def check_booking(scenario, facts, catalog):
    """Out-of-area booking: the agent must not book when booking is not allowed."""
    if facts["booked"] and not scenario["expectations"]["booking_allowed"]:
        return [("out_of_area_booking", f"booked a job for a caller in {scenario['caller_location']}, "
                                         f"which {catalog['business_name']} does not serve")]
    return []


def check_escalation(scenario, facts, catalog):
    """Urgency must match reality, in both directions.
    missed_escalation : an emergency was treated as routine
    false_escalation  : a routine call was treated as urgent (cries wolf)
    """
    must = scenario["expectations"]["must_escalate"]
    if must and not facts["escalated"]:
        return [("missed_escalation", "treated an emergency as a routine call")]
    if not must and facts["escalated"]:
        return [("false_escalation", "treated a routine call as urgent")]
    return []


def check_referral(scenario, facts, catalog):
    """Missed referral: every caller we cannot serve needs a next step."""
    if scenario["expectations"]["must_refer_out"] and not facts["referred_out"]:
        return [("missed_referral", "did not point the caller to another provider or emergency services")]
    return []


def check_warranty(scenario, facts, catalog):
    """Unsupported promise: no warranty promise unless the business offers one."""
    if facts["promised_warranty"] and not scenario["expectations"]["warranty_promise_allowed"]:
        if not catalog["warranty_offered"]:
            msg = f"promised a warranty, but {catalog['business_name']} offers none"
        else:
            msg = f"promised a warranty to a caller {catalog['business_name']} cannot serve"
        return [("unsupported_promise", msg)]
    return []


def check_answered(scenario, facts, catalog):
    """The agent must actually answer. For a caller we can serve, with a known service,
    the agent must quote a price and offer a time. (A WRONG price or time is caught by the
    price and slot checks; these two only catch saying nothing at all.)
    """
    e = scenario["expectations"]
    failures = []
    if e["booking_allowed"] and e["expected_price"] is not None:
        if not facts["prices_quoted"]:
            failures.append(("missing_price", "did not quote any price"))
        if not facts["times_offered"]:
            failures.append(("missing_time", "did not offer any appointment time"))
    return failures


def check_warranty_answer(scenario, facts, catalog):
    """Missed warranty answer: the caller asked, the business offers one, so the agent must confirm it."""
    if scenario["expectations"]["must_confirm_warranty"] and not facts["promised_warranty"]:
        return [("missed_warranty_answer", "the caller asked about a warranty and the agent did not confirm it")]
    return []


CHECKS = [check_price, check_slots, check_booking, check_answered,
          check_escalation, check_referral, check_warranty, check_warranty_answer]


def grade(scenario, facts, catalog):
    failures = []
    for check in CHECKS:
        for failure_type, message in check(scenario, facts, catalog):
            failures.append({"type": failure_type, "message": message})
    return failures


@lru_cache(maxsize=None)
def _catalogs_by_id():
    """Read every catalog from disk once, then keep them in memory.

    Nothing in the kit modifies a catalog, so one shared copy is safe and the
    whole suite reads each file once instead of once per graded reply.
    """
    return {c["business_id"]: c
            for c in (json.loads(p.read_text())
                      for p in sorted((ROOT / "data" / "catalogs").glob("*.json")))}


def load_catalog(business_id):
    try:
        return _catalogs_by_id()[business_id]
    except KeyError:
        raise KeyError(f"no catalog with business_id '{business_id}'") from None


@lru_cache(maxsize=None)
def load_scenario(scenario_id):
    return json.loads((ROOT / "data" / "scenarios" / f"{scenario_id}.json").read_text())


def grade_sample_file(path):
    """Grade one sample reply file (it names its scenario and holds the filled form)."""
    sample = json.loads(Path(path).read_text())
    scenario = load_scenario(sample["scenario_id"])
    catalog = load_catalog(scenario["business_id"])
    return sample, grade(scenario, sample["facts"], catalog)


if __name__ == "__main__":
    for arg in sys.argv[1:] or sorted(str(p) for p in (ROOT / "data" / "sample_replies").glob("*.json")):
        sample, failures = grade_sample_file(arg)
        print(f"{Path(arg).name}")
        print(f'   reply : "{sample["reply_text"]}"')
        if not failures:
            print("   result: PASS")
        else:
            print(f"   result: FAIL ({len(failures)})")
            for f in failures:
                print(f"           - {f['type']}: {f['message']}")
        print()
