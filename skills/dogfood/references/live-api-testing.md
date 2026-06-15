# Live API Testing Notes

Session-derived playbook for testing a deployed web app's backend directly from the terminal.

## When to use
- User asks to test/live-check APIs one by one
- Need to separate app bugs from upstream provider failures
- Need fast verification of deployed routes without browser overhead

## Practical flow
1. Enumerate routes from server entrypoint and route files:
   - `src/app.ts`
   - `src/routes/*.ts`
   - `tests/api/*.test.ts`
2. Start with cheap health/version checks:
   - `GET /api/health`
   - `GET /api/version`
3. Authenticate with a known good account and keep the token.
4. Test each endpoint individually with a raw HTTP client (`curl` or Python `urllib`) and record:
   - HTTP status
   - response body
   - whether the behavior matches the contract
5. For resource-producing flows, verify the follow-up resource too:
   - Example: create clipper job, then `GET /api/clipper/jobs/:id`
   - Example: if outputs are static files, verify with `HEAD` or `GET` on the returned URL
6. Distinguish three classes of outcomes:
   - Route bug: wrong status/schema/validation/auth behavior
   - Upstream/provider issue: route is healthy but provider returns 429/402/403/5xx
   - Expected denial: auth/admin/validation guard works as intended

## Useful observations from this codebase
- `/api/generate/*` may succeed at the route level while provider calls fail due to quota, billing, or missing voice IDs.
- Clipper jobs can progress asynchronously; re-query after a short delay before judging failure.
- A `HEAD` request is enough to confirm static clipper outputs are publicly served.
- Payments webhook tests should include an invalid-signature check to confirm HMAC verification.
- Non-admin access to `/api/dashboard/admin/summary` should return 403, not 200.

## Minimal probe pattern
```bash
curl -sS -H "Authorization: Bearer $TOKEN" https://example.com/api/dashboard/summary | jq
curl -sS -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN" \
  -d '{"capability":"text","prompt":"hello"}' https://example.com/api/generate | jq
curl -sSI https://example.com/clipper-output/<job>/<file>
```

## Reporting tip
When a provider fails, report it separately from the API route. Keep the route verdict and the provider verdict as two distinct findings.