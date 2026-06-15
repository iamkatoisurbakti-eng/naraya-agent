---
name: seo-growth
version: 1.0.0
description: Use when planning, auditing, or executing SEO/growth work for SaaS products, especially Nusantara AI SaaS. Covers technical SEO, keyword strategy, content clusters, landing-page optimization, safe outreach, measurement, and iteration.
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, growth, marketing, saas, content, outreach, analytics]
    related_skills: [web-app-release-workflow]
---

# SEO Growth

## Overview
Use this skill to improve discoverability and conversion for a SaaS website without guessing or exposing internal secrets. The workflow prioritizes measurable SEO changes, content clusters, landing-page intent matching, compliant outreach, and repeatable evaluation.

## When to Use
- User asks for SEO, marketing strategy, growth loops, content strategy, backlink ideas, or conversion optimization.
- User asks to promote a SaaS/product but has not provided explicit recipients or consent lists.
- User wants iterative evaluation/backtesting of marketing ideas.

## Core Workflow
1. Define the offer and ICP:
   - Product category, target users, core problems solved, pricing, geography/language.
   - For Nusantara AI SaaS: Indonesian AI studio for chat, image, video, voice/audio, AI clipper, free chat models, paid top-up credit.
2. Segment intent:
   - Informational: tutorials, comparisons, use cases.
   - Commercial: alternatives, pricing, best tools, local-language searches.
   - Transactional: free AI chat, AI video generator, AI clipper, top-up credit.
3. Audit technical SEO:
   - Title/meta/OG/Twitter tags, canonical URL, sitemap.xml, robots.txt, structured data, page speed, mobile, indexability.
   - For `news.nusantara-ai.online`, treat article/category routes as first-class SEO surfaces and verify public endpoints after deploy. See `references/news-subdomain-seo.md`.
   - Never print env secrets or analytics tokens.
4. Build keyword clusters:
   - Bahasa Indonesia first, then English expansion.
   - Prefer long-tail keywords with high intent and low competition.
5. Create page/content plan:
   - One landing page per major intent; FAQs with schema; internal links to studio/features.
   - Use clear benefits, screenshots, pricing, examples, trust signals, and CTAs.
   - For SPA homepages like `nusantara-ai.online`, align shell metadata (`web/index.html`) and hydrated runtime metadata (`document.title` + meta tags in React) together; otherwise search-visible HTML and client-side copy drift. See `references/homepage-cta-and-spa-seo.md`.
   - Prefer intent-led hero copy over generic branding when the page is meant to rank and convert. In this repo, terms like `AI Chat gratis`, `AI video generator`, `image studio`, `voice agent`, and `AI clipper` outperformed vague creative-language positioning.
6. Outreach safely:
   - Do not send cold spam automatically.
   - Draft emails/DMs only, or send only to user-provided opt-in/owned lists with explicit approval.
   - Include unsubscribe/compliance language for bulk email.
7. Measure:
   - Track search impressions/clicks, signups, activation, paid conversion, CAC, conversion rate.
   - Prefer experiments with UTM links and clear hypotheses.
8. Iterate:
   - Run a debate/evaluation loop: propose → score → pick → test → evaluate → refine.
9. For 24-hour SEO backtests on a live site, use `references/24h-seo-evaluation-loop.md` as the repeatable pattern for browser/terminal evidence, debate notes, and score-gated fixes.
10. For live landing-page evaluation loops on sites like `tourguide.nusantara-ai.online`, use `references/live-site-24h-eval-loop.md` for score-gated changes, build/deploy verification, and concise evidence-driven reporting.
11. For recurring A/B-style live SEO evaluations and 24h backtesting, use `references/live-seo-ab-looping.md` to keep the scoring rubric, voting, and live-host verification consistent.

12. For Google Search Console automation from a CLI/server, prefer OAuth Desktop credentials when service accounts cannot be added to GSC (`email tidak ditemukan`); persist PKCE `code_verifier`, handle localhost redirects safely, and never claim GSC access until `sites().list()` shows the property. See `references/google-search-console-oauth-automation.md`.

