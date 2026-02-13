# SPEC-ARIA-005 Project Test Scenarios

## Scenario 1: Summary Brevity + Actionability

- Command: `/aria:project`
- Target output: `project.summary.md`
- Expected depth: `express`
- Expected behavior:
  - Cost/timeline ranges remain exact
  - Brief action-oriented recommendations

## Scenario 2: Full Report Detail

- Command: `/aria:project --depth deep`
- Target output: `project.md`
- Expected behavior:
  - Expanded milestone and dependency explanation
  - No numeric changes from estimation/planning facts

## Scenario 3: Connector Fallback Interaction

- Command: `/aria:project --format notion`
- Expected behavior:
  - If connector unavailable, graceful fallback to markdown
  - Fallback output still follows selected depth policy
