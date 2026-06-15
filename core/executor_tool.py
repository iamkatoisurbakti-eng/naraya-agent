import os
import subprocess
from pathlib import Path

SAFE_DIR = Path(os.getenv("NARAYA_HOME") or os.getcwd()).resolve()

BLOCKED = [
    "rm -rf /",
    "rm -rf /*",
    "mkfs",
    "shutdown",
    "reboot",
    "poweroff",
    "dd if=",
    ":(){:|:&};:",
    "chmod -R 777 /",
    "chown -R",
    ">/dev/sda",
]

ALLOWED_PREFIX = [
    "pwd",
    "ls",
    "cat",
    "head",
    "tail",
    "grep",
    "find",
    "mkdir",
    "touch",
    "cp",
    "mv",
    "python3",
    "pip",
    "echo",
    "du",
    "df",
    "ps",
    "systemctl status",
    "journalctl",
]

def is_safe_command(command: str) -> bool:
    cmd = command.strip()
    low = cmd.lower()

    if not cmd:
        return False

    if any(bad in low for bad in BLOCKED):
        return False

    return any(cmd.startswith(prefix) for prefix in ALLOWED_PREFIX)

def run_shell(command: str) -> str:
    if not is_safe_command(command):
        return "COMMAND DIBLOKIR: hanya command aman yang boleh dijalankan."

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(SAFE_DIR),
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""

        if result.stdout:
            output += result.stdout

        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr

        if not output.strip():
            output = f"Command selesai dengan return code {result.returncode}"

        return output[:6000]

    except subprocess.TimeoutExpired:
        return "COMMAND TIMEOUT: lebih dari 30 detik."

    except Exception as e:
        return f"ERROR EXECUTOR: {e}"
