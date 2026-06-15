# Model repository workflow notes

Use this as the condensed support file for NVIDIA NeMo / Nemotron and similar model-repo setup work.

## Core pattern
- Check Python, git, and GPU visibility first.
- Prefer `uv venv` when system `venv` tooling is missing or incomplete.
- Install editable packages for repos the user may patch.
- If optional extras are needed for CLI commands, install the relevant extra instead of assuming the base install is enough.
- Verify imports and `--help` output after install.

## Pitfalls
- A successful clone does not mean the CLI or training stack is usable.
- Do not claim GPU readiness without a visible NVIDIA device or `nvidia-smi`.
- Keep API keys and model-provider credentials in env only.
