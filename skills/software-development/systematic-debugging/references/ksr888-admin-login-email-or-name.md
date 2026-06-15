# KSR888 admin login email-or-name

Observed in session:
- Admin login should accept a single generic `login` field.
- The controller can resolve the identifier as email or username automatically.
- Confirm the target account exists in the live DB and is admin-gated with `level` in `[1, 2]` before changing auth logic.
- Keep the form and controller field names aligned; mismatches are a common cause of failed admin sign-in.
