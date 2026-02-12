# Test Scenarios for SPEC-ARIA-003: /aria:chat

**SPEC**: SPEC-ARIA-003 - Command & Skill Architecture Restructure
**Scope**: /aria:chat conversational regulatory advisor
**Status**: Test scenarios documented
**Coverage Target**: 85%+ of chat command requirements

---

## Executive Summary

This document defines comprehensive test scenarios for the `/aria:chat` command, the conversational regulatory advisor that serves as the primary entry point for guided interaction. Tests cover natural dialogue flow, transparent skill invocation, progressive product profiling, auto-suggestion logic, and document upload handling.

---

## Test Strategy

### Test Categories

1. **Positive Tests** (50%): Expected conversation flows and skill routing
2. **Negative Tests** (20%): Edge cases and error handling
3. **Integration Tests** (20%): Skill invocation and context management
4. **UX Tests** (10%): Conversation quality and transparency

### Coverage Mapping

- Product context loading (5 cases)
- Input mode detection (conversational vs. document upload)
- Product profile management and completeness
- Conversational skill routing (5 skills)
- Auto-suggestion logic (3 states)
- Context integration from prior pipeline data
- Output handling (conversational vs. file storage)

---

## CH-001: Product Context Loading

**Requirement**: Workflow Step 1 - Product context management
**Priority**: Critical

### CH-001.1: Returning user with active product (Case 1)
```gherkin
Given .aria/active_product.json exists with valid product "cardiac-monitor-x1"
And .aria/products/cardiac-monitor-x1/{date}/profile.json exists
When /aria:chat is executed
Then active product shall be loaded
And existing profile.json shall be loaded
And last_accessed date shall be updated
And greeting shall include product context: "Welcome back. Continuing with cardiac-monitor-x1."
```

### CH-001.2: No products exist - fresh start (Case 5)
```gherkin
Given .aria/products/ directory is empty or does not exist
When /aria:chat is executed
Then conversation shall start fresh
And product entry shall be created when sufficient information is gathered
And product naming convention shall be enforced
```

### CH-001.3: Multiple products - selection menu (Case 2)
```gherkin
Given .aria/products/ contains multiple products
And .aria/active_product.json does NOT exist
When /aria:chat is executed
Then product selection menu shall be displayed
And user shall select or create a new product
```

---

## CH-002: Input Mode Detection

**Requirement**: Workflow Step 2 - Mode A (Conversational) vs Mode B (Document)
**Priority**: Critical

### CH-002.1: Conversational Q&A mode
```gherkin
Given user asks a question: "We're developing a wearable that measures heart rate."
When /aria:chat processes the input
Then ARIA shall respond naturally gathering product information
And profile shall be updated internally with device description
And no formal "profile form" shall be presented to user
```

### CH-002.2: Document upload mode
```gherkin
Given user uploads a technical specification PDF
When /aria:chat processes the document
Then product information shall be auto-extracted:
  - Device description
  - Intended use
  - Product form
  - Primary function
  - Target markets (if mentioned)
And gap analysis shall identify missing fields
And minimal Q&A (1-3 rounds) shall fill gaps
And profile shall be auto-populated from extracted data
```

### CH-002.3: Large document handling
```gherkin
Given user uploads a technical document with >100 pages
When /aria:chat processes the document
Then system shall analyze Table of Contents first
And only relevant sections shall be extracted
And extraction summary shall be presented naturally in conversation
```

---

## CH-003: Product Profile Management

**Requirement**: Workflow Step 3 - Progressive profile building
**Priority**: Critical

### CH-003.1: Profile updated during conversation
```gherkin
Given user mentions: "It's a Bluetooth-connected pulse oximeter for hospitals"
When profile management processes the message
Then profile.json shall be updated with:
  - description: includes "pulse oximeter" and "Bluetooth-connected"
  - intended_use: inferred from hospital context
  - product_form: "hardware" (physical device)
And completeness percentage shall increase
And update shall be silent (no notification to user)
```

