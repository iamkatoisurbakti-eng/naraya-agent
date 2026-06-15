---
name: third-party-repo-integration
description: "Evaluate, clone, and map external repositories into the current product without blindly copying them."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [software-development, integration, vendor, repository, mapping, evaluation, architecture]
    category: software-development
---

# Third-Party Repo Integration

Use this skill when the user wants to:
- clone an external repo for inspiration or reuse
- map a third-party project into the current app
- decide which features to adopt, adapt, or defer
- understand a vendor codebase quickly enough to integrate it safely

## Goal

Turn a foreign codebase into a practical integration plan for the current product.
Focus on feature mapping, safe reuse, and minimal-disruption adoption.

## Workflow
## Workflow

1. **Clone or inspect the repo first**
   - Capture the repo locally under `vendor/<repo-name>` or a similar isolated path.
   - Treat vendor code as reference material, not as source of truth for app behavior.
   - If the repo is an affiliate/commission platform, keep the host app's payment/referral tables as the source of truth and map the vendor concepts into them. See `references/affiliate-nusantara-mapping.md`.
   - If the repo is a mobile app or other foreign runtime, inspect it for product concepts first; do not assume the whole stack should be transplanted.

2. **Read the minimum set of files that reveal architecture**
   - `README.md`
   - `package.json`
   - main entrypoints such as `src/index.*`, core engines/services, and example scripts
   - any repo-level instruction file like `CLAUDE.md`, `CONTRIBUTING.md`, or similar
   - for Android/Gradle repos, also inspect `settings.gradle`, top-level `build.gradle`, module `build.gradle`, and any setup guide like `GUIDE.md`

3. **Build a feature map**
   Classify each useful capability into one of three buckets:
   - **Direct use**: can be adopted almost as-is
   - **Adapt**: useful concept, but must be reshaped for the host app
   - **Defer**: interesting but not needed now

   For SDK/repo-to-service migrations, call out whether the vendor is:
   - a library you can call directly
   - a CLI or server that must be wrapped by the host
   - a runtime mismatch (for example, Node SDK into a Python/FastAPI app) that should be translated into native host endpoints

4. **Map features to host-app modules**
   - Identify where each feature belongs in the current app
   - Prefer existing boundaries and patterns over creating a parallel stack
   - Keep the integration path explicit: UI, API, service, background job, or schema
   - For mobile repos, the host mapping can be a lightweight web/API adapter that reproduces the user value without copying the original runtime.
   - For vendor SDKs with a mismatched runtime, map the SDK concepts to host-native routes, validators, and service helpers instead of porting the whole package.

5. **Prioritize MVP first**
   - Identify the smallest set that delivers value quickly
   - Separate nice-to-have enterprise features from core functionality
   - Add a local fallback when the vendor service is optional or unstable.

6. **Verify before you commit to the plan**
   - If code is added, run the relevant build/test checks
   - If the vendor repo has its own verification instructions, follow them
   - When a build fails because of a local type/tooling issue, isolate whether it is pre-existing or introduced by the integration

7. **Close the loop with host-app UX**
   - Add the UI control only after the backend surface exists.
   - Surface the vendor-derived capability through the host app's own design language and navigation.

## Mapping rules

Use a compact mapping table in bullets:
- Vendor feature
- Nusantara equivalent
- Use mode: direct / adapt / defer
- Integration surface: frontend / backend / database / jobs / analytics
- Notes and pitfalls

## Third-party service/API mapping

If the integration target is a provider API instead of a code repository:
- map provider entities to host-app tables first (settings, providers, games, orders, balances)
- identify the real auth flow by probing the live login endpoint before assuming a static bearer token
- treat admin form fields as credentials only if the runtime DB/controller already uses them that way
- prefer local DB/cache as the source of truth for first render, and refresh remote data through explicit sync endpoints or background jobs
- if the provider exposes both legacy and new columns/aliases, keep them synchronized during save/sync so old admin screens continue to work

See `references/provider-api-mapping-and-auth-quirks.md` for the GameXaGlobal session notes and sync pitfalls.

