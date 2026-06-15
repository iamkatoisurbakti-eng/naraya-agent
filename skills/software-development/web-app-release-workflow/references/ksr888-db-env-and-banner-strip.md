# KSR888 DB env + banner-strip notes

## DB env recreation pitfall
- The KSR888 PHP web container must be recreated with the live DB credentials from the DB container, using the compose-interpolated `KSR888_DB_*` variables.
- Overriding plain `DB_*` variables at the shell level is not enough if the compose file maps `DB_*` from `KSR888_DB_*` defaults.
- After recreate, verify the container actually received the intended values with `docker inspect <web-container> --format '{{range .Config.Env}}{{println .}}{{end}}' | sort | grep '^DB_'`.
- If the app still throws `mysqli_sql_exception: Access denied`, inspect both the web-container env and the DB container’s actual user/password pairing before changing PHP code.

## Banner/category strip styling pattern
- For KSR888 banner-inspired category strips, use a late CSS override in the `*.luxury.css` file and bump the stylesheet version token in the PHP entry page.
- User references to `banner/2.png`, `banner/3.png`, or `banner/4.png` can mean different promo moods; choose the matching palette:
  - banner 2: dark, dramatic, blue-electric + gold jackpot look
  - banner 3: green/gold fantasy/adventure look
  - banner 4: dark strip with pink/magenta neon accents
- If an exact numbered file is missing, inspect the available banner contact sheet first and map the requested number to the nearest visible style instead of guessing.
- After patching, verify the live CSS response with the cache-busting query string and confirm the version token appears in the rendered HTML.
