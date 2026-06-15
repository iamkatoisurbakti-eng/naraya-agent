# BytePlus/ARK Seedance/Seedream local docs notes

Session source: local files `/root/.hermes/Byte1` through `/root/.hermes/Byte14`.

Use this when working on Nusantara-AI News image/video generation through BytePlus/ARK.

## Local doc map

- `Byte1`, `Byte2`: ARK Chat Completions docs.
  - Endpoint: `POST https://ark.ap-southeast.bytepluses.com/api/v3/chat/completions`
  - Covers text generation and visual understanding.
  - Message content supports `text`, `image_url`, and `video_url` depending on model.
  - Regions include `ap-southeast-1` and `eu-west-1`.
- `Byte3`: Hitem3D generation docs.
  - Endpoint: `POST /api/v3/contents/generations/tasks`
  - Image-to-3D via Hitem3d-2.0; not directly useful for Shorts/news unless 3D assets are explicitly requested.
- `Byte4`: Video Generation API docs.
  - Endpoint: `POST /api/v3/contents/generations/tasks`
  - Seedance video generation: text-to-video, image-to-video, first/last frame, multimodal reference, video with audio/silent video.
  - Seedance 2.0 supports text-to-video with 0 reference images, which matches Nusantara-AI current prompt-only video mode.
  - Important provider caveat: Seedance 2.0 does not support direct upload of reference images/videos containing real human faces except allowed generated/preset/authorized assets. Prefer prompt-only for news automation.
- `Byte5`: Image Generation API docs.
  - Endpoint: `POST /api/v3/images/generations`
  - Seedream image generation/editing: `seedream-5-0-lite`, `seedream-4-5/4-0`, `seedream-3-0-t2i`, `seededit-3-0-i2i`.
  - Prompt guidance: keep image prompts under ~600 English words to avoid scattered details.
  - Image inputs can be URL or lowercase data URL like `data:image/png;base64,...`.
- `Byte6`: ModelArk Coding Plan embeddings.
  - Model: `skylark-embedding-vision`
  - Base URL: `https://ark.ap-southeast.bytepluses.com/api/coding/v3`
  - OpenAI-compatible; useful for future semantic retrieval/knowledge-base, not core video generation.
- `Byte7`-`Byte14`: curl examples for image-to-video, text-to-video, image generation, and image editing.

## Security rule learned

Some local Byte example files contained literal ARK bearer tokens in curl snippets. When opening or reusing them:

1. Do not echo literal `ark-...` tokens in final responses.
2. Immediately sanitize local examples to `Authorization: Bearer $ARK_API_KEY` if a literal token is present.
3. Recommend rotating/revoking any exposed ARK key.
4. Keep `.env` secrets hidden; only report set/missing booleans.

Verification snippet:

```bash
python3 - <<'PY'
from pathlib import Path
import re, json
base=Path('/root/.hermes')
report={}
for i in range(1,15):
    p=base/f'Byte{i}'
    if p.exists():
        text=p.read_text(errors='replace')
        report[p.name]=bool(re.search(r'ark-[A-Za-z0-9_-]{20,}', text))
print(json.dumps(report, indent=2))
PY
```

Expected: all values `false`.

## Nusantara-AI defaults tied to these docs

- `SEEDANCE_BASE_URL` / `ARK_BASE_URL`: `https://ark.ap-southeast.bytepluses.com/api/v3`
- Video endpoint: `/contents/generations/tasks`
- Image endpoint: `/images/generations`
- Current Shorts policy: prompt-only text-to-video (`NEWS_VIDEO_USE_REFERENCE_IMAGE=0`), max 30 seconds, `2 x 15s`, generated-video/SEEDANCE audio, no OpenAI TTS.
- If ARK returns `AccountOverdueError` HTTP 403, treat it as provider billing/account state, not payload failure.
