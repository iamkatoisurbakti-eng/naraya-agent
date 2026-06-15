#!/usr/bin/env python3
"""
naraya.py — CLI Naraya-Agent.

Pertama kali (dari root repo):
    python naraya.py install     # pasang dependensi + daftar perintah global + onboarding
Setelahnya, dari folder mana saja:
    naraya                       # langsung masuk obrolan interaktif (REPL)
    naraya <perintah>

Perintah:
    install               Pasang dependensi + daftarkan perintah global `naraya` + onboarding
    chat                  Obrolan interaktif (REPL bersesi; perintah: /new /sessions /model /work)
    work "<goal>"         Kerjakan tugas via orkestrasi multi-agen (14+ agen)
                          opsi: --seq, --no-revise, --budget N
    gateway [platform]    Jalankan di Telegram (didukung) / wa/discord/slack (rencana)
    sessions              Daftar sesi tersimpan
    provider [nama]       Lihat/ganti provider LLM (--list, --test)
    model [nama]          Lihat/ganti model aktif
    agent                 REPL agen penuh (tools + RAG; butuh deps opsional)
    eval | learn | daemon Benchmark / self-learning sekali / daemon 24/7
    skills [kueri]        Lihat/cocokkan skills
    doctor | version      Diagnostik / versi

Flag global:
    --profile <nama>      Profil terpisah (sesi & pilihan provider/model sendiri)
    --continue, -c        Lanjutkan sesi terakhir
    --resume <id>, -r     Lanjutkan sesi tertentu
"""

from __future__ import annotations

import os
import sys
import time
import asyncio
from pathlib import Path


def _toks(s: str) -> int:
    """Estimasi kasar jumlah token (~4 char/token)."""
    return max(0, len(s or "") // 4)


def _ftok(n: int) -> str:
    """Format token ringkas: 1234 -> 1.2k."""
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def _fmt_dt(sec: float) -> str:
    """Format durasi: 65 -> '1m 5s', 8 -> '8s'."""
    s = int(round(sec))
    return f"{s // 60}m {s % 60}s" if s >= 60 else f"{s}s"

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)                                  # agar path relatif (data/, core/eval) konsisten
sys.path.insert(0, str(ROOT / "core"))          # modul inti ada di core/

__version__ = "0.1.0"

OPTS: dict = {}   # flag global: continue, resume, (profile/yolo via env)

CLARIFY_RULE = (
    "\n\nPENTING — KLARIFIKASI DULU: Jika permintaan pengguna belum lengkap detailnya "
    "(mis. 'buatkan landing page' tanpa tema, judul, gaya/desain, target pengguna, atau isi konten), "
    "JANGAN langsung mengerjakan. Ajukan dulu 2-4 pertanyaan klarifikasi singkat dalam Bahasa Indonesia, "
    "lalu tunggu jawaban. Kerjakan hanya setelah detail cukup, kecuali pengguna eksplisit bilang "
    "'langsung saja' atau 'pakai asumsimu'."
)

BANNER = """
  ███╗   ██╗ █████╗ ██████╗  █████╗ ██╗   ██╗ █████╗
  ████╗  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗
  ██╔██╗ ██║███████║██████╔╝███████║ ╚████╔╝ ███████║
  ██║╚██╗██║██╔══██║██╔══██╗██╔══██║  ╚██╔╝  ██╔══██║
  ██║ ╚████║██║  ██║██║  ██║██║  ██║   ██║   ██║  ██║
  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
"""


def _c(code: str, s: str) -> str:
    """Warna ANSI (otomatis nonaktif bila bukan TTY)."""
    if not sys.stdout.isatty() or os.getenv("NO_COLOR"):
        return s
    return f"\033[{code}m{s}\033[0m"


# Palet pelangi (256-color) untuk gradien horizontal banner.
_RAINBOW = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 48,
            50, 51, 45, 39, 33, 27, 63, 99, 135, 171, 207, 201]


def _rainbow(text: str) -> str:
    """Warnai teks dengan gradien pelangi per kolom (nonaktif bila bukan TTY)."""
    if not sys.stdout.isatty() or os.getenv("NO_COLOR"):
        return text
    n = len(_RAINBOW)
    lines = []
    for line in text.split("\n"):
        if not line.strip():
            lines.append(line)
            continue
        width = max(1, len(line) - 1)
        buf = []
        for i, ch in enumerate(line):
            if ch == " ":
                buf.append(" ")
            else:
                color = _RAINBOW[int(i / width * (n - 1))]
                buf.append(f"\033[1;38;5;{color}m{ch}")
        buf.append("\033[0m")
        lines.append("".join(buf))
    return "\n".join(lines)


