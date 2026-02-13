# SPEC-ARIA-005 Chat Test Scenarios

## Scenario 1: Insufficient Info Forces Express

- Input: `/aria:chat new cardiac wearable for US` 
- Expected depth: `express`
- Expected behavior:
  - States confidence as `insufficient`
  - Gives short rationale for why more data is needed
  - Asks exactly 1-3 follow-up questions
  - No deterministic class/pathway conclusion

## Scenario 2: Skill-Invoked Turn (Determination)

- Input: Sufficient intended use + mechanism + target market details
- Expected depth: `standard` (unless user overrides)
- Expected behavior:
  - `response_mode=skill_invoked`
  - Determination result explained in plain language
  - Regulatory facts and citations unchanged
  - Ends with one next-action question

## Scenario 3: User Override

- Input: `/aria:chat ... --depth deep`
- Expected behavior:
  - More detailed explanation than default
  - Still preserves facts, numbers, and disclaimer strength
