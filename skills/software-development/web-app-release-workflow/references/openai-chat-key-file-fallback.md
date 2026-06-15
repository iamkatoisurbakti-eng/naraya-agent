# OpenAI Chat Key File Fallback

Use this pattern when AI Chat must keep working without a visible model selector and the OpenAI key is stored in a local sensitive file instead of a normal env var.

## Pattern
- Prefer `OPENAI_API_KEY` from the environment when present.
- If missing, read a local project file that contains only the key value.
- Treat the file as sensitive input: never log its contents, never echo it back to the user, and never commit it.
- Keep the chat model fixed in backend routing and UI copy, so the user sees a free chat path rather than a model picker.

## Verification
- Confirm status endpoints report chat as available when either source exists.
- Run build + API tests after wiring the fallback.
- Check the frontend no longer renders a model dropdown for chat.

## Pitfalls
- Do not store the file contents in memory or documentation.
- Do not let the fallback path leak into public logs or bundle output.
- If the file path is host-specific, make it configurable before shipping beyond the current machine.
