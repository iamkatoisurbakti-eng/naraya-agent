# News card prompting for 4:5 Instagram renders

Use this when generating the hero image that will be composited into the 4:5 news card template.

## Goal
- Produce a realistic, editorial, newsy hero image.
- Leave all headline/branding text to the HTML template.
- Avoid generating any text inside the image itself.

## Recommended prompt pattern

```
Realistic news b-roll image, a clean editorial scene that visually represents: "{JUDUL BERITA}". {KONTEKS SINGKAT}. Photorealistic, natural lighting, modern Indonesian context, strong visual storytelling, cinematic composition, subject clearly centered, authentic real-world details, high detail, social-media friendly, no text, no logo, no watermark, no captions, no signage, no infographic, no poster elements.
```

## Shorter variant

```
Breaking news style photo, realistic documentary image, visually illustrating: "{JUDUL BERITA}". {KONTEKS SINGKAT}. Cinematic lighting, authentic expressions, newsworthy atmosphere, high detail, no text, no logo, no watermark, no signage.
```

## Negative prompt

```
text, typography, letters, words, subtitle, caption, watermark, logo, brand, sign, poster, flyer, infographic, UI, menu text, fake text, gibberish letters, blurry, low quality, extra fingers, deformed hands
```

## Workflow notes
- Put the headline in the template's text fields, not in the image prompt.
- Keep the image visually descriptive but text-free.
- If the user wants a card like the reference screenshot, use a black outer background, a rounded light hero panel, and a dark bottom text block.
- If the user asks to remove `GEN-Z NEWS`, keep the top pill as `TELEGRAM`, `VIRAL UPDATE`, or another short badge.
