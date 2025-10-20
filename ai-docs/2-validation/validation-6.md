---
Session: 6
Created: 2025-10-17
Inputs:
  - Brainstorming: session6.md
  - PRD: prd6.md
  - User Stories: stories-6.md
  - Specs: specs-6.md
Test Coverage Goal: 90%
Status: Draft
---

# C# Legacy Codebase Documentation System - Validation and Acceptance Criteria

# Testing Overview

## Test Strategy

**Approach**: Mixed (Automated + Manual)

**Coverage Goals**:
- Unit Tests: 80%+ for business logic
- Integration Tests: 90%+ for agent pipeline
- E2E Tests: 100% for critical user workflows
- Manual Tests: UI/UX validation, documentation quality review

**Test Environments**:
- **Development**: Local machine with Ollama, small C# codebase (100 files)
- **Staging**: CI/CD environment with medium codebase (1000 files), automated test execution
- **Production**: Production-like environment with large codebase (5000+ files), performance testing

## Test Data Requirements

- **Small C# Codebase**: 10-20 files with known structure for unit/integration testing
- **Medium C# Codebase**: 500-1000 files representative of typical legacy system
- **Large C# Codebase**: 5000+ files for scalability and performance testing
- **Malformed Files**: C# files with syntax errors, incomplete code, edge cases
- **Known Dependency Structures**: Files with circular dependencies, deep hierarchies, complex relationships

## Testing Tools

- **pytest**: Unit and integration testing framework
- **pytest-mock**: Mocking LLM responses and external dependencies
- **black**: Code formatting validation
- **mypy**: Type hint validation
- **radon**: Cyclomatic complexity measurement
- **Ollama**: Local LLM runtime for integration tests
- **Lighthouse**: Performance benchmarking (if web UI added)

---

# Feature 1: C# Code Parsing and Analysis

**Feature Description**: Parse C# files to extract AST structure, identify hierarchy, and analyze dependencies
**Related User Stories**: Story 1.1, Story 1.2, Story 1.3
**Related Specs**: Tasks 3.0-5.0
**Priority**: Critical

## Test Scenario 1.1: Parse Valid C# File

**Objective**: Verify parser correctly extracts classes, methods, and properties from valid C# file

**Preconditions**:
- CsAst package installed
- Sample C# file exists: `tests/fixtures/SampleClass.cs`

**Test Steps**:
1. Initialize Parser class
2. Call `parser.parse_file("tests/fixtures/SampleClass.cs")`
3. Inspect returned AST structure

**Expected Results**:
- ✓ AST object returned with no errors
- ✓ Classes identified correctly (count matches expected)
- ✓ Methods extracted with signatures (name, parameters, return type)
- ✓ Properties identified with types
- ✓ Processing completes in < 100ms for single file

**Acceptance Criteria**:
- [ ] Given a valid C# file, when parser processes it, then AST contains all top-level classes
- [ ] Given AST is generated, when I inspect methods, then all public methods are present with correct signatures
- [ ] Given AST is generated, when I check properties, then all properties have name and type information
- [ ] Given parser completes, when I measure time, then single file parsing takes < 100ms

**Test Type**: Unit
**Automation**: Yes
**Priority**: P0 (Critical)

---

## Test Scenario 1.2: Handle Malformed C# File Gracefully

**Objective**: Verify parser handles syntax errors without crashing

**Preconditions**:
- Sample malformed C# file: `tests/fixtures/MalformedClass.cs` (missing braces, incomplete methods)

**Test Steps**:
1. Initialize Parser class
2. Call `parser.parse_file("tests/fixtures/MalformedClass.cs")`
3. Check error handling

**Expected Results**:
- ✓ Parser does not crash or raise unhandled exception
- ✓ Error is logged at WARNING level with file path
- ✓ Partial AST returned with successfully parsed sections (if possible)
- ✓ Clear error message indicates what failed

**Acceptance Criteria**:
- [ ] Given a malformed C# file, when parser processes it, then it returns an error result without crashing
- [ ] Given parsing fails, when I check logs, then I see WARNING with file path and error description
- [ ] Given a malformed file, when parsing fails, then pipeline continues with next file
- [ ] Given parsing error, when I review error message, then it includes actionable information

**Test Type**: Unit
**Automation**: Yes
**Priority**: P1 (High)

---

## Test Scenario 1.3: Extract Dependency Hierarchy

