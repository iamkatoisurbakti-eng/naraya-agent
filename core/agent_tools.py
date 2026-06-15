"""
agent_tools.py — Pustaka kapabilitas (tools) untuk Naraya-Agent.

Setiap fungsi adalah "tool" yang bisa dipanggil agen. Semua dependensi berat
di-import lazy (di dalam fungsi) + dibungkus try/except, sehingga modul ini
SELALU bisa di-import (offline-safe) dan tool yang dependensinya/kuncinya hilang
mengembalikan pesan ramah + cara setup, bukan meledak.

Kapabilitas:
  Web & browser : web_search, web_browse, web_browse_cdp, web_automation
  Sistem        : run_python, terminal
  Agentik       : delegate_task, plan_task, compress_context
  Multimodal    : vision_analyze, generate_image, text_to_speech, speech_to_text
  Integrasi     : send_message, home_assistant, x_search
  Otomasi       : automate_schedule
  Pembelajaran  : rl_select, rl_feedback
  Computer use  : computer_screenshot, computer_click, computer_type, computer_key
  MCP           : mcp_list_servers, mcp_list_tools, mcp_call, mcp_add_server

Env penting (opsional): OPENAI_API_KEY/NARAYA_API_KEY, NARAYA_VISION_MODEL,
NARAYA_IMAGE_MODEL, NARAYA_TTS_MODEL, NARAYA_STT_MODEL, TELEGRAM_BOT_TOKEN,
TELEGRAM_CHAT_ID, NARAYA_WEBHOOK_URL, HA_URL, HA_TOKEN, X_BEARER_TOKEN, NARAYA_HOME.
"""

from __future__ import annotations

import os
import re
import sys
import json
import time
import base64
import sqlite3
import subprocess
import tempfile
from pathlib import Path

# ============================================================================
# HELPER HTTP & OPENAI
# ============================================================================

def _http_get(url, headers=None, params=None, timeout=20):
    try:
        import httpx
        r = httpx.get(url, headers=headers, params=params, timeout=timeout, follow_redirects=True)
        return r.status_code, r.text
    except Exception:
        import urllib.request, urllib.parse
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return resp.status, resp.read().decode("utf-8", errors="ignore")


