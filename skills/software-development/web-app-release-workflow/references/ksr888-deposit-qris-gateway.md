# KSR888 deposit / QRIS AutoGoPay gateway notes

Use this reference when a KSR888 deposit flow is failing, especially QRIS AutoGoPay, admin confirm, or user deposit status checks.

## What changed in the debugging session
- `UserDepositController::checkDepositStatus()` must scope to the logged-in user and deposit type, not the latest transaction across all users.
- `PaymentGatewayController::statusPayment()` should not depend on the legacy `fiver` provider path for QRIS confirmation.
- When QRIS status is paid, approve the transaction locally and update `Saldo` directly.
- If GameXaGlobal deposit sync fails during admin approval, do not roll back the local deposit approval; log a warning and continue so the user is not blocked by upstream API issues.

## Common symptoms
- Deposit confirmation appears to do nothing or checks another user’s pending deposit.
- QRIS payment is paid but the balance does not update because the legacy provider sync path rejects or is unavailable.
- Admin approval fails hard when upstream provider sync errors, even though local transaction state could be saved.

## Recovery pattern
1. Validate the route exists:
   - `/create-payment` for QRIS creation
   - `/payment/status` for paid confirmation
   - `/check-deposit-status` for polling the latest deposit for the authenticated user
2. Confirm the controller updates the local transaction first, then updates saldo.
3. If provider sync is best-effort, wrap it with logging and continue the local approval path.
4. After editing, syntax-check in the live container and restart the web container so the change is active.

## Verification
- `php -l app/Http/Controllers/UserDepositController.php`
- `php -l app/Http/Controllers/PaymentGatewayController.php`
- `curl -i https://ksr888.online/check-deposit-status` should return `401` when unauthenticated and a user-scoped JSON body when logged in.
