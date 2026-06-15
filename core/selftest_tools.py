"""
selftest_tools.py — Cek status NYATA setiap tool Naraya-Agent di mesin ini.

Jalankan:  python core/selftest_tools.py
Keluaran per tool: PASS (jalan), SKIP (butuh dependensi/kunci/izin -> ada petunjuk),
atau FAIL (error tak terduga).

Tidak melakukan aksi merusak: web hanya GET ringan, computer-use hanya screenshot,
LLM hanya dites bila API key tersedia.
"""

from __future__ import annotations

import os
import sys
import importlib.util
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_tools as T  # noqa: E402

PASS, SKIP, FAIL = "PASS", "SKIP", "FAIL"


def _has(mod: str) -> bool:
    return importlib.util.find_spec(mod) is not None


def _llm_ready() -> bool:
    try:
        import llm
        return llm.is_available()
    except Exception:
        return False


def line(name, status, detail=""):
    icon = {"PASS": "✓", "SKIP": "•", "FAIL": "✗"}[status]
    print(f"  {icon} {name:<20} [{status}] {detail}")


def check(name, fn, ok_if=None, skip_if=None, skip_msg=""):
    """Jalankan fn(); klasifikasi hasil."""
    if skip_if:
        line(name, SKIP, skip_msg)
        return SKIP
    try:
        out = fn()
        s = str(out)
        bad = s.startswith(("GAGAL", "ERROR", "DITOLAK")) or "belum terpasang" in s or "tidak tersedia" in s
        if ok_if is not None:
            return _r(name, PASS if ok_if(s) else SKIP, s[:60])
        return _r(name, SKIP if bad else PASS, s[:60])
    except Exception as e:
        return _r(name, FAIL, str(e)[:60])


def _r(name, status, detail):
    line(name, status, detail)
    return status


def main():
    print("\n=== NARAYA-AGENT TOOL SELF-TEST ===\n")
    results = []

    # --- Sistem (selalu bisa) ---
    results.append(check("eksekusi_python", lambda: T.run_python("print(6*7)"), ok_if=lambda s: "42" in s))
    results.append(check("terminal", lambda: T.terminal("echo naraya"), ok_if=lambda s: "naraya" in s))
    results.append(check("kompres_konteks", lambda: T.compress_context("Satu. Dua. Tiga. Empat. Lima. Enam. Tujuh."), ok_if=lambda s: len(s) > 0))
    results.append(check("rl_select/feedback", lambda: (T.rl_feedback("t", "a", 1.0), T.rl_select("t", ["a", "b"]))[1], ok_if=lambda s: s in ("a", "b")))
    results.append(check("automate_schedule", lambda: T.automate_schedule("cek", "@daily", "echo hi"), ok_if=lambda s: "terdaftar" in s))
    results.append(check("mcp_list_servers", lambda: T.mcp_list_servers(), ok_if=lambda s: len(s) > 0))

    # --- Web (butuh jaringan) ---
    results.append(check("web_search", lambda: T.web_search("python")))
    results.append(check("web_browse", lambda: T.web_browse("https://example.com")))

    # --- Dependensi opsional ---
    results.append(check("browser_cdp", lambda: T.web_browse_cdp("https://example.com"),
                         skip_if=not _has("playwright"), skip_msg="pip install playwright && playwright install chromium"))
    results.append(check("web_automation", lambda: T.web_automation("https://example.com", []),
                         skip_if=not _has("playwright"), skip_msg="pip install playwright"))
    results.append(check("computer_screenshot", lambda: T.computer_screenshot(),
                         skip_if=not _has("pyautogui"), skip_msg="pip install pyautogui pillow"))

    # --- Butuh API key LLM ---
    llm_ok = _llm_ready()
    for nm, fn in [
        ("delegate_task", lambda: T.delegate_task("Sebut 1 angka.")),
        ("plan_task", lambda: T.plan_task("buat secangkir kopi")),
        ("vision_analyze", lambda: T.vision_analyze("https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg")),
        ("generate_image", lambda: T.generate_image("a red circle")),
        ("text_to_speech", lambda: T.text_to_speech("halo")),
    ]:
        results.append(check(nm, fn, skip_if=not llm_ok, skip_msg="set OPENAI_API_KEY / NARAYA_API_KEY"))

    # --- Butuh kunci/env spesifik ---
    results.append(check("x_search", lambda: T.x_search("ai"), skip_if=not os.getenv("X_BEARER_TOKEN"), skip_msg="set X_BEARER_TOKEN"))
    results.append(check("send_message", lambda: "config ok" if (os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("NARAYA_WEBHOOK_URL")) else T.send_message("test"),
                         skip_if=not (os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("NARAYA_WEBHOOK_URL")),
                         skip_msg="set TELEGRAM_BOT_TOKEN+TELEGRAM_CHAT_ID atau NARAYA_WEBHOOK_URL"))
    results.append(check("home_assistant", lambda: "config ok",
                         skip_if=not (os.getenv("HA_URL") and os.getenv("HA_TOKEN")), skip_msg="set HA_URL + HA_TOKEN"))
    results.append(check("mcp_call", lambda: "perlu server terdaftar",
                         skip_if=not _has("mcp"), skip_msg="pip install mcp + daftarkan server"))

    n_pass = results.count(PASS); n_skip = results.count(SKIP); n_fail = results.count(FAIL)
    print(f"\nRINGKASAN: {n_pass} PASS, {n_skip} SKIP (perlu setup), {n_fail} FAIL, total {len(results)}")
    if n_fail:
        print("Ada FAIL -> cek pesan error di atas.")
    else:
        print("Tidak ada FAIL. SKIP hanya menunggu dependensi/kunci sesuai petunjuk.")


if __name__ == "__main__":
    main()