def _http_post(url, headers=None, json_body=None, timeout=20):
    try:
        import httpx
        r = httpx.post(url, headers=headers, json=json_body, timeout=timeout)
        return r.status_code, r.text
    except Exception:
        import urllib.request
        data = json.dumps(json_body or {}).encode()
        h = {"Content-Type": "application/json", **(headers or {})}
        req = urllib.request.Request(url, data=data, headers=h, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return resp.status, resp.read().decode("utf-8", errors="ignore")


def _openai_client():
    """Klien OpenAI memakai env (reuse logika llm.py)."""
    try:
        import llm
        return llm._get_client()
    except Exception as exc:
        raise RuntimeError(f"LLM/OpenAI tidak tersedia: {exc}")


# ============================================================================
# WEB & BROWSER
# ============================================================================

_TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_HTML_RE = re.compile(r"<[^>]+>")


def _html_to_text(html: str) -> str:
    html = _TAG_RE.sub(" ", html)
    text = _HTML_RE.sub(" ", html)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"')]:
        text = text.replace(a, b)
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()


def web_search(query: str, max_results: int = 5) -> str:
    """Cari di web (DuckDuckGo) dan kembalikan judul + URL hasil teratas."""
    try:
        status, html = _http_get("https://html.duckduckgo.com/html/", params={"q": query},
                                 headers={"User-Agent": "Mozilla/5.0 Naraya"})
        links = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
        if not links:
            links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
        out = []
        for href, title in links[:max_results]:
            out.append(f"- {_html_to_text(title)} :: {href}")
        return "\n".join(out) if out else "(tidak ada hasil)"
    except Exception as exc:
        return f"GAGAL web_search: {exc}"


def web_browse(url: str, max_chars: int = 4000, timeout: int = 20) -> str:
    """Ambil halaman web (HTTP statis) dan kembalikan teks bersih (tanpa JavaScript)."""
    if not re.match(r"^https?://", url):
        url = "https://" + url
    try:
        status, body = _http_get(url, headers={"User-Agent": "Naraya-Agent/1.0"}, timeout=timeout)
        out = f"[{status}] {url}\n\n{_html_to_text(body)}"
        return out[:max_chars] + ("\n…(dipotong)" if len(out) > max_chars else "")
    except Exception as exc:
        return f"GAGAL mengambil {url}: {exc}"


def web_browse_cdp(url: str, wait_ms: int = 1500, max_chars: int = 4000) -> str:
    """Render halaman ber-JavaScript (SPA) via Chromium (Playwright) lalu ambil teksnya."""
    if not re.match(r"^https?://", url):
        url = "https://" + url
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return "Playwright belum terpasang. Install: `pip install playwright && python -m playwright install chromium`"
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            pg = b.new_page()
            pg.goto(url, wait_until="networkidle", timeout=30000)
            pg.wait_for_timeout(wait_ms)
            text = pg.inner_text("body")
            b.close()
        out = f"[CDP] {url}\n\n" + re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()
        return out[:max_chars] + ("\n…(dipotong)" if len(out) > max_chars else "")
    except Exception as exc:
        return f"GAGAL render {url}: {exc}"


def web_automation(url: str, steps: list | None = None, max_chars: int = 2000) -> str:
    """Otomasi browser: buka url lalu jalankan langkah-langkah.
    steps = list of dict: {"action":"click|fill|press|wait|screenshot","selector":..,"value":..}."""
    if not re.match(r"^https?://", url):
        url = "https://" + url
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return "Playwright belum terpasang. Install: `pip install playwright && python -m playwright install chromium`"
    log = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            pg = b.new_page()
            pg.goto(url, wait_until="networkidle", timeout=30000)
            for s in (steps or []):
                act = s.get("action")
                if act == "click":
                    pg.click(s["selector"]); log.append(f"click {s['selector']}")
                elif act == "fill":
                    pg.fill(s["selector"], s.get("value", "")); log.append(f"fill {s['selector']}")
                elif act == "press":
                    pg.keyboard.press(s.get("value", "Enter")); log.append(f"press {s.get('value')}")
                elif act == "wait":
                    pg.wait_for_timeout(int(s.get("value", 1000))); log.append("wait")
                elif act == "screenshot":
                    path = s.get("value") or str(Path(tempfile.gettempdir()) / f"naraya_auto_{int(time.time())}.png")
                    pg.screenshot(path=path); log.append(f"screenshot {path}")
            text = pg.inner_text("body")[:max_chars]
            b.close()
        return "LANGKAH:\n" + "\n".join(log) + f"\n\nHASIL:\n{text}"
    except Exception as exc:
        return f"GAGAL web_automation: {exc} | langkah: {log}"


# ============================================================================
# SISTEM: code execution & terminal
# ============================================================================

def run_python(code: str, timeout: int = 20) -> str:
    """Jalankan kode Python di subprocess bertimeout; kembalikan stdout+stderr."""
    try:
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "snippet.py"
            f.write_text(code, encoding="utf-8")
            proc = subprocess.run([sys.executable, str(f)], capture_output=True, text=True, timeout=timeout, cwd=td)
        out = (proc.stdout or "") + (("\nSTDERR:\n" + proc.stderr) if proc.stderr else "")
        return (out or f"(selesai, rc {proc.returncode})")[:6000]
    except subprocess.TimeoutExpired:
        return f"TIMEOUT: melebihi {timeout} detik."
    except Exception as exc:
        return f"ERROR: {exc}"


def terminal(command: str, timeout: int = 30) -> str:
    """Jalankan perintah shell di folder kerja (NARAYA_HOME atau cwd). Kuat — pakai di mesin sendiri."""
    cwd = os.getenv("NARAYA_HOME") or os.getcwd()
    blocked = ["rm -rf /", "mkfs", "shutdown", "reboot", ":(){:|:&};:", "dd if=", ">/dev/sd"]
    if any(b in command for b in blocked):
        return "DITOLAK: perintah berpotensi merusak."
    try:
        proc = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        out = (proc.stdout or "") + (("\nSTDERR:\n" + proc.stderr) if proc.stderr else "")
        return (out or f"(selesai, rc {proc.returncode})")[:6000]
    except subprocess.TimeoutExpired:
        return f"TIMEOUT: melebihi {timeout} detik."
    except Exception as exc:
        return f"ERROR: {exc}"


# ============================================================================
# AGENTIK: delegasi, perencanaan, kompresi
# ============================================================================

def _run_async(coro):
    import asyncio
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


def delegate_task(task: str, role: str = "generalis") -> str:
    """Delegasikan tugas ke sub-agen khusus dan kembalikan hasilnya."""
    try:
        from agents import Agent, Runner
        sub = Agent(name=f"sub-{role}",
                    instructions=f"Kamu sub-agen {role} untuk Naraya. Selesaikan tugas dengan teliti dan ringkas.")
        res = _run_async(Runner.run(sub, task))
        return getattr(res, "final_output", str(res))
    except Exception:
        try:
            import llm
            if llm.is_available():
                return llm.chat(task, system=f"Kamu sub-agen {role} untuk Naraya. Jawab ringkas dan akurat.")
        except Exception:
            pass
        return "Delegasi gagal: agents SDK / LLM tidak tersedia (offline)."


def plan_task(goal: str) -> str:
    """Pecah sebuah goal menjadi rencana langkah teknis (JSON)."""
    try:
        from orchestrator_engine import create_task_plan
        return json.dumps(create_task_plan(goal), ensure_ascii=False, indent=2)
    except Exception:
        try:
            import llm
            if llm.is_available():
                return llm.chat(
                    f"Pecah goal ini menjadi langkah teknis berurutan yang konkret:\n{goal}",
                    system="Kamu perencana tugas. Jawab sebagai daftar langkah bernomor.",
                )
        except Exception:
            pass
        return "Perencanaan gagal: LLM tidak tersedia (offline)."


def compress_context(text: str, instruction: str | None = None, max_chars: int = 1500) -> str:
    """Ringkas/kompres teks panjang agar hemat token (LLM, fallback heuristik)."""
    text = (text or "").strip()
    if not text:
        return ""
    try:
        import llm
        if llm.is_available():
            sysp = ("Kamu peringkas ahli. Padatkan teks menjaga fakta, angka, keputusan, dan poin penting. "
                    "Buang basa-basi. Bahasa Indonesia, terstruktur.")
            user = (instruction or "Ringkas sepadat mungkin tanpa kehilangan info penting.") + f"\n\nTEKS:\n{text}"
            return llm.chat(user, system=sysp, temperature=0.2)[:max_chars]
    except Exception:
        pass
    sents = re.split(r"(?<=[.!?])\s+", text)
    if len(sents) <= 6:
        return text[:max_chars]
    return f"{' '.join(sents[:3])} … {' '.join(sents[-2:])}"[:max_chars]


# ============================================================================
# MULTIMODAL: vision, image-gen, voice
# ============================================================================

def vision_analyze(image: str, question: str = "Jelaskan isi gambar ini.") -> str:
    """Analisis gambar (path lokal atau URL) dengan model vision dan jawab pertanyaan."""
    try:
        client = _openai_client()
    except Exception as exc:
        return f"Vision tidak tersedia: {exc}"
    try:
        if re.match(r"^https?://", image):
            image_url = image
        else:
            data = Path(image).read_bytes()
            b64 = base64.b64encode(data).decode()
            image_url = f"data:image/png;base64,{b64}"
        model = os.getenv("NARAYA_VISION_MODEL", "gpt-4o-mini")
        res = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]}],
        )
        return (res.choices[0].message.content or "").strip()
    except Exception as exc:
        return f"GAGAL vision: {exc}"