### CH-003.2: Completeness calculation
```gherkin
Given the profile completeness formula:
  - name: 15%
  - description: 15%
  - intended_use: 20%
  - product_form: 15%
  - primary_function: 20%
  - target_markets: 15%
When profile has name + description + intended_use filled
Then completeness shall be 50% (15 + 15 + 20)
```

### CH-003.3: Threshold notifications
```gherkin
Given profile completeness increases during conversation
When completeness reaches 50%
Then user shall be informed of profile milestone
When completeness reaches 100%
Then user shall be informed that profile is complete
```

### CH-003.4: Profile never presented as form
```gherkin
Given any conversation flow
When ARIA gathers product information
Then no explicit "profile form" or "fill out these fields" shall be shown
And information shall be gathered through natural dialogue
And profile accumulation shall be invisible to user
```

---

## CH-004: Conversational Skill Routing

**Requirement**: Workflow Step 4 - Transparent skill invocation
**Priority**: Critical

### CH-004.1: Determination trigger (completeness >= 70%)
```gherkin
Given profile completeness >= 70%
And user asks about medical device status
When skill routing evaluates the conversation
Then Skill("aria-determination") shall be invoked transparently
And results shall be presented naturally: "With arrhythmia detection and physician alerting, this qualifies as a medical device..."
And skill invocation shall NOT be visible to user
```

### CH-004.2: Classification trigger (determination complete)
```gherkin
Given determination has been completed
And user asks about device class or risk level
When skill routing evaluates the conversation
Then Skill("aria-classification") shall be invoked
And results shall be presented naturally: "Expected classification: FDA Class II..."
```

### CH-004.3: Pathway trigger (classification complete)
```gherkin
Given classification has been completed
And user asks about submission routes or regulatory pathways
When skill routing evaluates the conversation
Then Skill("aria-pathway") shall be invoked
And results shall be presented naturally within dialogue
```

### CH-004.4: Estimation trigger (pathway determined)
```gherkin
Given pathway has been determined
And user asks about cost, budget, or timeline
When skill routing evaluates the conversation
Then Skill("aria-estimation") shall be invoked
And results shall be presented naturally
```

### CH-004.5: Planning trigger (estimation complete)
```gherkin
Given estimation has been completed
And user asks for a plan, roadmap, or milestones
When skill routing evaluates the conversation
Then Skill("aria-planning") shall be invoked
And results shall be presented naturally
```

### CH-004.6: General regulatory Q&A (no specific trigger)
```gherkin
Given user asks a general regulatory knowledge question
And no specific skill trigger is matched
When /aria:chat processes the question
Then a direct conversational answer shall be provided
And source attribution shall be included where applicable
And relevant commands shall be suggested for deeper analysis
```

### CH-004.7: Insufficient profile for skill invocation
```gherkin
Given profile completeness < 70%
And user asks about medical device status
When skill routing evaluates the conversation
Then determination skill shall NOT be invoked
And ARIA shall ask clarifying questions to build profile further
```

---

## CH-005: Auto-Suggestion Logic

**Requirement**: Workflow Step 5 - Suggest next steps based on data state
**Priority**: High

### CH-005.1: Profile sufficient, no assess data
```gherkin
Given profile completeness >= 70%
And no assess.summary.md exists
When auto-suggestion logic evaluates
Then ARIA shall suggest: "Want me to run a full regulatory assessment? (/aria:assess)"
And user approval shall be required before execution
And /aria:assess shall NOT auto-execute
```

### CH-005.2: Assess data exists, no project data
```gherkin
Given assess.summary.md exists
And project.summary.md does NOT exist
When auto-suggestion logic evaluates
Then ARIA shall suggest: "Ready for cost/timeline estimation? (/aria:project)"
And user approval shall be required before execution
```

### CH-005.3: All pipeline data exists
```gherkin
Given assess.summary.md and project.summary.md both exist
When auto-suggestion logic evaluates
Then ARIA shall suggest: "Want me to generate a comprehensive briefing? (/aria:report)"
And user approval shall be required before execution
```

### CH-005.4: Never auto-execute pipeline commands
```gherkin
Given any auto-suggestion scenario
When ARIA suggests a pipeline command
Then the command shall NEVER be auto-executed
And explicit user approval shall always be required
```

