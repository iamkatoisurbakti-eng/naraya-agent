# Archive and dump intake notes

Use this as the condensed support file for archive / dump inspection work.

## Core checks
- Verify the file exists and capture size first.
- Identify the file type with `file` plus byte inspection when needed.
- For ZIP/TAR-style inputs, inspect headers and trailing metadata; do not trust the filename alone.
- Use a second parser when the first reader says the archive is invalid.
- Read large dumps incrementally with offsets or line ranges.

## Common pitfalls
- Truncation or partial uploads can look valid at the start and still fail at the end.
- `zipfile.is_zipfile()` may disagree with archive tools when the file is malformed.
- Large dumps often contain secrets; avoid echoing sensitive content.
