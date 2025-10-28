# DocuGen Module Documentation

## Overview

DocuGen is a sophisticated multi-agent AI system designed to automatically generate comprehensive documentation for C# codebases using LangGraph orchestration and LLM-based analysis. The system implements a four-layer documentation pipeline that progressively builds understanding from high-level summaries to detailed architectural documentation.

**Purpose**: Transform legacy or undocumented C# codebases into well-structured, comprehensive documentation through automated analysis and intelligent synthesis.

**Key Technologies**:
- **LangGraph**: State machine orchestration for multi-agent workflows
- **LangChain**: LLM abstraction layer supporting multiple providers
- **Pydantic**: Data validation and structured output parsing
- **Loguru**: Structured logging
- **Click**: CLI framework
- **Rich**: Terminal UI components
- **Tree-sitter**: C# code parsing (csharp_structure_parser.py)

**LLM Provider Support**: Universal OpenAI-compatible API support enables:
- Ollama (local, privacy-focused)
- OpenRouter (multi-model gateway)
- Together AI (inference platform)
- OpenAI (GPT models)
- LM Studio (local server)
- Any OpenAI-compatible endpoint

## Architecture

### High-Level Design Pattern

DocuGen implements a **multi-agent pipeline architecture** with **iterative refinement loops**:

```
Input: C# Source Files
    ↓
┌─────────────────────────────────────────┐
│  Layer 1: File Summarization            │
│  (FileSummarizerAgent)                  │
│  Output: High-level summaries           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Validation Layer 1                     │
│  (ValidationAgent)                      │
│  → Pass: Continue to Layer 2            │
│  → Fail: Retry (max 3x) or Flag         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Layer 2: Detailed Documentation        │
│  (DetailingAgent)                       │
│  Output: Class/method documentation     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Validation Layer 2                     │
│  (ValidationAgent)                      │
│  → Pass: Continue to Layer 3            │
│  → Fail: Retry (max 3x) or Flag         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Layer 3: Relationship Mapping          │
│  (RelationshipMapperAgent)              │
│  Output: Dependencies & architecture    │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Validation Layer 3                     │
│  (ValidationAgent)                      │
│  → Pass: Save to JSON                   │
│  → Fail: Retry (max 3x) or Flag         │
└─────────────────────────────────────────┘
    ↓
JSON Files: layer1_summaries.json
            layer2_details.json
            layer3_relationships.json
    ↓
┌─────────────────────────────────────────┐
│  Layer 4: Documentation Synthesis       │
│  (DocumentationAgent)                   │
│  Output: DOCUMENTATION.md               │
└─────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Core Configuration System (`core.py`)

**Purpose**: Centralized configuration management and LLM client factory.

**Key Classes**:
- `DocuGenConfig`: Main configuration container with nested config models
- `ModelConfig`: LLM model selection per layer
- `ValidationConfig`: Quality control settings
- `OutputConfig`: Output directory and format options
- `ProcessingConfig`: Parallel processing and language support
- `LLMConfig`: API endpoint and authentication settings

**Key Functions**:
- `create_chat_model()`: Factory for creating LangChain ChatOpenAI instances with any provider
- `validate_config_path()`: Configuration file validation
- `validate_input_path()`: Source code directory validation
- `verify_ollama_running()`: Health check for local Ollama service

**Design Decision**: Uses Pydantic models throughout for type safety and automatic validation.

#### 2. State Management (`state.py`)

**Purpose**: Define all Pydantic models representing data flow through the pipeline.

**Key Models**:

**Layer Outputs**:
- `FileSummary`: Layer 1 output (summary, purpose, category, key_classes)
- `DetailedDocs`: Layer 2 output (classes, methods with full documentation)
- `RelationshipMap`: Layer 3 output (dependencies, architectural_role)

**Supporting Models**:
- `ClassDoc`: Detailed class documentation with methods, attributes, properties
- `MethodDoc`: Method signature, parameters, return type, description
- `AttributeDoc`: Field/attribute documentation
- `PropertyDoc`: Property documentation
- `DependencyInfo`: Cross-file dependency information
- `ValidationResult`: Validation output (passed, issues, refinement_instructions)

**Pipeline State**:
- `FileState`: Master state object passed through LangGraph nodes
  - Tracks all layer outputs
  - Maintains validation results
  - Counts iterations per layer
  - Stores error messages and review flags

**Configuration**:
- `GraphConfig`: LangGraph-specific configuration (models, prompts, validation rules)

#### 3. LangGraph Orchestrator (`orchestrator.py`)

**Purpose**: Implements the state machine that coordinates the multi-layer pipeline.

**Key Class**: `DocuGenOrchestrator`

**Workflow**:
1. Build LangGraph state machine with nodes for each layer and validation step
2. Define conditional edges based on validation results
3. Process files through the graph
4. Track iteration counts to prevent infinite loops
5. Flag files exceeding max iterations for manual review

**State Transitions**:
- `"proceed"`: Validation passed → next layer
- `"retry"`: Validation failed, iterations < max → retry current layer
- `"flag"`: Validation failed, iterations ≥ max → flag for review, continue

**Node Functions** (called by LangGraph):
- `_layer1_node()`: Execute FileSummarizerAgent
- `_validate_l1_node()`: Validate Layer 1 output
- `_layer2_node()`: Execute DetailingAgent
- `_validate_l2_node()`: Validate Layer 2 output
- `_layer3_node()`: Execute RelationshipMapperAgent
- `_validate_l3_node()`: Validate Layer 3 output

**Conditional Edge Functions**:
- `_should_retry_layer1/2/3()`: Determine next action after validation

**Public API**:
- `process_file(file_path)`: Process single file through complete pipeline
- `process_directory(directory, pattern)`: Batch process all matching files

#### 4. Agents (`agents/`)

All agents follow the **Four Pillars Architecture**:
1. **Model**: Configurable LLM (via LangChain ChatOpenAI)
2. **Prompt**: External markdown file (enables prompt versioning)
3. **Context**: Structured input with previous layer outputs
4. **Tools**: Structured output via Pydantic models

##### FileSummarizerAgent (`file_summarizer_agent.py`)

**Layer**: 1
**Purpose**: Generate high-level file summaries
**Model**: Fast model (default: codellama:7b)
**Input**: File content
**Output**: `FileSummary` (summary, purpose, category, key_classes, namespace info, technologies)
**Prompt**: `prompts/file_summarizer.md`

**Implementation Pattern**:
```python
# Structured output via Pydantic
self.model = base_model.with_structured_output(FileSummary)