def generate_image(prompt: str, path: str | None = None) -> str:
    """Hasilkan gambar dari teks; simpan PNG dan kembalikan path."""
    try:
        client = _openai_client()
    except Exception as exc:
        return f"Image-gen tidak tersedia: {exc}"
    try:
        model = os.getenv("NARAYA_IMAGE_MODEL", "gpt-image-1")
        res = client.images.generate(model=model, prompt=prompt, size="1024x1024")
        b64 = res.data[0].b64_json
        path = path or str(Path(tempfile.gettempdir()) / f"naraya_img_{int(time.time())}.png")
        Path(path).write_bytes(base64.b64decode(b64))
        return f"Gambar disimpan: {path}"
    except Exception as exc:
        return f"GAGAL generate_image: {exc}"


def text_to_speech(text: str, path: str | None = None) -> str:
    """Ubah teks menjadi suara (MP3); kembalikan path file."""
    try:
        client = _openai_client()
    except Exception as exc:
        return f"TTS tidak tersedia: {exc}"
    try:
        model = os.getenv("NARAYA_TTS_MODEL", "tts-1")
        voice = os.getenv("NARAYA_TTS_VOICE", "alloy")
        path = path or str(Path(tempfile.gettempdir()) / f"naraya_tts_{int(time.time())}.mp3")
        res = client.audio.speech.create(model=model, voice=voice, input=text)
        res.stream_to_file(path)
        return f"Audio disimpan: {path}"
    except Exception as exc:
        return f"GAGAL TTS: {exc}"


