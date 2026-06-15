"""
multi_agent.py — Orkestrasi Multi-Agen Naraya-Agent.

Setiap pekerjaan dijalankan sebagai PIPELINE 14 agen spesialis. Output tiap agen
dioper (handoff) ke agen berikutnya melalui "konteks berjalan" yang dikompres agar
hemat token. Semua run dicatat ke data/orchestration_runs.

Agen (urutan eksekusi):
  1. memory        — kumpulkan & ringkas konteks/memori relevan
  2. planner       — pecah goal jadi rencana langkah
  3. research      — kumpulkan fakta/informasi (boleh web_search)
  4. architect     — rancang arsitektur sistem/komponen & teknologi
  5. design        — rancang UX/UI & alur pengguna
  6. debate        — adu argumen pro-kontra, pilih opsi terbaik
  7. backend       — rancang API, model data, logika server
  8. frontend      — rancang komponen UI & integrasi
  9. coding        — tulis kode konkret
 10. testing       — rencana & kasus uji
 11. security      — tinjauan keamanan & mitigasi
 12. qa            — tinjauan kualitas menyeluruh
 13. documentation — dokumentasi ringkas
 14. deployment    — langkah deploy & rollback
(lalu memory menyimpan ringkasan hasil)

Offline-safe: tanpa API key, tiap agen mengembalikan status 'offline' tanpa crash,
dan orkestrator tetap menghasilkan struktur laporan.
"""

from __future__ import annotations

import json
import time
import sqlite3
from pathlib import Path

DB_PATH = Path("data/orchestration_runs.db")

# (key, Judul, system prompt, butuh_web)
AGENTS: dict[str, tuple[str, str, bool]] = {
    "memory": ("Memory Agent",
               "Kamu Memory Agent. Kumpulkan konteks relevan dan ringkas jadi fakta kunci, "
               "asumsi, dan batasan. Jika tidak ada, sebutkan asumsi wajar.", False),
    "planner": ("Planner Agent",
                "Kamu Planner Agent. Pecah goal menjadi rencana langkah berurutan yang konkret "
                "dan dapat dieksekusi. Tandai dependensi antar langkah.", False),
    "research": ("Research Agent",
                 "Kamu Research Agent. Kumpulkan informasi/fakta penting yang dibutuhkan untuk goal. "
                 "Sebutkan sumber bila ada. Fokus akurat, hindari mengada-ada.", True),
    "architect": ("Architect Agent",
                  "Kamu Architect Agent. Rancang arsitektur sistem: komponen, aliran data, pilihan "
                  "teknologi, dan trade-off utama.", False),
    "design": ("Design Agent",
               "Kamu Design Agent. Rancang UX/UI dan alur pengguna: layar utama, komponen, state, "
               "dan prinsip aksesibilitas. Jika non-UI, beri desain antarmuka/kontrak yang relevan.", False),
    "debate": ("Debate Agent",
               "Kamu Debate Agent. Tinjau rencana & arsitektur secara kritis. Adu argumen pro-kontra "
               "untuk opsi-opsi kunci, lalu PILIH opsi terbaik dengan alasan ringkas.", False),
    "backend": ("Backend Agent",
                "Kamu Backend Agent. Rancang API (endpoint), model data, dan logika server. "
                "Sertakan skema ringkas dan penanganan error.", False),
    "frontend": ("Frontend Agent",
                 "Kamu Frontend Agent. Rancang komponen UI dan integrasi ke backend (state, panggilan API, "
                 "penanganan loading/error).", False),
    "coding": ("Coding Agent",
               "Kamu Coding Agent. Tulis kode konkret sesuai rencana & arsitektur. Idiomatik, ringkas, "
               "dengan komentar seperlunya. Tunjukkan file/path bila relevan.", False),
    "testing": ("Testing Agent",
                "Kamu Testing Agent. Susun rencana uji dan kasus uji (unit/integrasi), termasuk edge case "
                "dan kriteria lulus.", False),
    "security": ("Security Agent",
                 "Kamu Security Agent. Tinjau risiko keamanan (input, auth, data, dependensi) dan beri "
                 "mitigasi konkret. Tolak pola berbahaya.", False),
    "qa": ("QA Agent",
           "Kamu QA Agent. Tinjau kualitas keseluruhan hasil agen sebelumnya. Temukan cacat/inkonsistensi "
           "dan beri rekomendasi perbaikan berprioritas.", False),
    "documentation": ("Documentation Agent",
                      "Kamu Documentation Agent. Tulis dokumentasi ringkas: ringkasan, cara pakai/menjalankan, "
                      "dan referensi API/konfigurasi bila ada.", False),
    "deployment": ("Deployment Agent",
                   "Kamu Deployment Agent. Susun langkah deploy yang konkret + prasyarat, variabel lingkungan, "
                   "dan rencana rollback.", False),
}

