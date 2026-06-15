"""
providers.py — Registry & pemilih provider LLM untuk Naraya-Agent.

Provider yang didukung:
  naraouter        NaraRouter   (https://router.naraya.ai/v1, OpenAI-compatible)
  openai           OpenAI       (https://api.openai.com/v1)
  anthropic        Anthropic    (Claude, SDK native)
  openrouter       OpenRouter   (https://openrouter.ai/api/v1)
  kilocode         Kilo Code    (https://api.kilo.ai/api/gateway, OpenAI-compatible)
  custom           Custom direct API   (base_url + key dari env, OpenAI-compatible)
  custom_endpoint  Custom Endpoint API (base_url + key dari env, OpenAI-compatible)

Pemilihan provider (urutan prioritas):
  argumen eksplisit > env NARAYA_PROVIDER > data/provider.json > auto-deteksi (key tersedia) > openai

Konfigurasi via environment (lihat .env.example). Tiap provider punya key_env sendiri,
dengan fallback ke NARAYA_API_KEY.
"""

from __future__ import annotations

import os
import json
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def _config_file() -> Path:
    try:
        import paths
        return paths.data_dir() / "provider.json"
    except Exception:
        return Path("data/provider.json")

# style: "openai" (pakai OpenAI SDK + base_url) atau "anthropic" (pakai Anthropic SDK)
REGISTRY: dict[str, dict] = {
    "naraouter": {
        "title": "NaraRouter (router.naraya.ai)",
        "style": "openai",
        "base_url": "https://router.naraya.ai/v1",
        "key_env": ["NARAROUTER_API_KEY", "NARAYA_API_KEY"],
        "default_model": "auto/naraya.ai",
    },
    "openai": {
        "title": "OpenAI",
        "style": "openai",
        "base_url": None,  # default SDK
        "key_env": ["OPENAI_API_KEY"],
        "default_model": "gpt-4.1-mini",
    },
    "anthropic": {
        "title": "Anthropic (Claude)",
        "style": "anthropic",
        "base_url": None,
        "key_env": ["ANTHROPIC_API_KEY"],
        "default_model": "claude-sonnet-4-6",
    },
    "openrouter": {
        "title": "OpenRouter",
        "style": "openai",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": ["OPENROUTER_API_KEY"],
        "default_model": "openai/gpt-4o-mini",
    },
    "kilocode": {
        "title": "Kilo Code (gateway)",
        "style": "openai",
        "base_url": "https://api.kilo.ai/api/gateway",
        "key_env": ["KILOCODE_API_KEY", "KILO_API_KEY"],
        "default_model": "",
    },
    "custom": {
        "title": "Custom direct API (OpenAI-compatible)",
        "style": "openai",
        "base_url_env": "NARAYA_CUSTOM_BASE_URL",
        "key_env": ["NARAYA_CUSTOM_API_KEY", "NARAYA_API_KEY"],
        "model_env": "NARAYA_CUSTOM_MODEL",
        "default_model": "",
    },
    "custom_endpoint": {
        "title": "Custom Endpoint API (OpenAI-compatible)",
        "style": "openai",
        "base_url_env": "NARAYA_ENDPOINT_URL",
        "key_env": ["NARAYA_ENDPOINT_API_KEY", "NARAYA_API_KEY"],
        "model_env": "NARAYA_ENDPOINT_MODEL",
        "default_model": "",
    },
}

ORDER = ["naraouter", "openai", "anthropic", "openrouter", "kilocode", "custom", "custom_endpoint"]


def _key_for(meta: dict) -> str | None:
    for env in meta.get("key_env", []):
        v = os.getenv(env)
        if v:
            return v
    return os.getenv("NARAYA_API_KEY")


def _load_cfg() -> dict:
    try:
        f = _config_file()
        if f.exists():
            return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _persisted() -> str | None:
    return _load_cfg().get("provider")


def _persisted_model() -> str | None:
    return _load_cfg().get("model")