def speech_to_text(audio_path: str) -> str:
    """Transkripsi file audio menjadi teks."""
    try:
        client = _openai_client()
    except Exception as exc:
        return f"STT tidak tersedia: {exc}"
    try:
        model = os.getenv("NARAYA_STT_MODEL", "whisper-1")
        with open(audio_path, "rb") as f:
            res = client.audio.transcriptions.create(model=model, file=f)
        return getattr(res, "text", str(res))
    except Exception as exc:
        return f"GAGAL STT: {exc}"


# ============================================================================
# INTEGRASI: messaging, home assistant, X/Twitter
# ============================================================================

def send_message(text: str, channel: str = "telegram", target: str | None = None) -> str:
    """Kirim pesan. channel=telegram (butuh TELEGRAM_BOT_TOKEN + chat id) atau webhook (NARAYA_WEBHOOK_URL)."""
    try:
        if channel == "telegram":
            token = os.getenv("TELEGRAM_BOT_TOKEN")
            chat = target or os.getenv("TELEGRAM_CHAT_ID")
            if not token or not chat:
                return "Set TELEGRAM_BOT_TOKEN dan TELEGRAM_CHAT_ID dulu."
            st, _ = _http_post(f"https://api.telegram.org/bot{token}/sendMessage",
                               json_body={"chat_id": chat, "text": text})
            return f"Terkirim ke Telegram (status {st})."
        if channel == "webhook":
            url = target or os.getenv("NARAYA_WEBHOOK_URL")
            if not url:
                return "Set NARAYA_WEBHOOK_URL atau beri target URL."
            st, _ = _http_post(url, json_body={"text": text})
            return f"Terkirim ke webhook (status {st})."
        return f"Channel '{channel}' tidak dikenal (pakai telegram/webhook)."
    except Exception as exc:
        return f"GAGAL kirim pesan: {exc}"


def home_assistant(domain: str, service: str, entity_id: str) -> str:
    """Panggil service Home Assistant, mis. domain=light service=turn_on entity_id=light.ruang_tamu."""
    base = os.getenv("HA_URL")
    token = os.getenv("HA_TOKEN")
    if not base or not token:
        return "Set HA_URL dan HA_TOKEN dulu."
    try:
        st, body = _http_post(
            f"{base.rstrip('/')}/api/services/{domain}/{service}",
            headers={"Authorization": f"Bearer {token}"},
            json_body={"entity_id": entity_id},
        )
        return f"HA {domain}.{service} -> {entity_id} (status {st})"
    except Exception as exc:
        return f"GAGAL Home Assistant: {exc}"


def x_search(query: str, max_results: int = 5) -> str:
    """Cari tweet terbaru via X/Twitter API v2 (butuh X_BEARER_TOKEN)."""
    token = os.getenv("X_BEARER_TOKEN")
    if not token:
        return "Set X_BEARER_TOKEN (X/Twitter API v2) dulu."
    try:
        st, body = _http_get(
            "https://api.twitter.com/2/tweets/search/recent",
            headers={"Authorization": f"Bearer {token}"},
            params={"query": query, "max_results": max(10, min(int(max_results), 100))},
        )
        data = json.loads(body)
        tweets = data.get("data", [])[:max_results]
        if not tweets:
            return f"(tidak ada hasil) status {st}"
        return "\n".join(f"- {t.get('text','').replace(chr(10),' ')}" for t in tweets)
    except Exception as exc:
        return f"GAGAL x_search: {exc}"


# ============================================================================
# OTOMASI (penjadwalan)
# ============================================================================

_JOBS_FILE = Path("data/automation_jobs.json")


