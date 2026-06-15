from pathlib import Path

src = Path("data/hermes_knowledge.md")
out = Path("data/hermes_preview.md")

text = src.read_text(encoding="utf-8", errors="ignore")

preview = text[:30000]

out.write_text(preview, encoding="utf-8")

print("OK:", out)
print("Karakter preview:", len(preview))
