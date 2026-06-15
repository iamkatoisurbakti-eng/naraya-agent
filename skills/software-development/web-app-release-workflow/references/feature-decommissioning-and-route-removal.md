# Feature Decommissioning and Route Removal

Use this checklist when the user wants a feature fully removed from a Dockerized React + Express app.

## Remove all runtime surfaces
- Delete the frontend entry point: nav item, card, section, modal, and any polling/fetch logic.
- Unmount the backend router from `src/app.ts` or equivalent.
- Remove feature-specific static asset routes.
- Delete the route file if it is no longer used anywhere.
- Update tests to assert absence or 404, not the old happy path.

## Clean source references
- Search the source tree for the feature keyword after each patch.
- Also grep the built browser bundle after `npm run build` for user-visible leftovers.
- Check landing pages, dashboards, auth flows, payment copy, and test fixtures for stale mentions.

## Handle schema/ledger leftovers
- If the feature created a table, enum, ledger reason, or other schema artifact, decide explicitly whether it is still needed.
- If it is not needed, remove the code references and plan a safe migration/drop path.
- Do not assume deleting the route file removes the feature from persistence.

## Verification
- `npm run build`
- relevant API/e2e tests
- runtime HTTP check for the removed endpoint returns 404
- grep the built bundle for the removed feature name

## Pitfall
- A feature can be “gone from the UI” but still linger in backend schema or copy. Treat those as part of the decommission unless the user explicitly wants to keep them.