def automate_schedule(name: str, schedule: str, command: str) -> str:
    """Daftarkan job otomasi (disimpan ke data/automation_jobs.json untuk dieksekusi runner/cron)."""
    try:
        Path("data").mkdir(parents=True, exist_ok=True)
        jobs = {}
        if _JOBS_FILE.exists():
            jobs = json.loads(_JOBS_FILE.read_text(encoding="utf-8"))
        jobs[name] = {"schedule": schedule, "command": command, "created_at": int(time.time())}
        _JOBS_FILE.write_text(json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8")
        return f"Job '{name}' terdaftar (schedule: {schedule}). Total job: {len(jobs)}."
    except Exception as exc:
        return f"GAGAL menjadwalkan: {exc}"


# ============================================================================
# REINFORCEMENT LEARNING (bandit epsilon-greedy sederhana)
# ============================================================================

_RL_DB = Path("data/rl_bandit.db")


def _rl_conn():
    Path("data").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_RL_DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS bandit (
        key TEXT, action TEXT, count INTEGER DEFAULT 0, total REAL DEFAULT 0,
        PRIMARY KEY (key, action))""")
    conn.commit()
    return conn


def rl_select(key: str, actions: list, epsilon: float = 0.1) -> str:
    """Pilih action terbaik untuk konteks `key` (epsilon-greedy berdasarkan reward historis)."""
    import random
    if not actions:
        return ""
    if random.random() < epsilon:
        return random.choice(actions)
    conn = _rl_conn()
    best, best_avg = actions[0], -1e9
    for a in actions:
        row = conn.execute("SELECT count, total FROM bandit WHERE key=? AND action=?", (key, a)).fetchone()
        avg = (row[1] / row[0]) if row and row[0] else 0.0
        if avg > best_avg:
            best, best_avg = a, avg
    conn.close()
    return best


def rl_feedback(key: str, action: str, reward: float) -> str:
    """Catat reward untuk pasangan (key, action) agar pilihan berikutnya membaik."""
    try:
        conn = _rl_conn()
        row = conn.execute("SELECT count, total FROM bandit WHERE key=? AND action=?", (key, action)).fetchone()
        if row:
            conn.execute("UPDATE bandit SET count=?, total=? WHERE key=? AND action=?",
                         (row[0] + 1, row[1] + float(reward), key, action))
        else:
            conn.execute("INSERT INTO bandit (key, action, count, total) VALUES (?,?,1,?)",
                         (key, action, float(reward)))
        conn.commit(); conn.close()
        return f"Reward dicatat: {key}/{action} += {reward}"
    except Exception as exc:
        return f"GAGAL rl_feedback: {exc}"


# ============================================================================
# COMPUTER USE (pyautogui)
# ============================================================================

def _pyautogui():
    import pyautogui
    pyautogui.FAILSAFE = True
    return pyautogui


def computer_screenshot(path: str | None = None) -> str:
    """Ambil screenshot layar; simpan PNG dan kembalikan path."""
    try:
        pg = _pyautogui()
    except Exception:
        return "pyautogui belum terpasang. Install: `pip install pyautogui pillow`"
    try:
        path = path or str(Path(tempfile.gettempdir()) / f"naraya_shot_{int(time.time())}.png")
        pg.screenshot(path)
        return f"Screenshot: {path}"
    except Exception as exc:
        return f"GAGAL screenshot: {exc}"


def computer_click(x: int, y: int, button: str = "left") -> str:
    """Klik mouse di (x, y). button: left/right/middle."""
    try:
        pg = _pyautogui()
    except Exception:
        return "pyautogui belum terpasang. Install: `pip install pyautogui`"
    try:
        pg.click(x=int(x), y=int(y), button=button)
        return f"Klik {button} di ({x}, {y})."
    except Exception as exc:
        return f"GAGAL klik: {exc}"


def computer_type(text: str, interval: float = 0.02) -> str:
    """Ketik teks pada fokus saat ini."""
    try:
        pg = _pyautogui()
    except Exception:
        return "pyautogui belum terpasang. Install: `pip install pyautogui`"
    try:
        pg.write(text, interval=interval)
        return f"Mengetik {len(text)} karakter."
    except Exception as exc:
        return f"GAGAL mengetik: {exc}"


def computer_key(keys: str) -> str:
    """Tekan tombol/kombinasi, mis. 'enter' atau 'ctrl+c'."""
    try:
        pg = _pyautogui()
    except Exception:
        return "pyautogui belum terpasang. Install: `pip install pyautogui`"
    try:
        combo = [k.strip() for k in keys.split("+") if k.strip()]
        pg.hotkey(*combo) if len(combo) > 1 else pg.press(combo[0])
        return f"Menekan: {keys}"
    except Exception as exc:
        return f"GAGAL menekan tombol: {exc}"


# ============================================================================
# MCP (client + extensions)
# ============================================================================

_MCP_CONFIG = Path("core/mcp_servers.json")
_MCP_CONFIG_ALT = Path("mcp_servers.json")


def _mcp_config_path() -> Path:
    return _MCP_CONFIG if _MCP_CONFIG.exists() else _MCP_CONFIG_ALT


def _load_mcp_config() -> dict:
    p = _mcp_config_path()
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8")).get("mcpServers", {})
        except Exception:
            return {}
    return {}


def mcp_list_servers() -> str:
    """Daftar MCP server yang terdaftar."""
    cfg = _load_mcp_config()
    if not cfg:
        return ('Belum ada MCP server. Tambah via mcp_add_server atau edit core/mcp_servers.json:\n'
                '{ "mcpServers": { "nama": { "command": "npx", "args": ["-y", "paket"] } } }')
    return "\n".join(f"- {n}: {m.get('command','')} {' '.join(m.get('args',[]))}" for n, m in cfg.items())


def mcp_add_server(name: str, command: str, args: list | None = None, env: dict | None = None) -> str:
    """MCP Extensions: daftarkan MCP server baru ke core/mcp_servers.json saat runtime."""
    try:
        p = _mcp_config_path()
        doc = {"mcpServers": {}}
        if p.exists():
            doc = json.loads(p.read_text(encoding="utf-8"))
            doc.setdefault("mcpServers", {})
        doc["mcpServers"][name] = {"command": command, "args": args or [], "env": env or {}}
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        return f"MCP server '{name}' didaftarkan."
    except Exception as exc:
        return f"GAGAL mcp_add_server: {exc}"


def _mcp_params(server_name: str):
    cfg = _load_mcp_config()
    if server_name not in cfg:
        raise ValueError(f"MCP server '{server_name}' tidak ada.")
    meta = cfg[server_name]
    from mcp import StdioServerParameters
    return StdioServerParameters(command=meta["command"], args=meta.get("args", []),
                                 env={**os.environ, **meta.get("env", {})})


def mcp_list_tools(server_name: str) -> str:
    """Lihat daftar tool sebuah MCP server."""
    try:
        from mcp import ClientSession
        from mcp.client.stdio import stdio_client
    except Exception:
        return "Paket MCP belum terpasang. Install: `pip install mcp`"

    async def _go():
        async with stdio_client(_mcp_params(server_name)) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                t = await s.list_tools()
                return "\n".join(f"- {x.name}: {(x.description or '').splitlines()[0] if x.description else ''}" for x in t.tools)
    try:
        return _run_async(_go()) or "(tidak ada tool)"
    except Exception as exc:
        return f"GAGAL list tools '{server_name}': {exc}"


def mcp_call(server_name: str, tool_name: str, arguments: dict | None = None) -> str:
    """Panggil tool pada MCP server eksternal."""
    try:
        from mcp import ClientSession
        from mcp.client.stdio import stdio_client
    except Exception:
        return "Paket MCP belum terpasang. Install: `pip install mcp`"

    async def _go():
        async with stdio_client(_mcp_params(server_name)) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                res = await s.call_tool(tool_name, arguments or {})
                parts = [getattr(c, "text", None) or str(c) for c in (getattr(res, "content", []) or [])]
                return "\n".join(parts) if parts else "(tidak ada output)"
    try:
        return _run_async(_go())
    except Exception as exc:
        return f"GAGAL {server_name}.{tool_name}: {exc}"


# Daftar tool agen (sumber hitung ringan untuk banner; samakan dgn ALL_TOOLS di rag_agent.py)
TOOL_NAMES = [
    "orkestrasi_multiagent",
    "cari_data_hermes", "jalankan_command_aman", "jalankan_orchestrator", "lihat_skill_hermes_terbaru",
    "web_search", "browser", "browser_cdp", "web_automation", "x_search",
    "eksekusi_python", "terminal",
    "delegate_task", "plan_task", "kompres_konteks",
    "vision_analyze", "generate_image", "text_to_speech", "speech_to_text",
    "computer_screenshot", "computer_click", "computer_type", "computer_key",
    "send_message", "home_assistant", "automate_schedule",
    "rl_select", "rl_feedback",
    "daftar_provider", "ganti_provider",
    "claude_code", "codex",
    "tugas_tetapkan", "tugas_selesai", "tugas_lihat",
    "baca_file", "tulis_file", "tambah_file", "edit_file", "hapus_file", "daftar_file", "buat_folder", "pindah_file",
    "mcp_daftar_server", "mcp_daftar_tool", "mcp_panggil", "mcp_tambah_server",
]
TOOL_COUNT = len(TOOL_NAMES)


if __name__ == "__main__":
    print("== smoke test (offline) ==")
    print("run_python:", run_python("print(6*7)").strip())
    print("compress :", compress_context("Satu. Dua. Tiga. Empat. Lima. Enam. Tujuh.")[:60])
    print("terminal :", terminal("echo halo").strip())
    print("rl_select:", rl_select("ctx", ["a", "b", "c"]))
    print("mcp      :", mcp_list_servers()[:60])
