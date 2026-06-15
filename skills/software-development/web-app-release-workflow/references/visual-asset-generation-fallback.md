# Visual Asset Generation Fallback

Use this pattern when a requested PNG/banner/popup asset should live in a web app repo but the image generator is unavailable or misconfigured.

## Session note
- In this session, the image-generation tool failed because `FAL_KEY` was missing.
- Fallback used: compose the asset locally with Pillow in `python3`, then verify the result with a vision pass.
- Output path used: `/root/nusantara-ai-saas/KSR888/pop-up.png`.

## Practical fallback flow
1. Check whether the generator is actually available/configured.
2. If not, build the raster asset locally with PIL / terminal scripting.
3. Keep the composition centered, high-contrast, and readable at the target aspect ratio.
4. Verify with a vision check for:
   - text readability
   - centering
   - cropped edges
   - CTA prominence
5. Save the final PNG into the repo path the user asked for.

## Pitfalls
- Do not keep retrying the same unavailable generator call if the key/env is missing.
- Do not ship a decorative asset without verifying the final raster looks balanced at its real size.
- If the asset is a popup, prioritize modal readability over packing in too many extra badges or labels.
