# KSR888 category/provider priority and detail routing

## When to use
Use this note when working on imported PHP hosts like KSR888 where game/provider cards must:
- point to the correct category/detail page
- follow provider priority from API payloads
- stay fast by reading images from DB/cache instead of live provider fetches

## Source-of-truth rules
- Keep provider/game rows in the DB as the render source of truth.
- Persist provider images (`provider_image`, `banner`, `mobile_banner`) during sync.
- Keep homepage rendering on cached DB rows; do not depend on live provider API fetches at render time.
- If the product wants only one active game API, keep the DB config row canonical and clear legacy provider API columns.

## Detail routing pattern
- Put the route mapping in a model accessor such as `detail_url`.
- Map `game_type` / `provider_type` to the correct category route instead of hardcoding route strings in each Blade view.
- Reuse the same accessor in:
  - homepage game rows
  - category game lists
  - provider rows/cards
- Keep category navigation consistent across desktop/mobile views.

## Provider ordering pattern
- Use API payload order as the first priority when category providers are merged.
- If the API does not provide a stable order, fall back to:
  1. `game_count` descending
  2. provider name ascending
- Preserve the API rank in a temporary field such as `__priority` before sorting.
- Apply category/type filters after merging API and DB rows so the visible category stays correct.

## Verification
1. Run syntax checks on the controller/model/view files you touched.
2. Deploy/restart the host-specific web service.
3. Probe live pages with `curl` and grep for:
   - category route hrefs
   - `detail_url`-driven links
   - image proxy URLs such as `game-image-proxy`
4. Confirm the live HTML still renders the intended category card set after cache refresh.

## Pitfalls
- Hardcoding route strings in multiple Blade files causes card/category drift.
- Sorting only by name hides the provider priority coming from the API.
- Rendering from live API calls at page load makes the homepage slow and fragile.
- If the homepage should not show a provider showcase section, remove the section entirely rather than hiding it with CSS.
