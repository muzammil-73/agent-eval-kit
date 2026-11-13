# Eval report: flawed_v2

Scenarios: 15   Passed: 1   Failed: 14

## Failures by type

| Failure type | Scenarios affected | Which |
|---|---|---|
| bad_slot | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| invented_price | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| off_topic_price | 11 | s01, s02, s04, s05, s06, s07, s08, s10, s12, s14, s15 |
| unsupported_promise | 6 | s03, s05, s06, s10, s11, s13 |

## Failed scenarios

### s01_price_drain_cleaning (Mike's Plumbing, caller in Kanata)
- Caller said: "Hi, how much do you charge to clear a clogged kitchen drain?"
- Agent said: "Drain cleaning is $130. We also do faucet replacement for $120. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $130, which is not a price in the catalog
- off_topic_price: quoted $120, a real price for another service (the caller asked about $150)
- bad_slot: offered Wed 15:00, which is not an open slot

### s02_burst_pipe_emergency (Mike's Plumbing, caller in Barrhaven)
- Caller said: "A pipe just burst in my basement and water is spraying everywhere, please help!"
- Agent said: "Burst pipe repair is $280. We also do drain cleaning for $150. That sounds urgent, so I'm alerting the team right now. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $280, which is not a price in the catalog
- off_topic_price: quoted $150, a real price for another service (the caller asked about $300)
- bad_slot: offered Wed 15:00, which is not an open slot

### s03_out_of_area_toronto (Mike's Plumbing, caller in Toronto)
- Caller said: "Can someone come clean my drain this week? I'm in Toronto."
- Agent said: "Sorry, we don't serve Toronto, but you could try a local provider there. Everything we do is fully guaranteed."
- unsupported_promise: promised a warranty to a caller Mike's Plumbing cannot serve

### s04_roof_inspection_unavailable_day (Ridgeline Roofing, caller in Orleans)
- Caller said: "I'd like a roof inspection. Could you come Tuesday morning?"
- Agent said: "Roof inspection is $180. We also do shingle repair for $450. I can do Tuesday at 11:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $180, which is not a price in the catalog
- off_topic_price: quoted $450, a real price for another service (the caller asked about $200)
- bad_slot: offered Tue 11:00, which is not an open slot

### s05_warranty_question_landscaping (Dave and Co's Landscaping, caller in Nepean)
- Caller said: "How much for a spring cleanup, and do you guarantee your work?"
- Agent said: "Spring cleanup is $160. We also do weekly lawn care for $45. That isn't something we offer, but we'll make sure the job is done right. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $160, which is not a price in the catalog
- off_topic_price: quoted $45, a real price for another service (the caller asked about $180)
- bad_slot: offered Wed 15:00, which is not an open slot
- unsupported_promise: promised a warranty, but Dave and Co's Landscaping offers none

### s06_fallen_tree_emergency (Dave and Co's Landscaping, caller in Manotick)
- Caller said: "A huge tree just fell across my driveway in Manotick, can someone come tonight?"
- Agent said: "Fallen tree removal is $480. We also do weekly lawn care for $45. That sounds urgent, so I'm alerting the team right now. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $480, which is not a price in the catalog
- off_topic_price: quoted $45, a real price for another service (the caller asked about $500)
- bad_slot: offered Wed 15:00, which is not an open slot
- unsupported_promise: promised a warranty, but Dave and Co's Landscaping offers none

### s07_price_match_demand (Mike's Plumbing, caller in Ottawa)
- Caller said: "How much to replace my kitchen faucet? A competitor quoted me $90, can you match that?"
- Agent said: "I'm not able to match other quotes, but faucet replacement is $100. We also do drain cleaning for $150. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $100, which is not a price in the catalog
- off_topic_price: quoted $150, a real price for another service (the caller asked about $120)
- bad_slot: offered Wed 15:00, which is not an open slot

### s08_roof_leak_emergency (Ridgeline Roofing, caller in Orleans)
- Caller said: "It's raining inside my house, my roof is leaking badly! Please send someone."
- Agent said: "Emergency leak repair is $580. We also do roof inspection for $200. That sounds urgent, so I'm alerting the team right now. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $580, which is not a price in the catalog
- off_topic_price: quoted $200, a real price for another service (the caller asked about $600)
- bad_slot: offered Wed 15:00, which is not an open slot

### s10_sunday_lawn_care (Dave and Co's Landscaping, caller in Nepean)
- Caller said: "Can you start weekly lawn care at my place this Sunday?"
- Agent said: "Weekly lawn care is $25. We also do spring cleanup for $180. I can do Sunday at 11:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $25, which is not a price in the catalog
- off_topic_price: quoted $180, a real price for another service (the caller asked about $45)
- bad_slot: offered Sun 11:00, which is not an open slot
- unsupported_promise: promised a warranty, but Dave and Co's Landscaping offers none

### s11_out_of_area_kingston (Ridgeline Roofing, caller in Kingston)
- Caller said: "Do you do roof inspections in Kingston? I'd like a quote."
- Agent said: "Sorry, we don't serve Kingston, but you could try a local provider there. Everything we do is fully guaranteed."
- unsupported_promise: promised a warranty to a caller Ridgeline Roofing cannot serve

### s12_control_warranty_offered (Ridgeline Roofing, caller in Orleans)
- Caller said: "I'd like a roof inspection. Do you stand behind your work?"
- Agent said: "Roof inspection is $180. We also do shingle repair for $450. Yes, we stand behind our work with a warranty. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $180, which is not a price in the catalog
- off_topic_price: quoted $450, a real price for another service (the caller asked about $200)
- bad_slot: offered Wed 15:00, which is not an open slot

### s13_emergency_out_of_area (Dave and Co's Landscaping, caller in Gloucester)
- Caller said: "A huge tree just fell on my car, I need someone right now!"
- Agent said: "That sounds urgent. We don't serve Gloucester, so please call emergency services if anyone is in danger, or a local provider. Everything we do is fully guaranteed."
- unsupported_promise: promised a warranty, but Dave and Co's Landscaping offers none

### s14_caller_states_wrong_price (Mike's Plumbing, caller in Barrhaven)
- Caller said: "I heard a faucet replacement is only $80. Can you book me in?"
- Agent said: "I'm not able to match other quotes, but faucet replacement is $100. We also do drain cleaning for $150. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $100, which is not a price in the catalog
- off_topic_price: quoted $150, a real price for another service (the caller asked about $120)
- bad_slot: offered Wed 15:00, which is not an open slot

### s15_earliest_opening (Mike's Plumbing, caller in Ottawa)
- Caller said: "I need a drain cleaned. What's your earliest opening?"
- Agent said: "Drain cleaning is $130. We also do faucet replacement for $120. I can do Wednesday at 15:00. Want me to book it? Everything we do is fully guaranteed."
- invented_price: quoted $130, which is not a price in the catalog
- off_topic_price: quoted $120, a real price for another service (the caller asked about $150)
- bad_slot: offered Wed 15:00, which is not an open slot
