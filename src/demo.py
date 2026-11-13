"""A short, readable demo of the eval kit (made for screen recording).

    python src/demo.py            # runs straight through
    python src/demo.py --pause    # waits for Enter between sections, so you can talk
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import grader  # noqa: E402
from extractor import extract_facts  # noqa: E402
from mock_agents import flawed_agent, good_agent, load_catalogs, load_scenarios  # noqa: E402
from run_eval import failures_by_type, run_agent  # noqa: E402

PAUSE = "--pause" in sys.argv


def section(title):
    if PAUSE:
        input("\n[press Enter to continue] ")
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def verdict(scenario, reply, catalog):
    failures = grader.grade(scenario, extract_facts(reply), catalog)
    if not failures:
        return ["PASS"]
    return [f"FAIL  {f['type']}: {f['message']}" for f in failures]


def main():
    catalogs = load_catalogs()
    good, flawed = good_agent(), flawed_agent()

    section("1. The answer key: one fake business")
    cat = catalogs["mikes_plumbing"]
    print(f"{cat['business_name']}   serves: {', '.join(cat['service_area'])}")
    for s in cat["services"]:
        tag = "  (emergency)" if s["emergency"] else ""
        print(f"   {s['name']:<20} ${s['price']:g}{tag}")
    print(f"   open slots: {', '.join(cat['available_slots'])}")
    print(f"   offers a warranty: {cat['warranty_offered']}")

    section("2. Three caller situations, two agents")
    for prefix in ("s02", "s03", "s04"):
        s = load_scenarios([prefix])[0]
        cat = catalogs[s["business_id"]]
        print(f"\nCALLER in {s['caller_location']} ({cat['business_name']}): \"{s['caller_opening']}\"")
        for label, agent in (("GOOD agent  ", good), ("FLAWED agent", flawed)):
            reply = agent.respond(cat, s["caller_opening"], s["caller_location"])
            lines = verdict(s, reply, cat)
            print(f"  {label} says: {reply}")
            for line in lines:
                print(f"       -> {line}")

    section("3. All 15 scenarios")
    for label, agent in (("Good agent  ", good), ("Flawed agent", flawed)):
        results = run_agent(agent)
        passed = sum(1 for r in results if not r["failures"])
        print(f"{label}: {passed} of {len(results)} scenarios passed")
        if label.startswith("Flawed"):
            print("\nMistakes found in the flawed agent, by type:")
            for t, ids in sorted(failures_by_type(results).items(), key=lambda kv: -len(kv[1])):
                print(f"   {t:<24} {len(ids):>2} scenarios")

    section("4. Who checks the checker?")
    print("The kit has its own automatic tests. Run:  python -m pytest tests -q")
    print("They plant known bugs in an agent, and the kit must catch every one.")


if __name__ == "__main__":
    main()
