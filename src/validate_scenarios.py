"""Check scenarios two ways.

1. SHAPE: does each scenario follow scenario.schema.json?
2. CONSISTENCY: do its expectations agree with the business catalog (ground truth)?

Usage:
    python src/validate_scenarios.py data/scenarios
    python src/validate_scenarios.py data/bad_scenarios
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parent.parent
SCENARIO_SCHEMA = json.loads((ROOT / "schemas" / "scenario.schema.json").read_text())
CATALOGS = {}
for p in (ROOT / "data" / "catalogs").glob("*.json"):
    c = json.loads(p.read_text())
    CATALOGS[c["business_id"]] = c


def consistency_problems(s: dict) -> list[str]:
    """Compare a scenario's expectations to the ground truth."""
    problems = []
    cat = CATALOGS.get(s["business_id"])
    if cat is None:
        return [f"unknown business_id '{s['business_id']}'"]
    exp = s["expectations"]

    service = None
    if s["service_requested"] is not None:
        service = next((x for x in cat["services"] if x["name"] == s["service_requested"]), None)
        if service is None:
            problems.append(f"service '{s['service_requested']}' is not offered by {cat['business_name']}")

    in_area = s["caller_location"] in cat["service_area"]
    if exp["booking_allowed"] != in_area:
        problems.append(f"booking_allowed is {exp['booking_allowed']} but '{s['caller_location']}' "
                        f"{'is' if in_area else 'is NOT'} in the service area")

    if service is not None:
        if in_area and exp["expected_price"] != service["price"]:
            problems.append(f"expected_price is {exp['expected_price']} but catalog price is {service['price']}")
        if exp["must_escalate"] != service["emergency"]:
            problems.append(f"must_escalate is {exp['must_escalate']} but catalog emergency flag is {service['emergency']}")

    should_refer = not in_area
    if exp["must_refer_out"] != should_refer:
        problems.append(f"must_refer_out is {exp['must_refer_out']} but it should be {should_refer} "
                        f"(caller {'is' if in_area else 'is NOT'} in the service area)")

    should_allow_warranty = bool(cat["warranty_offered"] and in_area)
    if exp["warranty_promise_allowed"] != should_allow_warranty:
        problems.append(f"warranty_promise_allowed is {exp['warranty_promise_allowed']} but it should be "
                        f"{should_allow_warranty} (warranty offered: {cat['warranty_offered']}, "
                        f"caller {'is' if in_area else 'is NOT'} in the service area)")
    asks = any(w in s["caller_opening"].lower() for w in ("guarantee", "warranty", "stand behind"))
    should_confirm = bool(asks and should_allow_warranty)
    if exp["must_confirm_warranty"] != should_confirm:
        problems.append(f"must_confirm_warranty is {exp['must_confirm_warranty']} but it should be {should_confirm} "
                        f"(caller asked about a warranty: {asks}, warranty may be promised: {should_allow_warranty})")
    return problems


def run(folder: Path) -> int:
    validator = Draft202012Validator(SCENARIO_SCHEMA)
    bad = 0
    for path in sorted(folder.glob("*.json")):
        s = json.loads(path.read_text())
        shape = [e.message for e in validator.iter_errors(s)]
        if shape:
            bad += 1
            print(f"FAIL  {path.name}  (shape)")
            for m in shape:
                print(f"        {m}")
            continue
        consistency = consistency_problems(s)
        if consistency:
            bad += 1
            print(f"FAIL  {path.name}  (consistency)")
            for m in consistency:
                print(f"        {m}")
        else:
            print(f"OK    {path.name}")
    return bad


if __name__ == "__main__":
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "scenarios"
    sys.exit(1 if run(folder) else 0)
