# Visual reference intake

Use when the user says to make a dashboard/site look like a PNG, screenshot, mockup, or reference image.

## Fast intake rules
- Ask for the actual image file or a direct path/URL if the image is not accessible.
- If repo/file access fails, do not guess the layout from the filename alone.
- Prefer inspecting the reference image directly before editing source.

## Screenshot capture on terminal systems
Common Linux capture commands:
- `gnome-screenshot -f /tmp/screen.png`
- `scrot /tmp/screen.png`
- `import -window root /tmp/screen.png`

Then ask the user to send the saved path, e.g. `/tmp/screen.png`.

## Implementation note
- Once the reference is available, map visible sections into source components first.
- Keep the first pass focused on structure, spacing, and hierarchy before fine styling.
