---
name: stakeapi
description: "Use when working with the ChipaDevTeam StakeAPI Python wrapper for stake.com: installation checks, read-only account/balance/statistics queries, examples, and safe handling of Stake credentials."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [stakeapi, python, api, integration, gambling, credentials]
    related_skills: [hermes-agent-skill-authoring]
---

# StakeAPI

## Overview
Use this skill for the unofficial Python package `stakeapi` from `https://github.com/ChipaDevTeam/StakeAPI`.

Installed in this environment:
- Python package: `stakeapi==0.1.0`
- Source clone: `/root/.hermes/vendor/StakeAPI`
- Docs: `https://chipadevteam.github.io/StakeAPI/`

StakeAPI is an unofficial wrapper for stake.com. Treat it as sensitive and high-risk because it can interact with gambling-related account data.

## When to Use
- User asks to install or use StakeAPI.
- User needs examples for `StakeAPI(access_token=...)`.
- User needs read-only checks such as account balance, profile, casino/sports data, statistics.
- User needs troubleshooting import/auth/rate-limit errors.

Do not use it to place bets, bypass platform limits, automate gambling, evade jurisdiction restrictions, or scrape/private-abuse endpoints.

## Setup
Installed command used:

```bash
apt-get update && apt-get install -y python3-pip git
python3 -m pip install --break-system-packages --user git+https://github.com/ChipaDevTeam/StakeAPI.git
git clone https://github.com/ChipaDevTeam/StakeAPI.git /root/.hermes/vendor/StakeAPI
```

Verify:

```bash
python3 - <<'PY'
import stakeapi
print(stakeapi.__file__)
print([x for x in dir(stakeapi) if not x.startswith('_')])
PY
```

## Credentials
Never print or store raw access tokens in chat, logs, source code, or final responses.

Expected env vars:

```bash
export STAKE_ACCESS_TOKEN='[REDACTED]'
export STAKE_SESSION_COOKIE='[REDACTED]'  # optional depending on method
```

Recommended: put secrets in a private env file or Hermes env path, not in source.

## Basic Read-only Example

```python
import asyncio
import os
from stakeapi import StakeAPI

async def main():
    token = os.environ['STAKE_ACCESS_TOKEN']
    async with StakeAPI(access_token=token) as client:
        balance = await client.get_user_balance()
        print(balance)

asyncio.run(main())
```

## Offline wager/backtest simulator
Use `scripts/wager_backtest.py` when the user wants wagering/level math, strategy comparisons, or risk estimates. It performs Monte Carlo simulation only; it makes no Stake API calls and never places bets.

Example:

```bash
python ~/.hermes/skills/integrations/stakeapi/scripts/wager_backtest.py --balance 200000 --target-wager 1000000 --bet-size 500 --runs 20000
```

## Safe Usage Rules
1. Prefer read-only endpoints: balance, profile, statistics, public casino/sports data.
2. Ask for explicit confirmation before any account-changing action.
3. Refuse requests to automate betting or gambling decisions, including autobet patterns intended to raise wager/VIP level.
4. Offer safe alternatives: offline simulations/backtests, expected-cost calculators, bankroll risk analysis, and read-only progress monitoring.
5. Do not expose affiliate links unless user explicitly asks.
6. Respect local laws and Stake terms.
7. If a token appears in chat/output, immediately advise rotating/revoking it; do not reuse, echo, persist, or pass it into scripts.

## Safe Offline Wager Simulation Pattern
When a user asks for autobet or wager-level optimization, do not connect to Stake or place bets. Instead, you can create/run an offline Monte Carlo simulator that models house-edge games with parameters like starting balance, target wager, flat bet size, win chance, and payout multiplier. Use it to show expected cost (`target_wager × house_edge`), bust rate, target-hit rate, and drawdown. Explicitly note that martingale/progression systems do not change negative expected value and often increase ruin/tail-loss risk.

## Troubleshooting
- `ModuleNotFoundError: stakeapi`: run the install command or check `python3 -m site --user-site`.
- Auth errors: verify `STAKE_ACCESS_TOKEN` is set and current; do not print it.
- Rate limit errors: reduce request frequency; use retries/backoff.
- API shape errors: inspect `/root/.hermes/vendor/StakeAPI/examples` and package source.

## Verification Checklist
- [ ] `import stakeapi` works.
- [ ] Source clone exists at `/root/.hermes/vendor/StakeAPI`.
- [ ] No token/cookie printed.
- [ ] Only read-only calls unless user explicitly authorizes account-changing action.
- [ ] Gambling/legal risk noted when relevant.
