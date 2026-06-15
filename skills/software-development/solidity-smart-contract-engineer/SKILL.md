---
name: solidity-smart-contract-engineer
description: "Use when designing, implementing, testing, auditing, or deploying Solidity smart contracts and Ethereum-compatible blockchain systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [solidity, smart-contracts, ethereum, evm, audit, security, web3]
    related_skills: [security-engineer, senior-developer, test-driven-development, test-locally]
---

# Solidity Smart Contract Engineer

## Overview

Use this skill when working on Solidity contracts or EVM-based systems that need correctness, security, and testable deployment paths.

## When to Use

Use when you need to:

- design smart contracts or contract architectures
- implement Solidity functions, storage, and events
- test contract behavior locally
- review contracts for security issues
- prepare deployment or upgrade strategies
- reason about gas, access control, and invariants

## Working Style

1. Define the contract’s purpose and threat model.
2. Minimize privileged and mutable surface area.
3. Encode invariants with explicit checks.
4. Test behavior, edge cases, and failure paths.
5. Review upgrade, permission, and token flows carefully.

## Core Concerns

- Access control and roles
- Reentrancy and external calls
- Integer and precision issues
- Upgradeability and storage layout
- Event emission and traceability
- Gas efficiency without sacrificing clarity
- Deployment, verification, and rollback strategy

## Common Pitfalls

- Leaving critical functions unprotected.
- Assuming external contracts behave safely.
- Missing tests for revert paths and edge cases.
- Breaking storage layout in upgrades.
- Optimizing gas before correctness.

## Verification Checklist

- [ ] Contract purpose and invariants are clear
- [ ] Security risks were considered
- [ ] Tests cover success and failure paths
- [ ] Gas or complexity trade-offs were reviewed
- [ ] Deployment or upgrade path is defined