# Invoke with system + user messages
summary = self.model.invoke([
    SystemMessage(content=self.system_prompt),
    HumanMessage(content=user_message)
])
```

##### DetailingAgent (`detailing_agent.py`)

**Layer**: 2
**Purpose**: Generate detailed class/method documentation
**Model**: Quality model (default: codellama:13b)
**Input**: File content + Layer 1 summary
**Output**: `DetailedDocs` (classes with methods, standalone methods)
**Prompt**: `prompts/detailing_agent.md`

**Context Enhancement**: Includes Layer 1 summary to maintain consistency and understanding.

##### RelationshipMapperAgent (`relationship_mapper_agent.py`)

**Layer**: 3
**Purpose**: Map cross-file dependencies and architectural patterns
**Model**: Fast model (default: codellama:7b)
**Input**: File content + Layer 1 & 2 outputs
**Output**: `RelationshipMap` (dependencies, dependents, architectural_role)
**Prompt**: `prompts/relationship_mapper.md`

**Dependency Analysis**: Infers relationships from:
- Using statements (namespace dependencies)
- Class instantiation patterns
- Dependency injection patterns
- Inheritance relationships

##### ValidationAgent (`validation_agent.py`)

**Purpose**: Hybrid quality validation (programmatic + LLM semantic checks)
**Model**: Quality model (defaults to detailing_model)
**Validation Strategy**: Two-phase approach

**Phase 1: Fast Programmatic Pre-checks**
- Structure validation (required fields present)
- Length requirements (e.g., min_summary_length)
- Data type validation
- Empty field detection

**Phase 2: LLM Semantic Validation**
- Accuracy: Does documentation match the code?
- Completeness: Are major components covered?
- Clarity: Is it understandable?
- Specificity: Is it specific to this file?

**Validation Methods**:
- `validate_layer1()`: Validates FileSummary
- `validate_layer2()`: Validates DetailedDocs
- `validate_layer3()`: Validates RelationshipMap

**Output**: `ValidationResult` with:
- `passed` (bool)
- `issues` (list of specific problems)
- `refinement_instructions` (actionable guidance for retry)

##### DocumentationAgent (`documentation_agent.py`)

**Layer**: 4
**Purpose**: Synthesize all JSON outputs into comprehensive markdown documentation
**Model**: Quality model (defaults to detailing_model)
**Input**: layer1_summaries.json, layer2_details.json, layer3_relationships.json
**Output**: DOCUMENTATION.md (comprehensive markdown)
**Prompt**: `prompts/documentation_agent.md`

**Synthesis Approach**: LLM reads all three JSON files and generates human-readable markdown with:
- Architecture overview
- Component documentation
- Dependency graphs
- Module organization
- Design patterns identified

#### 5. CLI Interface (`cli.py`)

**Framework**: Click (decorators-based command-line interface)

**Main Commands**:

```bash
# Full pipeline
docugen document -c config.yaml -i /path/to/code

