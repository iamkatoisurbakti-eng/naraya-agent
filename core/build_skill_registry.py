from pathlib import Path
import json
import time

HERMES_SKILLS = Path("/root/.hermes/skills")

OUT = Path(
    "/root/naraya-agent/data/hermes_skill_registry.json"
)

skills = []

for path in HERMES_SKILLS.rglob("SKILL.md"):

    try:

        stat = path.stat()

        rel = path.relative_to(HERMES_SKILLS)

        category = rel.parts[0] if len(rel.parts) > 1 else "general"

        skills.append({
            "name": path.parent.name,
            "category": category,
            "path": str(rel),
            "updated": int(stat.st_mtime),
            "updated_human": time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(stat.st_mtime)
            )
        })

    except Exception:
        pass

skills.sort(
    key=lambda x: x["updated"],
    reverse=True
)

OUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUT.write_text(
    json.dumps(
        skills,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

print(f"OK registry: {len(skills)} skills")