PIPELINE = [
    "memory", "planner", "research", "architect", "design", "debate",
    "backend", "frontend", "coding", "testing", "security", "qa",
    "documentation", "deployment",
]

# Mode PARALEL: agen yang tidak saling bergantung dijalankan serentak dalam satu fase.
# Fase dieksekusi berurutan; anggota dalam satu fase berjalan paralel (ThreadPool).
PHASES = [
    ["memory"],                              # konteks awal
    ["planner"],                             # rencana
    ["research"],                            # fakta pendukung
    ["architect", "design"],                 # rancangan sistem & UX (paralel)
    ["debate"],                              # putuskan opsi terbaik
    ["backend", "frontend"],                 # rancang dua sisi (paralel)
    ["coding"],                              # implementasi
    ["testing", "security", "qa"],           # tinjauan mutu (paralel)
    ["documentation", "deployment"],         # rilis (paralel)
]


def _ensure_db() -> None:
    Path("data").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS orchestration_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT, report TEXT, created_at INTEGER
        )"""
    )
    conn.commit()
    conn.close()


def _research_context(goal: str) -> str:
    """Tambahan fakta dari web untuk research agent (best-effort)."""
    try:
        import agent_tools
        res = agent_tools.web_search(goal, max_results=4)
        if res and not res.startswith("GAGAL"):
            return f"\n\nHASIL WEB_SEARCH:\n{res}"
    except Exception:
        pass
    return ""


def _run_agent(key: str, goal: str, context: str, agents_map: dict | None = None) -> str:
    amap = agents_map or AGENTS
    title, sys_p, need_web = amap[key]
    try:
        import llm
    except Exception:
        return f"[error] modul llm tidak tersedia"
    if not llm.is_available():
        return f"[offline] {title} siap; set provider/API key untuk menjalankan."

    extra = _research_context(goal) if need_web else ""
    user = (
        f"GOAL:\n{goal}\n\n"
        f"KONTEKS RINGKAS (ringkasan berjalan + skill relevan):\n{context or '(belum ada)'}{extra}\n\n"
        f"Sebagai {title}, kerjakan bagianmu. SANGAT ringkas & konkret (hemat token). "
        f"Manfaatkan SKILLS relevan yang tercantum bila cocok. "
        f"Jika bagian ini kurang relevan dengan goal, jawab satu baris saja."
    )
    try:
        return llm.chat(user, system=sys_p, temperature=0.3)
    except Exception as exc:
        return f"[error] {title}: {exc}"


def _compress(context: str, budget: int = 700) -> str:
    try:
        import agent_tools
        return agent_tools.compress_context(context, max_chars=budget)
    except Exception:
        return context[-budget:]


def _running_update(summary: str, title: str, out: str, budget: int = 700) -> str:
    """Pertahankan RINGKASAN BERJALAN yang padat (hemat token). Tambah digest 1 baris;
    bila melebihi budget, kompres sekali."""
    digest = re.sub(r"\s+", " ", (out or "")).strip()[:180]
    s = (summary + f"\n- {title}: {digest}").strip()
    if len(s) > budget:
        s = _compress(s, budget)
    return s


def _skills_block(goal: str) -> str:
    """Daftar skill relevan untuk disuntik ke konteks agen (selalu pakai skills)."""
    try:
        import skills_index
        return skills_index.relevant_text(goal, k=6)
    except Exception:
        return "(skill index tidak tersedia)"


def _dynamic_specialists(goal: str, max_extra: int = 3) -> dict:
    """Minta LLM menentukan agen spesialis TAMBAHAN bila pekerjaan membutuhkannya.
    Kembalikan map {key: (Title, system_prompt, need_web)}. Offline -> kosong."""
    try:
        import llm
        if not llm.is_available():
            return {}
        j = llm.chat_json(
            f"Untuk goal berikut, apakah perlu agen spesialis TAMBAHAN di luar tim standar "
            f"(memory, planner, research, architect, design, debate, backend, frontend, coding, "
            f"testing, security, qa, documentation, deployment)?\n\nGOAL: {goal}\n\n"
            f"Jika perlu, beri maksimal {max_extra}. Jika tidak, kembalikan list kosong.",
            system=('Kamu perancang tim agen. Jawab JSON: {"agents":[{"key":"data_engineer",'
                    '"title":"Data Engineer Agent","role":"deskripsi singkat tugasnya"}]}. '
                    'key huruf kecil_dengan_garis_bawah.'),
            default={"agents": []},
        )
        out = {}
        for a in (j.get("agents") or [])[:max_extra]:
            key = re.sub(r"[^a-z0-9_]", "", str(a.get("key", "")).lower())
            if not key or key in AGENTS:
                continue
            title = a.get("title") or key.replace("_", " ").title()
            role = a.get("role") or title
            out[key] = (title, f"Kamu {title}. {role} Ringkas dan konkret.", False)
        return out
    except Exception:
        return {}


def _phases_filtered(selected: set | None) -> list[list[str]]:
    if not selected:
        return PHASES
    out = []
    for ph in PHASES:
        grp = [k for k in ph if k in selected]
        if grp:
            out.append(grp)
    return out


REVIEW_AGENTS = ["testing", "security", "qa"]
FIXER_AGENT = "coding"
_REVISION_KEYWORDS = ["rentan", "vulnerab", "cacat", "bug", "gagal", "kritis", "perbaiki",
                      "tidak aman", "error", "masalah", "kurang", "risiko tinggi", "belum"]


def _needs_revision(findings: str) -> tuple[bool, str]:
    """Putuskan apakah temuan review menuntut revisi kode. LLM-judge bila ada, else heuristik."""
    try:
        import llm
        if llm.is_available():
            j = llm.chat_json(
                "Tinjau temuan Testing/Security/QA berikut. Apakah ADA isu yang HARUS diperbaiki "
                f"di kode sebelum rilis?\n\n{findings}",
                system='Kamu reviewer rilis. Jawab JSON {"needs_revision": true/false, "issues": "ringkasan isu yang harus diperbaiki"}.',
                default={"needs_revision": False, "issues": ""},
            )
            return bool(j.get("needs_revision")), str(j.get("issues", ""))
    except Exception:
        pass
    low = (findings or "").lower()
    hits = [k for k in _REVISION_KEYWORDS if k in low]
    return (len(hits) > 0, ("Indikasi isu: " + ", ".join(hits)) if hits else "")


def orchestrate(goal: str, agents: list[str] | None = None,
                mode: str = "sequential", max_workers: int = 4, verbose: bool = False,
                revise: bool = False, max_revisions: int = 2, on_event=None,
                dynamic: bool = True, context_budget: int = 700) -> dict:
    """Jalankan pipeline multi-agen — hemat token (ringkasan berjalan), pakai skills, agen dinamis.

    mode="sequential"|"parallel". agents: subset key (opsional). revise: loop perbaikan otomatis.
    on_event(ev): streaming progress. dynamic: tambah agen spesialis bila pekerjaan butuh.
    context_budget: batas karakter ringkasan antar-agen (hemat token).
    """
    import threading
    selected = set(agents) if agents else None

    # Tim agen = standar (+ spesialis dinamis bila perlu & tidak dibatasi subset)
    amap = dict(AGENTS)
    dyn_keys: list[str] = []
    if dynamic and not selected:
        for k, v in _dynamic_specialists(goal).items():
            amap[k] = v
            dyn_keys.append(k)

    skills_ctx = f"SKILLS RELEVAN (pakai bila cocok):\n{_skills_block(goal)}"
    report: dict[str, str] = {}
    order: list[str] = []
    summary = ""          # RINGKASAN BERJALAN yang padat (hemat token)
    events: list[dict] = []
    _lock = threading.Lock()

    def emit(agent, status, rnd=0, preview=""):
        ev = {"t": time.time(), "agent": agent, "status": status, "round": rnd, "preview": (preview or "")[:120]}
        with _lock:
            events.append(ev)
        if on_event:
            try:
                on_event(ev)
            except Exception:
                pass
        elif verbose:
            tag = f" (rev{rnd})" if rnd else ""
            print(f"  [{status:>5}]{tag} {amap.get(agent, (agent, '', False))[0]}")

    def agent_ctx():
        return f"{skills_ctx}\n\nRINGKASAN BERJALAN:\n{summary or '(kosong)'}"

    def run_one(key, ctx, rnd=0):
        emit(key, "start", rnd)
        out = _run_agent(key, goal, ctx, amap)
        emit(key, "done", rnd, out)
        return out

    # Susun fase; sisipkan spesialis dinamis sebagai fase setelah 'research'
    if mode == "parallel":
        phases = [list(p) for p in _phases_filtered(selected)]
        if dyn_keys:
            at = next((i + 1 for i, p in enumerate(phases) if "research" in p), len(phases))
            phases.insert(at, dyn_keys)
        from concurrent.futures import ThreadPoolExecutor
        for phase in phases:
            ctx = agent_ctx()  # snapshot sama untuk semua anggota fase
            if len(phase) == 1:
                outs = {phase[0]: run_one(phase[0], ctx)}
            else:
                outs = {}
                with ThreadPoolExecutor(max_workers=min(max_workers, len(phase))) as ex:
                    futs = {ex.submit(run_one, k, ctx): k for k in phase}
                    for fut in futs:
                        outs[futs[fut]] = fut.result()
            for k in phase:
                report[k] = outs[k]
                order.append(k)
                summary = _running_update(summary, amap[k][0], outs[k], context_budget)
    else:
        base = [k for k in (agents or PIPELINE) if k in amap]
        if dyn_keys:
            idx = (base.index("research") + 1) if "research" in base else len(base)
            base[idx:idx] = dyn_keys
        for key in base:
            out = run_one(key, agent_ctx())
            report[key] = out
            order.append(key)
            summary = _running_update(summary, amap[key][0], out, context_budget)

    # --- LOOP REVISI OTOMATIS: temuan review -> Coding perbaiki -> review ulang ---
    revisions: list[dict] = []
    have_review = [a for a in REVIEW_AGENTS if a in report]
    if revise and FIXER_AGENT in report and have_review:
        for rnd in range(1, max_revisions + 1):
            findings = "\n".join(f"{amap[a][0]}: {report[a][:200]}" for a in have_review)
            need, issues = _needs_revision(findings)
            emit("debate", "review", rnd, issues or "tidak ada isu")
            if not need:
                break
            fix_ctx = (f"{skills_ctx}\n\nRINGKASAN:\n{summary}\n\n"
                       f"TEMUAN YANG HARUS DIPERBAIKI (putaran {rnd}):\n{issues or findings}\n\n"
                       f"HASIL CODING SEBELUMNYA:\n{report.get(FIXER_AGENT, '')[:800]}")
            fixed = run_one(FIXER_AGENT, fix_ctx, rnd)
            report[f"{FIXER_AGENT}#rev{rnd}"] = fixed
            order.append(f"{FIXER_AGENT}#rev{rnd}")
            summary = _running_update(summary, f"Coding (revisi {rnd})", fixed, context_budget)
            rev_ctx = agent_ctx()
            re_outs = {}
            if mode == "parallel" and len(have_review) > 1:
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=min(max_workers, len(have_review))) as ex:
                    futs = {ex.submit(run_one, a, rev_ctx, rnd): a for a in have_review}
                    for fut in futs:
                        re_outs[futs[fut]] = fut.result()
            else:
                for a in have_review:
                    re_outs[a] = run_one(a, rev_ctx, rnd)
            for a in have_review:
                report[f"{a}#rev{rnd}"] = re_outs[a]
                order.append(f"{a}#rev{rnd}")
                report[a] = re_outs[a]
                summary = _running_update(summary, f"{amap[a][0]} (revisi {rnd})", re_outs[a], context_budget)
            revisions.append({"round": rnd, "issues": issues})

    # Memory Agent menyimpan ringkasan akhir
    try:
        from memory_cache import add_knowledge
        add_knowledge("system", "orchestration", f"GOAL: {goal}\nRINGKASAN: {summary}", confidence=0.8)
    except Exception:
        pass

    _ensure_db()
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO orchestration_runs (goal, report, created_at) VALUES (?,?,?)",
                     (goal, json.dumps(report, ensure_ascii=False), int(time.time())))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return {"goal": goal, "agents": order, "mode": mode, "report": report, "summary": summary,
            "events": events, "revisions": revisions, "dynamic_agents": dyn_keys,
            "agent_titles": {k: amap[k][0] for k in order}}


def _title_of(key: str, titles: dict | None = None) -> str:
    titles = titles or {}
    if "#rev" in key:
        base, rnd = key.split("#rev")
        t = titles.get(base) or AGENTS.get(base, (base,))[0]
        return f"{t} (revisi {rnd})"
    return titles.get(key) or AGENTS.get(key, (key, "", False))[0]


def format_report(result: dict) -> str:
    """Rangkai laporan jadi teks rapi untuk ditampilkan ke pengguna."""
    revs = result.get("revisions", [])
    titles = result.get("agent_titles", {})
    dyn = result.get("dynamic_agents", [])
    head = f"# Hasil Multi-Agen untuk: {result['goal']}"
    meta = (f"_mode: {result.get('mode','?')} · agen: {len(result.get('agents', []))} · "
            f"dinamis: {len(dyn)} · revisi: {len(revs)}_")
    lines = [head, meta, ""]
    for key in result.get("agents", []):
        lines.append(f"## {_title_of(key, titles)}")
        lines.append(result["report"].get(key, "").strip() or "(kosong)")
        lines.append("")
    if revs:
        lines.append("## Ringkasan Revisi Otomatis")
        for r in revs:
            lines.append(f"- Putaran {r['round']}: {r.get('issues','') or '(perbaikan diterapkan)'}")
    return "\n".join(lines)


def work(goal: str, mode: str = "parallel", revise: bool = True, on_event=None) -> str:
    """Entry praktis: orkestrasi penuh (default PARALEL + revisi otomatis) -> laporan teks.
    on_event(ev): callback untuk streaming progress tiap agen."""
    return format_report(orchestrate(goal, mode=mode, revise=revise, on_event=on_event))


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:]]
    mode = "sequential" if "--seq" in args else "parallel"
    no_revise = "--no-revise" in args
    args = [a for a in args if a not in ("--seq", "--no-revise")]
    g = " ".join(args) or "Buat aplikasi to-do list sederhana berbasis web."
    print(f"(mode: {mode} · revisi: {not no_revise}) — streaming progress:")
    res = orchestrate(g, mode=mode, revise=not no_revise, verbose=True)
    print(f"\nputaran revisi: {len(res['revisions'])}")
    print("\n=== RINGKASAN AKHIR ===")
    print(res["summary"][:800])
