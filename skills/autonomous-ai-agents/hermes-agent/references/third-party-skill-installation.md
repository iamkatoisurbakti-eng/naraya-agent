# Third-party skill installation notes

Session-derived workflow for installing skills from a raw GitHub `SKILL.md` URL.

## Good pattern

```bash
hermes skills tap add owner/repo
hermes skills install --yes --category autonomous-ai-agents https://raw.githubusercontent.com/owner/repo/main/.agents/skills/<skill>/SKILL.md
hermes skills list | grep '<skill>'
```

## Important behavior

- `hermes skills install` accepts a direct `https://.../SKILL.md` URL.
- `--yes` skips the interactive confirm prompt; it is required for unattended/TUI use.
- `--force` overrides scan verdicts (`CAUTION` / `DANGEROUS`) when the user explicitly wants the install.
- Even when the scan reports `BLOCKED`, the installer may still place the skill on disk if `--force` is used, so verify with `hermes skills list` or a filesystem check.
- For batch installs, install one skill per command so failures are isolated and reviewable.
- Prefer keeping third-party skills in a consistent category bucket unless a project convention says otherwise.

## Verification

```bash
hermes skills list | egrep 'skill-a|skill-b'
python - <<'PY'
from pathlib import Path
base = Path.home()/'.hermes'/'skills'/'autonomous-ai-agents'
print((base/'skill-name').exists())
PY
```

## Pitfalls observed

- Raw URL installs may quarantine the skill first and then run the scanner.
- A scan warning does not mean the installer failed; inspect the final install status and the on-disk path.
- Some skills ship with risky behaviors such as persistence, exfiltration patterns, traversal, obfuscation, or supply-chain installation commands. Treat `CAUTION`/`DANGEROUS` as real signals and force only when the user explicitly asks.
