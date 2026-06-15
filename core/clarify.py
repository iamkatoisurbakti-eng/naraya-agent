"""
clarify.py — Gerbang klarifikasi: cegah Naraya langsung mengeksekusi tugas yang
detailnya belum lengkap. Menilai goal; bila ambigu/kurang detail, kembalikan
pertanyaan klarifikasi yang paling penting.
"""

from __future__ import annotations

_HEUR_Q = [
    "Apa tujuan/hasil akhir yang diharapkan?",
    "Ada batasan teknologi, format keluaran, atau target pengguna tertentu?",
    "Ada ruang lingkup yang harus disertakan / dikecualikan?",
]


def assess(goal: str) -> tuple[bool, list[str]]:
    """Kembalikan (perlu_klarifikasi, daftar_pertanyaan[2-4])."""
    g = (goal or "").strip()
    if not g:
        return True, ["Apa yang ingin kamu kerjakan?"]
    try:
        import llm
        if llm.is_available():
            j = llm.chat_json(
                f'Permintaan user: "{g}"\n\n'
                "Apakah detailnya CUKUP untuk dikerjakan dengan baik, atau ada info penting yang "
                "kurang (tujuan, ruang lingkup, teknologi/stack, target pengguna, format keluaran, "
                "batasan, data/sumber)? Bila kurang, beri 2-4 pertanyaan klarifikasi paling penting.",
                system=('Kamu analis kebutuhan yang teliti. Jawab JSON: '
                        '{"needs_clarification": true/false, "questions": ["..."]}. '
                        'Tandai true HANYA bila benar-benar ambigu/kurang detail untuk hasil berkualitas. '
                        'Untuk permintaan yang sudah jelas & spesifik, kembalikan false dengan questions kosong.'),
                default={"needs_clarification": False, "questions": []},
            )
            need = bool(j.get("needs_clarification"))
            qs = [str(q).strip() for q in (j.get("questions") or []) if str(q).strip()][:4]
            return (need and len(qs) > 0), qs
    except Exception:
        pass
    # Heuristik offline: terlalu pendek/generik -> minta detail.
    if len(g.split()) < 4:
        return True, _HEUR_Q[:2]
    return False, []


if __name__ == "__main__":
    import sys
    print(assess(" ".join(sys.argv[1:]) or "buat aplikasi"))
