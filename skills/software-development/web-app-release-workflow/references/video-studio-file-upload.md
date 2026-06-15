# Video studio file-upload notes

Session-derived pattern for the studio/generate flow when the user wants every reference input to be an uploaded file, not a link.

## Payload shape
- Frontend converts `File` to JSON payload `{ name, type, dataUrl }` using `FileReader.readAsDataURL`.
- Backend accepts file fields alongside the normal generate body, including:
  - `startKeyframeFile`
  - `endKeyframeFile`
  - `referenceImageFile`
  - `referenceVideoFile`
  - `referenceAudioFile`
- Keep URL-based fields only if the provider still needs them for other modes; for the file-upload request path, treat the file payload as the source of truth.

## Storage + serving
- Save uploaded assets under `data/generate-assets/<jobId>/...`.
- Expose them publicly with a static route such as `/generated-media/...`.
- Allow local generated-media URLs in URL validation / normalization so saved assets remain usable after upload.

## Naming
- Preserve the source extension when the uploaded file name already matches the mime/extension; avoid double extensions like `foo.png.png`.

## Verification
- A successful upload test can still end in `503 PROVIDER_NOT_CONFIGURED` if the provider env is missing; that means upload/storage worked and the provider layer is the blocker.
- Confirm files exist on disk after the request before debugging provider logic.