**Objective**: Verify dependency analyzer identifies cross-file references correctly

**Preconditions**:
- Directory with 5 C# files having known dependencies
- File A references File B and C
- File B references File C
- File C has no dependencies

**Test Steps**:
1. Parse all files in directory
2. Run DependencyAnalyzer on parsed results
3. Generate dependency tree

**Expected Results**:
- ✓ File C identified as high-priority (no dependencies, 2 dependents)
- ✓ File B identified as medium-priority (1 dependency, 1 dependent)
- ✓ File A identified as entry point (2 dependencies, 0 dependents)
- ✓ Dependency graph accurately reflects using statements

**Acceptance Criteria**:
- [ ] Given files with known dependencies, when analyzer runs, then dependency counts match expected values
- [ ] Given dependency tree is generated, when I query File C dependents, then I see File A and File B
- [ ] Given dependency analysis completes, when I request prioritized list, then File C appears first
- [ ] Given entry points are identified, when I check results, then File A is flagged as entry point

**Test Type**: Integration
**Automation**: Yes
**Priority**: P0 (Critical)

---

# Feature 2: Multi-Agent Documentation Pipeline

**Feature Description**: Orchestrate three layers of agents (Summarizer, Detailing, RelationshipMapper) with validation
**Related User Stories**: Story 2.1, Story 2.2, Story 2.3, Story 6.1, Story 6.2, Story 6.3
**Related Specs**: Tasks 6.0-17.0
**Priority**: Critical

## Test Scenario 2.1: Layer 1 - File Summarizer Agent Generates Summary

**Objective**: Verify FileSummarizerAgent produces high-level file summary

**Preconditions**:
- Ollama running with codellama:7b model
- Sample C# file parsed with known classes and methods
- Agent system prompt loaded

**Test Steps**:
1. Initialize FileSummarizerAgent
2. Provide file content and hierarchy data as input
3. Invoke agent
4. Validate output structure

**Expected Results**:
- ✓ Summary is 2-4 sentences describing file purpose
- ✓ Key classes are listed in output
- ✓ Output conforms to FileSummaryOutput Pydantic schema
- ✓ No implementation details included (high-level only)
- ✓ Processing completes within 30 seconds

**Acceptance Criteria**:
- [ ] Given a C# file, when FileSummarizerAgent processes it, then output contains a summary field with 2-4 sentences
- [ ] Given summary is generated, when I validate against schema, then it passes Pydantic validation
- [ ] Given summary is generated, when I review content, then it describes purpose without implementation details
- [ ] Given agent runs, when I measure time, then processing completes in under 30 seconds

**Test Type**: Integration
**Automation**: Yes (with mocked LLM for speed)
**Priority**: P0 (Critical)

---

## Test Scenario 2.2: Layer 2 - Detailing Agent Generates Function Docstrings

**Objective**: Verify DetailingAgent produces detailed documentation for all public methods

**Preconditions**:
- Layer 1 summary exists for file
- File contains 5 public methods with known signatures
- Ollama running with codellama:13b model

**Test Steps**:
1. Initialize DetailingAgent
2. Provide file, Layer 1 summary, and hierarchy as input
3. Invoke agent
4. Validate output

**Expected Results**:
- ✓ All 5 public methods have docstrings
- ✓ Each docstring includes: purpose, parameters, return value
- ✓ Output conforms to DetailingAgentOutput Pydantic schema
- ✓ Docstrings reference Layer 1 summary for context
- ✓ Processing completes within 60 seconds

**Acceptance Criteria**:
- [ ] Given a file with 5 public methods, when DetailingAgent processes it, then output contains 5 method_docs entries
- [ ] Given method_docs are generated, when I inspect each, then it includes purpose, parameters, and return type
- [ ] Given docstrings are created, when I validate schema, then output passes Pydantic validation
- [ ] Given detailed docs exist, when I review them, then they reference concepts from Layer 1 summary

**Test Type**: Integration
**Automation**: Yes (with mocked LLM for speed)
**Priority**: P0 (Critical)

---

## Test Scenario 2.3: Layer 3 - Relationship Mapper Documents Dependencies

**Objective**: Verify RelationshipMapperAgent documents cross-file relationships

**Preconditions**:
- Layer 1 and Layer 2 documentation exists
- Dependency data shows file references 3 other files
- Ollama running

