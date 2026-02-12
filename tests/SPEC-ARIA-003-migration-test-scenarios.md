# Test Scenarios for SPEC-ARIA-003: Migration & Backward Compatibility

**SPEC**: SPEC-ARIA-003 - Command & Skill Architecture Restructure
**Scope**: Migration validation and backward compatibility
**Status**: Test scenarios documented
**Coverage Target**: 85%+ of migration requirements

---

## Executive Summary

This document defines comprehensive test scenarios for the SPEC-ARIA-003 migration, verifying backward compatibility with existing `.aria/` data, correct removal of deprecated commands and skills, and smooth transition from the 8-command architecture to the 4-command architecture.

---

## Test Strategy

### Test Categories

1. **Backward Compatibility Tests** (40%): Legacy data handling
2. **Migration Tests** (30%): Command/skill removal and replacement
3. **File Structure Tests** (20%): New vs old output formats
4. **Regression Tests** (10%): Existing functionality preservation

### Coverage Mapping

- Deprecated command removal (6 commands)
- Deprecated skill removal (2 skills) and migration (1 skill)
- Legacy .aria/ data handling
- New output file format validation
- Skill refactoring verification (5 skills: I/O removed, pure logic kept)
- Plugin manifest update
- Command count reduction (8 -> 4)

---

## MG-001: Deprecated Command Removal

**Requirement**: Migration Plan - 6 commands deleted
**Priority**: Critical

### MG-001.1: /aria:determine removed
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the commands directory is inspected
Then aria/commands/determine.md shall NOT exist
And /aria:assess shall handle determination logic
```

### MG-001.2: /aria:classify removed
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the commands directory is inspected
Then aria/commands/classify.md shall NOT exist
And /aria:assess shall handle classification logic
```

### MG-001.3: /aria:pathway removed
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the commands directory is inspected
Then aria/commands/pathway.md shall NOT exist
And /aria:assess shall handle pathway logic
```

### MG-001.4: /aria:estimate removed
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the commands directory is inspected
Then aria/commands/estimate.md shall NOT exist
And /aria:project shall handle estimation logic
```

### MG-001.5: /aria:plan removed
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the commands directory is inspected
Then aria/commands/plan.md shall NOT exist
And /aria:project shall handle planning logic
```

### MG-001.6: /aria:compare removed
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the commands directory is inspected
Then aria/commands/compare.md shall NOT exist
And comparison logic shall be absorbed by /aria:assess and /aria:project inline
```

### MG-001.7: Only 4 commands remain
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When aria/commands/ directory is listed
Then exactly 4 command files shall exist:
  - chat.md
  - assess.md
  - project.md
  - report.md
And no other .md files shall be present in the commands directory
```

---

## MG-002: Deprecated Skill Removal

**Requirement**: Migration Plan - 2 skills deleted, 1 skill moved
**Priority**: Critical

### MG-002.1: Briefing skill removed
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the skills directory is inspected
Then aria/skills/briefing/SKILL.md shall NOT exist
And briefing logic shall be absorbed by /aria:report command
```

### MG-002.2: Comparison skill removed
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the skills directory is inspected
Then aria/skills/comparison/SKILL.md shall NOT exist
And comparison logic shall be absorbed inline by assess and project commands
```

### MG-002.3: Connectors skill merged into CONNECTORS.md
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When the skills directory is inspected
Then aria/skills/connectors/SKILL.md shall NOT exist
And connector patterns shall be documented in aria/CONNECTORS.md
```

### MG-002.4: Only 5 skills remain
```gherkin
Given the SPEC-ARIA-003 restructure is complete
When aria/skills/ directory is listed
Then exactly 5 skill directories shall exist:
  - determination/
  - classification/
  - pathway/
  - estimation/
  - planning/
And no other skill directories shall be present
```

---

## MG-003: Skill Refactoring Verification

**Requirement**: Migration Plan - 5 skills refactored (I/O removed)
**Priority**: Critical

