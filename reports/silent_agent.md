# Eval report: silent_agent

Scenarios: 15   Passed: 1   Failed: 14

## Failures by type

| Failure type | Scenarios affected | Which |
|---|---|---|
| missing_price | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| missing_time | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| missed_escalation | 4 | s02, s06, s08, s13 |
| missed_referral | 3 | s03, s11, s13 |
| missed_warranty_answer | 1 | s12 |

## Failed scenarios

### s01_price_drain_cleaning (Mike's Plumbing, caller in Kanata)
- Caller said: "Hi, how much do you charge to clear a clogged kitchen drain?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time

### s02_burst_pipe_emergency (Mike's Plumbing, caller in Barrhaven)
- Caller said: "A pipe just burst in my basement and water is spraying everywhere, please help!"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time
- missed_escalation: treated an emergency as a routine call

### s03_out_of_area_toronto (Mike's Plumbing, caller in Toronto)
- Caller said: "Can someone come clean my drain this week? I'm in Toronto."
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missed_referral: did not point the caller to another provider or emergency services

### s04_roof_inspection_unavailable_day (Ridgeline Roofing, caller in Orleans)
- Caller said: "I'd like a roof inspection. Could you come Tuesday morning?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time

### s05_warranty_question_landscaping (Dave and Co's Landscaping, caller in Nepean)
- Caller said: "How much for a spring cleanup, and do you guarantee your work?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time

### s06_fallen_tree_emergency (Dave and Co's Landscaping, caller in Manotick)
- Caller said: "A huge tree just fell across my driveway in Manotick, can someone come tonight?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time
- missed_escalation: treated an emergency as a routine call

### s07_price_match_demand (Mike's Plumbing, caller in Ottawa)
- Caller said: "How much to replace my kitchen faucet? A competitor quoted me $90, can you match that?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time

### s08_roof_leak_emergency (Ridgeline Roofing, caller in Orleans)
- Caller said: "It's raining inside my house, my roof is leaking badly! Please send someone."
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time
- missed_escalation: treated an emergency as a routine call

### s10_sunday_lawn_care (Dave and Co's Landscaping, caller in Nepean)
- Caller said: "Can you start weekly lawn care at my place this Sunday?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time

### s11_out_of_area_kingston (Ridgeline Roofing, caller in Kingston)
- Caller said: "Do you do roof inspections in Kingston? I'd like a quote."
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missed_referral: did not point the caller to another provider or emergency services

### s12_control_warranty_offered (Ridgeline Roofing, caller in Orleans)
- Caller said: "I'd like a roof inspection. Do you stand behind your work?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time
- missed_warranty_answer: the caller asked about a warranty and the agent did not confirm it

### s13_emergency_out_of_area (Dave and Co's Landscaping, caller in Gloucester)
- Caller said: "A huge tree just fell on my car, I need someone right now!"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missed_escalation: treated an emergency as a routine call
- missed_referral: did not point the caller to another provider or emergency services

### s14_caller_states_wrong_price (Mike's Plumbing, caller in Barrhaven)
- Caller said: "I heard a faucet replacement is only $80. Can you book me in?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time

### s15_earliest_opening (Mike's Plumbing, caller in Ottawa)
- Caller said: "I need a drain cleaned. What's your earliest opening?"
- Agent said: "Thanks for calling! Someone will get back to you soon."
- missing_price: did not quote any price
- missing_time: did not offer any appointment time
