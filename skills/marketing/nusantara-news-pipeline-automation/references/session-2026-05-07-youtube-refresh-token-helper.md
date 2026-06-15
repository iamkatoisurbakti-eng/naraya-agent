# Session 2026-05-07: YouTube refresh-token helper and env validation

## What was learned

For Nusantara-AI YouTube Shorts automation, the user had a valid Desktop OAuth client JSON at:

`/root/.hermes/client_secret_1061338379955-39a7j4c6cpsu3m652be1pnkpi9mrqe1e.apps.googleusercontent.com.json`

The project initially had no `.env`; later `.env.example` temporarily contained real secrets and had to be sanitized. Treat any real value found in `.env.example` as compromised and blank it immediately.

## Implemented helper

Project helper added:

`/root/nusantara-ai-saas/scripts/youtube-oauth-refresh-token.ts`

NPM script:

`npm run youtube:oauth`

Flow:

1. Generate auth URL and write `YOUTUBE_CLIENT_ID`/`YOUTUBE_CLIENT_SECRET` to `.env` without printing the secret:

   `npm run youtube:oauth -- --auth-url`

2. User opens the auth URL, approves YouTube upload scope, and copies the full `http://localhost/?code=...` redirected URL from the browser address bar. Browser localhost error is expected.

3. Exchange the code and store `YOUTUBE_REFRESH_TOKEN` in `.env` without printing it:

   `npm run youtube:oauth -- --code "http://localhost/?code=..."`

4. Validate `.env` status; the refresh token must be a non-empty token value. Do not accept `https://oauth2.googleapis.com/token` as `YOUTUBE_REFRESH_TOKEN`.

## Verification pattern

- `npm run build:server`
- `npm run youtube:oauth -- --auth-url`
- Verify:
  - `/root/nusantara-ai-saas/data/logs/youtube-oauth-state.json` exists
  - `/root/nusantara-ai-saas/.env` exists with mode `600`
  - `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET` are set
  - `YOUTUBE_REFRESH_TOKEN` remains missing until user returns auth code

## Security rules reinforced

- Never copy credentials from chat into `.env`; ask user to rotate/regenerate and enter through prompt or OAuth flow.
- Never print `client_secret`, refresh token, API keys, or bot tokens.
- `.env.example` must remain placeholder-only and may be committed; `.env` is local secret storage and must be gitignored/chmod 600.