**Test Steps**:
1. Initialize RelationshipMapperAgent
2. Provide file, L1/L2 docs, and dependency graph as input
3. Invoke agent
4. Validate output

**Expected Results**:
- ✓ All 3 dependencies documented
- ✓ Relationship descriptions explain how files interact
- ✓ Output conforms to RelationshipMapperOutput Pydantic schema
- ✓ Data flow between files is described
- ✓ Processing completes within 45 seconds

**Acceptance Criteria**:
- [ ] Given file with 3 dependencies, when RelationshipMapperAgent processes it, then output contains 3 dependency entries
- [ ] Given relationships are documented, when I review them, then each includes description of interaction
- [ ] Given output is generated, when I validate schema, then it passes Pydantic validation
- [ ] Given relationships are mapped, when I check data flow, then agent describes how data moves between files

**Test Type**: Integration
**Automation**: Yes (with mocked LLM for speed)
**Priority**: P1 (High)

---

## Test Scenario 2.4: LangGraph Orchestrates Complete Pipeline

**Objective**: Verify LangGraph state machine correctly orchestrates all three layers

**Preconditions**:
- All agents implemented and tested individually
- LangGraph state machine defined
- Sample C# file ready for processing

**Test Steps**:
1. Initialize OrchestratorController
2. Load configuration
3. Run pipeline on single file
4. Verify state transitions

**Expected Results**:
- ✓ File progresses through: Parse → L1 → Validate → L2 → Validate → L3 → Output
- ✓ Each layer receives outputs from previous layer as context
- ✓ Final output includes all three layers of documentation
- ✓ State transitions logged at INFO level
- ✓ Total processing time < 2 minutes for single file

**Acceptance Criteria**:
- [ ] Given pipeline runs, when I check logs, then I see state transitions for Parse, L1, L2, L3, Output
- [ ] Given L2 runs, when I inspect input, then it contains L1 summary as context
- [ ] Given L3 runs, when I inspect input, then it contains both L1 and L2 documentation
- [ ] Given pipeline completes, when I check output, then markdown file contains all three layers

**Test Type**: E2E
**Automation**: Yes
**Priority**: P0 (Critical)

---

# Feature 3: Validation and Refinement System

**Feature Description**: Automated validation using Pydantic schemas with refinement loops
**Related User Stories**: Story 3.1, Story 3.2
**Related Specs**: Tasks 18.0-20.0
**Priority**: Critical

## Test Scenario 3.1: Validation Agent Passes Valid Documentation

**Objective**: Verify ValidationAgent correctly validates compliant documentation

**Preconditions**:
- Pydantic validation schema defined for Layer 1
- Sample output that meets all criteria (summary length, required fields)

**Test Steps**:
1. Initialize ValidationAgent with Layer 1 schema
2. Provide valid Layer 1 output
3. Run validation
4. Check result

**Expected Results**:
- ✓ Validation passes
- ✓ Result indicates "PASS" status
- ✓ No refinement instructions generated
- ✓ Validation completes in < 1 second

**Acceptance Criteria**:
- [ ] Given valid documentation, when ValidationAgent runs, then result status is "PASS"
- [ ] Given validation passes, when I check refinement instructions, then none are generated
- [ ] Given validation completes, when I check logs, then I see INFO message "Validation passed"
- [ ] Given validation runs, when I measure time, then it completes in under 1 second

**Test Type**: Unit
**Automation**: Yes
**Priority**: P0 (Critical)

---

## Test Scenario 3.2: Validation Agent Fails Incomplete Documentation

**Objective**: Verify ValidationAgent detects missing required fields

**Preconditions**:
- Pydantic schema requires summary and key_classes fields
- Sample output missing key_classes field

**Test Steps**:
1. Initialize ValidationAgent
2. Provide incomplete Layer 1 output
3. Run validation
4. Check result and refinement instructions

**Expected Results**:
- ✓ Validation fails
- ✓ Result indicates "FAIL" status
- ✓ Specific error message: "Missing required field: key_classes"
- ✓ Refinement instructions generated for agent to retry

**Acceptance Criteria**:
- [ ] Given incomplete documentation, when ValidationAgent runs, then result status is "FAIL"
- [ ] Given validation fails, when I check error details, then I see specific missing field identified
- [ ] Given validation fails, when I review refinement instructions, then they specify what to add
- [ ] Given validation fails, when I check logs, then I see WARNING with validation error details

**Test Type**: Unit
**Automation**: Yes
**Priority**: P0 (Critical)

