# KSR888 GameXaGlobal Transaction Sync

Use this note when a KSR888 deposit/withdraw/admin-confirm flow needs to sync a local transaction into live GameXaGlobal.

## Trigger conditions
- User reports deposit/withdraw not reaching provider balance.
- Admin confirm/reject still uses legacy provider logic.
- QRIS/AutoGoPay payment is approved locally but provider balance is not updated.

## Reliable pattern
1. Resolve the player from the local user first (`extplayer` fallback to `name`).
2. If the player is missing, auto-create it in GameXaGlobal before any balance mutation.
3. Call the provider mutation with a stable reference id:
   - deposit: `playerDeposit(playerId, ['amount' => ..., 'reference_id' => ...])`
   - withdraw: `playerWithdraw(playerId, ['amount' => ..., 'reference_id' => ...])`
   - balance refresh: `playerBalance(playerId)`
4. After success, refresh local `Saldo` from provider balance when available.
5. If the user-facing flow is already paid/approved and provider sync fails, log a warning and decide whether to:
   - continue local approval for user-facing payment flows, or
   - hard-fail admin confirmation if the business rule requires provider sync.

## Implementation notes used in KSR888
- Add an `ensureGamexaglobalPlayerId()` helper that:
  - searches players by username
  - creates a player with username/name/email/phone if missing
  - retries player lookup after create
- Use the helper in:
  - `UserDepositController`
  - `UserWithdrawController`
  - `PaymentGatewayController`
  - `backoffice/DepositController`
- Keep local transaction state and provider state aligned, but avoid blocking user QRIS completion when the provider is temporarily unavailable.
- `checkDepositStatus()` should scope to the authenticated user and deposit type, not the global latest transaction.

## Pitfalls
- Do not use the old `fiver` path for GameXaGlobal balance mutation.
- Do not assume provider search always returns `id`; inspect `id` and `player_id`.
- Do not save raw secrets or tokens in the note; provider config is already in env/DB.
- If provider sync fails during admin confirm, ensure the local transaction is not partially committed.

## Verification
- Run PHP lint on every changed controller.
- Restart the web container after deploy.
- Smoke-check the route that consumes the flow and confirm it returns the expected HTTP status.
- For deposit status endpoints, verify unauthenticated requests return 401 and authenticated requests are user-scoped.
