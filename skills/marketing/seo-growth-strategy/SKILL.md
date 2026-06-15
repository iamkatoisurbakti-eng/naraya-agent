---
name: seo-growth-strategy
description: Use when planning SEO, content marketing, growth experiments, or go-to-market strategy for a web/SaaS product. Produces keyword clusters, landing page priorities, content briefs, outreach drafts, measurement loops, and safe promotion plans without spam.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, marketing, growth, content, saas, analytics]
    related_skills: [web-app-release-workflow]
---

# SEO Growth Strategy

## Overview
Use this skill to build and iterate SEO/growth strategy for a SaaS product. The workflow prioritizes ethical acquisition: technical SEO, landing pages, content clusters, social/community content, compliant email drafts, analytics instrumentation, and experiment evaluation.

## When to Use
- User asks for SEO strategy, marketing strategy, growth plan, promotion plan, or keyword research.
- User wants iterative evaluation, debate/voting, or multi-agent strategy selection.
- User wants emails or promotional copy, but has not provided explicit sending scope.

Do not use this to send unsolicited bulk email, spam social platforms, or publish content without explicit approval, channel access, and final copy review.

## Workflow
1. Define goal and constraints:
   - Product, URL, ICP, geography/language, budget, timeframe.
   - Conversion goal: signup, top-up, paid subscription, demo, waitlist.
2. Audit current surface:
   - Homepage title/meta/H1/copy, sitemap/robots, indexability, page speed basics.
   - Existing feature pages and gaps.
   - For React/SPA apps, inspect both the HTML shell and route-level client-side SEO behavior.
3. Build keyword map:
   - Brand keywords.
   - Commercial keywords: “AI video generator Indonesia”, “AI image generator Indonesia”, “AI clipper YouTube”, “AI chat gratis Indonesia”.
   - Problem keywords: “buat video AI dari prompt”, “ubah YouTube jadi shorts otomatis”.
   - Comparison keywords: “alternatif Runway/Kling/ElevenLabs Indonesia”.
4. Create page/content plan:
   - One landing page per high-intent feature.
   - Use Bahasa Indonesia first for Nusantara-focused market.
   - Add proof, pricing clarity, FAQ, examples, schema markup.
   - When the homepage is brand-first, add a keyword-rich intro/H1 variant so search intent is not buried behind marketing copy.
5. Promotion plan:
   - Organic posts for TikTok/X/LinkedIn/Facebook communities.
   - Founder/community outreach drafts.
   - Email drafts only for opted-in users/leads.
6. Measurement:
   - Track impressions, clicks, signup conversion, activation, top-up conversion, CAC proxy.
   - Run weekly evaluation and keep/kill experiments.
7. Debate/voting pattern:
   - Have separate agents propose SEO, content/community, and conversion/email strategies.
   - Score each by impact, speed, cost, risk, and fit.
   - Pick top 3 experiments for the next sprint.
8. Recurring growth automation:
   - When a user asks to keep SEO/content/conversion work running in parallel, split it into staggered jobs instead of one overloaded cron.
   - A useful default pattern is: SEO audit/research, content/publishing readiness, and conversion/lead-funnel review on different offsets so outputs do not overlap.
   - After creating multiple jobs, verify each job separately with `cronjob list` so schedule, enabled state, and next run are correct.
   - If a job is meant to stay read-only, keep it read-only; do not silently add posting/sending side effects.
9. For 24-hour looping promotion requests, use the safe scheduled-loop pattern in `references/24h-promotion-loop.md`: iterate strategy/drafts/evaluation without unauthorized posting or email sending.
9. For 24-hour SEO backtests on a live site, use `references/24h-seo-evaluation-loop.md`: score each run, debate pro/con, and allow source-only fixes only when score >= 90.
10. For TikTok/video automation or auto-upload requests, use `references/tiktok-promotion-automation.md`: create daily draft/asset loops by default, and require explicit credentials, permissions, approval policy, and budget before any public upload.
11. For SPA SEO audits in this codebase, consult `references/nusantara-spa-seo-audit.md` for the observed home/news metadata gaps and the fastest 24-hour fix order.
12. For nonstop KSR888 growth automation, split themes into staggered offsets and verify the live job list after every create/update/remove batch; see `references/ksr888-growth-automation-trio.md` for the clean 00/05/15/30/45-minute pattern.

## Deliverables
- SEO audit checklist.
- Keyword clusters and landing-page map.
- 30-day content calendar.
- Email/social copy drafts.
- Experiment backlog with scores.
- Implementation checklist for code changes.

## Common Pitfalls
1. Sending email without consent. Only draft unless the user explicitly provides a compliant recipient list and approval.
2. Publishing unverifiable claims. Avoid “terbaik/termurah” unless backed by proof.
3. Over-optimizing homepage. Create dedicated feature pages for search intent.
4. Ignoring Indonesian terms. Mix English model terms with Indonesian buyer intent.
5. No measurement loop. Every campaign needs metric, target, and review date.

## Verification Checklist
- [ ] No spam or unauthorized posting/sending.
- [ ] Strategy includes keywords, pages, content, and conversion actions.
- [ ] Recommendations are specific to the product and market.
- [ ] Experiments are scored and prioritized.
- [ ] Next actions are clear and measurable.

## Support files
- See `references/24h-promotion-loop.md` for safe 24-hour looping promotion/backtest jobs with debate/voting, multi-perspective evaluation, and no unauthorized external sending/posting.
- See `references/ksr888-seo-recovery.md` for the live PHP-host crawlability recovery sequence, DB-auth failure pattern, and safe verification commands.
- See `references/ksr888-live-seo-snapshot.md` for the May 2026 live audit snapshot: robots/sitemap OK, but homepage missing crawl-visible H1 and JSON-LD schema, plus the fastest verification commands.