---

## Test Scenario 3.3: Refinement Loop Improves Documentation

**Objective**: Verify refinement loop successfully improves failed documentation

**Preconditions**:
- First attempt produces documentation that fails validation (summary too short)
- Max iterations set to 3

**Test Steps**:
1. Run pipeline with file that produces short summary
2. Validation fails on first attempt
3. Refinement loop triggers FileSummarizerAgent with feedback
4. Second attempt generates longer summary
5. Validation passes

**Expected Results**:
- ✓ First validation fails with specific feedback
- ✓ Refined prompt includes validation feedback
- ✓ Second attempt produces longer summary
- ✓ Second validation passes
- ✓ Iteration counter increments from 1 to 2
- ✓ Final documentation marked as "validated after 2 iterations"

**Acceptance Criteria**:
- [ ] Given short summary, when validation runs, then it fails with "summary too short" message
- [ ] Given validation fails, when agent retries, then prompt includes refinement instructions
- [ ] Given second attempt completes, when validation runs, then it passes
- [ ] Given refinement succeeds, when I check metadata, then it shows "validated in 2 iterations"

**Test Type**: Integration
**Automation**: Yes
**Priority**: P1 (High)

---

## Test Scenario 3.4: Max Iteration Limit Prevents Infinite Loop

**Objective**: Verify system stops after max iterations and flags for manual review

**Preconditions**:
- File consistently produces documentation that fails validation
- Max iterations set to 3

**Test Steps**:
1. Run pipeline with problematic file
2. Each attempt fails validation
3. After 3 attempts, system should stop

**Expected Results**:
- ✓ 3 validation attempts occur
- ✓ After 3rd failure, no 4th attempt
- ✓ File flagged for manual review in output
- ✓ ERROR logged with details
- ✓ Pipeline continues with next file

**Acceptance Criteria**:
- [ ] Given documentation fails 3 times, when 3rd attempt fails, then no 4th attempt occurs
- [ ] Given max iterations reached, when I check output, then file is flagged "MANUAL_REVIEW_REQUIRED"
- [ ] Given max iterations reached, when I check logs, then ERROR message explains failure
- [ ] Given one file fails, when pipeline continues, then other files are still processed

**Test Type**: Integration
**Automation**: Yes
**Priority**: P1 (High)

---

# Feature 4: Configuration and CLI

**Feature Description**: User-friendly CLI with configuration management
**Related User Stories**: Story 4.1, Story 4.2, Story 4.3
**Related Specs**: Tasks 8.0, 24.0-26.0
**Priority**: High

## Test Scenario 4.1: Load Configuration from YAML File

**Objective**: Verify system correctly loads and validates configuration

**Preconditions**:
- Valid config.yaml exists with all required fields

**Test Steps**:
1. Initialize Config class
2. Load config from config.yaml
3. Validate loaded values

**Expected Results**:
- ✓ Configuration loads without errors
- ✓ All fields present (models, validation, output, processing)
- ✓ Default values applied for optional fields
- ✓ Configuration passes Pydantic schema validation

**Acceptance Criteria**:
- [ ] Given valid config file, when Config loads it, then no errors are raised
- [ ] Given config is loaded, when I access config.models.default, then I see configured model name
- [ ] Given optional field is missing, when config loads, then default value is used
- [ ] Given config loads, when I validate schema, then it passes Pydantic validation

**Test Type**: Unit
**Automation**: Yes
**Priority**: P1 (High)

---

## Test Scenario 4.2: Detect Invalid Configuration with Clear Error

**Objective**: Verify system provides actionable error for invalid configuration

**Preconditions**:
- Invalid config.yaml with missing required field (e.g., output.base_path)

**Test Steps**:
1. Initialize Config class
2. Attempt to load invalid config
3. Catch validation error

**Expected Results**:
- ✓ ValidationError raised with clear message
- ✓ Error specifies which field is missing or invalid
- ✓ Error includes example of correct format
- ✓ System does not start with invalid config

**Acceptance Criteria**:
- [ ] Given invalid config, when Config loads it, then ValidationError is raised
- [ ] Given validation error, when I read message, then it specifies missing/invalid field
- [ ] Given validation error, when I review message, then it includes remediation steps
- [ ] Given invalid config, when I run CLI, then system exits with error before processing

**Test Type**: Unit
**Automation**: Yes
**Priority**: P1 (High)

