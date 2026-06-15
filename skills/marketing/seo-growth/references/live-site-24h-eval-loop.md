# Live Site 24h Evaluation Loop

Use this pattern for live landing-page backtesting on Nusantara AI sites such as `tourguide.nusantara-ai.online`.

## Loop goals
- Evaluate UX, copy clarity, conversion readiness, performance, SEO, and marketing fit over 24 hours.
- Compare each run against the previous result; only recommend changes when a measurable improvement opportunity exists.
- If the score is at or above 90 and the fix is low-risk and clearly beneficial, the agent may patch source, run build, deploy, and verify live.

## Evidence sources
- Browser inspection of the live page.
- `curl -I` / `curl` for live availability and metadata checks.
- Source inspection in `/root/nusantara-ai-saas`.
- `npm run build` and `bash scripts/deploy.sh` after changes.

## Practical workflow
1. Inspect live page and note score.
2. Compare with prior hour and identify deltas.
3. Decide whether the issue is real and low-risk.
4. If score >= 90 and improvement is clear: patch source, build, deploy, verify live.
5. Otherwise, report findings and suggested fixes only.

## Tour guide session specifics
- Live target: `https://tourguide.nusantara-ai.online`
- Common jobs used:
  - `tourguide-website-24h-eval`
  - `tourguide-seo-24h-eval`
  - `tourguide-marketing-24h-eval`
- The loop was used to monitor and optionally improve a Bali tour-guide landing page for international travelers.

## Pitfalls
- Do not make speculative edits without a clear measured issue.
- Do not skip build/deploy verification after source changes.
- Keep the scoring/backtest narrative concise and evidence-based.
