# KSR888 GameXaGlobal provider/navigation consistency

Use this reference when the task is to make KSR888 front provider lists and play links stay aligned with GameXaGlobal API output.

## What this session established
- Front provider lists should come from GameXaGlobal API, not stale local provider tables, when the goal is the public provider surface.
- `ViewServiceProvider` is a good place to hydrate shared navbar data from GameXaGlobal because the navbar needs both games and providers.
- Version cache keys when changing provider-source semantics, otherwise stale local-provider collections can survive deploys.
- Provider cards should continue using model accessors such as `frontend_provider_image`, `frontend_mobile_image`, and `frontend_banner_image` so image fallback stays centralized.
- Provider cards and navbar cards should link to the same launch path pattern used by the controller: `/game_process/{game_code}/{game_provider}` for game tiles and `detail_url`/`provider-launch` for provider tiles.

## Cleanup checklist
1. Search Blade files for hardcoded provider brands and static image buckets.
2. Replace static provider arrays with API-driven collections.
3. Keep `detail_url` on provider objects as the single front-end link target for provider tiles.
4. Make sure any game tile that should launch directly uses the `game_process` route, not `/slots/`.
5. Add fallback images in the view only if the model accessor can still return an empty string.
6. Clear or version caches after switching provider sources.

## Pitfalls
- A view can look dynamic but still be indirectly hardcoded if the shared view composer is still querying local `providers`.
- If the navbar shows API-driven provider tiles but the play card still points to `/slots/`, the front end feels inconsistent even though the provider list is technically dynamic.
- After changing provider-source logic, stale cache keys are the most common reason old providers keep showing.
- Do not assume a provider list is correct unless both the provider tile and the play path resolve from the same API-backed object.

## Verification
- Check that front provider collections render from GameXaGlobal payloads.
- Confirm the navbar and provider rows still render when the API is unavailable by falling back cleanly.
- Verify one provider tile, one game tile, and one mobile tile all route to the intended launch path.
- Re-read any rewritten Blade after patching; indentation drift can hide accidental markup damage.