---

## Test Scenario 4.3: CLI Document Command Processes Codebase

**Objective**: Verify CLI `document` command successfully processes a codebase

**Preconditions**:
- Small test codebase in `tests/fixtures/csharp_sample/`
- Valid configuration file
- Ollama running locally

**Test Steps**:
1. Run: `python -m cli.main document --config config.yaml --input tests/fixtures/csharp_sample/`
2. Monitor progress output
3. Check output directory

**Expected Results**:
- ✓ CLI displays progress bar or status updates
- ✓ All files in codebase are processed
- ✓ Markdown documentation files created in output directory
- ✓ Success message displayed at completion
- ✓ Exit code 0 (success)

**Acceptance Criteria**:
- [ ] Given CLI runs, when I monitor output, then I see progress updates for each file
- [ ] Given processing completes, when I check output directory, then markdown files exist for all input files
- [ ] Given processing succeeds, when I check exit code, then it is 0
- [ ] Given CLI finishes, when I review output, then I see success message with file count

**Test Type**: E2E
**Automation**: Yes
**Priority**: P0 (Critical)

---

## Test Scenario 4.4: CLI Status Command Shows Progress

**Objective**: Verify `status` command displays current pipeline state

**Preconditions**:
- Pipeline running on medium codebase (500 files)
- Some files completed, some in progress

**Test Steps**:
1. Start pipeline in background
2. Run: `python -m cli.main status`
3. Review output

**Expected Results**:
- ✓ Current file being processed displayed
- ✓ Progress shown as percentage or fraction (e.g., "45/500 files")
- ✓ Current layer displayed (L1/L2/L3)
- ✓ Estimated time remaining calculated
- ✓ Validation pass rate shown

**Acceptance Criteria**:
- [ ] Given pipeline is running, when I run status command, then I see current file name
- [ ] Given status is displayed, when I check progress, then I see "45/500 files (9%)" format
- [ ] Given status shows layer, when I review output, then I see "Layer: 2 (Detailing)"
- [ ] Given status includes ETA, when I check time, then it shows reasonable estimate

**Test Type**: Integration
**Automation**: Partial (manual verification of display)
**Priority**: P2 (Medium)

---

# Feature 5: Incremental Documentation Updates

**Feature Description**: Detect changed files and update only affected documentation
**Related User Stories**: Story 5.1, Story 5.2
**Related Specs**: Tasks 27.0-28.0
**Priority**: Medium

## Test Scenario 5.1: Detect Changed Files Since Last Run

**Objective**: Verify ChangeDetector identifies files modified after last run

**Preconditions**:
- Previous pipeline run completed with metadata saved
- 3 files modified after last run (timestamp newer)
- 7 files unchanged

**Test Steps**:
1. Initialize ChangeDetector
2. Load last run metadata
3. Compare with current file timestamps
4. Get list of changed files

**Expected Results**:
- ✓ 3 files identified as changed
- ✓ 7 files identified as unchanged
- ✓ Changed file list includes exact file paths
- ✓ Detection completes in < 5 seconds for 1000 files

**Acceptance Criteria**:
- [ ] Given 3 files changed, when ChangeDetector runs, then it returns list of 3 file paths
- [ ] Given 7 files unchanged, when I check results, then they are not in changed list
- [ ] Given detection completes, when I verify paths, then they match expected changed files
- [ ] Given large codebase, when detection runs, then it completes in under 5 seconds

**Test Type**: Unit
**Automation**: Yes
**Priority**: P2 (Medium)

---

## Test Scenario 5.2: Incremental Update Processes Only Changed Files

**Objective**: Verify incremental mode processes only changed files

**Preconditions**:
- 10 file codebase with full documentation
- 2 files modified
- Incremental mode enabled

**Test Steps**:
1. Run: `python -m cli.main document --incremental`
2. Monitor processing
3. Check output

**Expected Results**:
- ✓ Only 2 files processed (not all 10)
- ✓ Existing documentation for 8 unchanged files preserved
- ✓ Updated documentation for 2 changed files
- ✓ Index file updated with new timestamps
- ✓ Total time significantly less than full regeneration

**Acceptance Criteria**:
- [ ] Given 2 files changed, when incremental update runs, then only 2 files are processed
- [ ] Given 8 files unchanged, when update completes, then their documentation is untouched
- [ ] Given 2 files updated, when I check output, then new documentation reflects current code
- [ ] Given incremental completes, when I compare time, then it's at least 80% faster than full run

