---
name: threat-detection-engineer
description: "Use when designing or operating systems that detect suspicious behavior, anomalies, abuse, or security threats in logs, events, and telemetry."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [threat-detection, security, telemetry, logs, anomaly-detection, detection-engineering]
    related_skills: [security-engineer, incident-response-commander, security-audit, senior-developer]
---

# Threat Detection Engineer

## Overview

Use this skill when the job is to detect threats or suspicious behavior from logs, telemetry, events, or application signals.
It focuses on practical detection engineering, signal quality, and response readiness.

## When to Use

Use when you need to:

- design detections for suspicious activity
- review logs or telemetry for indicators of compromise
- tune alerts to reduce noise and false positives
- build event-based detection logic
- map threat scenarios to observable signals
- support incident response with actionable alerts

## Working Style

1. Define the threat scenario and assets at risk.
2. Identify observable signals and data sources.
3. Write detections that are specific and testable.
4. Reduce false positives without hiding real risk.
5. Validate detections against known cases.

## Core Concerns

- Log quality and coverage
- Alert thresholds and tuning
- False positives and blind spots
- Attribution vs. detection confidence
- Correlation across multiple sources
- Response routing and escalation

## Common Pitfalls

- Creating alerts that are too broad to be useful.
- Relying on a single noisy signal.
- Ignoring data gaps or missing logs.
- Treating detection as a one-time task instead of ongoing tuning.

## Verification Checklist

- [ ] Threat scenario is defined
- [ ] Signals and sources are identified
- [ ] Detection logic is testable
- [ ] False positives were considered
- [ ] Response path is clear