## Practical heuristics

- If the vendor repo is a library/SDK, map its *capabilities* rather than importing its entire API shape.
- If the vendor repo is a full product, extract only the reusable subsystem(s).
- If the vendor README makes strong performance or production claims, verify the actual code paths before repeating them.
- Prefer single-purpose adaptation layers over deep forks.
- Keep secrets, API keys, and provider credentials out of code and out of final responses.
- For external lookup services, probe the health/root endpoint first, then the real lookup endpoint. If the lookup path times out, preserve a local fallback so the host app remains usable.
- For news aggregation integrations, normalize heterogeneous payloads and treat upstream HTTP errors as soft failures. Return a fallback digest if the provider is rate-limited, unavailable, or returns an unexpected shape.
- For WhatsApp/Cloud-API-style vendor repos, treat the vendor wrapper as a capability catalog and map it into the host app's existing auth/session/token model; preserve FlowKirim-style `/api/...` compatibility if upstream docs or clients already expect it.
- When the host app is a different runtime from the vendor repo, keep the integration as a native adapter layer plus local persistence, not a port of the foreign stack.

See `references/news-aggregation-playbook.md` for the ASPRI BERITA integration notes, provider quirks, and verification commands.
See `references/whatsapp-cloud-api-wrapper-and-flowkirim-notes.md` for the WhatsApp Cloud API + FlowKirim compatibility mapping and verification notes.

See `references/news-aggregation-playbook.md` for the ASPRI BERITA integration notes, provider quirks, and verification commands.

## External artifact intake patterns

Treat these as the same broad class of work when the input is coming from outside the host app:

### Archive and dump inspection
- Verify size/type first, then use a second parser if the archive looks malformed.
- Inspect large dumps incrementally instead of loading them whole.
- Prefer recovery and listing over naive extraction when the file may be truncated.
- See `references/archive-dump-intake.md` for the condensed checklist.

### Provider/API doc drafting
- When the user hands over snippets, live docs, or a minified bundle, reconstruct the contract carefully and redact secrets.
- Keep the section hierarchy stable so the draft stays easy to extend.
- See `references/provider-doc-contract-drafting.md` for the condensed drafting rules.

### Model / recipe repo workflows
- Use this for GPU-aware vendor repos like NeMo/Nemotron and similar model-training stacks.
- Check prerequisites, install editable packages, and verify help/imports before declaring success.
- See `references/model-repo-workflows.md` for the condensed install/verify pattern.

## Pitfalls

- Copying a vendor architecture wholesale when the host app already has a different stack.
- Trusting README marketing claims without checking entrypoints and examples.
- Creating a duplicate module when the host app already has the right extension point.
- Forgetting to note what was cloned into `vendor/` and why.
- Missing repo-specific instruction files like `CLAUDE.md` that change the expected workflow.
- Assuming an external repo's skill catalog is fully indexed by the hub. Some repos expose skills only under nested trees like `.agents/skills/`, so you must clone and enumerate the directory directly before concluding that search/install is broken.
- Assuming an API uses a fixed bearer token when the live login flow actually requires a credential exchange first.
- Trying to reuse a Node SDK verbatim inside a Python/FastAPI host. Translate the SDK into native host routes/services instead.

## Output shape

When reporting back, keep it concise and structured:
- what was cloned
- what the repo does
- What can be reused in Nusantara
- What should be deferred
- Next implementation step

## Related support files

- `references/node-service-integration.md` — condensed notes for Node vendor services, endpoint probing, and fallback handling.

## Linked references

- See `references/mapping-playbook.md` for a reusable inspection and mapping checklist.
- See `references/vendor-integration-session-notes.md` for concrete notes from cek-resi and ArenaFinder-Mobile integration.
- See `references/whatsapp-cloud-api-wrapper-flowkirim-and-news-fallback.md` for the WhatsApp Cloud API wrapper mapping and news-provider 404 fallback pattern from this session.
- See `references/whatsapp-cloud-api-wrapper-integration.md` for FastAPI mapping notes and webhook verification quirks.
