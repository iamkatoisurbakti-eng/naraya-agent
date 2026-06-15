# External skill installation notes

Use this workflow for third-party skill repos such as `ruvnet/ruflo`:

- `hermes skills tap add <owner>/<repo>` only registers a source. It does not guarantee that a skill name will resolve via `hermes skills install <name>`.
- If name resolution fails, install from the raw `SKILL.md` URL instead:
  `hermes skills install --yes --category <category> https://raw.githubusercontent.com/<owner>/<repo>/main/<path>/SKILL.md`
- In non-interactive sessions, pass `--yes` to skip the confirmation prompt.
- If the scanner flags the skill as `CAUTION` or `DANGEROUS` and you have reviewed it, add `--force`.
- Always verify the result with both `hermes skills list` and the filesystem path under `~/.hermes/skills/<category>/<name>/`.
- Treat scanner output as advisory context, but do not ignore it; forced installs should be reviewed before use.
