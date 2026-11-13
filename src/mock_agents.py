"""Mock receptionist agents: stand-ins for a real product, so the kit can run end to end.

IMPORTANT: these are simple rule-based programs, NOT AI. They exist to give the graders
something to grade. A mock agent receives only what a real agent would:
    - the business's own catalog (a real agent is configured with the owner's price list)
    - what the caller said
    - the caller's town
It NEVER sees the hidden expectations.

Usage:
    python src/mock_agents.py            # show good vs flawed replies for all scenarios
    python src/mock_agents.py s01 s13    # only scenarios whose id starts with these
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

DAYS = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday",
        "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}

# Words that tell the agent which service the caller means
KEYWORDS = {
    "drain cleaning": ["drain", "clog"],
    "faucet replacement": ["faucet"],
    "burst pipe repair": ["burst"],
    "roof inspection": ["inspection"],
    "shingle repair": ["shingle"],
    "emergency leak repair": ["leak"],
    "weekly lawn care": ["lawn"],
    "spring cleanup": ["cleanup", "spring"],
    "fallen tree removal": ["tree"],
}
WARRANTY_WORDS = ["guarantee", "warranty", "stand behind"]

# Deliberate bugs a flawed agent can have (each one trips a specific failure type)
ALL_FLAWS = {
    "invents_price",      # quotes $20 less than the real price         -> invented_price
    "adds_extra_price",   # also mentions another service's price       -> off_topic_price
    "bad_slot",           # offers a time that is not open              -> bad_slot
    "books_out_of_area",  # books callers it does not serve             -> out_of_area_booking
    "never_escalates",    # treats emergencies as routine               -> missed_escalation
    "no_referral",        # says goodbye with no next step              -> missed_referral
    "promises_warranty",  # tells everyone "everything is guaranteed"   -> unsupported_promise
    "cries_wolf",         # calls every call urgent                     -> false_escalation
    "says_nothing",       # "someone will get back to you", nothing else -> missing_price / missing_time
    "ignores_warranty_question",  # never answers a warranty question -> missed_warranty_answer
}
DEFAULT_FLAWED = {"invents_price", "bad_slot", "never_escalates", "books_out_of_area", "promises_warranty"}


def say_slot(slot):
    day, time = slot.split()
    return f"{DAYS[day]} at {time}"


def find_service(catalog, text):
    lower = text.lower()
    for service in catalog["services"]:
        if any(k in lower for k in KEYWORDS.get(service["name"], [])):
            return service
    return None


def requested_day(text):
    lower = text.lower()
    for abbr, full in DAYS.items():
        if full.lower() in lower:
            return abbr
    return None


class MockAgent:
    def __init__(self, flaws=()):
        self.flaws = set(flaws)
        unknown = self.flaws - ALL_FLAWS
        if unknown:
            raise ValueError(f"unknown flaws: {unknown}")

    def respond(self, catalog, caller_opening, caller_location):
        if "says_nothing" in self.flaws:
            return "Thanks for calling! Someone will get back to you soon."
        extras = " Everything we do is fully guaranteed." if "promises_warranty" in self.flaws else ""
        if "cries_wolf" in self.flaws:
            extras += " That sounds urgent, so I'm alerting the team right now."
        service = find_service(catalog, caller_opening)
        if service is None:
            return "Happy to help! Can you tell me a bit more about what's going on?" + extras
        if caller_location not in catalog["service_area"]:
            return self._out_of_area(catalog, service, caller_location) + extras
        return self._in_area(catalog, service, caller_opening) + extras

    def _out_of_area(self, catalog, service, town):
        name = service["name"].capitalize()
        if "books_out_of_area" in self.flaws:
            return f"Sure! {name} is ${service['price']:g}. I've booked you in for {say_slot(catalog['available_slots'][0])}!"
        if "no_referral" in self.flaws and not service["emergency"]:
            return f"Sorry, we don't serve {town}. Goodbye."
        if service["emergency"]:
            if "never_escalates" in self.flaws:
                return "Sorry, that's outside our service area."
            if "no_referral" in self.flaws:
                return f"That sounds urgent, but we don't serve {town}. Goodbye."
            return (f"That sounds urgent. We don't serve {town}, so please call emergency services "
                    f"if anyone is in danger, or a local provider.")
        return f"Sorry, we don't serve {town}, but you could try a local provider there."

    def _in_area(self, catalog, service, opening):
        lower = opening.lower()
        name = service["name"].capitalize()
        price = service["price"] - 20 if "invents_price" in self.flaws else service["price"]
        parts = []

        if "$" in opening:
            parts.append(f"I'm not able to match other quotes, but {service['name']} is ${price:g}.")
        else:
            parts.append(f"{name} is ${price:g}.")
        if "adds_extra_price" in self.flaws:
            other = next(s for s in catalog["services"] if s["name"] != service["name"])
            parts.append(f"We also do {other['name']} for ${other['price']:g}.")

        if service["emergency"] and "never_escalates" not in self.flaws:
            parts.append("That sounds urgent, so I'm alerting the team right now.")

        if any(w in lower for w in WARRANTY_WORDS) and "ignores_warranty_question" not in self.flaws:
            if catalog["warranty_offered"]:
                parts.append("Yes, we stand behind our work with a warranty.")
            else:
                parts.append("That isn't something we offer, but we'll make sure the job is done right.")

        real = catalog["available_slots"]
        day = requested_day(opening)
        if "bad_slot" in self.flaws:
            pick = f"{DAYS[day]} at 11:00" if day else "Wednesday at 15:00"
            parts.append(f"I can do {pick}.")
        elif day and any(s.startswith(day) for s in real):
            parts.append(f"I have {say_slot(next(s for s in real if s.startswith(day)))} open.")
        elif day:
            parts.append(f"We're not open on {DAYS[day]}, but I have {say_slot(real[0])} or {say_slot(real[1])}.")
        else:
            parts.append(f"I have {say_slot(real[0])} open.")

        parts.append("Want me to book it?")
        return " ".join(parts)


def good_agent():
    return MockAgent()


def flawed_agent():
    return MockAgent(DEFAULT_FLAWED)


def load_catalogs():
    out = {}
    for p in (ROOT / "data" / "catalogs").glob("*.json"):
        c = json.loads(p.read_text())
        out[c["business_id"]] = c
    return out


def load_scenarios(prefixes=()):
    items = []
    for p in sorted((ROOT / "data" / "scenarios").glob("*.json")):
        s = json.loads(p.read_text())
        if not prefixes or any(s["scenario_id"].startswith(x) for x in prefixes):
            items.append(s)
    return items


if __name__ == "__main__":
    catalogs = load_catalogs()
    good, flawed = good_agent(), flawed_agent()
    for s in load_scenarios(sys.argv[1:]):
        cat = catalogs[s["business_id"]]
        # The agent is handed ONLY the caller's half. Never the expectations.
        args = (cat, s["caller_opening"], s["caller_location"])
        print(f"{s['scenario_id']}  ({cat['business_name']}, caller in {s['caller_location']})")
        print(f"   caller : {s['caller_opening']}")
        print(f"   good   : {good.respond(*args)}")
        print(f"   flawed : {flawed.respond(*args)}")
        print()