# Test individual layers
docugen test layer1 -i file.cs -c config.yaml
docugen test layer2 -i file.cs -c config.yaml
docugen test layer3 -i file.cs -c config.yaml

# Test LLM connection
docugen test-connection -c config.yaml

# Status monitoring (placeholder)
docugen status -c config.yaml

# Resume interrupted job (placeholder)
docugen resume -c config.yaml
```

**Features**:
- Rich terminal UI with progress bars, tables, and colored output
- Verbose mode for debugging
- Dry-run mode for configuration validation
- Parallel file processing with progress tracking
- Error handling with detailed troubleshooting messages

#### 6. C# Structure Parser (`csharp_structure_parser.py`)

**Purpose**: Parse C# files to extract structural information using Tree-sitter.

**Key Classes**:
- `CSharpStructureParser`: Main parser class
- `ClassInfo`: Represents a C# class with metadata
- `MethodInfo`: Method signature and metadata
- `AttributeInfo`: Field/property information

**Capabilities**:
- Extract namespaces
- Identify classes and nested classes
- Parse methods and constructors
- Extract properties and fields
- Detect modifiers (public, private, static, etc.)
- Parse base classes and interfaces
- Extract method parameters

**CLI Support**: Standalone CLI for testing parser on individual files or directories.

**Usage**:
```bash
python csharp_structure_parser.py /path/to/file.cs --json
python csharp_structure_parser.py /path/to/directory/
```

#### 7. Writers (`writers/`)

##### json_writer.py

**Purpose**: Serialize layer outputs to JSON files for Layer 4 processing.

**Key Function**: `save_layer_outputs(results, output_dir)`

**Output Files**:
- `layer1_summaries.json`: All file summaries
- `layer2_details.json`: All detailed documentation
- `layer3_relationships.json`: All relationship mappings

**Data Structure**: List of dictionaries, each containing file path and corresponding layer output.

#### 8. Logging (`logger.py`)

**Framework**: Loguru (structured, contextual logging)

**Configuration**:
- Console handler: Colorized output for interactive use
- File handler: Structured logs with rotation (10 MB, 10 days retention)
- Thread-safe logging with enqueue=True

**Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL, SUCCESS

**Contextual Logging**: Supports keyword arguments for structured data:
```python
logger.info("Processing file", file=str(file_path), layer="Layer1")
```

## Implementation Details

### Data Flow Through System

1. **Input Phase**:
   - User provides config.yaml and source directory
   - CLI validates configuration and Ollama connection
   - System discovers all .cs files recursively

2. **Processing Phase** (per file):
   - Read file content
   - Create `FileState` object
   - Pass through LangGraph orchestrator
   - Each layer:
     - Agent processes state
     - Validation checks output
     - Retry if validation fails (max 3x)
     - Flag for review if max iterations reached
   - Return final `FileState`

3. **Aggregation Phase**:
   - Collect all `FileState` objects
   - Extract layer outputs
   - Serialize to JSON files

4. **Synthesis Phase**:
   - DocumentationAgent reads all JSON files
   - LLM generates comprehensive markdown
   - Write DOCUMENTATION.md

### Configuration Management

**Configuration Hierarchy**:
1. Default values (hardcoded in Pydantic models)
2. config.yaml overrides
3. CLI argument overrides (e.g., --output)

**Example config.yaml**:
```yaml
llm:
  base_url: "http://localhost:11434/v1"
  api_key_env: null  # Use env var name for API key
  timeout: 300

models:
  default: "codellama:13b"
  summarizer: "codellama:7b"
  detailing: "codellama:13b"
  relationship_mapper: "codellama:7b"
  validation: null  # Defaults to detailing

