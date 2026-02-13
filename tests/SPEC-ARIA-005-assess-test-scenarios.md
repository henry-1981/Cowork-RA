# SPEC-ARIA-005 Assess Test Scenarios

## Scenario 1: Summary Output Default Depth

- Command: `/aria:assess --format markdown`
- Target output: `assess.summary.md`
- Expected depth: `express`
- Expected behavior:
  - Conclusion first
  - Key evidence in concise bullets
  - Recommended next actions
  - No semantic drift in class/pathway/timeline values

## Scenario 2: Full Report Output Default Depth

- Command: `/aria:assess --format markdown`
- Target output: `assess.md`
- Expected depth: `deep`
- Expected behavior:
  - Full narrative structure
  - Preserved regulatory facts and disclaimer

## Scenario 3: Override to Standard

- Command: `/aria:assess --depth standard`
- Expected behavior:
  - Reduced narrative volume vs deep
  - Same factual outcomes as baseline