### MG-003.1: Skills contain no product context loading
```gherkin
Given the 5 remaining skills (determination, classification, pathway, estimation, planning)
When each skill's SKILL.md is reviewed
Then no product context loading logic shall be present
And no .aria/active_product.json references shall exist
And no file path management shall be included
```

### MG-003.2: Skills contain no flag handling
```gherkin
Given the 5 remaining skills
When each skill's SKILL.md is reviewed
Then no --lang flag handling shall be present
And no --format flag handling shall be present
And flag handling shall be the responsibility of commands only
```

### MG-003.3: Skills contain no file storage logic
```gherkin
Given the 5 remaining skills
When each skill's SKILL.md is reviewed
Then no .aria/products/ path references for writing shall be present
And no output file generation logic shall be included
And file storage shall be the responsibility of commands only
```

### MG-003.4: Skills contain no pipeline connections
```gherkin
Given the 5 remaining skills
When each skill's SKILL.md is reviewed
Then no "Next step: /aria:XXX" suggestions shall be present
And no inter-skill routing logic shall be included
And pipeline orchestration shall be the responsibility of commands only
```

### MG-003.5: Skills retain pure analysis logic
```gherkin
Given the 5 remaining skills
When each skill's SKILL.md is reviewed
Then pure analysis frameworks shall be preserved:
  - determination: FDA/EU MDR/MFDS qualification criteria
  - classification: Multi-region classification rules and decision logic
  - pathway: Submission route selection logic
  - estimation: Three-point cost/timeline frameworks
  - planning: Milestone generation templates
And module references (modules/ directory) shall be preserved
And decision frameworks and classification rules shall be preserved
And traffic light / escalation logic shall be preserved
And knowledge base date references shall be preserved
```

---

## MG-004: Legacy Data Backward Compatibility

**Requirement**: Existing .aria/ data handling
**Priority**: Critical

### MG-004.1: /aria:report reads legacy determination data
```gherkin
Given .aria/products/{product}/{date}/ contains:
  - determination.md + determination.summary.md (legacy format)
And no assess.md exists
When /aria:report loads pipeline data
Then legacy determination data shall be loaded successfully
And briefing shall include determination findings from legacy file
```

### MG-004.2: /aria:report reads legacy classification data
```gherkin
Given .aria/products/{product}/{date}/ contains:
  - classification.md + classification.summary.md (legacy format)
When /aria:report loads pipeline data
Then legacy classification data shall be loaded successfully
```

### MG-004.3: /aria:report reads legacy pathway data
```gherkin
Given .aria/products/{product}/{date}/ contains:
  - pathway.md + pathway.summary.md (legacy format)
When /aria:report loads pipeline data
Then legacy pathway data shall be loaded successfully
```

### MG-004.4: /aria:report reads legacy estimation data
```gherkin
Given .aria/products/{product}/{date}/ contains:
  - estimation.md + estimation.summary.md (legacy format)
When /aria:report loads pipeline data
Then legacy estimation data shall be loaded successfully
```

### MG-004.5: /aria:report reads legacy plan data
```gherkin
Given .aria/products/{product}/{date}/ contains:
  - plan.md + plan.summary.md (legacy format)
When /aria:report loads pipeline data
Then legacy plan data shall be loaded successfully
```

### MG-004.6: /aria:project reads legacy summary data
```gherkin
Given .aria/products/{product}/{date}/ contains legacy format:
  - determination.summary.md
  - classification.summary.md
  - pathway.summary.md
And no assess.summary.md exists
When /aria:project loads assessment data
Then legacy summaries shall be loaded as fallback
And user shall be informed about legacy data usage
```

### MG-004.7: New format preferred over legacy
```gherkin
Given .aria/products/{product}/{date}/ contains both:
  - assess.md (new format)
  - determination.md + classification.md + pathway.md (legacy format)
When /aria:report loads pipeline data
Then new format (assess.md) shall be preferred
And legacy files shall be ignored for overlapping data
```

---

## MG-005: New Output File Format

**Requirement**: New .aria/ file structure
**Priority**: High

