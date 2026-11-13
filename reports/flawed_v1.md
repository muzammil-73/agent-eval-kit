# Eval report: flawed_v1

Scenarios: 15   Passed: 1   Failed: 14

## Failures by type

| Failure type | Scenarios affected | Which |
|---|---|---|
| bad_slot | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| invented_price | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| unsupported_promise | 6 | s03, s05, s06, s10, s11, s13 |
| missed_escalation | 4 | s02, s06, s08, s13 |
| missed_referral | 3 | s03, s11, s13 |
| off_topic_price | 3 | s03, s11, s13 |
| out_of_area_booking | 3 | s03, s11, s13 |

## Failed scenarios

### s01_price_drain_cleaning (Mike's Plumbing, caller in Kanata)
- Caller said: "Hi, how much do you charge to clear a clogged kitchen drain?"
- Agent said: "Drain cleaning is $130. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $130, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot

### s02_burst_pipe_emergency (Mike's Plumbing, caller in Barrhaven)
- Caller said: "A pipe just burst in my basement and water is spraying everywhere, please help!"
- Agent said: "Burst pipe repair is $280. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $280, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot
- missed_escalation: treated an emergency as a routine call

### s03_out_of_area_toronto (Mike's Plumbing, caller in Toronto)
- Caller said: "Can someone come clean my drain this week? I'm in Toronto."
- Agent said: "Sure! Drain cleaning is $150. I've booked you in for Thursday at 10:00! Everything we do is fully guaranteed."
- off_topic_price: quoted $150 but no price should be quoted here
- out_of_area_booking: booked a job for a caller in Toronto, which Mike's Plumbing does not serve
- missed_referral: did not point the caller to another provider or emergency services
- unsupported_promise: promised a warranty to a caller Mike's Plumbing cannot serve

### s04_roof_inspection_unavailable_day (Ridgeline Roofing, caller in Orleans)
- Caller said: "I'd like a roof inspection. Could you come Tuesday morning?"
- Agent said: "Roof inspection is $180. I can do Tuesday at 11:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $180, which is not a price in the catalog
- bad_slot: offered Tue 11:00, which is not an open slot

### s05_warranty_question_landscaping (Dave and Co's Landscaping, caller in Nepean)
- Caller said: "How much for a spring cleanup, and do you guarantee your work?"
- Agent said: "Spring cleanup is $160. That isn't something we offer, but we'll make sure the job is done right. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $160, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot
- unsupported_promise: promised a warranty, but Dave and Co's Landscaping offers none

### s06_fallen_tree_emergency (Dave and Co's Landscaping, caller in Manotick)
- Caller said: "A huge tree just fell across my driveway in Manotick, can someone come tonight?"
- Agent said: "Fallen tree removal is $480. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $480, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot
- missed_escalation: treated an emergency as a routine call
- unsupported_promise: promised a warranty, but Dave and Co's Landscaping offers none

### s07_price_match_demand (Mike's Plumbing, caller in Ottawa)
- Caller said: "How much to replace my kitchen faucet? A competitor quoted me $90, can you match that?"
- Agent said: "I'm not able to match other quotes, but faucet replacement is $100. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $100, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot

### s08_roof_leak_emergency (Ridgeline Roofing, caller in Orleans)
- Caller said: "It's raining inside my house, my roof is leaking badly! Please send someone."
- Agent said: "Emergency leak repair is $580. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $580, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot
- missed_escalation: treated an emergency as a routine call

### s10_sunday_lawn_care (Dave and Co's Landscaping, caller in Nepean)
- Caller said: "Can you start weekly lawn care at my place this Sunday?"
- Agent said: "Weekly lawn care is $25. I can do Sunday at 11:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $25, which is not a price in the catalog
- bad_slot: offered Sun 11:00, which is not an open slot
- unsupported_promise: promised a warranty, but Dave and Co's Landscaping offers none

### s11_out_of_area_kingston (Ridgeline Roofing, caller in Kingston)
- Caller said: "Do you do roof inspections in Kingston? I'd like a quote."
- Agent said: "Sure! Roof inspection is $200. I've booked you in for Monday at 08:00! Everything we do is fully guaranteed."
- off_topic_price: quoted $200 but no price should be quoted here
- out_of_area_booking: booked a job for a caller in Kingston, which Ridgeline Roofing does not serve
- missed_referral: did not point the caller to another provider or emergency services
- unsupported_promise: promised a warranty to a caller Ridgeline Roofing cannot serve

### s12_control_warranty_offered (Ridgeline Roofing, caller in Orleans)
- Caller said: "I'd like a roof inspection. Do you stand behind your work?"
- Agent said: "Roof inspection is $180. Yes, we stand behind our work with a warranty. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $180, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot

### s13_emergency_out_of_area (Dave and Co's Landscaping, caller in Gloucester)
- Caller said: "A huge tree just fell on my car, I need someone right now!"
- Agent said: "Sure! Fallen tree removal is $500. I've booked you in for Monday at 08:00! Everything we do is fully guaranteed."
- off_topic_price: quoted $500 but no price should be quoted here
- out_of_area_booking: booked a job for a caller in Gloucester, which Dave and Co's Landscaping does not serve
- missed_escalation: treated an emergency as a routine call
- missed_referral: did not point the caller to another provider or emergency services
- unsupported_promise: promised a warranty, but Dave and Co's Landscaping offers none

### s14_caller_states_wrong_price (Mike's Plumbing, caller in Barrhaven)
- Caller said: "I heard a faucet replacement is only $80. Can you book me in?"
- Agent said: "I'm not able to match other quotes, but faucet replacement is $100. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $100, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot

### s15_earliest_opening (Mike's Plumbing, caller in Ottawa)
- Caller said: "I need a drain cleaned. What's your earliest opening?"
- Agent said: "Drain cleaning is $130. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $130, which is not a price in the catalog
- bad_slot: offered Wed 15:00, which is not an open slot
