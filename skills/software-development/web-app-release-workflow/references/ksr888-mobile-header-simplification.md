# KSR888 mobile header simplification

Session takeaway from a cluttered mobile landing/header:

## Symptom
- Mobile hero/header showed a huge repeated title, duplicated branding, and too much copy above the fold.
- The page looked visually noisy even though the site was functional.

## Fix pattern
1. Inspect both the page assembly file and the template partial; imported PHP hosts often split the visible UI across multiple files.
2. Remove duplicate hero headings first.
3. Replace long hero paragraphs with one short, action-oriented line.
4. Shrink marquee/running-text content to a neutral short phrase.
5. Keep only one clear action row above the fold.
6. Re-check desktop and mobile versions separately; a fix in `mobile/template/home.php` may not fully affect `mobile/index.php`, and desktop may still carry old hero copy in `dekstop/template/home.php`.

## Verification
- Grep the relevant PHP templates for the old headline string.
- Confirm the visible copy is now short and action-first.
- Prefer a live mobile screenshot or browser check when possible, because build success alone does not prove the clutter is gone.