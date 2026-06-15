# KSR888 mobile game launch verification

Use this reference when a KSR888 game card/menu appears clickable on mobile but the launch flow does not reach a valid provider launch page.

## Verify in the right order
1. Test the live site with a mobile user-agent and the exact touch target the user taps.
2. Confirm whether the click lands on the intended route (for KSR888, often `/game_process/{game_code}/{game_provider}` or a provider-launch endpoint).
3. Separate frontend click handling from upstream launch success:
   - If the anchor/route is reached but the response is `10016`, `Player not found`, or `Missing required fields`, the frontend is not the root cause.
   - If mobile taps are opening `/masuk` or another gating page, check the guest/login redirect logic before touching provider code.
4. Re-run the same game on mobile after the container is rebuilt/restarted; KSR888 live PHP/Blade changes may not show until the container is recreated.

## Observed upstream failure patterns
- `{"error":"Failed to launch game","code":10016,"message":"The account has been frozen. Please contact the administrator"}`
- `Player not found`
- `Missing required fields: player_id, game_uid`

## Practical debugging rule
- Do not declare the mobile launch fix complete until one specific game opens a real provider launch URL in the live mobile flow.
- If the live mobile click reaches the expected route but the provider still rejects the request, treat it as a provider/account configuration issue, not a click-target bug.
