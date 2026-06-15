# Google Search Console OAuth automation notes

Use when a live SEO/indexing loop needs Google Search Console (GSC) API access from a CLI/server.

## When service accounts fail
- GSC UI may reject service-account emails with `email tidak ditemukan` / `user not found`.
- If adding the service account as a GSC user fails or `sites().list()` returns an empty list, switch to OAuth Desktop credentials using the Google account that owns/has access to the GSC property.
- Do not claim GSC access is active until `sites().list()` shows the target property.

## Preferred OAuth setup
1. In Google Cloud, enable `Google Search Console API`.
2. Create OAuth Client ID with application type `Desktop app`.
3. Store the client JSON securely (for this repo pattern: `secrets/<site>-gsc-oauth-client.json`, `chmod 600`).
4. Generate an authorization URL for scope:
   - `https://www.googleapis.com/auth/webmasters`
5. User opens the URL, approves with the Google account that has GSC access, then sends back the full `http://localhost:.../?code=...&state=...` redirect URL.
6. Exchange the code for a refresh token and store token securely (`chmod 600`).

## PKCE pitfall
- `google_auth_oauthlib.flow.Flow.authorization_url()` may autogenerate a PKCE `code_verifier`.
- Persist the `code_verifier` with the pending OAuth session and restore it before `fetch_token()`.
- If you do not persist it, code exchange can fail with:
  - `InvalidGrantError: Missing code verifier.`
- Redirect URLs are one-use/short-lived. If exchange fails, generate a fresh auth URL and have the user approve again.
- For localhost redirect exchange in headless CLI, set `OAUTHLIB_INSECURE_TRANSPORT=1` or OAuthlib may reject the `http://localhost` redirect with `InsecureTransportError`.

## GSC verification checklist
- `sites().list()` includes either:
  - `sc-domain:<domain>` or
  - `https://<domain>/`
- `sitemaps().get(siteUrl=..., feedpath='https://<domain>/sitemap.xml')` returns status or known error.
- URL Inspection API can query the canonical URLs.
- If no API permission exists, continue live crawl-readiness checks (HTTP 200, robots, sitemap, canonical, AMP, schema) but explicitly report that direct GSC inspection/submission is unavailable.

## Security
- Never echo client secrets, private keys, access tokens, refresh tokens, or full JSON credential contents in final responses.
- If a client secret was pasted in chat, recommend rotating/deleting that OAuth credential in Google Cloud after setup.
