# Provider doc and contract drafting notes

Use this as the condensed support file for API documentation work that arrives from snippets, live docs, or bundles.

## Essentials
- Preserve the user-provided endpoint paths, headers, body fields, and example values.
- Redact secrets aggressively: tokens, keys, passwords, bearer values.
- Keep a clean section hierarchy: authentication, resources, request/response examples, notes/errors.
- When docs are hidden behind a SPA or minified bundle, inspect the shipped JS for the real endpoint contract.
- Prefer incremental patches over rewriting the whole document.

## Pitfalls
- Do not normalize away meaningful example formatting unless safety requires it.
- Do not invent fields that the user did not provide.
- Do not repeat raw credentials in final docs or notes.
