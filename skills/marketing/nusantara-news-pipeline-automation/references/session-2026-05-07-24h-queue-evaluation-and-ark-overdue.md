# 2026-05-07: 24h Queue Evaluation + ARK AccountOverdueError

Context: User asked to evaluate the 24-hour nonstop Nusantara-AI News YouTube Shorts automation after enabling cinematic, copyright-safe, narration-fill, and growth mode.

Observed safe status checks:
- Poll active Hermes process session first, then verify OS process tree with `ps -eo pid,ppid,etime,cmd` filtered for `run-youtube-hourly-queue.sh`, `news-youtube-hourly-queue.ts`, and `gen:news-youtube-queue`.
- Inspect `/root/nusantara-ai-saas/data/logs/youtube-hourly-queue.log` and `/root/nusantara-ai-saas/data/logs/youtube-hourly-queue-state.json` as JSON lines/state.
- Run build validation: `npm run build:server >/tmp/news-24h-eval-build.log`.
- Check `.env` only as key set/missing + non-secret numeric/boolean defaults; never print credential values.
- Check public news API with `curl -sS --max-time 20 https://news.nusantara-ai.online/api/news/articles` and parse nested shape: response may be `{ articles: { articles: [...] } }`, not a flat array.

Result from evaluation:
- Queue was running as one process chain; no duplicate queue process.
- Current 24h state fields showed slots=24, intervalSeconds=3600, monitorHours=24, strictNoDuplicate=1, historyMaxItems=240, scarcityPolicy=skip-slot-if-no-unique-viral-news, youtubeGrowthMode=1.
- Credential statuses: YouTube/OAuth, ARK, OpenAI, Telegram set; Meta page access token missing.
- Public news API returned HTTP 200 and article data.
- Slot 1 failed before upload because ARK/BytePlus media generation returned HTTP 403 `AccountOverdueError` on `images/generations` or `contents/generations/tasks`.

Important diagnosis:
- `AccountOverdueError` is a provider billing blocker, not a coding, YouTube, Telegram, or article route failure.
- While queue remains alive, every future slot that relies on ARK image/video generation is likely to fail until the ARK/BytePlus balance/overdue issue is fixed or a fallback provider/path is enabled.

Future handling:
1. Report queue runtime separately from production-output health:
   - queue/process/config can be healthy while content production is blocked.
2. Do not claim YouTube uploads are working if media generation never produced a final MP4.
3. Recommend resolving ARK/BytePlus billing first.
4. For resilient 24h automation, add or enable fallback media generation when provider errors include `AccountOverdueError`, `rate limit`, or transient 5xx.
5. If adding fallback, keep copyright-safe/event-scene/center-safe/cinematic/growth constraints active in fallback prompts.
