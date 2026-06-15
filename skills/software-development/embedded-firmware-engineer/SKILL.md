---
name: embedded-firmware-engineer
description: "Use when designing, implementing, debugging, or testing embedded firmware for microcontrollers, peripherals, and hardware-adjacent systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [embedded, firmware, microcontroller, bare-metal, hardware, embedded-c, debugging]
    related_skills: [senior-developer, systematic-debugging, test-locally, security-engineer]
---

# Embedded Firmware Engineer

## Overview

Use this skill when working close to hardware: microcontrollers, peripherals, sensors, drivers, interrupts, RTOS tasks, and firmware bring-up.

## When to Use

Use when you need to:

- design embedded firmware logic
- debug boot, timing, or peripheral issues
- work with registers, interrupts, DMA, or IO
- build drivers or board support code
- test firmware on target hardware or simulators
- improve reliability, power, or latency

## Working Style

1. Identify the hardware, constraints, and timing budget.
2. Understand the data path from peripheral to software.
3. Keep interrupt and real-time code minimal.
4. Verify one subsystem at a time.
5. Check logs, traces, and hardware state before guessing.

## Core Concerns

- Startup and boot flow
- Interrupt safety and race conditions
- Timing and latency constraints
- Peripheral configuration
- Memory limits and stack usage
- Power and reliability
- Firmware update and recovery paths

## Common Pitfalls

- Doing too much inside interrupts.
- Ignoring clock, voltage, or pin configuration.
- Assuming hardware behaves like a desktop environment.
- Skipping instrumentation when debugging.
- Overlooking watchdogs, brownouts, or reset causes.

## Verification Checklist

- [ ] Hardware constraints are known
- [ ] Timing-sensitive paths are minimal
- [ ] Peripheral setup was checked
- [ ] Debugging used real measurements or logs
- [ ] The firmware behavior was verified on target or simulator