def _stats():
    """Hitung total tools / skills / agen secara ringan & aman."""
    tools = skills = agents = None
    try:
        import agent_tools
        tools = agent_tools.TOOL_COUNT
    except Exception:
        pass
    try:
        import skills_index
        skills = len(skills_index.load_skills())
    except Exception:
        pass
    try:
        import multi_agent
        agents = len(multi_agent.AGENTS)
    except Exception:
        pass
    return tools, skills, agents


def _rule(width: int = 54) -> str:
    return _c("2", "  " + "─" * width)


def _print_columns(items, cols: int = 3, indent: str = "  ") -> None:
    """Cetak daftar dalam beberapa kolom rapi."""
    items = list(items)
    if not items:
        return
    w = max(len(str(x)) for x in items) + 2
    for i in range(0, len(items), cols):
        row = items[i:i + cols]
        print(indent + "".join(str(x).ljust(w) for x in row).rstrip())


def _boxed_input(width: int = 58) -> str:
    """Input chat pengguna di dalam kotak."""
    print(_c("36", "╭" + "─" * width + "╮"))
    try:
        s = input(_c("36", "│ ") + _c("32;1", "❯ "))
    finally:
        print(_c("36", "╰" + "─" * width + "╯"))
    return s


def print_banner():
    print(_rainbow(BANNER))
    prov, mdl = "?", "?"
    try:
        import providers
        cfg = providers.resolve()
        prov, mdl = cfg["name"], (cfg["model"] or "default")
    except Exception:
        pass
    print("  " + _c("1", "Naraya Agent") + _c("2", "  |  ") + _c("36;1", prov)
          + _c("2", "  |  ") + _c("36;1", mdl))
    print(_rule())
    t, s, _a = _stats()
    seg = []
    if t is not None:
        seg.append(_c("36;1", f"{t}") + _c("2", " tools"))
    if s is not None:
        seg.append(_c("36;1", f"{s}") + _c("2", " skills"))
    if seg:
        print("  " + _c("2", "  ·  ").join(seg))
    print(_rule())
    print()


