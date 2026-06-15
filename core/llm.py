"""
llm.py — Klien LLM multi-provider terpusat untuk Naraya-Agent.

Provider dipilih lewat core/providers.py (NaraRouter, OpenAI, Anthropic, OpenRouter,
Kilo Code, Custom direct API, Custom Endpoint). Modul ini menyembunyikan perbedaan
antara gaya OpenAI (chat.completions) dan Anthropic (messages).

Surface publik (stabil):
  is_available()                      -> bool (provider aktif punya API key)
  chat(user, system, model, ...)      -> str
  chat_json(user, system, ...)        -> obj (parse JSON, tahan-banting)
  _get_client()                       -> klien OpenAI (untuk tool vision/image/voice)
  DEFAULT_MODEL, JUDGE_MODEL          -> dari provider aktif
  LLMUnavailable                      -> exception

Offline-safe: tanpa API key, panggilan melempar LLMUnavailable yang ditangkap engine.
"""

from __future__ import annotations

import re
import json
from typing import Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import providers


class LLMUnavailable(RuntimeError):
    """Dilempar saat LLM tidak bisa dipakai (mis. tidak ada API key)."""


def _cfg(provider: str | None = None) -> dict:
    return providers.resolve(provider)


# Dihitung dari provider aktif saat import (boleh berubah saat runtime via providers.set_provider).
_active = _cfg()
DEFAULT_MODEL = _active["model"] or "gpt-4.1-mini"
JUDGE_MODEL = _active["judge_model"] or DEFAULT_MODEL


def is_available(provider: str | None = None) -> bool:
    """True kalau provider aktif punya API key."""
    return bool(_cfg(provider)["api_key"])


# cache klien per (style, base_url, key)
_clients: dict = {}


def _openai_client_for(cfg: dict):
    key = ("openai", cfg["base_url"], cfg["api_key"])
    if key in _clients:
        return _clients[key]
    if not cfg["api_key"]:
        raise LLMUnavailable(f"Provider '{cfg['name']}' tidak punya API key.")
    try:
        from openai import OpenAI
    except Exception as exc:  # pragma: no cover
        raise LLMUnavailable(f"paket openai belum terpasang: {exc}") from exc
    kwargs: dict[str, Any] = {"api_key": cfg["api_key"]}
    if cfg["base_url"]:
        kwargs["base_url"] = cfg["base_url"]
    client = OpenAI(**kwargs)
    _clients[key] = client
    return client


def _anthropic_client_for(cfg: dict):
    key = ("anthropic", cfg["base_url"], cfg["api_key"])
    if key in _clients:
        return _clients[key]
    if not cfg["api_key"]:
        raise LLMUnavailable(f"Provider '{cfg['name']}' tidak punya API key.")
    try:
        import anthropic
    except Exception as exc:
        raise LLMUnavailable(f"paket anthropic belum terpasang (pip install anthropic): {exc}") from exc
    client = anthropic.Anthropic(api_key=cfg["api_key"])
    _clients[key] = client
    return client


def _get_client(provider: str | None = None):
    """Klien gaya-OpenAI untuk tool yang butuh OpenAI API (vision/image/voice).
    Untuk provider Anthropic, ini tetap mencoba OpenAI-compatible bila base_url ada."""
    cfg = _cfg(provider)
    return _openai_client_for(cfg)


def _create_compat(client, kwargs: dict):
    """chat.completions.create yang tahan-banting: bila model menolak suatu parameter
    (mis. temperature pada model reasoning), drop param itu lalu ulangi."""
    k = dict(kwargs)
    for _ in range(5):
        try:
            return client.chat.completions.create(**k)
        except Exception as exc:
            msg = str(exc).lower()
            # model reasoning kadang minta max_completion_tokens, bukan max_tokens
            if "max_completion_tokens" in msg and "max_tokens" in k:
                k["max_completion_tokens"] = k.pop("max_tokens")
                continue
            dropped = False
            for p in ("temperature", "top_p", "frequency_penalty", "presence_penalty", "max_tokens"):
                if p in k and p in msg:
                    k.pop(p, None)
                    dropped = True
                    break
            if not dropped:
                raise
    return client.chat.completions.create(**k)


def chat(user: str, system: str | None = None, model: str | None = None,
         temperature: float = 0.3, max_tokens: int | None = None,
         provider: str | None = None) -> str:
    """Panggilan chat lintas-provider; kembalikan teks jawaban."""
    cfg = _cfg(provider)
    mdl = model or cfg["model"] or DEFAULT_MODEL

    if cfg["style"] == "anthropic":
        client = _anthropic_client_for(cfg)
        msg = client.messages.create(
            model=mdl, max_tokens=max_tokens or 2048,
            system=system or "", messages=[{"role": "user", "content": user}],
        )
        parts = [getattr(b, "text", "") for b in msg.content]
        return "".join(parts).strip()

    # gaya OpenAI
    client = _openai_client_for(cfg)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    kwargs: dict[str, Any] = {"model": mdl, "messages": messages, "temperature": temperature}
    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    res = _create_compat(client, kwargs)
    return (res.choices[0].message.content or "").strip()


def _extract_json(text: str) -> Any:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    for opener, closer in (("{", "}"), ("[", "]")):
        start, end = text.find(opener), text.rfind(closer)
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except Exception:
                continue
    raise ValueError("Tidak menemukan JSON valid pada output LLM.")


def chat_json(user: str, system: str | None = None, model: str | None = None,
              temperature: float = 0.0, default: Any = None, provider: str | None = None) -> Any:
    """Chat yang memaksa & mem-parse JSON. Kembalikan `default` bila gagal (jika diberi)."""
    cfg = _cfg(provider)
    prompt = user + "\n\nBalas HANYA dengan JSON valid, tanpa penjelasan lain."

    # Anthropic atau provider tanpa response_format: andalkan parsing
    if cfg["style"] == "anthropic":
        try:
            return _extract_json(chat(prompt, system=system, model=model, temperature=temperature, provider=provider))
        except Exception:
            if default is not None:
                return default
            raise

    client = _openai_client_for(cfg)
    mdl = model or cfg["model"] or DEFAULT_MODEL
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        res = _create_compat(client, {
            "model": mdl, "messages": messages, "temperature": temperature,
            "response_format": {"type": "json_object"},
        })
        return _extract_json(res.choices[0].message.content or "")
    except LLMUnavailable:
        raise
    except Exception:
        try:
            return _extract_json(chat(prompt, system=system, model=model, temperature=temperature, provider=provider))
        except Exception:
            if default is not None:
                return default
            raise


def refresh() -> dict:
    """Muat ulang provider aktif (mis. setelah providers.set_provider) + reset cache klien."""
    global _active, DEFAULT_MODEL, JUDGE_MODEL
    _clients.clear()
    _active = _cfg()
    DEFAULT_MODEL = _active["model"] or "gpt-4.1-mini"
    JUDGE_MODEL = _active["judge_model"] or DEFAULT_MODEL
    return _active


if __name__ == "__main__":
    c = _cfg()
    print("provider :", c["name"], "|", c["title"])
    print("style    :", c["style"])
    print("base_url :", c["base_url"] or "(default)")
    print("model    :", c["model"])
    print("available:", is_available())