validation:
  max_iterations: 3
  min_summary_length: 50
  require_all_public_methods: true

output:
  base_path: "./docs_output"
  format: "markdown"
  include_metadata: true

processing:
  parallel_files: 4
  enable_incremental: true
  supported_languages: ["csharp"]
```

### Error Handling Strategy

**Graceful Degradation**:
- File processing errors don't stop the entire pipeline
- Failed files are flagged and tracked separately
- Error messages stored in `FileState.error_message`
- Final summary shows success rate and lists problematic files

**Retry Mechanism**:
- Each layer can retry up to `max_iterations` times
- Validation provides specific refinement instructions
- After max retries, file is flagged but pipeline continues

**Logging Levels**:
- DEBUG: Detailed execution flow
- INFO: Progress and milestones
- WARNING: Validation failures, retries
- ERROR: Processing errors, missing files
- CRITICAL: System failures
- SUCCESS: Completed operations (custom Loguru level)

### LLM Integration Patterns

**Provider Abstraction**:
```python
# Unified factory function supports any OpenAI-compatible API
client = create_chat_model(
    base_url="http://localhost:11434/v1",  # or any provider
    model_name="codellama:7b",
    api_key_env="OPENAI_API_KEY",  # optional
    timeout=300
)
```

**Structured Output Pattern**:
```python
# LangChain's with_structured_output() enforces Pydantic schema
model = base_model.with_structured_output(FileSummary)
result = model.invoke([system_msg, user_msg])
# result is a FileSummary instance, not raw text
```

**Benefits**:
- Type-safe outputs
- Automatic validation
- No JSON parsing errors
- Schema enforcement by LLM

### Prompt Engineering Approach

**Prompt Storage**: External markdown files in `prompts/` directory
- Enables version control of prompts
- Allows prompt iteration without code changes
- Supports A/B testing and experimentation

**Prompt Structure** (example: file_summarizer.md):
1. **Role Definition**: "You are a File Summarizer Agent..."
2. **Objectives**: Numbered list of goals
3. **Input Context**: What data will be provided
4. **Output Format**: JSON schema with examples
5. **Guidelines**: DO/DON'T lists
6. **Examples**: 3+ concrete examples with input/output
7. **Quality Criteria**: How output will be validated
8. **Module-Specific Instructions**: Domain-specific guidance

**Validation Prompts**: Separate prompts for each layer's validation
- `validation_layer1.md`: File summary validation
- `validation_layer2.md`: Detailed docs validation
- `validation_layer3.md`: Relationship mapping validation

### Testing Strategy

**Test Organization**: Tests located in `tests/` subdirectory within module
- `test_core.py`: Configuration loading and validation
- `test_cli.py`: CLI command testing
- Fixtures in `tests/fixtures/sample_csharp/`

**Isolated Testing**: CLI provides test commands for individual layers:
```bash
# Test Layer 1 only
docugen test layer1 -i MyFile.cs -c config.yaml -o results.json

# Test with limit
docugen test layer1 -i src/ -l 5  # Process only 5 files
```

**Benefits**:
- Fast iteration during development
- Agent-specific debugging
- Output inspection before full pipeline run
- No need to run entire pipeline to test changes

## Usage

### Common Workflows

#### 1. First-Time Setup

```bash
# Install dependencies
uv add langgraph pydantic pyyaml ollama click rich loguru

# Start Ollama (local option)
ollama serve
ollama pull codellama:7b
ollama pull codellama:13b

# Create configuration
cp src/modules/docugen/config/config.example.yaml config.yaml
# Edit config.yaml with your settings

# Test connection
docugen test-connection -c config.yaml
```

#### 2. Full Documentation Generation

```bash
# Process entire codebase
docugen document -c config.yaml -i /path/to/csharp/project

# With verbose logging
docugen document -c config.yaml -i /path/to/project -v

# Custom output directory
docugen document -c config.yaml -i /path/to/project -o ./my_docs
```

**Outputs**:
- `docs_output/layer1_summaries.json`
- `docs_output/layer2_details.json`
- `docs_output/layer3_relationships.json`
- `docs_output/DOCUMENTATION.md`

#### 3. Iterative Development

```bash
# Test Layer 1 agent on single file
docugen test layer1 -i src/Services/UserService.cs -c config.yaml

# Test Layer 2 with limited files
docugen test layer2 -i src/Services/ -l 3 -c config.yaml

