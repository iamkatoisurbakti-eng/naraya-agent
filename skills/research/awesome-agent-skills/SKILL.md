---
name: awesome-agent-skills
description: Index and usage notes for VoltAgent/awesome-agent-skills, a curated catalog of official/community agent skills. Use when discovering external agent skills from Anthropic, VoltAgent, Angular, Supabase, Gemini, Stripe, Cloudflare, Vercel, Netlify, Hugging Face, Trail of Bits, Sentry, Expo, and others.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-skills, voltagent, officialskills, external-skills, catalog]
---

# Awesome Agent Skills

This skill installs the VoltAgent `awesome-agent-skills` catalog as a Hermes-discoverable reference.

Source repository:

```text
https://github.com/VoltAgent/awesome-agent-skills
```

Local mirror:

```text
/root/.hermes/vendor/awesome-agent-skills
```

Hermes tap added:

```text
VoltAgent/awesome-agent-skills
```

## Important compatibility note

The repository is an awesome-list/catalog, not a repo of directly installable Hermes `SKILL.md` bundles. At install time it contained no `SKILL.md` files. Use it as an index to discover external skills, then install compatible raw `SKILL.md` URLs individually when needed.

## How to use

1. Read `references/README.md` to find relevant skill names and source URLs.
2. Prefer official source URLs listed in the catalog.
3. If a target repo contains actual `SKILL.md` files, install those raw `SKILL.md` URLs with:

```bash
hermes skills inspect <raw-SKILL.md-url>
hermes skills install <raw-SKILL.md-url> --yes
```

4. If a listed page is only a web page (for example `officialskills.sh/...`) and Hermes cannot install it directly, use it as documentation or locate its upstream GitHub repo/path.

## Verification

- Tap is present in `hermes skills tap list`.
- Local mirror exists at `/root/.hermes/vendor/awesome-agent-skills`.
- The catalog README is available as `references/README.md`.
- To refresh parsed catalog references after pulling the repo, run `scripts/parse-awesome-agent-skills.py`.
