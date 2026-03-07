# Cowork-RA

Anthropic Cowork plugin marketplace repository for ARIA.

[Korean (default)](./README.md) | [English](./README.en.md)

## Overview

`Cowork-RA` ships only the current v1.0 ARIA assets needed to install and use the plugin in Cowork.

ARIA focuses on two RA jobs behind a single entry point:

- `determination`: medical device status evaluation
- `fair-competition`: Fair Competition Code review and internal drafting support

Historical pipeline specs, migration notes, and one-off refactoring utilities are kept locally under `_archive/` and are not part of the shipped repository surface.

## V1.0 Scope

| Component | Current scope |
|---|---|
| Entry command | `/aria:assist` |
| Skill 1 | `determination` |
| Skill 2 | `fair-competition` |
| Response style | concise by default, deeper on request |
| Knowledge assets | bundled skill-local references or modules |

## When ARIA Fits Best

| Situation | What ARIA does |
|---|---|
| You need an early device-status decision | Runs determination against intended use and operating mechanism. |
| You need a quick Fair Competition Code check | Maps the activity type and guides the review against the code. |
| You need an internal approval draft | Uses the fair-competition context to support drafting and review prep. |

## Quick Start

Everything starts from `/aria:assist`.

```text
/aria:assist Is this ECG wearable a medical device?
/aria:assist I need a fair-competition review and draft for a product presentation event.
```

ARIA routes the request internally to `determination` or `fair-competition`.

## Installation

1. Install the Claude Desktop App.
   - https://claude.com/download
2. Open the Cowork tab in Claude Desktop.
3. Go to plugin installation in Cowork.
   - Plugins -> `+` -> Browse Plugins -> Personal -> Add marketplace from GitHub
4. Use this GitHub URL:
   - `https://github.com/henry-1981/Cowork-RA.git`

## Documentation

- ARIA usage guide: [`aria/README.md`](./aria/README.md)
- Single entry command: [`aria/commands/assist.md`](./aria/commands/assist.md)
- Plugin changelog: [`aria/CHANGELOG.md`](./aria/CHANGELOG.md)

## Troubleshooting

- ARIA can still operate with bundled references even if some MCP connectors are unavailable.
- Detailed document outputs depend on the tools/connectors available in your environment.

## License

[Apache-2.0](./aria/LICENSE)
