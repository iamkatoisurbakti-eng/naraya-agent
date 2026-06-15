# Session 2026-05-07 — Content Filter + Light Script Handoff

## What changed

Nusantara-AI's routine content workflow was extended from a simple `Content Ideation -> Script Writing` handoff into a gated, safer multi-agent chain:

```text
Content Ideation Agent
  -> Filter Agent
  -> Script Writing Agent
  -> Filter Agent
  -> Visual & Audio Creation Agent
  -> Filter Agent
  -> Quality Check Agent
  -> Scheduler Agent
```

The Filter Agent blocks or holds content before it can become a script, prompt, audio/video input, or public metadata.

## Persistent files created/updated

- Filter skill: `/root/.hermes/skills/marketing/filter-agent/SKILL.md`
- Filter config: `/root/nusantara-ai-saas/config/content-filter.json`
- Local validator: `/root/nusantara-ai-saas/scripts/content-filter.mjs`
- Content ideation config: `/root/nusantara-ai-saas/config/content-ideation.json`
- Script output paths:
  - `/root/nusantara-ai-saas/data/content-scripts/scripts-YYYY-MM-DD.jsonl`
  - `/root/nusantara-ai-saas/data/content-scripts/latest.json`

## Filter defaults

Environment/config defaults added without printing secrets:

```env
NEWS_FILTER_ENABLED=1
NEWS_FILTER_CONFIG_PATH=/root/nusantara-ai-saas/config/content-filter.json
NEWS_FILTER_BLOCK_CATEGORIES=pornography,pedophilia,violence,religion,politics
NEWS_FILTER_FAIL_CLOSED=1
```

Blocked categories:

- pornography
- pedophilia / child exploitation
- violence / gore / sadistic crime
- religion / SARA / religious conflict
- politics / campaign / election / parties / political figures

Filter decisions:

- `PASS`: may continue
- `BLOCK`: must not continue
- `REVIEW`: hold for manual review

Outputs should report only category, count, severity, and decision. Do not show explicit sensitive terms in final/user-facing responses.

## Local validation command

Safe text should exit 0:

```bash
node scripts/content-filter.mjs --text='Kabar positif tentang inovasi teknologi pendidikan Indonesia'
```

Forbidden-category text should exit 2 and return `decision: BLOCK`:

```bash
node scripts/content-filter.mjs --text='Artikel kampanye partai politik dan konflik agama'
```

## Routine jobs updated

Content Ideation routine:

- job id: `88cf553230f7`
- skills: `content-ideation-agent`, `filter-agent`, `hermes-agent-orchestration`
- cadence: every 3h
- rule: only trusted Indonesian sources, positive/neutral sentiment, score >=90, `filter_result.decision=PASS`

Script Writing routine:

- job id: `ffdaf3401381`
- skills: `script-writing-agent`, `filter-agent`, `hermes-agent-orchestration`
- cadence: every 3h
- rule: only consume filtered `PASS_TO_SCRIPT` ideas; filter again after writing script

## Script style learning

The user wants Script Writing Agent to produce short scripts from filtered ideas with a `ringan-menarik-baku` style:

- Bahasa Indonesia baku/KBBI, but warm, light, and easy to hear
- 30–60 seconds, ideally 4–7 narration sentences
- concise hook that explains why the story matters
- avoid slang/nonstandard terms: `gak`, `nggak`, `ga`, `rame`, `bikin`, `guys`, `bestie`, `kepo`, `cuma`, `lagi`, `viral banget`, `subscribe`, `share`, `update`, `scroll`
- CTA should be natural: `Berlangganan Nusantara-AI News untuk ringkasan berikutnya.`
- `script_narasi` is text handoff only; it must not imply OpenAI TTS is enabled

Validation after the run showed 10 `SCRIPT_READY`, 0 blocked, filter PASS, no informal terms, and `language_style: ringan-menarik-baku`.

## Pitfalls

- Do not pass an idea to Script Writing if `filter_result.decision` is missing or not `PASS`.
- Do not display the exact sensitive matched terms in final reports.
- If filtering config cannot be read and `NEWS_FILTER_FAIL_CLOSED=1`, do not treat content as safe.
- User wants class-level reusable agent skills, not one-session-only skill fragments. Store session specifics here as references and keep SKILL.md concise.