# Save test results for inspection
docugen test layer1 -i src/ -l 10 -o layer1_test.json
```

#### 4. Using Different LLM Providers

**Ollama (Local)**:
```yaml
llm:
  base_url: "http://localhost:11434/v1"
  api_key_env: null
```

**OpenRouter**:
```yaml
llm:
  base_url: "https://openrouter.ai/api/v1"
  api_key_env: "OPENROUTER_API_KEY"
models:
  detailing: "anthropic/claude-3-5-sonnet"
```

**OpenAI**:
```yaml
llm:
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"
models:
  detailing: "gpt-4"
```

**.env file**:
```
OPENROUTER_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
```

### Integration with Other Modules

**Input**: Any C# codebase (directory with .cs files)

**Output**: Structured JSON + Markdown documentation

**Potential Integrations**:
- CI/CD pipelines: Auto-generate docs on commit
- Code review tools: Provide AI-generated context
- Knowledge bases: Feed documentation to search systems
- Training materials: Generate onboarding documentation

## Development Guidelines

### Coding Conventions

**Type Safety**:
- All data models use Pydantic
- Type hints on all function signatures
- No raw dictionaries for structured data

**Error Handling**:
- Use try/except with specific exception types
- Log exceptions with `logger.exception()`
- Store error messages in state objects
- Never let single file failure stop batch processing

**Logging**:
- Use appropriate log levels
- Include contextual information (file names, layer, iteration)
- Use `logger.success()` for positive milestones
- Debug logs should be traceable through entire pipeline

**State Management**:
- Never mutate state outside LangGraph nodes
- Always return new/updated state from agents
- Use FileState as single source of truth
- Track iterations explicitly

### Testing Approach

**Unit Tests**:
```python
# Test configuration loading
def test_config_loading():
    config = DocuGenConfig.from_yaml(Path("config.example.yaml"))
    assert config.models.summarizer == "codellama:7b"

# Test validation logic
def test_layer1_validation():
    agent = ValidationAgent(config)
    result = agent.validate_layer1(valid_summary, file_content)
    assert result.passed == True
```

**Integration Tests**:
```bash
# Test full pipeline on sample codebase
docugen document -c test_config.yaml -i tests/fixtures/sample_csharp/
```

**Prompt Testing**:
- Use `docugen test layer1/2/3` commands
- Inspect JSON outputs manually
- Verify structured output compliance
- Check for hallucinations or inaccuracies

### How to Extend Functionality

#### Adding a New Layer

1. **Define State Model** (in `state.py`):
```python
class Layer4Output(BaseModel):
    """Layer 4 output model."""
    field1: str
    field2: List[str]
```

2. **Create Agent** (new file `agents/layer4_agent.py`):
```python
class Layer4Agent:
    def __init__(self, config: GraphConfig):
        self.model = create_chat_model(...).with_structured_output(Layer4Output)
    
    def invoke(self, state: FileState) -> FileState:
        # Process state, call LLM, update state
        state.layer4_output = result
        return state
```

3. **Update Orchestrator** (in `orchestrator.py`):
```python
# Add node
workflow.add_node("layer4", self._layer4_node)
workflow.add_node("validate_l4", self._validate_l4_node)

# Add edges
workflow.add_edge("layer3", "layer4")
workflow.add_conditional_edges("validate_l4", ...)
```

4. **Create Prompt** (`prompts/layer4_agent.md`)

5. **Add Validation** (`prompts/validation_layer4.md`)

6. **Update FileState** (in `state.py`):
```python
class FileState(BaseModel):
    # ... existing fields ...
    layer4_output: Optional[Layer4Output] = None
    layer4_validation: Optional[ValidationResult] = None
    layer4_iterations: int = Field(default=0)
```

#### Adding Support for New Language

1. **Create Parser** (e.g., `python_structure_parser.py`):
```python
class PythonStructureParser:
    def parse_file(self, file_path: str) -> List[ClassInfo]:
        # Use tree-sitter-python or ast module
        pass
```

2. **Update Configuration**:
```yaml
processing:
  supported_languages: ["csharp", "python"]
```

3. **Create Language-Specific Prompts**:
- `prompts/file_summarizer_python.md`
- `prompts/detailing_agent_python.md`

4. **Add Language Detection** (in `core.py` or CLI):
```python
def detect_language(file_path: Path) -> str:
    if file_path.suffix == ".cs":
        return "csharp"
    elif file_path.suffix == ".py":
        return "python"
