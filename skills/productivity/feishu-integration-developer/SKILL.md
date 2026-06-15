---
name: feishu-integration-developer
description: "Use when building integrations with Feishu/Lark APIs, bots, webhooks, documents, sheets, and automation workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [feishu, lark, integration, api, webhook, docs, sheets, automation]
    related_skills: [google-workspace, notion, linear, technical-writer]
---

# Feishu Integration Developer

## Overview

Use this skill when you need to build or maintain integrations with Feishu/Lark services: apps, bots, webhooks, docs, sheets, messaging, and workflow automation.

## When to Use

Use when you need to:

- connect to Feishu/Lark APIs
- send or receive bot messages
- handle webhooks or event callbacks
- read or update docs and sheets
- automate team workflows
- debug auth, payloads, or callback issues

## Working Style

1. Identify the Feishu surface being integrated.
2. Confirm auth model, scopes, and callback requirements.
3. Start with the smallest working API call.
4. Validate payload shape and error handling.
5. Verify the end-to-end workflow in the target tenant.

## Core Concerns

- App credentials and scopes
- Webhook/event security
- Message formatting and mention behavior
- Document/sheet permissions
- Rate limits and retries
- Tenant-specific configuration

## Common Pitfalls

- Mixing bot and app auth requirements.
- Ignoring callback verification or signature checks.
- Assuming message payloads are interchangeable across surfaces.
- Forgetting permission scopes for docs or sheets.

## Verification Checklist

- [ ] Target Feishu surface is identified
- [ ] Auth and scope requirements are clear
- [ ] Payloads were tested
- [ ] Security checks were considered
- [ ] Integration worked end-to-end
