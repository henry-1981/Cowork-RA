# SPEC-ARIA-005 Report Test Scenarios

## Scenario 1: Executive Summary Readability

- Command: `/aria:report`
- Target outputs: `briefing.summary.md` + `briefing.md`
- Expected behavior:
  - Summary keeps decision-first structure
  - Full report remains complete and audit-friendly

## Scenario 2: PDF + Deep

- Command: `/aria:report --format pdf --depth deep --lang en`
- Expected behavior:
  - Deep narrative maintained in markdown source
  - PDF generated from same preserved factual content

## Scenario 3: Insufficient Data State

- Command: `/aria:report` with missing assess/project artifacts
- Expected behavior:
  - Reports insufficiency clearly
  - Requests minimum missing steps (1-3)
  - No fabricated recommendations
