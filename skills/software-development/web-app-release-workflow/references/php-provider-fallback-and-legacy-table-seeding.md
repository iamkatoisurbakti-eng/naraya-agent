# PHP provider fallback and legacy table seeding

Use this when a copied PHP gambling/game-style site partially works after deploy but register, footer, or game pages still fail because the source expects a legacy provider API and extra DB tables.

## What happened
- The imported app used both env-style provider calls and legacy DB-backed API credentials in `tb_api`.
- The upstream provider endpoint returned either non-JSON HTML (`GSC-404-Path Not Specified`) or JSON-style errors such as `{"errCode":"90","errMsg":"INVALID_PARAMETER"}`.
- Local account creation in `tb_user` still mattered even when provider-side member creation failed.
- Register pages returned `500` because a footer query referenced a legacy table `game_baru` that was not part of the initial inferred schema.

## Practical fixes
1. Keep provider secrets in env, but also seed/update `tb_api` so old helper files and admin maintenance pages still read sane values.
2. Patch credential loaders like `main/API/credential.php` to prefer env and fall back to DB.
3. Patch registration handlers so provider member creation failure is logged, not shown as a false user-facing failure, when the product can tolerate local-only signup.
4. Guard repeated `session_start()` calls with `session_status() !== PHP_SESSION_ACTIVE` to avoid noisy notices during redirect/login flows.
5. Seed legacy UI tables required by templates, not just core account tables:
   - `game_baru`
   - `tb_provider`
   - `tb_games`
   - `tb_gamelist`
6. Make game launch endpoints fail-safe: if launch URL is absent, redirect back with a status param instead of leaving a blank response.

## Verification recipe
- `GET /dekstop/index.php?page=register` -> 200
- `GET /mobile/index.php?page=register` -> 200
- POST a full registration form with the live captcha field and confirm a redirect rather than `500`/fatal output.
- Check DB counts after smoke registration:
  - `tb_user`
  - `tb_saldo`
  - `tb_bank`
- Probe provider wrapper from inside the PHP container and inspect whether the failure is transport, non-JSON body, or provider `INVALID_PARAMETER`.
- Visit one slot/provider page and confirm sample game rows render.

## Pitfalls
- A provider failure can surface as a misleading frontend alert (`Daftar Akun Gagal`) even when the local inserts succeeded. Fix the handler logic, not just the message.
- Legacy template includes can query extra tables from footer/header files; scan logs when a page that looks unrelated to games fails.
- If `playGame.php` assumes `data.balance` and `launch_url` always exist, missing provider data can create PHP notices or dead-end redirects.
