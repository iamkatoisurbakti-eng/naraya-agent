# Repo-backed skill tap workflow

Use this when a GitHub repo exposes skills under a nested path such as `.agents/skills/`.

Observed sequence
1. Add the repo as a tap if supported:
   - `hermes skills tap add ruvnet/ruflo`
2. Do not assume the tap makes names searchable.
3. Clone the repo and inspect its docs:
   - `git clone --depth 1 https://github.com/ruvnet/ruflo`
   - read `README.md` and `.agents/README.md`
4. Enumerate installable skills:
   - `find .agents/skills -name 'SKILL.md' -o -name 'skill.md'`
5. Install from the raw URL, not the bare skill name, when discovery fails:
   - `hermes skills install --yes --category autonomous-ai-agents https://raw.githubusercontent.com/ruvnet/ruflo/main/.agents/skills/<skill>/SKILL.md`
6. If the scan blocks but the user explicitly wants it, use:
   - `hermes skills install --yes --force --category autonomous-ai-agents <raw-url>`

Pitfalls
- `hermes skills install <skill-name>` may fail even after a tap is added if the repo is not indexed into the hub.
- Non-interactive installs need `--yes`; otherwise the confirmation prompt can cancel the install.
- Community skills are quarantined and scanned before install.

Verification
- `hermes skills list | grep <skill-name>`
- `test -d ~/.hermes/skills/autonomous-ai-agents/<skill-name>`