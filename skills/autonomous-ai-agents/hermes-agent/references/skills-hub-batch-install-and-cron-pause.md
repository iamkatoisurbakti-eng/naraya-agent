# Skills Hub batch install and pause-all-cron workflow

Use when a user points at `https://hermes-agent.nousresearch.com/docs/skills/` and says to install it, or asks to pause every Hermes cron job.

## Skills Hub URL caveat

`https://hermes-agent.nousresearch.com/docs/skills/` is a Docusaurus HTML catalog page, not a direct `SKILL.md`. `hermes skills inspect https://hermes-agent.nousresearch.com/docs/skills/` will fail with `Could not find ... in any source`.

For a single skill, install by identifier from the hub:

```bash
hermes skills browse --source official --size 100
hermes skills install --yes <skill-name>
```

For all official optional skills shipped with the local Hermes checkout, enumerate local optional `SKILL.md` files and install by their frontmatter `name:`. This avoids scraping the HTML catalog and works offline if the checkout includes `optional-skills/`.

```bash
python3 - <<'PY'
import pathlib, re, subprocess
base = pathlib.Path('/usr/local/lib/hermes-agent/optional-skills')
names = []
for p in sorted(base.rglob('SKILL.md')):
    txt = p.read_text(errors='ignore')
    m = re.search(r'^name:\s*["\']?([^"\'\n]+)', txt, re.M)
    if m:
        names.append(m.group(1).strip())
print(f'Installing/enabling {len(names)} official optional skills...')
ok, fail = [], []
for i, name in enumerate(names, 1):
    print(f'[{i}/{len(names)}] {name}', flush=True)
    proc = subprocess.run(
        ['hermes', 'skills', 'install', '--yes', name],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120,
    )
    tail = '\n'.join(proc.stdout.strip().splitlines()[-6:])
    print(tail)
    (ok if proc.returncode == 0 else fail).append((name, proc.returncode, tail))
print('SUMMARY ok', len(ok), 'fail', len(fail))
for name, code, tail in fail:
    print('FAIL', name, code, tail.replace('\n', ' | '))
PY
```

Verify:

```bash
python3 - <<'PY'
import pathlib, re
skills=[]
for p in pathlib.Path('/root/.hermes/skills').rglob('SKILL.md'):
    txt=p.read_text(errors='ignore')[:2000]
    m=re.search(r'^name:\s*["\']?([^"\'\n]+)', txt, re.M)
    skills.append(m.group(1).strip() if m else p.parent.name)
print('INSTALLED_SKILL_FILES', len(skills))
for target in ['blackbox','honcho','docker-management','page-agent','duckduckgo-search','stable-diffusion-image-generation','whisper','1password']:
    print(target, 'YES' if target in skills else 'NO')
PY
hermes skills list | tail -20
```

## Pause all Hermes cron jobs

Preferred path when the cronjob tool is available:
1. `cronjob(action='list')`.
2. Pause every job whose `enabled` is true or whose `state` is not already `paused`.
3. Run `cronjob(action='list')` again and confirm every job has `enabled=false` and `state=paused`.

If using CLI instead of the tool:

```bash
hermes cron list --all
hermes cron pause <job_id>
# repeat for every active job
hermes cron list --all
```

Report concise totals: total jobs, active paused now, failures if any. Do not paste long cron job prompts unless needed for debugging.