**Test Type**: Integration
**Automation**: Yes
**Priority**: P2 (Medium)

---

# Non-Functional Requirements

## Performance Validation

### Test Scenario P.1: Process 100 Files Per Hour

**Objective**: Verify system meets throughput target

**Preconditions**:
- Medium codebase with 100 C# files
- Standard hardware: 8-core CPU, 16GB RAM
- Ollama with codellama:7b and codellama:13b

**Test Steps**:
1. Start timer
2. Run full pipeline on 100 files
3. Record completion time
4. Calculate throughput

**Expected Results**:
- ✓ 100 files processed in ≤ 60 minutes
- ✓ Average processing time ≤ 36 seconds per file
- ✓ No memory leaks or crashes
- ✓ CPU utilization reasonable (50-80%)

**Acceptance Criteria**:
- [ ] Given 100 file codebase, when pipeline runs, then it completes in under 60 minutes
- [ ] Given processing completes, when I calculate throughput, then it's ≥ 100 files/hour
- [ ] Given pipeline runs, when I monitor memory, then usage stays under 8GB
- [ ] Given processing occurs, when I check CPU, then no core is pegged at 100% continuously

**Test Type**: Performance
**Automation**: Yes
**Tools**: time, psutil for monitoring
**Priority**: P1 (High)

---

### Test Scenario P.2: Scale to 5000 File Codebase

**Objective**: Verify system handles large codebases without failure

**Preconditions**:
- Large codebase with 5000 C# files
- Standard hardware

**Test Steps**:
1. Run full pipeline on 5000 files
2. Monitor resource usage
3. Verify completion

**Expected Results**:
- ✓ Pipeline completes successfully (no crashes)
- ✓ Memory usage stays under 8GB
- ✓ All 5000 files documented
- ✓ Resume capability works if interrupted

**Acceptance Criteria**:
- [ ] Given 5000 file codebase, when pipeline runs, then it completes without crashing
- [ ] Given large run, when I monitor memory, then peak usage is under 8GB
- [ ] Given pipeline completes, when I check output, then all 5000 files have documentation
- [ ] Given pipeline is interrupted, when I resume, then it continues from last completed file

**Test Type**: Performance/Reliability
**Automation**: Yes
**Priority**: P1 (High)

---

## Security Validation

### Test Scenario S.1: All Processing Occurs Locally

**Objective**: Verify no data leaves local machine

**Preconditions**:
- Network monitoring tool running
- Air-gapped environment (no internet connection)

**Test Steps**:
1. Disconnect network
2. Run pipeline on sample codebase
3. Monitor network activity
4. Verify completion

**Expected Results**:
- ✓ Pipeline completes successfully without network
- ✓ No network requests attempted
- ✓ All LLM calls go to local Ollama
- ✓ No external API calls logged

**Acceptance Criteria**:
- [ ] Given network is disconnected, when pipeline runs, then it completes successfully
- [ ] Given network monitoring active, when I check logs, then no outbound requests are detected
- [ ] Given Ollama is local, when I verify LLM calls, then all go to localhost
- [ ] Given pipeline completes, when I review logs, then no errors about network unavailability

**Test Type**: Security
**Automation**: Partial (network disconnection may be manual)
**Priority**: P0 (Critical)

---

### Test Scenario S.2: Sensitive Data Not Logged

**Objective**: Verify source code snippets not logged at INFO level

**Preconditions**:
- Codebase with proprietary code
- Logging level set to INFO

**Test Steps**:
1. Run pipeline with INFO logging
2. Review log files
3. Search for code snippets

**Expected Results**:
- ✓ File paths and names logged (metadata OK)
- ✓ No full source code snippets in logs
- ✓ No proprietary function implementations logged
- ✓ DEBUG level may contain code (but not INFO)

**Acceptance Criteria**:
- [ ] Given logging at INFO, when I review logs, then I see file paths but not code content
- [ ] Given logs are generated, when I search for proprietary code, then it's not found at INFO level
- [ ] Given DEBUG logging enabled, when I check logs, then code snippets may appear (acceptable)
- [ ] Given logs exist, when I verify security, then no sensitive business logic is exposed at INFO

**Test Type**: Security
**Automation**: Yes (log parsing)
**Priority**: P1 (High)

---

## Usability Validation

