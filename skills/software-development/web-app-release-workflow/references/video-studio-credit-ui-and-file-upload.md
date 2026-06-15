# Video studio file-upload + credit badge notes

Context: session update for the Nusantara AI SaaS video studio.

## Learned pattern
- When the user asks for media references to be files, not links, convert the frontend inputs to `File | null` state and submit JSON payloads as data URLs (`{ name, type, dataUrl }`).
- Backend should persist uploaded assets under `data/generate-assets/<jobId>/...` and expose them via a static `/generated-media/...` route.
- Keep URL cleaning permissive enough to accept already-stored `/generated-media/...` paths, but do not rely on user-pasted external links for the upload-only flow.

## Runtime verification pitfall
- Repo-wide TypeScript may be noisy and unrelated to the feature change.
- Prefer a small runtime probe with an isolated test DB/env to confirm the upload path actually stores files and returns a generation response.
- A `503 PROVIDER_NOT_CONFIGURED` during the probe can still be a valid success signal for the upload/storage path if the files are present on disk.

## Filename handling
- When storing uploaded assets, sanitize names and avoid double extensions.
- Only append the detected extension if the sanitized filename does not already end with it.

## Credit badge pattern
- For generate buttons, show the credit cost inline on the CTA and also as a small helper note below the button.
- Keep the cost mapping capability-based in the UI so the user sees the exact deduction before submitting.
- Current repo mapping used during the session:
  - text: 5
  - image: 25
  - video: 250
  - audio: 40
  - voice: 5
