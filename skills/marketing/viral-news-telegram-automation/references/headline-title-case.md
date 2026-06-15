# Headline title handling notes

Use these rules when a news title looks awkward, all-caps, or sliced from a feed.

## Goal
Produce titles that are:
- readable in a flyer/video card
- natural Indonesian
- compact enough for the template
- not over-slurred by headline cleanup

## Normalization rules
1. Strip noisy prefixes:
   - `Foto:`, `Video:`, `Breaking:`, `News:`, `Viral:`
   - `Berita`, `Update`
2. Preserve acronyms and number tokens:
   - `SDM`, `OJK`, `QRIS`, `5G`, `16:9`
3. Convert the remaining title to title case, but keep short function words lower when they appear in the middle:
   - `dan`, `di`, `ke`, `dari`, `untuk`, `pada`, `oleh`, `dalam`, `sebagai`, `serta`
4. Prefer the full cleaned title first, then shorten by word boundary if needed.
5. Do not chop in the middle of a clause unless there is no alternative.

## Recommended helpers
- `normalizeNewsTitle()` for title cleanup + casing
- `smartTruncateText()` for boundary-aware shortening
- `buildCardHeadline()` for the final card headline

## Quick examples
- `foto: evakuasi penumpang kapal pesiar yang terpapar hantavirus` → `Evakuasi Penumpang Kapal Pesiar yang Terpapar Hantavirus`
- `breaking: ojk imbau masyarakat waspada penipuan tiket event olahraga` → `OJK Imbau Masyarakat Waspada Penipuan Tiket Event Olahraga`
- `kapolri hadiri rakernis reskrim: jadi upaya penguatan sdm dan profesionalisme` → `Kapolri Hadiri Rakernis Reskrim: Jadi Upaya Penguatan SDM dan Profesionalisme`
