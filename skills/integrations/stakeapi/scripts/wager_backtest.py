#!/usr/bin/env python3
"""
Offline wager/backtest simulator for Stake-style house-edge games.
No API calls. No real bets. No secrets.

Use for risk estimates and strategy comparison only. Do not connect this to StakeAPI
or use it to automate betting.
"""
from __future__ import annotations

import argparse
import random
import statistics
from dataclasses import dataclass


@dataclass
class RunResult:
    final_balance: float
    total_wager: float
    bets: int
    busted: bool
    max_drawdown: float


def simulate_flat(starting_balance: float, bet_size: float, target_wager: float, win_chance: float, payout_multiplier: float, max_bets: int, rng: random.Random) -> RunResult:
    balance = starting_balance
    peak = starting_balance
    max_drawdown = 0.0
    total_wager = 0.0
    bets = 0
    while total_wager < target_wager and bets < max_bets:
        stake = min(bet_size, balance, target_wager - total_wager)
        if stake <= 0:
            return RunResult(balance, total_wager, bets, True, max_drawdown)
        balance -= stake
        if rng.random() < win_chance:
            balance += stake * payout_multiplier
        total_wager += stake
        bets += 1
        peak = max(peak, balance)
        if peak > 0:
            max_drawdown = max(max_drawdown, (peak - balance) / peak)
    return RunResult(balance, total_wager, bets, False, max_drawdown)


def simulate_martingale(starting_balance: float, base_bet: float, target_wager: float, win_chance: float, payout_multiplier: float, max_bets: int, max_steps: int, rng: random.Random) -> RunResult:
    balance = starting_balance
    peak = starting_balance
    max_drawdown = 0.0
    total_wager = 0.0
    bets = 0
    step = 0
    while total_wager < target_wager and bets < max_bets:
        stake = min(base_bet * (2 ** step), balance, target_wager - total_wager)
        if stake <= 0:
            return RunResult(balance, total_wager, bets, True, max_drawdown)
        balance -= stake
        won = rng.random() < win_chance
        if won:
            balance += stake * payout_multiplier
            step = 0
        else:
            step = min(step + 1, max_steps)
        total_wager += stake
        bets += 1
        peak = max(peak, balance)
        if peak > 0:
            max_drawdown = max(max_drawdown, (peak - balance) / peak)
    return RunResult(balance, total_wager, bets, False, max_drawdown)


def summarize(results: list[RunResult], starting_balance: float) -> dict:
    finals = [r.final_balance for r in results]
    wagers = [r.total_wager for r in results]
    profits = [r.final_balance - starting_balance for r in results]
    drawdowns = [r.max_drawdown for r in results]
    return {
        "runs": len(results),
        "avg_final_balance": statistics.mean(finals),
        "median_final_balance": statistics.median(finals),
        "avg_profit_loss": statistics.mean(profits),
        "median_profit_loss": statistics.median(profits),
        "avg_wager_completed": statistics.mean(wagers),
        "bust_rate_pct": 100 * sum(r.busted for r in results) / len(results),
        "target_hit_rate_pct": 100 * sum(not r.busted for r in results) / len(results),
        "avg_max_drawdown_pct": 100 * statistics.mean(drawdowns),
        "p05_profit_loss": sorted(profits)[int(0.05 * (len(profits) - 1))],
        "p95_profit_loss": sorted(profits)[int(0.95 * (len(profits) - 1))],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--balance", type=float, default=100.0)
    p.add_argument("--target-wager", type=float, default=1000.0)
    p.add_argument("--bet-size", type=float, default=1.0)
    p.add_argument("--runs", type=int, default=10000)
    p.add_argument("--max-bets", type=int, default=100000)
    p.add_argument("--win-chance", type=float, default=0.495, help="0.495 approximates 1%% edge at 2x payout")
    p.add_argument("--payout", type=float, default=2.0)
    p.add_argument("--seed", type=int, default=7)
    args = p.parse_args()

    rng = random.Random(args.seed)
    flat = [simulate_flat(args.balance, args.bet_size, args.target_wager, args.win_chance, args.payout, args.max_bets, rng) for _ in range(args.runs)]
    rng = random.Random(args.seed)
    mart = [simulate_martingale(args.balance, args.bet_size, args.target_wager, args.win_chance, args.payout, args.max_bets, 12, rng) for _ in range(args.runs)]

    house_edge = 1.0 - args.win_chance * args.payout
    expected_cost = args.target_wager * max(0.0, house_edge)
    print(f"Parameters: balance={args.balance:.2f}, target_wager={args.target_wager:.2f}, bet_size={args.bet_size:.2f}, runs={args.runs}")
    print(f"Game model: win_chance={args.win_chance:.4f}, payout={args.payout:.4f}, house_edge≈{house_edge*100:.2f}%")
    print(f"Theoretical expected cost to wager target: {expected_cost:.4f}")
    for name, data in [("flat", flat), ("martingale", mart)]:
        print("\n" + name.upper())
        for k, v in summarize(data, args.balance).items():
            print(f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}")


if __name__ == "__main__":
    main()
