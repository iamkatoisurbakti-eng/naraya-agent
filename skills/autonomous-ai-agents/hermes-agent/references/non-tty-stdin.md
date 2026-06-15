# Hermes CLI non-TTY stdin note

Observed in this environment:

- `hermes < file.txt` starts the CLI but exits immediately with `Warning: Input is not a terminal (fd=0).`
- The CLI is expecting a real TTY/prompt_toolkit session, not plain stdin redirection.

Workarounds:

- Use a PTY, e.g. `tmux new-session -d -s <name> 'hermes'` and then send the prompt with `tmux send-keys`.
- For one-shot runs, pass the prompt as a quoted query, e.g. `hermes chat -q "$(cat file.txt)"`.
- For scripted use, keep the input inside the prompt string instead of piping raw stdin.

Verification:

- If stdin is not a TTY, expect Hermes to exit without processing the prompt.
- If the prompt is delivered through a PTY or `chat -q`, the session should stay interactive or complete the one-shot query.