---

## CH-006: Context Integration

**Requirement**: Workflow Step 6 - Load prior pipeline data
**Priority**: High

### CH-006.1: Load profile.json context
```gherkin
Given profile.json exists from a prior chat session
When /aria:chat starts a new session
Then profile data shall be loaded and used
And conversation shall continue from existing profile state
```

### CH-006.2: Reference assess results in conversation
```gherkin
Given assess.summary.md exists
And user asks about their device classification
When ARIA processes the question
Then assessment results shall be referenced in the answer
And prior classification data shall be cited
```

### CH-006.3: Reference project results in conversation
```gherkin
Given project.summary.md exists
And user asks about estimated costs
When ARIA processes the question
Then project plan results shall be referenced
And prior cost/timeline estimates shall be cited
```

---

## CH-007: Output Handling

**Requirement**: Workflow Step 7 - Conversational output vs file storage
**Priority**: High

### CH-007.1: Skill-invoked output - natural presentation
```gherkin
Given a skill is invoked during conversation
When results are generated
Then results shall be presented naturally within conversation
And no formal report structure shall be visible
And key findings shall be highlighted conversationally
And ARIA shall offer: "Want me to save this as a formal report?"
```

### CH-007.2: General Q&A - no file storage
```gherkin
Given user asks a general regulatory knowledge question
When ARIA provides a conversational answer
Then NO files shall be saved to .aria/products/
And response shall be purely conversational
```

### CH-007.3: Profile updates - silent
```gherkin
Given conversation provides new product information
When profile.json is updated
Then update shall be silent (no notification)
And profile shall be saved automatically
```

---

## CH-008: Flag Handling

**Requirement**: --lang flag
**Priority**: High

### CH-008.1: Korean conversation (default)
```gherkin
Given no --lang flag is specified
When /aria:chat responds
Then conversation shall be in Korean
And regulation codes shall remain in English (e.g., "FDA 510(k)")
```

### CH-008.2: English conversation
```gherkin
Given --lang en flag is specified
When /aria:chat responds
Then conversation shall be in English
```

---

## CH-009: Conversation Quality

**Requirement**: Design principles compliance
**Priority**: High

### CH-009.1: No visible pipeline mechanics
```gherkin
Given any skill is invoked during chat
When results are delivered
Then no "Step 1", "Step 2", "Step 3" labels shall appear
And no "Running determination skill..." status messages shall be shown
And results shall feel like a natural conversation
```

### CH-009.2: 510(k) vs PMA explanation (general Q&A)
```gherkin
Given user asks: "What's the difference between 510(k) and PMA?"
When ARIA processes the general knowledge question
Then a clear conversational explanation shall be provided
And comparison table or structured format may be used
And source attribution shall reference FDA guidance
And ARIA shall offer to check which pathway applies to their device
```

---

## Negative Tests

### NT-CH-001: Ambiguous product description
```gherkin
Given user provides a vague description: "We make things for health"
When ARIA processes the input
Then ARIA shall ask clarifying questions
And shall NOT attempt skill invocation with insufficient data
And profile completeness shall remain low
```

### NT-CH-002: Off-topic questions
```gherkin
Given user asks a non-regulatory question: "What's the weather today?"
When ARIA processes the input
Then ARIA shall politely redirect to regulatory topics
And shall explain its scope as a regulatory intelligence assistant
```

### NT-CH-003: Contradictory information
```gherkin
Given user previously said "hardware device"
And later says "it's a software-only product"
When profile management processes the update
Then the newer information shall take precedence
And profile.json shall be updated with product_form: "software"
And ARIA may ask for confirmation about the change
```

---

## Summary

**Total Test Scenarios**: 30+ test cases
**Coverage**: Product context, input modes, profile management, skill routing, auto-suggestions, context integration, output handling, conversation quality
**Focus**: Conversational UX quality and transparent skill integration
**Quality Target**: 85%+ acceptance criteria coverage

---

**Version**: 1.0.0
**Created**: 2026-02-12
**Author**: team-tester (ARIA Plugin Team)
