# Seedance Template Guidance for Clean News Flyers

Use this when prompting Seedance to generate the visual layer for a flyer/poster.

## Core rule
Seedance should generate only the image content that belongs in the transparent/top visual slot. The rest of the flyer layout stays fixed in HTML/CSS.

## Prompt pattern
- State the canvas is a template with a transparent image area.
- Ask Seedance to fill only the top visual region.
- Explicitly forbid text, logos, watermarks, captions, or UI-like overlays.
- Ask for realistic, editorial, documentary-style imagery that matches the news topic.
- Keep the composition clean and professional.

## Good wording
"Use this as a fixed poster template. Generate only the visual in the transparent top area. Do not generate the white or lower text panel. No text, no watermark, no logo, no caption, no frame. Make the image look like a clean editorial news photo."

## Pitfalls
- Do not ask the model to recreate the whole flyer.
- Do not let the model invent typography; the HTML handles copy.
- Do not place source text inside the flyer if the user said no source.
- If the visual looks messy, tighten the prompt before changing the layout.
