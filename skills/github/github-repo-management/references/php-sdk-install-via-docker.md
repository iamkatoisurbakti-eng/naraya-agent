# PHP SDK install via Docker Composer

Use this when a cloned GitHub repo is a PHP library and the machine does not have native `php`/`composer` installed.

Known-good flow:

```bash
git clone https://github.com/<owner>/<repo>.git /root/.hermes/vendor/<repo>
docker run --rm -v /root/.hermes/vendor/<repo>:/app -w /app composer:2 install --no-interaction --no-progress

docker run --rm -v /root/.hermes/vendor/<repo>:/app -w /app composer:2 php -r "require 'vendor/autoload.php'; echo class_exists('<Fully\\Qualified\\Class>') ? 'autoload-ok' : 'autoload-fail';"
```

Notes:
- This keeps host state clean and avoids assuming `composer` is available on the machine.
- Prefer Docker Composer only for install/verification; do not bake secrets into the image or command line.
- If the repo has tests, run them in the same container after install.
