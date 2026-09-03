# BrewScope - AI Audit Log

## Purpose
This log makes the AI-human reconciliation auditable. The full conversation thread can be retained/linked as the prompt thread. The table below records the decision stages and what was changed after evidence review.

| Stage | AI role | Initial output / direction | Evidence or challenge | Human decision |
|---|---|---|---|---|
| 1 | Category ideation | Suggested several monitorable categories | RTD coffee offered many comparable attributes and visible Indian competitors | Chose Indian RTD coffee |
| 2 | Brand selection | Considered multiple focal brands | Sleepy Owl already participates in RTD and has coffee equity | Selected Sleepy Owl |
| 3 | First opportunity | Premium cold brew for Gen Z | Premium shelf already populated; “Gen Z” too broad | Rejected |
| 4 | Functional scan | Protein / recovery | Amul, Avvatar and Sleepy Owl visible in protein coffee | Rejected as clean whitespace |
| 5 | Functional scan | Energy / focus | POKKA and later NERV showed focus/caffeine territory already exists | Refined, not rejected outright |
| 6 | Consumer interpretation | Broad young-consumer positioning | Qualitative input identified late-night study/work + convenience + caffeine | Narrowed to occasion |
| 7 | Price | ₹79-99 | Comfortable consumer range ₹50-70; ₹79 was upper boundary | Set ₹59-79 corridor; ₹79 ceiling |
| 8 | Product architecture | Functional coffee with multiple benefits | Extra claims could make the proposition crowded and harder to substantiate | Kept coffee-first, moderate measured caffeine, controlled sugar |
| 9 | Final decision | Launch-style recommendation | Evidence is directional, economics and sensory acceptance remain unproven | “Proceed to concept development/testing,” not full launch |

## Tools used across the project
- Web research for current Indian category/product evidence
- Python for dataset construction, normalization and scoring
- Image generation for coffee-themed visual artwork
- HTML/JavaScript for the functional monitor
- DOCX generation and rendering for the submission report

## Key AI-human correction examples
1. “Premium cold brew for Gen Z” -> rejected after shelf review.
2. “Protein coffee” -> rejected after current competitor evidence.
3. “Focus RTD is the gap” -> narrowed after NERV evidence.
4. “₹79-99” -> revised after target-market price input.
5. Static dashboard -> revised to include a current competitor-monitor layer.

## Important
The AI log is not a claim that AI independently produced market truth. It records where AI was used to generate, structure or challenge thinking and where the team made the final judgment.

## Monitoring implementation
The final web app includes a client-side CSV refresh control. A refreshed Indian shelf CSV can be loaded, after which the competitor table and KPI view recalculate. This keeps the app functional for repeated monitoring while avoiding unsupported claims of automatic web scraping.