### Test Scenario U.1: Clear Error Messages for Common Issues

**Objective**: Verify user receives actionable error messages

**Preconditions**:
- Ollama not running

**Test Steps**:
1. Ensure Ollama is stopped
2. Run CLI document command
3. Observe error message

**Expected Results**:
- ✓ Error clearly states "Ollama is not running"
- ✓ Message includes remediation: "Start Ollama with: ollama serve"
- ✓ Exit code is non-zero (failure)
- ✓ No stack trace shown to user (logged separately)

**Acceptance Criteria**:
- [ ] Given Ollama not running, when I run document command, then I see clear error message
- [ ] Given error occurs, when I read message, then it includes how to fix the issue
- [ ] Given error is displayed, when I check exit code, then it's non-zero
- [ ] Given error happens, when I view output, then no Python stack trace is shown to user

**Test Type**: Usability/Manual
**Automation**: Partial
**Priority**: P2 (Medium)

---

### Test Scenario U.2: Progress Visibility During Long Runs

**Objective**: Verify user can see progress during long-running operations

**Preconditions**:
- Medium codebase (500 files)

**Test Steps**:
1. Run document command
2. Observe output during processing
3. Verify user feedback

**Expected Results**:
- ✓ Progress bar or percentage shown
- ✓ Current file name displayed
- ✓ Updates occur frequently (every 1-2 seconds)
- ✓ ETA displayed and updates reasonably

**Acceptance Criteria**:
- [ ] Given pipeline runs, when I watch output, then I see progress bar or percentage
- [ ] Given processing occurs, when I monitor display, then current file name is shown
- [ ] Given long run, when I observe updates, then they occur at least every 2 seconds
- [ ] Given progress shown, when I check ETA, then it provides reasonable time estimate

**Test Type**: Usability/Manual
**Automation**: No (visual verification)
**Priority**: P2 (Medium)

---

# Edge Cases and Error Scenarios

## Feature: C# Code Parsing

### Edge Case 1: Empty C# File

**Test**: Parse file with no classes or methods (only comments)
**Expected**: Parser returns empty AST without error, file skipped gracefully
**Priority**: Medium

### Edge Case 2: Very Large C# File (>10,000 lines)

**Test**: Parse file exceeding typical size
**Expected**: Parser chunks file if needed, processing completes successfully within 5 seconds
**Priority**: Medium

### Edge Case 3: Circular File Dependencies

**Test**: File A references B, File B references A
**Expected**: Dependency analyzer detects cycle, logs warning, prioritizes based on other factors
**Priority**: High

### Error Scenario 1: Ollama Service Crashes During Processing

**Trigger**: Kill Ollama process while agent is running
**Expected Error Handling**:
- Display: "LLM service unavailable. Please restart Ollama and resume."
- Logging: ERROR with exception details
- Recovery: Save state, allow user to resume after restarting Ollama
**Priority**: High

### Error Scenario 2: Disk Full During Documentation Write

**Trigger**: Fill disk to capacity during output generation
**Expected Error Handling**:
- Display: "Insufficient disk space. Please free up space and retry."
- Logging: ERROR with available space info
- Recovery: Rollback partial writes, exit gracefully
**Priority**: Medium

### Error Scenario 3: Invalid Pydantic Schema in Configuration

**Trigger**: User provides malformed validation schema in config
**Expected Error Handling**:
- Display: "Invalid validation schema in config: [specific error]"
- Logging: ERROR with schema details
- Recovery: Exit before processing, do not corrupt existing docs
**Priority**: High

---

# Integration Testing

## Integration Point 1: Parser ↔ Hierarchy Extractor

**Integration Type**: Data Pipeline

**Test Scenarios**:
- [ ] Successful AST passed to HierarchyExtractor, produces valid hierarchy
- [ ] Empty AST handled gracefully by HierarchyExtractor
- [ ] Large AST with 100+ classes processes without performance degradation
- [ ] Malformed AST raises clear validation error in HierarchyExtractor

---

## Integration Point 2: Agents ↔ Ollama LLM

**Integration Type**: External Service

**Test Scenarios**:
- [ ] Agent successfully invokes Ollama and receives response
- [ ] Agent handles Ollama timeout gracefully (retry or error)
- [ ] Agent handles invalid model name with clear error
- [ ] Agent respects context window limits, chunks if needed

---

## Integration Point 3: Validation ↔ Refinement Loop

**Integration Type**: Control Flow

