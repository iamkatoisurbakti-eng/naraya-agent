from agent_core import ask_naraya

FEATURES = {
    "chat": "Agent Chat umum Naraya",
    "bisnis": "Agent Bisnis: analisis bisnis, strategi UMKM, upload produk",
    "keuangan": "Agent Keuangan: cashflow, transaksi, laporan, stok",
    "jasa": "Agent Jasa: marketplace, rekomendasi jasa, order flow",
    "content": "Agent Content: caption, hashtag, template konten",
    "bantu": "Agent Bantu: otomasi, WhatsApp, email, voice, CRM",
    "dompet": "Agent Dompet: QRIS, transaksi, ledger, pembayaran",
    "video": "Agent Video: reels, short video, script, caption video",
    "belajar": "Agent Belajar: tutor, kelas, skill, kurikulum",
    "sehat": "Agent Sehat: wellness, kebiasaan, tips kesehatan",
}

def detect_feature(message: str) -> str:
    msg = message.lower()

    mapping = {
        "bisnis": ["bisnis", "umkm", "jualan", "produk", "marketing"],
        "keuangan": ["uang", "cashflow", "transaksi", "stok", "laporan"],
        "jasa": ["jasa", "marketplace", "pesan jasa"],
        "content": ["caption", "konten", "hashtag", "instagram", "tiktok"],
        "bantu": ["otomasi", "whatsapp", "email", "voice", "crm"],
        "dompet": ["dompet", "qris", "transfer", "bayar"],
        "video": ["video", "reels", "short"],
        "belajar": ["belajar", "kelas", "skill", "tutor"],
        "sehat": ["sehat", "kesehatan", "tidur", "olahraga"],
    }

    for feature, keywords in mapping.items():
        if any(k in msg for k in keywords):
            return feature

    return "chat"

async def run_feature_worker(feature: str, message: str, user_id: str = "web-app") -> str:
    feature = feature.lower().strip()

    if feature not in FEATURES:
        feature = detect_feature(message)

    role = FEATURES.get(feature, FEATURES["chat"])

    prompt = f"""
    Kamu adalah worker fitur aplikasi Naraya.

    FITUR:
    {feature}

    ROLE:
    {role}

    Tugas:
    - jawab sesuai konteks fitur
    - jika perlu, beri langkah eksekusi
    - jangan keluar dari kebutuhan user
    - jawaban enak dibaca, ringkas, pakai emoji secukupnya

    PESAN USER:
    {message}
    """

    return await ask_naraya(prompt, user_id=user_id)