### MG-005.1: Assess command output format
```gherkin
Given /aria:assess completes successfully
When output directory is inspected
Then the following files shall exist:
  - assess.md (integrated regulatory assessment)
  - assess.summary.md (compressed summary)
And the following legacy files shall NOT be created:
  - determination.md
  - classification.md
  - pathway.md
  - comparison.md
```

### MG-005.2: Project command output format
```gherkin
Given /aria:project completes successfully
When output directory is inspected
Then the following files shall exist:
  - project.md (integrated project plan)
  - project.summary.md (compressed summary)
And the following legacy files shall NOT be created:
  - estimation.md
  - plan.md
```

### MG-005.3: Chat command output format
```gherkin
Given /aria:chat builds a product profile
When output directory is inspected
Then profile.json shall exist with product profile data
And no other files shall be created by chat (unless user requests)
```

### MG-005.4: Brief command output format
```gherkin
Given /aria:report completes successfully
When output directory is inspected
Then the following files shall exist:
  - briefing.md (comprehensive briefing report)
  - briefing.summary.md (compressed summary for audit)
```

### MG-005.5: Total output files reduced
```gherkin
Given a complete pipeline execution (assess -> project -> brief)
When all output files are counted
Then new format shall produce 6 files:
  - profile.json
  - assess.md + assess.summary.md
  - project.md + project.summary.md
  - briefing.md (+ briefing.summary.md)
And legacy format produced 14 files (7 pairs of md + summary.md)
And file count shall be reduced from 14 to approximately 7
```

---

## MG-006: Plugin Manifest Consistency

**Requirement**: plugin.json accuracy after migration
**Priority**: High

### MG-006.1: Version updated
```gherkin
Given SPEC-ARIA-003 restructure is complete
When aria/.claude-plugin/plugin.json is read
Then version shall be "0.1.0"
```

### MG-006.2: Command count reflects 4 commands
```gherkin
Given plugin.json is updated
When command registry is reviewed
Then exactly 4 commands shall be listed:
  - /aria:chat
  - /aria:assess
  - /aria:project
  - /aria:report
And no deprecated commands shall be listed
```

---

## MG-007: No Orphaned References

**Requirement**: Clean migration with no broken references
**Priority**: High

### MG-007.1: No references to deleted commands in remaining files
```gherkin
Given all files in aria/ directory
When searching for references to deleted commands
Then no references to /aria:determine shall exist (except historical docs)
And no references to /aria:classify shall exist
And no references to /aria:pathway shall exist
And no references to /aria:estimate shall exist
And no references to /aria:plan shall exist
And no references to /aria:compare shall exist
```

### MG-007.2: No references to deleted skills in command files
```gherkin
Given the 4 remaining command files
When searching for skill references
Then no reference to "briefing" skill shall exist in commands
And no reference to "comparison" skill shall exist in commands
And no reference to "connectors" skill shall exist in commands
```

---

## Regression Tests

### RG-001: Existing .aria/ directory not modified
```gherkin
Given existing .aria/products/ data from prior ARIA versions
When SPEC-ARIA-003 commands are used
Then existing legacy files shall NOT be modified or deleted
And new output shall be created alongside legacy data
And data integrity of prior results shall be preserved
```

### RG-002: active_product.json compatibility
```gherkin
Given .aria/active_product.json from prior ARIA version
When new commands reference active product
Then active_product.json format shall remain compatible
And product reference shall resolve correctly
```

### RG-003: aria.local.md playbook compatibility
```gherkin
Given aria.local.md configuration from prior ARIA version
When new commands load playbook settings
Then all existing settings shall be recognized
And language preferences shall continue to work
And data retention settings shall be respected
```

---

## Summary

**Total Test Scenarios**: 35+ test cases
**Coverage**: Command removal, skill removal/refactoring, legacy data compatibility, new file format, plugin manifest, orphaned references, regression
**Focus**: Safe migration from 8-command to 4-command architecture with zero data loss
**Quality Target**: 85%+ migration acceptance criteria coverage

---

**Version**: 1.0.0
**Created**: 2026-02-12
**Author**: team-tester (ARIA Plugin Team)
