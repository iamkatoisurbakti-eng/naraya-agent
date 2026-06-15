# Score-Gated Release Review

Use this when a live app change needs a subjective go/no-go decision after implementation.

## Panel method
Run 3 perspectives:
1. Critic — strict, looks for regressions and fragility.
2. Advocate — generous, highlights what works.
3. Voter — balanced, decides approve/reject.

## Suggested rubric
- Visual polish: 30
- Menu/category or core-flow fit: 20
- Asset health: 20
- Responsiveness: 15
- Regression risk: 15

Score each perspective out of 100, then compute:
- average score
- median score

## Decision rule
- If final score > 60 and there is no critical blocker, changes may be approved.
- If the critic uncovers a serious functional or auth regression, reject even if the average is above 60.
- When scores differ, explicitly note the disagreement instead of hiding it.

## Verification bias
Prefer live checks over build-only confidence:
- HTTP 200 for the rendered page
- cache-busted CSS/asset fetches
- container/runtime env confirmation
- browser smoke when available

## Output format
Keep it short:
- final score
- 2–3 strongest strengths/risks
- approve/reject
- one-sentence reason