def _auto_detect() -> str | None:
    for name in ORDER:
        if _key_for(REGISTRY[name]):
            return name
    return None


def current_name(explicit: str | None = None) -> str:
    name = (explicit or os.getenv("NARAYA_PROVIDER") or _persisted() or _auto_detect() or "openai")
    return name if name in REGISTRY else "openai"


def resolve(explicit: str | None = None) -> dict:
    """Kembalikan konfigurasi provider terpilih: name, title, style, base_url, api_key, model, judge_model."""
    name = current_name(explicit)
    meta = REGISTRY[name]
    base_url = os.getenv(meta["base_url_env"]) if meta.get("base_url_env") else meta.get("base_url")
    api_key = _key_for(meta)
    model = (os.getenv("NARAYA_MODEL")
             or _persisted_model()
             or (os.getenv(meta["model_env"]) if meta.get("model_env") else None)
             or meta.get("default_model") or "")
    judge = os.getenv("NARAYA_JUDGE_MODEL") or model
    return {
        "name": name, "title": meta["title"], "style": meta["style"],
        "base_url": base_url, "api_key": api_key, "model": model, "judge_model": judge,
    }


def set_provider(name: str) -> str:
    """Pilih provider aktif (disimpan, sadar-profil)."""
    if name not in REGISTRY:
        return f"Provider '{name}' tidak dikenal. Pilihan: {', '.join(ORDER)}"
    cfg_doc = _load_cfg()
    cfg_doc["provider"] = name
    _config_file().write_text(json.dumps(cfg_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    cfg = resolve(name)
    status = "siap (ada API key)" if cfg["api_key"] else "BELUM ada API key — set di .env"
    return f"Provider aktif: {cfg['title']} [{name}] · model: {cfg['model'] or '(set NARAYA_MODEL)'} · {status}"


def set_model(model: str) -> str:
    """Tetapkan model aktif (disimpan, sadar-profil)."""
    cfg_doc = _load_cfg()
    cfg_doc["model"] = model
    _config_file().write_text(json.dumps(cfg_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    cfg = resolve()
    return f"Model aktif: {model or '(default provider)'} · provider: {cfg['title']}"


def list_models(limit: int = 60) -> list[str]:
    """Ambil daftar model dari provider aktif (best-effort). Kosong bila tak didukung."""
    cfg = resolve()
    if not cfg["api_key"]:
        return []
    try:
        if cfg["style"] == "anthropic":
            import anthropic
            c = anthropic.Anthropic(api_key=cfg["api_key"])
            return [m.id for m in c.models.list().data][:limit]
        import llm
        c = llm._get_client()
        ids = [m.id for m in c.models.list().data]
        return sorted(ids)[:limit]
    except Exception:
        return []


def list_providers() -> str:
    """Daftar provider + status key + mana yang aktif."""
    active = current_name()
    lines = []
    for name in ORDER:
        cfg = resolve(name)
        mark = "●" if name == active else "○"
        keyst = "key✓" if cfg["api_key"] else "key✗"
        base = cfg["base_url"] or "(default)"
        lines.append(f" {mark} {name:<16} {REGISTRY[name]['title']:<38} {keyst}  {base}")
    return "Provider (● aktif):\n" + "\n".join(lines)


def test_provider(name: str | None = None) -> str:
    """Uji koneksi nyata: kirim 1 prompt kecil ke provider."""
    import llm
    cfg = resolve(name)
    if not cfg["api_key"]:
        return f"[{cfg['name']}] tidak ada API key."
    try:
        out = llm.chat("Balas satu kata: ok", model=cfg["model"] or None, provider=cfg["name"], temperature=0)
        return f"[{cfg['name']}] OK -> {out[:60]}"
    except Exception as exc:
        return f"[{cfg['name']}] GAGAL: {exc}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(set_provider(sys.argv[1]))
    else:
        print(list_providers())
