# Receptionist Agent Eval Kit

![tests](https://github.com/muzammil-73/agent-eval-kit/actions/workflows/tests.yml/badge.svg)

A small test kit that checks whether an AI phone receptionist gives correct answers: the right price,
real appointment times, and a proper response to emergencies.

> **Status:** working prototype. The agents inside it are simple rule-based stand-ins (not AI), and the
> businesses are made up. See [Limits](#limits).

## Why this exists

An AI receptionist talks to many customers, so one mistake can repeat hundreds of times without anyone
noticing: a wrong price, a time that doesn't exist, an emergency treated as routine. An AI also never words
things the same way twice, so you can't test it by looking for one exact sentence.

This kit tests the **facts** in a reply, not the wording, using plain code (no AI judge), so the same input
always gives the same verdict.

## How it works

```
caller's words -> agent -> reply (words) -> extractor -> six yes/no boxes -> graders -> report
                                                                              ^
                                                              hidden scoring sheet
```

1. **Catalogs** (`data/catalogs`): fake businesses with a price list, service area, open slots and warranty. This is the answer key.
2. **Scenarios** (`data/scenarios`): 15 caller situations. Each has the caller's words, and a hidden scoring sheet the agent never sees.
3. **Agent**: receives only the caller's words and replies in plain text.
4. **Extractor**: reads the reply and fills in six boxes: prices quoted, times offered, booked, urgent, referred out, promised a warranty.
5. **Graders**: compare the boxes to the hidden sheet and record each mistake.
6. **Runner and report**: repeat for all 15 scenarios, count mistakes by type, and compare two runs (what a change fixed, and what it broke).

## What it checks

| The agent must NOT | The agent MUST |
|---|---|
| quote an invented price (`invented_price`) | quote the right price (`missing_price`) |
| quote another service's price (`off_topic_price`) | offer an appointment time (`missing_time`) |
| offer a time that is not open (`bad_slot`) | say it is urgent for an emergency (`missed_escalation`) |
| book a caller the business does not serve (`out_of_area_booking`) | give a next step to a caller it cannot serve (`missed_referral`) |
| promise a warranty the business does not offer (`unsupported_promise`) | confirm a warranty when asked and offered (`missed_warranty_answer`) |
| call a routine call urgent (`false_escalation`) | |

## Example

Caller (Barrhaven): *"A pipe just burst in my basement and water is spraying everywhere, please help!"*

- **Good agent:** "Burst pipe repair is $300. That sounds urgent, so I'm alerting the team right now. I have Thursday at 10:00 open. Want me to book it?"  
  Verdict: PASS
- **Flawed agent:** "Burst pipe repair is $280. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."  
  Verdict: FAIL: invented_price; bad_slot; missed_escalation

## Results

The good stand-in agent passes all 15 scenarios. A flawed stand-in agent (bugs added on purpose) passes 1 of 15.
Mistakes found in the flawed agent, by type:

| Failure type | Scenarios affected | Which |
|---|---|---|
| bad_slot | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| invented_price | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| unsupported_promise | 6 | s03, s05, s06, s10, s11, s13 |
| missed_escalation | 4 | s02, s06, s08, s13 |
| missed_referral | 3 | s03, s11, s13 |
| off_topic_price | 3 | s03, s11, s13 |
| out_of_area_booking | 3 | s03, s11, s13 |

## How to run

Needs Python 3.9 or newer. Tested on 3.9, 3.11 and 3.13.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python src/demo.py                          # short readable demo
python src/demo.py --pause                  # same, pausing between sections
python src/run_eval.py --agent good         # run the good agent
python src/run_eval.py --agent flawed --label flawed_v1 --out reports/flawed_v1
python src/run_eval.py --flaws invents_price,bad_slot,promises_warranty,adds_extra_price --label flawed_v2 --out reports/flawed_v2
python src/run_eval.py --compare reports/flawed_v1.json reports/flawed_v2.json
python -m pytest tests -q                   # the kit's own tests
```

## How the kit itself is tested

A test kit is only useful if you can trust it, so it is tested with answers we already know:

- **File validators** must reject deliberately broken catalogs and scenarios (`data/bad_examples`, `data/bad_scenarios`).
- **The extractor** must reproduce the boxes filled in by hand for every sample reply (`data/sample_replies`).
- **The graders** must flag each hand-written bad reply with exactly the expected mistake type.
- **Planted bugs:** there are 10 bugs that can be switched on in a stand-in agent. The kit must catch every one, and the good agent must still pass all 15 scenarios.

Together these are 109 automatic tests. A kit that approved everything would pass the good agent, and a kit that
rejected everything would "catch" the flawed one, which is why both agents are needed.

Every push runs the tests and re-validates the data files on Python 3.9, 3.11 and 3.13
(`.github/workflows/tests.yml`), so a scenario that stops agreeing with its catalog fails the build.

## Project layout

```
data/catalogs/        the answer key (3 fake businesses)
data/scenarios/       15 caller scenarios and their hidden scoring sheets
data/sample_replies/  hand-written replies with hand-filled boxes
schemas/              JSON schemas for catalogs, scenarios, and the six-box form
src/                  validators, extractor, graders, mock agents, runner, demo
tests/                the kit's own tests
reports/              example reports
.github/workflows/    tests and data validation on every push
```

## Design decisions

- Any caller outside the service area gets a next step (another provider or emergency services), not only emergencies.
- A warranty may be promised only if the business offers one and the caller is in its service area.
- Quoting extra prices is flagged, to keep replies on topic.
- Calling a routine call urgent is a mistake, not just missing a real emergency.
- For a caller the business can serve, with a known service, the agent must give a price and a time.
- Harmless extra help (such as an unrequired referral) is not flagged.

## Limits

- The stand-in agents are rule-based, not AI. They exist so the kit has something to grade.
- The extractor only understands the stand-in agents' wording (plus a few similar phrasings). A real agent would need an LLM
  to fill in the same six boxes under the same schema. The graders would not change.
- Businesses and scenarios are made up. The kit has not been run on a real product's transcripts.
- Mistake types are counted equally. A missed emergency is worse than an extra price, but the report does not weight that yet.
- A vague request (the sink "acting weird") does not yet require the agent to ask a follow-up question.

## Next steps

- Grade real call transcripts (anonymized) against a real price list.
- Add severity weights to the report.
- Replace the rule-based extractor with an LLM extractor and test it against hand-labelled replies.
- Run the same graders on live calls as monitoring.
