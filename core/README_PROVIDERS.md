# Naraya-Agent — Provider LLM (multi-provider)

Naraya bisa terhubung ke banyak provider lewat satu antarmuka (`core/llm.py` + `core/providers.py`).

## Provider yang didukung

| nama | provider | base URL | gaya | catatan |
|------|----------|----------|------|---------|
| `naraouter` | NaraRouter | https://router.naraya.ai/v1 | OpenAI | model contoh `auto/naraya.ai` |
| `openai` | OpenAI | (default) | OpenAI | |
| `anthropic` | Anthropic (Claude) | (default) | Anthropic | `pip install anthropic` |
| `openrouter` | OpenRouter | https://openrouter.ai/api/v1 | OpenAI | 300+ model |
| `kilocode` | Kilo Code | https://api.kilo.ai/api/gateway | OpenAI | gateway |
| `custom` | Custom direct API | `NARAYA_CUSTOM_BASE_URL` | OpenAI | endpoint OpenAI-compatible |
| `custom_endpoint` | Custom Endpoint API | `NARAYA_ENDPOINT_URL` | OpenAI | endpoint OpenAI-compatible |

## Memilih provider

```bash
python core/select_provider.py            # menu interaktif
python core/select_provider.py naraouter  # set langsung
python core/select_provider.py --list     # status semua provider
python core/select_provider.py --test     # uji koneksi provider aktif
```

Atau set di `core/.env`: `NARAYA_PROVIDER=naraouter` (+ key terkait). Pilihan menu
tersimpan di `data/provider.json`. Prioritas: argumen > `NARAYA_PROVIDER` > `data/provider.json` > auto-deteksi (key terisi) > `openai`.

Lewat agen: tool `daftar_provider` dan `ganti_provider("naraouter")`.

## Kunci API (di .env)

`NARAROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`,
`KILOCODE_API_KEY`, atau pasangan custom (`NARAYA_CUSTOM_BASE_URL`/`_API_KEY`/`_MODEL`,
`NARAYA_ENDPOINT_URL`/`_API_KEY`/`_MODEL`). Fallback umum: `NARAYA_API_KEY`.
Model dipaksa lewat `NARAYA_MODEL` (opsional; jika kosong pakai default provider).

## Catatan
- Semua engine (orkestrasi 14-agen, evolusi, tools) otomatis ikut provider aktif.
- Ganti provider saat runtime: `providers.set_provider("openrouter"); llm.refresh()`.
- Offline-safe: tanpa key, panggilan melempar `LLMUnavailable` (ditangani anggun).
