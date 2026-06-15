# Ruflo skill install notes

Scope: Installing skills from https://github.com/ruvnet/ruflo/tree/main/.agents/skills

Observed workflow
- `hermes skills tap add ruvnet/ruflo` adds the repo as a source, but direct skill-name lookup may still fail.
- The reliable path is installing from the raw `SKILL.md` URL.
- Use `--yes` in non-interactive/TUI contexts to skip the confirmation prompt.
- `hermes skills inspect <url>` previews the skill before install.
- When a scan returns SAFE, install proceeds normally.
- When a scan returns CAUTION or DANGEROUS, `hermes skills install --force --yes <url>` can still install, but the scan verdict remains visible and the skill should be reviewed before use.

Verification
- `hermes skills list | grep <skill-name>`
- Check filesystem: `~/.hermes/skills/<category>/<skill-name>/`
- For ruflo installs in this session, the category used was `autonomous-ai-agents`.

Pitfall
- The repo exposes many skills under `.agents/skills/`, but they are not always discoverable by plain name search. URL-based install is the safest default.