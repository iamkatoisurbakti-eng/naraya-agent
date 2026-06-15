# Cronjob scheduling pattern

This reference captures the worked pattern for automating repeatable repo maintenance tasks in Hermes.

## What worked
- Build a standalone re-runnable script first.
- Place the script in `~/.hermes/scripts/`.
- Create the cron job using only the script filename.
- Run the script once manually to verify the end-to-end behavior before scheduling.

## Example from KSR888 image sync
- Script: `ksr888_gamexaglobal_image_sync.sh`
- Location: `~/.hermes/scripts/ksr888_gamexaglobal_image_sync.sh`
- Job name: `ksr888-gamexaglobal-image-sync`
- Schedule: `20 */6 * * *`
- Result: provider and game images are synced to DB automatically without manual clicks.

## Pitfalls
- Absolute paths for script are rejected by the cronjob tool.
- If the script launches a PHP command, verify that the target container actually has PHP installed.
- Use concise output from the script so future scheduled runs are easy to scan.