def _need(mod: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(mod) is not None


DEPS_SENTINEL = ROOT / ".naraya" / "deps_ok"


def _pip(pkgs: list[str]) -> bool:
    import subprocess
    base = [sys.executable, "-m", "pip", "install", "-q"] + pkgs
    for extra in ([], ["--user"], ["--break-system-packages"]):
        try:
            if subprocess.call(base + extra) == 0:
                return True
        except Exception:
            continue
    return False


def _bootstrap(force: bool = False):
    """Auto-install tahan-banting: pasang INTI dulu (cepat) lalu sisanya best-effort."""
    core_ready = _need("openai") and _need("dotenv")
    if DEPS_SENTINEL.exists() and core_ready and not force:
        return
    print(_c("36", "Menyiapkan Naraya (sekali saja)..."))
    # 1) Inti wajib — agar chat/work langsung jalan walau paket berat gagal
    if not core_ready:
        core_ready = _pip(["openai", "python-dotenv"])
    # 2) Sisanya (anthropic, httpx, playwright, mcp, chromadb, ...) — best-effort
    req = ROOT / "requirements.txt"
    if req.exists():
        _pip(["-r", str(req)])
    if core_ready:
        DEPS_SENTINEL.parent.mkdir(parents=True, exist_ok=True)
        DEPS_SENTINEL.write_text("ok")
        print(_c("32", "Siap.\n"))
    else:
        print(_c("33", "Gagal memasang inti. Coba manual: pip install openai python-dotenv\n"))


def _register_global_command() -> bool:
    """Daftarkan perintah global `naraya` (pip install -e .) agar bisa dipakai dari mana saja."""
    import subprocess
    # setuptools lawas tak dukung editable PEP 660 -> upgrade dulu (best-effort)
    _pip(["-U", "pip", "setuptools", "wheel"])
    base = [sys.executable, "-m", "pip", "install", "-q", "-e", "."]
    for cmd in (base, base + ["--user"], base + ["--break-system-packages"]):
        try:
            if subprocess.call(cmd, cwd=str(ROOT)) == 0:
                return True
        except Exception:
            continue
    return False


def _scripts_dir() -> str:
    try:
        import sysconfig
        return sysconfig.get_path("scripts") or ""
    except Exception:
        return ""


def cmd_install(args):
    """Onboarding utama: pasang dependensi + daftarkan perintah global `naraya` + wizard."""
    _bootstrap(force=True)
    cmd_setup(args)


def cmd_update(args):
    """Update Naraya dari git lalu pasang dependensi baru (bila ada)."""
    import subprocess
    print(_c("36", "Memperbarui Naraya dari GitHub ..."))
    rc = subprocess.call(["git", "-C", str(ROOT), "pull", "--ff-only"])
    if rc != 0:
        print(_c("33", "git pull gagal — mungkin ada perubahan lokal. Pilihan:"))
        print("  git -C \"%s\" stash && git -C \"%s\" pull --ff-only" % (ROOT, ROOT))
        print("  atau (buang perubahan lokal): git -C \"%s\" fetch origin && git -C \"%s\" reset --hard origin/main" % (ROOT, ROOT))
        return
    _bootstrap(force=True)
    print(_c("32", "Update selesai.") + " Cek: naraya doctor")


def cmd_setup(args):
    """Wizard onboarding pertama kali."""
    print_banner()
    print(_c("1", "Selamat datang! Menyiapkan Naraya...\n"))

    # 1) cek dependensi inti
    core_ok = _need("openai") and _need("dotenv")
    print(f"  1) Dependensi inti  : {_c('32','OK ✓') if core_ok else _c('33','belum — jalankan: pip install -r requirements.txt')}")

    # 2) cek API key / provider
    has_env = (ROOT / ".env").exists()
    key = False
    provname = "-"
    try:
        import providers
        cfg = providers.resolve()
        provname = cfg["name"]
        key = bool(cfg["api_key"])
    except Exception:
        pass
    if key:
        print(f"  2) Provider         : {_c('32','OK ✓')} ({provname})")
    else:
        print(f"  2) Provider         : {_c('33','belum ada API key')}")
        if not has_env:
            print(_c("2", "       • salin contoh : cp core/.env.example .env"))
        print(_c("2", "       • isi salah satu: OPENAI_API_KEY / NARAROUTER_API_KEY / OPENROUTER_API_KEY ..."))
        print(_c("2", "       • pilih provider: naraya provider <nama>"))

    # 3) skills
    try:
        import skills_index
        nsk = len(skills_index.load_skills())
    except Exception:
        nsk = 0
    print(f"  3) Skills           : {_c('32', str(nsk) + ' terindeks ✓') if nsk else _c('33','0 — cek folder skills/')}")

    # 4) daftarkan perintah global `naraya` agar bisa dipakai dari mana saja (tanpa cd)
    gok = _register_global_command()
    if gok:
        print(f"  4) Perintah global  : {_c('32', 'naraya ✓ (bisa dari folder mana saja)')}")
    else:
        print(f"  4) Perintah global  : {_c('33', 'belum — pakai: python naraya.py <perintah>')}")
        sd = _scripts_dir()
        if sd:
            print(_c("2", f"       • bila 'naraya' tak dikenali, tambahkan ke PATH: {sd}"))

    print()
    if core_ok and key:
        print(_c("32;1", "Siap! Dari folder mana saja:"))
        print('   naraya work "Buat REST API katalog produk"')
        print("   naraya chat")
    else:
        print(_c("33;1", "Lengkapi API key di .env, lalu jalankan: naraya doctor"))
    print()


def cmd_version(args):
    print(f"Naraya-Agent {__version__}")


def cmd_doctor(args):
    import importlib.util
    print(f"Naraya-Agent {__version__}")
    print("Python   :", sys.version.split()[0])
    try:
        import providers, llm
        cfg = providers.resolve()
        print("Provider :", cfg["name"], f"({cfg['title']})")
        print("Model    :", cfg["model"] or "(default)")
        print("API key  :", "ada ✓" if cfg["api_key"] else "TIDAK ADA ✗ (isi .env)")
    except Exception as e:
        print("Provider : error:", e)
    deps = ["openai", "dotenv", "anthropic", "httpx", "playwright", "pyautogui",
            "PIL", "mcp", "apscheduler", "agents", "chromadb"]
    print("Dependensi:")
    for d in deps:
        print(f"  {'✓' if importlib.util.find_spec(d) else '·'} {d}")
    print("Skills    :", end=" ")
    try:
        import skills_index
        print(len(skills_index.load_skills()), "terindeks")
    except Exception as e:
        print("error:", e)


def cmd_provider(args):
    import providers
    rest = args
    if not rest:
        print(providers.list_providers()); return
    if rest[0] == "--list":
        print(providers.list_providers()); return
    if rest[0] == "--test":
        print(providers.test_provider(rest[1] if len(rest) > 1 else None)); return
    print(providers.set_provider(rest[0]))
    try:
        import llm; llm.refresh()
    except Exception:
        pass


def cmd_model(args):
    import providers
    if args:
        print(providers.set_model(" ".join(args)))
    else:
        print("Model aktif:", providers.resolve()["model"] or "(default provider)")
        print("Ganti: naraya model <nama-model>")
    try:
        import llm; llm.refresh()
    except Exception:
        pass


def cmd_gateway(args):
    import gateway
    gateway.run(args[0] if args else "telegram")


def cmd_coders(args):
    import coding_cli
    if args and args[0] in ("install", "--install"):
        print(coding_cli.install_coding_clis())
    else:
        print(coding_cli.status())
        print("\nPasang Claude Code & Codex: naraya coders install")


def cmd_install_coders(args):
    import coding_cli
    print(coding_cli.install_coding_clis())


def _pick_provider():
    """Pemilih provider interaktif (list bernomor)."""
    import providers
    names = providers.ORDER
    active = providers.current_name()
    print("Pilih provider:")
    for i, n in enumerate(names, 1):
        cfg = providers.resolve(n)
        mark = "●" if n == active else " "
        keyst = "key✓" if cfg["api_key"] else "key✗"
        print(f"  {i:>2}. {mark} {providers.REGISTRY[n]['title']:<34} [{n}]  {keyst}")
    try:
        choice = input("Nomor/nama (ENTER batal): ").strip()
    except (EOFError, KeyboardInterrupt):
        print(); return
    if not choice:
        return
    if choice.isdigit() and 1 <= int(choice) <= len(names):
        choice = names[int(choice) - 1]
    print(providers.set_provider(choice))
    try:
        import llm; llm.refresh()
    except Exception:
        pass


def _pick_model():
    """Pemilih model interaktif: ambil daftar dari provider aktif lalu pilih."""
    import providers
    print("Mengambil daftar model dari provider aktif ...")
    models = providers.list_models()
    if not models:
        print("Tak bisa mengambil daftar otomatis (provider tak mendukung / tanpa key).")
        try:
            m = input("Ketik nama model (ENTER batal): ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); return
        if m:
            print(providers.set_model(m))
    else:
        for i, m in enumerate(models, 1):
            print(f"  {i:>2}. {m}")
        try:
            choice = input("Nomor/nama (ENTER batal): ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); return
        if not choice:
            return
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            choice = models[int(choice) - 1]
        print(providers.set_model(choice))
    try:
        import llm; llm.refresh()
    except Exception:
        pass


def cmd_providers(args):
    import providers
    if args:
        print(providers.set_provider(args[0]))
        try:
            import llm; llm.refresh()
        except Exception:
            pass
    else:
        _pick_provider()


def cmd_models(args):
    import providers
    if args:
        print(providers.set_model(" ".join(args)))
        try:
            import llm; llm.refresh()
        except Exception:
            pass
    else:
        _pick_model()


def cmd_chat(args):
    import llm, prompt_store, providers, session_store
    if not llm.is_available():
        print("Tidak ada API key. Set provider/.env dulu (lihat: naraya doctor)."); return

    sess = None
    if OPTS.get("resume"):
        sess = session_store.load(OPTS["resume"])
        if sess is None:
            print(_c("33", f"Sesi '{OPTS['resume']}' tidak ditemukan, membuat baru."))
    if sess is None and OPTS.get("continue"):
        sess = session_store.latest()
    if sess is None:
        sess = session_store.create()

    print_banner()
    cfg = providers.resolve()
    prof = __import__('paths').profile()
    prof_txt = _c("2", f"  ·  profil {prof}") if prof != "default" else ""
    print("  " + _rainbow(f"[Sesi {sess['id']}]") + prof_txt)
    cont = f"  ·  lanjut {len(sess['messages'])} pesan" if sess.get("messages") else ""
    print("  " + _c("2", "ketik ") + _c("1", "/help") + _c("2", " untuk perintah")
          + _c("2", cont))
    print(_rule())
    print()
    sysp = prompt_store.get_active_prompt() + CLARIFY_RULE

    while True:
        try:
            msg = _boxed_input().strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        if not msg:
            continue
        low = msg.lower()
        if low in ("/exit", "/quit", "exit", "quit"):
            break
        if low == "/help":
            print(_c("2", "  /new  /sessions  /todo  /tools  /skills  /models  /providers  /work <goal>  /exit"))
            continue
        if low == "/tools":
            cmd_tools([]); continue
        if low == "/skills" or low.startswith("/skills "):
            cmd_skills(msg.split()[1:]); continue
        if low == "/todo" or low.startswith("/todo "):
            import todo
            parts = msg.split()
            if len(parts) == 1:
                print(todo.render())
            elif parts[1] == "add" and len(parts) > 2:
                print(todo.render(todo.add(msg.split(maxsplit=2)[2])))
            elif parts[1] == "done" and len(parts) > 2:
                try:
                    print(todo.render(todo.done(int(parts[2]))))
                except ValueError:
                    print(_c("2", "  pakai: /todo done <nomor>"))
            elif parts[1] == "clear":
                todo.clear(); print(_c("2", "  to-do dikosongkan"))
            else:
                print(todo.render())
            continue
        if low == "/new":
            sess = session_store.create(); print(_c("2", f"  sesi baru: {sess['id']}")); continue
        if low == "/sessions":
            for s in session_store.list_sessions():
                print(f"  {s['id']}  ({s['turns']} pesan)  {s['title']}")
            continue
        if low in ("/models", "/model"):
            _pick_model(); sysp = prompt_store.get_active_prompt() + CLARIFY_RULE; continue
        if low.startswith("/model"):           # /model <nama-model>
            cmd_models(msg.split(maxsplit=1)[1:]); sysp = prompt_store.get_active_prompt() + CLARIFY_RULE; continue
        if low in ("/providers", "/provider"):
            _pick_provider(); cfg = providers.resolve(); continue
        if low.startswith("/provider"):        # /provider <nama>
            cmd_providers(msg.split()[1:]); cfg = providers.resolve(); continue
        if low.startswith("/work"):
            force = msg.lstrip().startswith("/work!")
            goal = (msg.split("!", 1)[1] if force else msg[5:]).strip()
            if not goal:
                print(_c("2", "  pakai: /work <tugas>   (/work! untuk lewati klarifikasi)")); continue
            if not force:
                import clarify
                need, qs = clarify.assess(goal)
                if need and qs:
                    print(_c("33", "  Butuh detail dulu (ENTER untuk lewati tiap pertanyaan):"))
                    extra = []
                    for q in qs:
                        try:
                            a = input(_c("36", f"  • {q}\n    > ")).strip()
                        except (EOFError, KeyboardInterrupt):
                            a = ""; print()
                        if a:
                            extra.append(f"- {q} {a}")
                    if extra:
                        goal += "\n\nDetail tambahan:\n" + "\n".join(extra)
            import multi_agent
            print(_c("2", f"  ⋯ {cfg['model'] or cfg['name']} · ctx {_ftok(_toks(sysp + goal))}"))
            t0 = time.time()
            res = multi_agent.orchestrate(goal, revise=True, on_event=lambda ev: print(
                _c("2", f"    [{ev['status']}] {ev['agent']}" + (f" rev{ev['round']}" if ev.get('round') else ""))))
            print(_c("2", f"  ✓ selesai {time.time() - t0:.1f}s"))
            ans = _finish_project(res)
            print("\n" + ans + "\n")
            session_store.append(sess, "user", msg)
            session_store.append(sess, "assistant", ans)
            continue
        else:
            hist = session_store.history_text(sess)
            prompt = (f"Riwayat percakapan:\n{hist}\n\nPesan baru: {msg}" if hist else msg)
            t0 = time.time()
            try:
                ans = llm.chat(prompt, system=sysp)
            except Exception as e:
                ans = f"[error] {e}"
            dt = time.time() - t0
        print("\n" + ans + "\n")
        print(_c("2", f"({_fmt_dt(dt)} · ↓ {_ftok(_toks(ans))} tokens)") + "\n")
        session_store.append(sess, "user", msg)
        session_store.append(sess, "assistant", ans)


def _finish_project(res: dict) -> str:
    """Tulis berkas hasil ke workspace/ dan kembalikan RINGKASAN singkat (tanpa kode utuh)."""
    import workspace_writer
    info = workspace_writer.write_project(res)
    lines = [_c("32;1", "✓ Project siap")
             + _c("2", f"  ·  {res.get('mode','?')} · {len(res.get('agents', []))} agen · revisi {len(res.get('revisions', []))}")]
    lines.append(_c("1", f"  📁 {info['dir']}"))
    if info["files"]:
        for f in info["files"]:
            lines.append(_c("36", f"   + {f['path']}") + _c("2", f"  ({f['bytes']} B)"))
    else:
        lines.append(_c("33", "   (tidak ada berkas kode terdeteksi)"))
    lines.append(_c("2", f"   laporan lengkap → {info['dir']}/REPORT.md"))
    summ = (res.get("summary") or "").strip()
    if summ:
        lines.append("")
        lines.append(_c("2", "  Ringkasan: ") + summ[:400])
    return "\n".join(lines)


def cmd_work(args):
    import multi_agent
    mode = "sequential" if "--seq" in args else "parallel"
    revise = "--no-revise" not in args
    budget = 700
    if "--budget" in args:
        try:
            budget = int(args[args.index("--budget") + 1])
        except Exception:
            pass
    goal = " ".join(a for a in args if not a.startswith("--") and not a.isdigit()) \
        or " ".join(a for a in args if not a.startswith("--"))
    force = "--yes" in args or "-y" in args
    goal = " ".join(a for a in args if a not in ("--seq", "--no-revise", "--budget", "--yes", "-y", str(budget)))
    if not goal.strip():
        print('Pakai: naraya work "deskripsi tugas"   (tambah --yes untuk lewati klarifikasi)'); return
    if not force:
        import clarify
        need, qs = clarify.assess(goal)
        if need and qs:
            print("Butuh detail dulu (jawab; ENTER lewati tiap pertanyaan; atau pakai --yes):")
            extra = []
            for q in qs:
                try:
                    a = input(f"  • {q}\n    > ").strip()
                except (EOFError, KeyboardInterrupt):
                    a = ""; print()
                if a:
                    extra.append(f"- {q} {a}")
            if extra:
                goal += "\n\nDetail tambahan:\n" + "\n".join(extra)
    print(f"(mode={mode} · revise={revise} · budget={budget})\n")
    res = multi_agent.orchestrate(goal, mode=mode, revise=revise, context_budget=budget,
                                  on_event=lambda ev: print(_c("2", f"  [{ev['status']}] {ev['agent']}"
                                                            + (f" rev{ev['round']}" if ev['round'] else ""))))
    print("\n" + _finish_project(res))


def cmd_agent(args):
    if not (_need("agents") and _need("chromadb")):
        print("REPL agen penuh butuh: pip install openai-agents chromadb")
        print("Untuk sekarang gunakan: naraya chat  atau  naraya work \"...\"")
        return
    import rag_agent
    asyncio.run(rag_agent.main())


def cmd_eval(args):
    import llm
    if not llm.is_available():
        print("Tidak ada API key (lihat: naraya doctor)."); return
    from benchmark_engine import run_benchmark
    res = run_benchmark()
    print(f"SKOR: {res['score']}/100 ({res['num_tasks']} task)")
    for d in res["details"]:
        print(f"  {d['id']:<22} {d['total']:<6} det={d['deterministic']} judge={d['judge']}")


def cmd_learn(args):
    import naraya_daemon
    import json
    print(json.dumps(naraya_daemon.learn_cycle(), ensure_ascii=False, indent=2))


def cmd_daemon(args):
    import naraya_daemon
    naraya_daemon.main()


def cmd_tools(args):
    import agent_tools
    names = sorted(agent_tools.TOOL_NAMES)
    print(_c("1", f"{len(names)} tools:") + "\n")
    _print_columns(names, cols=3)


def cmd_skills(args):
    import skills_index
    if args:
        print(skills_index.relevant_text(" ".join(args), k=15))
        return
    from collections import defaultdict
    skills = skills_index.load_skills()
    groups = defaultdict(list)
    for s in skills:
        groups[(s.get("category") or "lainnya").strip() or "lainnya"].append(s.get("name", ""))
    print(_c("1", f"{len(skills)} skills") + _c("2", f" · {len(groups)} kategori"))
    for cat in sorted(groups):
        items = sorted(x for x in groups[cat] if x)
        print("\n" + _c("36;1", cat) + _c("2", f"  ({len(items)})"))
        _print_columns(items, cols=3)


def cmd_todo(args):
    import todo
    if not args:
        print(todo.render()); return
    sub = args[0]
    if sub == "add" and len(args) > 1:
        print(todo.render(todo.add(" ".join(args[1:]))))
    elif sub == "done" and len(args) > 1:
        try:
            print(todo.render(todo.done(int(args[1]))))
        except ValueError:
            print("pakai: naraya todo done <nomor>")
    elif sub == "set" and len(args) > 1:
        print(todo.render(todo.set_items([x.strip() for x in " ".join(args[1:]).split(";") if x.strip()])))
    elif sub == "clear":
        todo.clear(); print("To-do dikosongkan.")
    else:
        print(todo.render())


def cmd_sessions(args):
    import session_store
    rows = session_store.list_sessions()
    if not rows:
        print("Belum ada sesi. Mulai: naraya chat"); return
    print("Sesi (terbaru dulu):")
    for s in rows:
        print(f"  {s['id']}  ({s['turns']} pesan)  {s['title']}")
    print("\nLanjutkan: naraya --resume <id>   |   terbaru: naraya --continue")


COMMANDS = {
    "setup": cmd_setup, "install": cmd_install, "update": cmd_update, "version": cmd_version, "doctor": cmd_doctor,
    "provider": cmd_provider, "providers": cmd_providers, "model": cmd_model, "models": cmd_models,
    "gateway": cmd_gateway, "coders": cmd_coders, "install-coders": cmd_install_coders,
    "chat": cmd_chat, "work": cmd_work, "agent": cmd_agent, "sessions": cmd_sessions, "todo": cmd_todo,
    "eval": cmd_eval, "learn": cmd_learn, "daemon": cmd_daemon, "skills": cmd_skills, "tools": cmd_tools,
}

# Perintah ringan yang TIDAK memicu auto-install
_NO_BOOTSTRAP = {"version", "-h", "--help", "help", "install", "update", "sessions", "todo", "tools", "skills"}


def _parse_global(argv):
    """Sisihkan flag global: --profile, --continue/-c, --resume/-r, --yolo."""
    OPTS.clear()
    rest = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--profile" and i + 1 < len(argv):
            os.environ["NARAYA_PROFILE"] = argv[i + 1]; i += 2; continue
        if a in ("--continue", "-c"):
            OPTS["continue"] = True; i += 1; continue
        if a in ("--resume", "-r") and i + 1 < len(argv):
            OPTS["resume"] = argv[i + 1]; i += 2; continue
        if a == "--yolo":
            os.environ["NARAYA_YOLO"] = "1"; i += 1; continue
        rest.append(a); i += 1
    return rest


def main():
    argv = _parse_global(sys.argv[1:])

    # Tanpa perintah -> langsung chat REPL (gaya Hermes) bila sudah ter-install.
    if not argv:
        if DEPS_SENTINEL.exists():
            _bootstrap(); cmd_chat([]); return
        print_banner()
        print(_c("33", "Pemakaian pertama? Jalankan: ") + _c("1", "python naraya.py install") + "\n")
        print(__doc__); return

    if argv[0] in ("-h", "--help", "help"):
        print_banner(); print(__doc__); return

    cmd, rest = argv[0], argv[1:]
    fn = COMMANDS.get(cmd)
    if not fn:
        print(f"Perintah tidak dikenal: {cmd}\n")
        print(__doc__); return
    if cmd not in _NO_BOOTSTRAP:
        _bootstrap()                 # pasang dependensi otomatis pada pemakaian pertama
    fn(rest)


if __name__ == "__main__":
    main()