```

5. **Update Agents** to select prompt based on language

### Common Patterns to Follow

**Agent Structure**:
```python
class NewAgent:
    def __init__(self, config: GraphConfig):
        # Load prompt
        # Create model with structured output
        # Store configuration
    
    def invoke(self, state: FileState) -> FileState:
        # Prepare context
        # Call LLM
        # Update state
        # Handle errors
        return state
```

**Validation Pattern**:
```python
# Phase 1: Fast pre-checks
if not output:
    return ValidationResult(passed=False, issues=["Missing output"])

precheck_issues = []
# Check structure, required fields, data types
if precheck_issues:
    return ValidationResult(passed=False, issues=precheck_issues)

# Phase 2: LLM semantic validation
result = self._call_llm_validator(prompt, context)
return result
```

**Error Recovery**:
```python
try:
    # Processing logic
    result = agent.invoke(state)
except Exception as e:
    logger.exception(f"Agent failed: {e}")
    state.error_message = f"Layer failed: {str(e)}"
    state.flagged_for_review = True
    return state
```

## Troubleshooting

### Common Issues

#### 1. Ollama Not Running
**Symptom**: Connection refused errors
**Solution**:
```bash
ollama serve
# In another terminal:
ollama pull codellama:7b
```

#### 2. Model Not Found
**Symptom**: "model 'codellama:7b' not found"
**Solution**:
```bash
ollama list  # Check available models
ollama pull codellama:7b  # Download if missing
```

#### 3. API Key Not Configured
**Symptom**: "API key environment variable 'OPENROUTER_API_KEY' is not set"
**Solution**:
- Create `.env` file in project root
- Add: `OPENROUTER_API_KEY=your-key-here`
- Verify with: `echo $OPENROUTER_API_KEY`

#### 4. Out of Memory
**Symptom**: System slowdown, killed processes
**Solution**:
- Reduce `parallel_files` in config.yaml (try 2)
- Use smaller models (codellama:7b instead of 13b)
- Process fewer files at once

#### 5. Validation Always Failing
**Symptom**: Files repeatedly retrying and being flagged
**Debug**:
```bash
# Run with verbose mode
docugen test layer1 -i problem_file.cs -v

# Check validation prompts
cat src/modules/docugen/prompts/validation_layer1.md

# Adjust validation settings
validation:
  max_iterations: 5  # Allow more retries
  min_summary_length: 30  # Reduce requirements
