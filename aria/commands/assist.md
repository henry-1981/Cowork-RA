---
description: ARIA regulatory assistant - single entry point for determination and fair-competition
argument-hint: "[Question or activity description] [--lang en|ko]"
---

# /aria:assist - Regulatory Assistant

## Purpose

Single entry point for ARIA v1.0.

It routes the user to one of two capabilities:

1. `determination` — medical device status evaluation
2. `fair-competition` — Fair Competition Code review and drafting support

## Design Principles

1. Conversation first, structure behind
2. Ask for missing critical inputs before deciding
3. Keep the first response short by default
4. Do not expose removed pipeline commands as active flows

## Workflow

### 1. Intent Detection

Detect which skill the user needs.

**Determination Intent**
- User describes a product and asks whether it is a medical device
- Keywords: 의료기기, medical device, 해당여부, device status, determination
- Route to: `Skill("aria-determination")`

**Fair Competition Intent**
- User asks about Fair Competition Code review, prior review, expense reporting, or approval drafting
- Keywords: 공정경쟁규약, 사전심의, 지출보고서, 기안, fair competition, KMDIA
- Route to: `Skill("aria-fair-competition")`

**Ambiguous Intent**
- Ask the user which job they need:
  - medical device determination
  - fair-competition review or drafting support

### 2. Determination Flow

Before invoking the skill, check whether the request includes enough information:

- intended medical claim
- product mechanism or software role
- measured parameters or source of data
- care context or target use context

If critical inputs are missing, ask 1-3 follow-up questions first.
If the inputs are sufficient, invoke `Skill("aria-determination")`.

### 3. Fair Competition Flow

Detect whether the user needs Draft (기안) or Review (리뷰):

**Draft Intent** (사업팀)
- Keywords: 기안, 작성, 사전심의 준비, 지출보고서, "이거 해도 돼?", 활동 기획
- Route to: `Skill("aria-fair-competition")` → Draft Mode

**Review Intent** (법무정책실/RA팀)
- Keywords: 검토, 리뷰, 적합성 확인, 규정 위반, 체크
- Route to: `Skill("aria-fair-competition")` → Review Mode

**Ambiguous**: Ask "기안 작성(사업팀)과 규정 검토(법무/RA) 중 어느 쪽이 필요하신가요?"

## Output Contract

- `format`: `markdown`
- `language`: `ko | en` (from `--lang`, default: `ko`)
- `depth`: `express | standard | deep` (default: `express`)

## Flags

- `--lang en|ko`: Output language (default: `ko`)

## Disclaimer

This is an AI-powered regulatory intelligence tool, not a substitute for qualified regulatory review.

- No legal effect
- Expert validation required
- Final decisions must follow official guidance
