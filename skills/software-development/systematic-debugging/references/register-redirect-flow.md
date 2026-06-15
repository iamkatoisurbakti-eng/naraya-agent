# Register redirect flow checklist

Use this when a user says registration succeeds but the UI jumps back to home or the wrong page.

## KSR888-specific finding

There are two separate PHP handlers:
- `KSR888/site/mobile/function/daftar_akun.php`
- `KSR888/site/dekstop/function/daftar_akun.php`

On success, both should:
- create the user
- set session values (`username`, `extplayer`, `id`)
- redirect to the member/profile area, not the homepage

Expected redirect used in this session:
- `header("Location:../index.php?page=profile&pesan=3");`

## Debug steps

1. Inspect the actual handler that processes the form submit.
2. Verify the success branch uses the intended redirect target.
3. Check both mobile and desktop handlers; they are often duplicated and can drift.
4. If the redirect is correct in source but the browser still lands on home, check:
   - stale cache / old deployed bundle
   - wrong form action path
   - session not persisting
   - a different route consuming the success response

## Quick verification

```bash
grep -n "Location:../index.php?page=profile&pesan=3" \
  KSR888/site/mobile/function/daftar_akun.php \
  KSR888/site/dekstop/function/daftar_akun.php
```

If both files match, the redirect target is aligned.