```

#### 6. Structured Output Errors
**Symptom**: "Failed to parse LLM output as structured schema"
**Causes**:
- Model too small (try larger model)
- Prompt unclear (review prompt file)
- Model doesn't support function calling

**Solution**:
- Use larger, more capable model
- Simplify Pydantic schema
- Add more examples to prompt

#### 7. Slow Performance
**Optimization**:
- Use smaller, faster models for Layers 1 & 3
- Reserve large model only for Layer 2 (quality critical)
- Increase `parallel_files` if CPU/RAM available
- Use local Ollama for faster inference

### Debug Strategies

**Enable Verbose Logging**:
```bash
docugen document -c config.yaml -i /path -v
```

**Test Individual Layers**:
```bash
# Isolate the problem layer
docugen test layer2 -i problem_file.cs -c config.yaml -v
```

**Inspect JSON Outputs**:
```bash
# Save and review intermediate results
docugen test layer1 -i src/ -o debug_layer1.json
cat debug_layer1.json | jq '.[0]'  # Pretty print first result
```

**Check Log Files**:
```bash
# Logs stored in ./logs/app.log
tail -f logs/app.log  # Monitor in real-time
grep ERROR logs/app.log  # Find errors
```

**Validate Configuration**:
```bash
# Dry run to check config
docugen document -c config.yaml -i /path --dry-run
```

**Test LLM Connection**:
```bash
docugen test-connection -c config.yaml
```

### Performance Considerations

**Hardware Requirements**:
- **Minimum**: 8GB RAM, 4-core CPU
- **Recommended**: 16GB RAM, 8-core CPU
- **Optimal**: 32GB RAM, 16-core CPU, GPU (for local models)

**Expected Throughput**:
- Small codebases (<100 files): 5-10 minutes
- Medium codebases (100-1000 files): 30-60 minutes
- Large codebases (1000-5000 files): 2-4 hours
- Varies based on model size and hardware

**Optimization Tips**:
- Use quantized models (Q4, Q5) for faster inference
- Enable parallelization: `parallel_files: 4-8`
- Use SSD for faster file I/O
- Close other applications to free memory
- Use smaller models for non-critical layers

## Key Design Decisions

### Why LangGraph?
- **State machine semantics**: Clear visualization of workflow
- **Conditional edges**: Elegant retry logic implementation
- **Type-safe state**: Pydantic integration
- **Debugging**: Built-in state inspection

### Why External Prompts?
- **Version control**: Track prompt changes over time
- **Iteration**: Modify prompts without code changes
- **Testing**: A/B test different prompt strategies
- **Collaboration**: Non-developers can improve prompts

### Why Hybrid Validation?
- **Speed**: Fast programmatic checks catch obvious issues
- **Quality**: LLM semantic checks catch subtle problems
- **Cost**: Reduce LLM calls by pre-filtering
- **Reliability**: Fallback if LLM validation fails

### Why Multi-Layer Pipeline?
- **Separation of concerns**: Each agent has focused responsibility
- **Incremental understanding**: Build complexity gradually
- **Error isolation**: Problems in one layer don't corrupt others
- **Flexibility**: Replace individual layers without full rewrite

### Why Structured Output?
- **Type safety**: Pydantic validation at runtime
- **Consistency**: Same schema every time
- **Integration**: Easy to consume by Layer 4 and external systems
- **Error reduction**: No JSON parsing failures

## Module Dependencies

**Direct Dependencies** (from imports):
- `langgraph`: State machine orchestration
- `langchain_openai`: LLM client (ChatOpenAI)
- `langchain_core`: Message types (SystemMessage, HumanMessage)
- `pydantic`: Data validation and models
- `loguru`: Structured logging
- `click`: CLI framework
- `rich`: Terminal UI
- `yaml` (PyYAML): Configuration parsing
- `tree_sitter`: Code parsing
- `tree_sitter_c_sharp`: C# grammar
- `dotenv`: Environment variable loading

**Python Standard Library**:
- `pathlib`: Path manipulation
- `json`: JSON serialization
- `subprocess`: Ollama health checks
- `os`: Environment variables
- `sys`: System operations
- `dataclasses`: Data structures (parser)
- `typing`: Type hints

## Future Enhancements

**Planned Features** (from README and code):
- Multi-language support (Java, Python, JavaScript)
- Incremental documentation updates (only changed files)
- Resume capability for interrupted jobs
- Status monitoring for long-running jobs
- Enhanced dependency graph visualization
- API server mode for programmatic access
- Integration with documentation hosting platforms

**Architecture Improvements**:
- Parallel file processing implementation (currently sequential)
- Caching layer for repeated analysis
- Database backend for state persistence
- Webhook notifications for completion
- Real-time progress WebSocket API

**Quality Enhancements**:
- Confidence scores for each layer output
- Human-in-the-loop review interface
- Batch refinement mode for flagged files
- Custom validation rule framework
- Output quality metrics dashboard

## File Locations Reference

All paths are absolute from project root:

**Core Files**:
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/core.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/state.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/orchestrator.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/cli.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/logger.py`

**Agents**:
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/agents/file_summarizer_agent.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/agents/detailing_agent.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/agents/relationship_mapper_agent.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/agents/validation_agent.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/agents/documentation_agent.py`

**Utilities**:
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/csharp_structure_parser.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/writers/json_writer.py`

**Configuration**:
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/config/config.example.yaml`

**Prompts**:
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/prompts/file_summarizer.md`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/prompts/detailing_agent.md`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/prompts/relationship_mapper.md`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/prompts/documentation_agent.md`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/prompts/validation_layer1.md`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/prompts/validation_layer2.md`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/prompts/validation_layer3.md`

**Tests**:
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/tests/test_core.py`
- `/home/Andrea/Projects/ai-dev-environment/src/modules/docugen/tests/test_cli.py`

## Summary

DocuGen is a production-ready, extensible documentation generation system that demonstrates best practices in:
- Multi-agent AI system design
- LangGraph state machine orchestration
- Structured LLM output with Pydantic
- Provider-agnostic LLM integration
- Robust error handling and validation
- CLI-first developer experience
- Test-driven development

The module is well-architected with clear separation of concerns, extensive logging, graceful error handling, and comprehensive configuration options. It serves as an excellent reference implementation for building multi-agent LLM systems with quality validation and iterative refinement.
