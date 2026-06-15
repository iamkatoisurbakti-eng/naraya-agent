# TikTok promotion automation boundaries

Use when the user asks for automated TikTok/video promotion, daily generation, auto-upload, or promotion "outside my control".

## Safe default
- Do not auto-post, auto-upload, DM, comment, or email without explicit account access, platform permission, final approval, and scope.
- If credentials/API access are missing, create a draft/asset-generation loop instead of publishing.
- Keep public posting under user control by default; publishing to a brand account is an external side effect.

## Daily TikTok draft automation pattern
- Schedule a cron job that produces a daily TikTok-ready package:
  - 9:16 concept for 60-120 seconds
  - time-coded voiceover script
  - 6-10 scenes/shot list
  - prompts for visual/video clips
  - caption, hashtags, CTA, A/B hooks, editing checklist
- For AI video systems capped at short durations (for example Seedance around 15s), plan 4-8 short clips and stitch them into a 60-120s TikTok instead of expecting one long provider render.
- Never mention internal pricing/margin/provider API costs in promotional copy.

## If user wants full auto-upload
Ask for or verify:
- TikTok Business/API access with upload permission
- client id/secret/access token stored in environment only
- target account/handle
- post mode: draft vs direct publish
- posting schedule/timezone
- daily budget/credit cap for video generation
- approval policy for copy/video before publish

## Refusal/redirect wording
Acknowledge the goal, refuse only the unsafe uncontrolled publishing part, then immediately offer/execute the safe automation: strategy loop, draft content generation, SEO changes, opt-in outreach drafts, or approved channel setup.
