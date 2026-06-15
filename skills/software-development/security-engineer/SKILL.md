---
name: security-engineer
description: "Use when designing, reviewing, or hardening systems with security-first engineering judgment across authentication, authorization, secrets, threat modeling, and secure delivery."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security-engineer, security, threat-modeling, auth, secrets, hardening, secure-coding]
    related_skills: [security-audit, senior-developer, test-locally, request-code-review]
---

# Security Engineer

## Overview

Use this skill when a task requires security-first engineering judgment: threat modeling, secret handling, authn/authz, secure defaults, and practical hardening.

## When to Use

Use when you need to:

- design secure system behavior
- review code for vulnerabilities
- harden authentication or authorization flows
- handle secrets, tokens, or credentials safely
- assess attack surface and trust boundaries
- plan remediation for security issues

## Working Style

1. Identify assets, trust boundaries, and likely threats.
2. Minimize attack surface and privileges.
3. Treat secrets and user data as sensitive by default.
4. Validate inputs and outputs at the boundaries.
5. Verify fixes with tests or security checks.

## Core Concerns

- Authentication and session security
- Authorization and least privilege
- Secret management and leakage prevention
- Input validation and output encoding
- CSRF, XSS, SSRF, SQL injection, path traversal
- Dependency and supply-chain risk
- Logging, auditability, and incident response

## Common Pitfalls

- Storing secrets in source or logs.
- Trusting client-side checks.
- Over-permissive roles or policies.
- Shipping fixes without regression tests.
- Ignoring failure modes and abuse cases.

## Verification Checklist

- [ ] Threats and trust boundaries were considered
- [ ] Secrets are handled safely
- [ ] Authorization is least-privilege
- [ ] Inputs are validated
- [ ] Fixes were verified locally or with checks
