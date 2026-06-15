# ASPRI BELAJAR → ASPRI Chat redirect pattern

Use this when the user wants class cards in ASPRI BELAJAR to start tutoring immediately instead of opening an in-page detail panel.

Repo/file:
- `/root/nusantara-agent/aspri-nusantara-app/frontend/index.html`

Pattern:
1. Keep the class cards with inline `onclick="openPopularClass('learn-0x')"` for mobile tap reliability.
2. Make `openPopularClass(materialId)` load `/learning/materials?...&limit=100` if needed, find the selected material, then call `startPopularLearningChat(material)`.
3. `startPopularLearningChat(material)` should:
   - Set `selectedPopularMaterial`.
   - Mark the active `.kcard` if useful.
   - Build a tutor prompt from `material.title`, `material.summary`, or `material.content`.
   - Call `nav('chat')`.
   - Clear the chat input.
   - Send the prompt through a reusable chat helper, e.g. `sendMessageToNusantara(prompt)`.
4. Refactor chat sending so manual chat and auto-start tutoring share a helper:
   - `sendMessageToNusantara(message, options = {})` posts to `ASPRI_API` and appends user/AI bubbles.
   - `sendToNusantara()` only reads and clears the input, then calls the helper.
5. Avoid duplicate prompt sends:
   - Do not add a second `addEventListener('click', () => openPopularClass(...))` to `.kcard` if cards already use inline `onclick`.
6. If keeping `loadPopularClasses()`, add an option like `{autoOpen:false}` so loading class metadata does not auto-open the old detail view.

Verification:
- Extract inline `<script>` blocks and run `node --check` on the combined JS.
- HTTP-check frontend on port 8091 and backend on port 8090.
- Smoke-test `/chat` with a learning prompt and verify an AI tutor answer.
- If browser automation fails due Chrome ProcessSingleton/profile socket errors, rely on HTTP/HTML/JS/API checks and report browser as environment-blocked.
