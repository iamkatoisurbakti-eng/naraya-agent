# Session 2026-05-07: Facebook Page automation + new HTML templates

Context: User requested Meta/Facebook Page posting automation and then two new HTML templates: Instagram 4:5 and YouTube Shorts 9:16.

## Facebook Page posting implementation

- Pipeline file: `/root/nusantara-ai-saas/scripts/news-pipeline.ts`.
- Env keys:
  - `NEWS_FACEBOOK_AUTOPOST=1` enables posting unless `--skip-facebook` or dry-run.
  - `META_GRAPH_VERSION=v21.0` default.
  - `META_PAGE_ID` or `FACEBOOK_PAGE_ID`.
  - `META_PAGE_ACCESS_TOKEN` or `FACEBOOK_PAGE_ACCESS_TOKEN`.
- Posting endpoint: `https://graph.facebook.com/{version}/{pageId}/photos`.
- Uses generated Instagram 4:5 image as `source` plus caption/article link as `message`.
- Report records per item:
  - `facebookSent`
  - `facebookPostId`
- If credentials are missing, step must be `skipped`, not failed.
- Never print Page Access Token; report only set/missing.
- Secret installer created: `/root/nusantara-ai-saas/scripts/set-meta-page-secrets.sh`.

## Template files created

- Instagram 4:5:
  - `/root/nusantara-ai-saas/templates/nusantara_instagram_4x5.html`
  - Canvas: 1080x1350, `data-aspect="4:5"`.
  - Required selectors for screenshot automation:
    - `#slide`
    - `#hookText`
    - `#descText`
    - `#catPill`
    - `#slideCounter`
    - `#imgZone`
- YouTube Shorts 9:16:
  - `/root/nusantara-ai-saas/templates/nusantara_shorts_9x16.html`
  - Canvas: 1080x1920, `data-aspect="9:16"`.
  - Required selectors:
    - `#shorts-canvas`
    - `#slide` (alias compatibility)
    - `#videoZone`
    - `#imgZone`
    - `#hookText`
    - `#descText`
    - `#catPill`
  - Includes visual CTA: `Subscribe Nusantara-AI News`.

## Env defaults updated

- `.env` and `.env.example` now point to:
  - `NEWS_IMAGE_CARD_TEMPLATE_PATH=/root/nusantara-ai-saas/templates/nusantara_instagram_4x5.html`
  - `NEWS_VIDEO_OVERLAY_TEMPLATE_PATH=/root/nusantara-ai-saas/templates/nusantara_shorts_9x16.html`
  - `NEWS_INSTAGRAM_ASPECT=4:5`

## Validation recipe

Run from `/root/nusantara-ai-saas`:

```bash
npm run build:server
bash -n scripts/run-youtube-hourly-queue.sh
bash -n scripts/youtube-scheduled-upload.sh
bash -n scripts/set-meta-page-secrets.sh
node - <<'NODE'
const fs=require('fs');
const templates={
  instagram:'templates/nusantara_instagram_4x5.html',
  shorts:'templates/nusantara_shorts_9x16.html'
};
const required={
  instagram:['id="slide"','data-aspect="4:5"','--w: 1080px','--h: 1350px','id="hookText"','id="descText"','id="catPill"','id="slideCounter"','id="imgZone"'],
  shorts:['id="shorts-canvas"','data-aspect="9:16"','--w: 1080px','--h: 1920px','id="videoZone"','id="imgZone"','id="hookText"','id="descText"','id="catPill"','Subscribe Nusantara-AI News']
};
for (const [name,file] of Object.entries(templates)) {
  const html=fs.readFileSync(file,'utf8');
  const missing=required[name].filter(s=>!html.includes(s));
  if (missing.length) throw new Error(`${name} missing ${missing.join(', ')}`);
}
console.log('template-validation-ok');
NODE
```

## Pitfalls

- A Meta Business Manager link is not enough for posting. Facebook Page posting requires Page ID + Page Access Token with proper Page permissions.
- Dry-run should include the `post-facebook-page` step but skip live posting.
- Do not restart a running queue silently after template/env updates unless the user requested it; note that a running queue needs restart to pick up new env/template paths.
- Keep generated visuals as event/behavior scenes; text/headline belongs in templates, not image/video generation prompts.
