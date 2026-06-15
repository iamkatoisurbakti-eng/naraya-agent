# Browser visual QA fallback notes

Session note: in this environment, Chrome/Chromium auto-launch can fail with a ProcessSingleton/socket-directory error (exit code 21) even after temp profile cleanup. Playwright browser installation may also be unavailable on the host platform.

Fallback pattern:
1. Reuse any existing screenshot artifacts from /tmp when browser launch is blocked.
2. Analyze those screenshots with vision rather than retrying identical browser launches.
3. If a fresh browser capture is required, change the launch strategy, profile path, or executable before retrying; do not loop on the same failing command.

Useful failure signatures:
- `Failed to create socket directory`
- `Failed to create a ProcessSingleton for your profile directory`
- `Chrome exited early (exit code: 21)`
- Playwright install refusal on `ubuntu26.04-x64`
