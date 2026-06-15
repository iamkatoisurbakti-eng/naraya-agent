# Feature Removal / Backend Teardown Checklist

Use this when the user asks to remove a feature completely from a production repo.

## Checklist
1. Search source, tests, generated build output, and deployment files for the feature name and route/path variants.
2. Remove the backend route mount, route file, static output route, job scheduler, worker entrypoint, and any schema/table additions.
3. Remove UI entry points: sidebar items, cards, imports, conditional renders, and any dead component files.
4. Remove tests that target the deleted feature, then add a negative smoke check if the feature should now 404.
5. Remove Dockerfile/package/deploy references that copy or install the feature's vendor/runtime dependencies.
6. Rebuild the project, then delete any stale generated `dist/` artifacts that still reference the feature.
7. Run the focused test slice, then full build, then redeploy.
8. Smoke-test the live endpoint after deploy to confirm the route is gone or behavior changed as requested.

## Gotchas observed
- A clean source tree can still leave old endpoints in `dist/` until the next build or manual cleanup.
- Deleting the route file alone is not enough if the app still imports or mounts it.
- If the feature used a job table, update schema initialization and any test fixtures together or the app can recreate the table on startup.
- When removing a feature that added a static asset route, verify both API and static paths; users can still hit old output URLs even after the API is gone.