**Test Scenarios**:
- [ ] Failed validation triggers refinement with feedback
- [ ] Successful validation skips refinement, proceeds to next layer
- [ ] Max iteration limit prevents infinite refinement
- [ ] Refinement feedback correctly incorporated into retry prompt

---

# Traceability Matrix

| User Story | Technical Spec | Test Scenario | Status |
|------------|----------------|---------------|---------|
| Story 1.1  | Task 3.0      | TS 1.1, 1.2   | ⏳ Pending |
| Story 1.2  | Task 5.0      | TS 1.3        | ⏳ Pending |
| Story 1.3  | Task 4.0      | -             | ⏳ Pending |
| Story 2.1  | Task 9.0-11.0 | TS 2.1        | ⏳ Pending |
| Story 2.2  | Task 12.0-14.0| TS 2.2        | ⏳ Pending |
| Story 2.3  | Task 15.0-17.0| TS 2.3        | ⏳ Pending |
| Story 3.1  | Task 18.0-19.0| TS 3.1, 3.2   | ⏳ Pending |
| Story 3.2  | Task 20.0     | TS 3.3, 3.4   | ⏳ Pending |
| Story 4.1  | Task 8.0      | TS 4.1, 4.2   | ⏳ Pending |
| Story 4.2  | Task 24.0     | TS 4.3        | ⏳ Pending |
| Story 4.3  | Task 25.0     | TS 4.4        | ⏳ Pending |
| Story 5.1  | Task 27.0     | TS 5.1        | ⏳ Pending |
| Story 5.2  | Task 28.0     | TS 5.2        | ⏳ Pending |
| Story 6.1  | Task 6.0      | TS 2.4        | ⏳ Pending |
| Story 6.2  | Task 9.0-17.0 | TS 2.1-2.3    | ⏳ Pending |
| Story 6.3  | Task 7.0      | TS 2.4        | ⏳ Pending |

---

# Test Execution Summary

**Test Run Date**: Not yet executed
**Environment**: Development
**Build Version**: v0.1.0-dev

| Feature | Total Tests | Passed | Failed | Blocked | Pass Rate |
|---------|-------------|--------|--------|---------|-----------|
| Code Parsing | 3 | 0 | 0 | 0 | N/A |
| Multi-Agent Pipeline | 4 | 0 | 0 | 0 | N/A |
| Validation System | 4 | 0 | 0 | 0 | N/A |
| Configuration & CLI | 4 | 0 | 0 | 0 | N/A |
| Incremental Updates | 2 | 0 | 0 | 0 | N/A |
| Performance | 2 | 0 | 0 | 0 | N/A |
| Security | 2 | 0 | 0 | 0 | N/A |
| Usability | 2 | 0 | 0 | 0 | N/A |

**Overall Pass Rate**: 0% (Not yet executed)
**Total Test Scenarios**: 23
**Estimated Test Execution Time**: ~8 hours (including manual tests)

---

# Test Execution Plan

## Phase 1: Unit Tests (Estimated: 2 hours)
- Test Scenarios: 1.1, 1.2, 3.1, 3.2, 4.1, 4.2
- Focus: Individual component validation
- Can be run in parallel with development

## Phase 2: Integration Tests (Estimated: 3 hours)
- Test Scenarios: 1.3, 2.1, 2.2, 2.3, 3.3, 3.4, 5.1, 5.2
- Focus: Component interactions
- Requires completed units from Phase 1

## Phase 3: E2E Tests (Estimated: 2 hours)
- Test Scenarios: 2.4, 4.3
- Focus: Complete user workflows
- Requires full system integration

## Phase 4: Non-Functional Tests (Estimated: 1 hour)
- Test Scenarios: P.1, P.2, S.1, S.2, U.1, U.2
- Focus: Performance, security, usability
- Run after functional tests pass

---

# Acceptance Sign-Off

This validation document will be considered complete when:

- [ ] All P0 (Critical) test scenarios pass
- [ ] 90% of P1 (High) test scenarios pass
- [ ] Code coverage exceeds 80% for business logic
- [ ] Performance benchmarks met (100 files/hour, 5000 file scalability)
- [ ] Security validation confirms local-only processing
- [ ] Manual usability tests show positive user experience
- [ ] Traceability matrix shows all user stories validated
- [ ] No critical bugs remain unresolved

**Approved By**: [Pending]
**Date**: [Pending]
