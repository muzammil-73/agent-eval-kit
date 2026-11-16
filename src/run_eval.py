"""Run an agent through every scenario, grade it, and write a failure report.

Usage
    python src/run_eval.py --agent good --out reports/good_agent
    python src/run_eval.py --agent flawed --out reports/flawed_v1
    python src/run_eval.py --flaws invents_price,bad_slot --label my_agent --out reports/my_agent
    python src/run_eval.py --compare reports/flawed_v1.json reports/flawed_v2.json

Each run writes <out>.json (full results) and <out>.md (a readable report).
The agent only ever receives the caller's half of a scenario.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import grader  # noqa: E402
from extractor import extract_facts  # noqa: E402
from mock_agents import (ALL_FLAWS, MockAgent, flawed_agent, good_agent,  # noqa: E402
                         load_catalogs, load_scenarios)

ROOT = Path(__file__).parent.parent


def run_agent(agent, scenarios=None, catalogs=None):
    """Reply, extract the form, grade. Returns one result per scenario."""
    catalogs = catalogs or load_catalogs()
    scenarios = scenarios if scenarios is not None else load_scenarios()
    results = []
    for s in scenarios:
        cat = catalogs[s["business_id"]]
        reply = agent.respond(cat, s["caller_opening"], s["caller_location"])  # caller half only
        facts = extract_facts(reply)
        failures = grader.grade(s, facts, cat)
        results.append({
            "scenario_id": s["scenario_id"],
            "category": s["category"],
            "business": cat["business_name"],
            "caller_opening": s["caller_opening"],
            "caller_location": s["caller_location"],
            "reply": reply,
            "facts": facts,
            "failures": failures,
        })
    return results


def failures_by_type(results):
    out = defaultdict(list)
    for r in results:
        for t in sorted({f["type"] for f in r["failures"]}):
            out[t].append(r["scenario_id"])
    return dict(out)


def format_report(label, results):
    passed = sum(1 for r in results if not r["failures"])
    lines = [f"# Eval report: {label}", "",
             f"Scenarios: {len(results)}   Passed: {passed}   Failed: {len(results) - passed}", ""]
    by_type = failures_by_type(results)
    if by_type:
        lines += ["## Failures by type", "", "| Failure type | Scenarios affected | Which |", "|---|---|---|"]
        for t, ids in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"| {t} | {len(ids)} | {', '.join(i.split('_')[0] for i in ids)} |")
        lines.append("")
        lines.append("## Failed scenarios")
        for r in results:
            if not r["failures"]:
                continue
            lines += ["", f"### {r['scenario_id']} ({r['business']}, caller in {r['caller_location']})",
                      f"- Caller said: \"{r['caller_opening']}\"",
                      f"- Agent said: \"{r['reply']}\""]
            for f in r["failures"]:
                lines.append(f"- {f['type']}: {f['message']}")
    else:
        lines.append("All scenarios passed.")
    return "\n".join(lines) + "\n"


def pairs(results):
    return {(r["scenario_id"], f["type"]) for r in results for f in r["failures"]}


def format_compare(label_a, results_a, label_b, results_b):
    pa, pb = pairs(results_a), pairs(results_b)
    fixed, new = sorted(pa - pb), sorted(pb - pa)
    pass_a = sum(1 for r in results_a if not r["failures"])
    pass_b = sum(1 for r in results_b if not r["failures"])
    lines = [f"# Comparison: {label_a} -> {label_b}", "",
             f"Scenarios passing: {pass_a} -> {pass_b}",
             f"Individual failures: {len(pa)} -> {len(pb)}", ""]
    ta, tb = failures_by_type(results_a), failures_by_type(results_b)
    lines += ["## By failure type (scenarios affected)", ""]
    for t in sorted(set(ta) | set(tb)):
        lines.append(f"- {t}: {len(ta.get(t, []))} -> {len(tb.get(t, []))}")
    lines += ["", f"## Fixed ({len(fixed)}): failed before, fine now"]
    lines += [f"- {sid.split('_')[0]}: {t}" for sid, t in fixed] or ["- none"]
    lines += ["", f"## Newly broken ({len(new)}): fine before, failing now"]
    lines += [f"- {sid.split('_')[0]}: {t}" for sid, t in new] or ["- none"]
    return "\n".join(lines) + "\n"


def save(label, results, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".json").write_text(json.dumps({"label": label, "results": results}, indent=2) + "\n")
    out.with_suffix(".md").write_text(format_report(label, results))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--agent", choices=["good", "flawed"], help="a built-in mock agent")
    p.add_argument("--flaws", help="comma-separated flaws for a custom mock agent")
    p.add_argument("--label", help="name shown in the report")
    p.add_argument("--out", help="path without extension, e.g. reports/flawed_v1")
    p.add_argument("--compare", nargs=2, metavar=("BEFORE_JSON", "AFTER_JSON"))
    args = p.parse_args()

    if args.compare:
        a = json.loads(Path(args.compare[0]).read_text())
        b = json.loads(Path(args.compare[1]).read_text())
        print(format_compare(a["label"], a["results"], b["label"], b["results"]))
        return

    if args.flaws is not None:
        try:
            agent = MockAgent(f.strip() for f in args.flaws.split(",") if f.strip())
        except ValueError as e:
            sys.exit(f"{e}\nKnown flaws: {', '.join(sorted(ALL_FLAWS))}")
        label = args.label or "custom_agent"
    elif args.agent == "flawed":
        agent, label = flawed_agent(), args.label or "flawed_agent"
    else:
        agent, label = good_agent(), args.label or "good_agent"

    results = run_agent(agent)
    if args.out:
        save(label, results, args.out)
    print(format_report(label, results))


if __name__ == "__main__":
    main()
