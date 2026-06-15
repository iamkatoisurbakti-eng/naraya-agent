# KSR888 Mobile Homepage Game Selection

## When this applies
Use this note when editing the KSR888 mobile homepage ordering or the GAME TERPOPULAR / provider sections.

## Pattern learned
- Mobile homepage order should be: progressive jackpot -> banner slider -> provider section -> GAME TERPOPULAR.
- GAME TERPOPULAR should be sourced from active providers only.
- Show at most one game per provider code.
- Exclude games without a usable image.
- If controller data is incomplete, keep a Blade fallback that still dedupes by provider and filters missing images.
- After editing Blade/PHP, copy files into the live KSR888 container and restart it before verifying.

## Verification
- Check rendered mobile HTML for the expected order.
- Confirm no duplicate provider codes in GAME TERPOPULAR.
- Confirm no empty image entries are rendered.
