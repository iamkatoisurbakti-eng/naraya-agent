#!/usr/bin/env python3
"""Parse VoltAgent/awesome-agent-skills README links into split markdown catalogs.

Usage:
  python parse-awesome-agent-skills.py /path/to/awesome-agent-skills /path/to/output-dir
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def parse(readme: str):
    pattern = re.compile(r"- \*\*\[([^\]]+)\]\(([^)]+)\)\*\* - (.+)")
    return [(m.group(1).strip(), m.group(2).strip(), m.group(3).strip()) for m in pattern.finditer(readme)]


def render(items, title: str, source: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"Source: {source}",
        f"Entries in this file: {len(items)}",
        "",
        "| Skill | URL | Description |",
        "|---|---|---|",
    ]
    for name, url, desc in items:
        lines.append(f"| {name} | {url} | {desc.replace('|', '\\|')} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else "/root/.hermes/vendor/awesome-agent-skills")
    out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "/root/.hermes/skills/research/awesome-agent-skills/references")
    readme_path = repo / "README.md"
    if not readme_path.exists():
        raise SystemExit(f"README not found: {readme_path}")
    links = parse(readme_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    mid = (len(links) + 1) // 2
    source = "https://github.com/VoltAgent/awesome-agent-skills"
    (out_dir / "catalog-part-1.md").write_text(render(links[:mid], "VoltAgent Awesome Agent Skills Catalog Part 1", source), encoding="utf-8")
    (out_dir / "catalog-part-2.md").write_text(render(links[mid:], "VoltAgent Awesome Agent Skills Catalog Part 2", source), encoding="utf-8")
    (out_dir / "README.md").write_text(
        f"# VoltAgent Awesome Agent Skills Summary\n\nSource: {source}\n\n"
        "This catalog is an awesome-list of external skills, not a repository of directly installable SKILL.md files.\n\n"
        f"Parsed entries: {len(links)}\n\nUse catalog-part-1.md and catalog-part-2.md to browse links.\n",
        encoding="utf-8",
    )
    print(f"parsed_entries={len(links)} part1={mid} part2={len(links)-mid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