## Debate Scoring Rubric
Score 1-5 for each idea:
- Impact: likely signups/revenue.
- Confidence: evidence strength.
- Speed: can ship/test quickly.
- Cost: low cost scores higher.
- Risk: compliance/reputation risk; low risk scores higher.

ICE-like score: `(Impact + Confidence + Speed + Cost + Risk) / 5`.

## Nusantara AI SaaS Keyword Seeds
- ai chat gratis indonesia
- ai video generator indonesia
- seedance ai video generator
- ai clipper youtube shorts
- generator video ai bahasa indonesia
- ai image generator indonesia
- text to video ai indonesia
- alternatif chatgpt gratis indonesia
- tools ai konten kreator indonesia
- buat video pendek dari youtube otomatis

## Safe Outreach Templates
Use only for opt-in lists or drafts requiring approval.

Subject: Coba Nusantara AI untuk bikin konten AI lebih cepat

Halo {name},

Saya ingin mengenalkan Nusantara AI, studio AI berbahasa Indonesia untuk Chat AI gratis, generate gambar/video, voice/audio, dan AI Clipper untuk membuat konten pendek dari YouTube.

Kalau relevan untuk workflow konten Anda, saya bisa kirim demo singkat atau akses trial.

Terima kasih,
{sender}

## Common Pitfalls
1. Promosi otomatis ke alamat yang tidak jelas izinnya. Draft boleh; kirim hanya dengan approval dan daftar opt-in.
2. Mengoptimasi homepage saja. Buat halaman per intent/fitur.
3. Keyword terlalu umum seperti “AI” tanpa intent lokal/komersial.
4. Tidak memasang sitemap/canonical/structured data.
5. Tidak mengukur funnel dari impression → signup → aktivasi → paid.
6. Relying on client-side title/meta only for news/article routes. For `news.nusantara-ai.online`, the host should also expose `robots.txt` and `sitemap.xml`, and article/category pages should be verified publicly after deploy.

9. For 24-hour SEO backtests on a live site, use `references/24h-seo-evaluation-loop.md` as the repeatable pattern for browser/terminal evidence, debate notes, and score-gated fixes.
10. For live landing-page evaluation loops on sites like `tourguide.nusantara-ai.online`, use `references/live-site-24h-eval-loop.md` for score-gated changes, build/deploy verification, and concise evidence-driven reporting.
11. For recurring A/B-style live SEO evaluations and 24h backtesting, use `references/live-seo-ab-looping.md` to keep the scoring rubric, voting, and live-host verification consistent.
11. For public-domain SEO patches behind Docker/reverse proxies, verify both the source/container HTML and the live origin HTML with cache-busting queries; if they diverge, inspect the actual upstream service and cache layers. See `references/live-deploy-verification.md`.
12. For Google Search Console API work, prefer OAuth with the actual GSC owner account when service-account sharing fails or the UI says the service-account email is not found. For `web` OAuth clients, add `http://localhost:1/` as an authorized redirect URI, then exchange the full redirected URL. See `references/google-search-console-oauth-and-starlink-loop.md`.
13. For fast traffic ramps, use the 7-day execution loop in `references/7day-seo-traffic-ramp.md`: one pillar page, several long-tail support pages, one trust/comparison page, then internal links + snippet tuning + Search Console review.
13. For `starlinkindonesia.shop` AMP/GSC work, use `references/starlink-amp-seo-24h-loop.md`: 4 focused URLs, AMP validator, GSC-readiness checks, responsible-play wording, and the no-heavy-logo performance constraint.
14. For `starlinkindonesia.shop` KSR888 AMP/GSC readiness, use `references/starlink-amp-seo-24h-loop.md`: AMP-valid static pages, focused host sitemap, safe slot-keyword wording, hourly 24h multi-agent GSC-readiness/backtest loop, and no false claim of indexing without GSC/API evidence.
13. For `starlinkindonesia.shop` KSR888 AMP SEO work, use `references/starlink-amp-seo-24h-loop.md`: focused AMP-valid root page, three support pages, host-specific sitemap, FAQ schema, responsible-play wording, AMP validator checks, and 2-hour x 12-run backtest loop.
