# 24h SEO Evaluation Loop

Use this as the canonical prompt/checklist for 24-hour SEO backtests on live Nusantara AI SaaS surfaces.

## Loop structure
- Run on a fixed interval (usually hourly) for 24 repetitions.
- Evaluate the live site with browser evidence and terminal checks.
- Score each run from 0-100.
- If score >= 90, allow safe source-only SEO improvements, then rebuild, deploy, and verify live.
- If score < 90, report only; do not modify source.

## Evidence to collect each run
- Public landing page title/H1/copy clarity.
- robots.txt and sitemap.xml availability.
- Canonical / OG / Twitter metadata presence.
- Mobile readability and CTA clarity.
- Console errors and broken routes/assets.
- Search-intent alignment for Indonesian keywords.

## Debate prompt
Always include:
- strongest argument that SEO is already good
- strongest argument that SEO is weak
- the single highest-impact change if allowed

## Safe action order when score >= 90
1. Patch the smallest source-only SEO improvement.
2. Build.
3. Deploy via bash scripts/deploy.sh.
4. Verify the public live host directly.
5. Re-score after deploy.

## Report format
- score
- decision: no-change | fixed-and-deployed
- top SEO findings
- debate notes
- any changes made
- verification results
- pass/fail