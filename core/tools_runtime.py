import subprocess
from pathlib import Path

SAFE_DIR = Path("/root/naraya-agent")

def run_bash(command: str):

    blocked = [
        "rm -rf /",
        "shutdown",
        "reboot",
        ":(){:|:&};:"
    ]

    lower = command.lower()

    if any(x in lower for x in blocked):
        return "COMMAND DIBLOKIR"

    try:

        result = subprocess.run(
            command,
            shell=True,
            cwd=SAFE_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout + "\n" + result.stderr

        return output[:4000]

    except Exception as e:
        return str(e)
