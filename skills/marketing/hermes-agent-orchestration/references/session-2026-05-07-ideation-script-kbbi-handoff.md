# Session note: routine ideation-to-script handoff and KBBI gate

Context learned in the 2026-05-07 Nusantara-AI News automation session.

## Durable workflow

- Content Ideation Agent should run routinely and only collect ideas; it must not render media, upload YouTube, or send Telegram.
- Script Writing Agent should consume the latest `idea_packet` outputs and write `script_packet` records for the next Visual & Audio stage.
- Handoff storage conventions:
  - ideas: `/root/nusantara-ai-saas/data/content-ideas/ideas-YYYY-MM-DD.jsonl`
  - latest ideas: `/root/nusantara-ai-saas/data/content-ideas/latest.json`
  - scripts: `/root/nusantara-ai-saas/data/content-scripts/scripts-YYYY-MM-DD.jsonl`
  - latest scripts: `/root/nusantara-ai-saas/data/content-scripts/latest.json`
- Routine cron jobs created in this session:
  - `nusantara-content-ideation-agent-routine`, job id `88cf553230f7`, every 3h, skills `content-ideation-agent` + `hermes-agent-orchestration`.
  - `nusantara-script-writing-agent-routine`, job id `ffdaf3401381`, every 3h, skills `script-writing-agent` + `hermes-agent-orchestration`, context_from ideation job.

## Language/KBBI gate

Before any audio-producing stage, script text must pass formal Indonesian normalization:
- remove slang and abbreviations (`gak/nggak/ga`, `rame`, `bikin`, `subscribe`, `share`, `update`, `scroll`, etc.)
- use Bahasa Indonesia baku/KBBI-style
- avoid adding facts outside `source_context`
- keep OpenAI TTS disabled unless user explicitly re-enables it

Code artifacts introduced/used:
- `/root/nusantara-ai-saas/src/services/indonesian-nlp.ts`
- `/root/nusantara-ai-saas/tests/unit/indonesian-nlp.test.ts`

## Verification pattern

For script handoff runs, verify:
- `latest.json` has `SCRIPT_READY` records
- `language_style == "baku-indonesia"`
- `no_openai_tts == true`
- no informal tokens from the validation list remain
- output is not sent to YouTube/Telegram at this stage
