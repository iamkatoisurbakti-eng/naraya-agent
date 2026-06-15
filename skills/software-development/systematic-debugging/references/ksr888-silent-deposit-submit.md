# KSR888 silent deposit submit

Observed in session:
- Deposit QRIS form looked like it did nothing because the primary flow was using a custom JS submit handler.
- The page had a hidden validation blocker: a `bukti_transfer` file input marked `required`, which prevented submit when no file was chosen.
- Fix pattern: prefer a native form submit for the main deposit flow, and only keep AJAX/JSON handling if it is proven end-to-end.
- After patching Blade, clear view/application cache and restart the web container so the served page changes immediately.
