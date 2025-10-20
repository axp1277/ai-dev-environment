# DocuGen - AI-Powered Code Documentation System

## Overview

DocuGen is a sophisticated multi-agent AI system that automatically generates comprehensive, multi-layered documentation for C# codebases using LangGraph orchestration and Large Language Models (LLMs). The system processes source code through a four-layer pipeline, progressively building documentation from high-level summaries to detailed API documentation with cross-file dependency mapping.

### Key Technologies

- **LangGraph**: Multi-agent workflow orchestration with state management
- **LangChain**: Universal LLM provider abstraction (supports Ollama, OpenAI, OpenRouter, Together AI)
- **Pydantic**: Strong typing and data validation across all layers
- **Click**: Professional CLI interface with subcommands
- **Rich**: Terminal UI with progress tracking and formatted output
- **Python 3.11+**: Modern Python with type hints throughout

### What It Accomplishes

1. **Automated Documentation Generation**: Transforms legacy C# codebases into comprehensive markdown documentation without manual effort
2. **Multi-Layer Analysis**: Builds understanding progressively from file summaries → detailed documentation → architectural relationships
3. **Quality Assurance**: Validates each layer with hybrid programmatic + LLM semantic checks and auto-refinement
4. **Provider Flexibility**: Works with local models (Ollama) for privacy or cloud APIs (OpenRouter, OpenAI) for performance
5. **Scalability**: Processes large codebases (5000+ files) with parallel processing and iteration limits

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         DocuGen System                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ Layer 1  │───▶│ Layer 2  │───▶│ Layer 3  │───▶│ Layer 4  │ │
│  │Summarize │    │ Detail   │    │Relation  │    │Synthesis │ │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └──────────┘ │
│       │               │               │                        │
│       ▼               ▼               ▼                        │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                   │
│  │Validate │    │Validate │    │Validate │                   │
│  │L1 (max  │    │L2 (max  │    │L3 (max  │                   │
│  │3 retries│    │3 retries│    │3 retries│                   │
│  └─────────┘    └─────────┘    └─────────┘                   │
│                                                                 │
│  Output: layer1.json → layer2.json → layer3.json → DOCS.md    │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. CLI Layer (`cli.py`)
Entry point providing comprehensive command-line interface:

**Commands:**
- `document`: Full pipeline execution with progress tracking
- `test layer1/layer2/layer3`: Isolated agent testing
- `test-connection`: LLM connectivity validation
- `status`: Job monitoring (planned)
- `resume`: Interrupted job recovery (planned)
- `validate`: Documentation quality checks (planned)

**Design Pattern:** Command pattern with Click decorators, Rich console output, comprehensive error handling

#### 2. Core Configuration (`core.py`)
Centralized configuration management with Pydantic validation:

**Key Models:**
- `DocuGenConfig`: Root configuration with nested models
- `ModelConfig`: Per-agent LLM model selection
- `LLMConfig`: Universal provider configuration (OpenAI-compatible)
- `ValidationConfig`: Quality thresholds and iteration limits
- `ProcessingConfig`: Parallelism and language support
- `OutputConfig`: File paths and metadata settings

**Design Pattern:** Configuration as code with YAML serialization, environment variable injection via python-dotenv

**Critical Function:** `create_chat_model()` - Universal LLM factory supporting any OpenAI-compatible endpoint

#### 3. State Management (`state.py`)
Type-safe state objects passed through LangGraph workflow:

**Core Models:**
- `FileState`: Complete pipeline state for a single file
  - Input: `file_path`, `file_content`
  - Layer 1: `layer1_summary`, `layer1_validation`, `layer1_iterations`
  - Layer 2: `layer2_details`, `layer2_validation`, `layer2_iterations`
  - Layer 3: `layer3_relationships`, `layer3_validation`, `layer3_iterations`
  - Metadata: `current_layer`, `flagged_for_review`, `error_message`

- `GraphConfig`: Orchestrator configuration (models, prompts, validation rules)

**Documentation Models:**
- `FileSummary`: Layer 1 output (summary, key_classes, purpose, category)
- `DetailedDocs`: Layer 2 output (classes[], standalone_methods[])
- `RelationshipMap`: Layer 3 output (dependencies[], dependents[], architectural_role)
- `ValidationResult`: Validation output (passed, issues[], refinement_instructions)

**Design Pattern:** Immutable state transitions, Pydantic validation at every layer

#### 4. Orchestration (`orchestrator.py`)
LangGraph state machine coordinating the entire pipeline:

**Class: `DocuGenOrchestrator`**

**Graph Structure:**
```python
START → layer1 → validate_l1 → [proceed → layer2 | retry → layer1 | flag → END]
        layer2 → validate_l2 → [proceed → layer3 | retry → layer2 | flag → END]
        layer3 → validate_l3 → [proceed → END | retry → layer3 | flag → END]
```

**Key Methods:**
- `_build_graph()`: Constructs LangGraph workflow with conditional edges
- `_layer1_node()`, `_layer2_node()`, `_layer3_node()`: Agent execution nodes
- `_validate_l1_node()`, `_validate_l2_node()`, `_validate_l3_node()`: Validation nodes
- `_should_retry_layer{1,2,3}()`: Conditional routing logic (proceed/retry/flag)
- `process_file()`: Single file pipeline execution
- `process_directory()`: Batch processing with error recovery

**Iteration Control:**
- Max 3 retries per layer (configurable)
- Automatic flagging for manual review after max iterations
- Graceful degradation: flagged files continue through pipeline

**Design Pattern:** State machine orchestration, graceful failure handling, structured logging with loguru

#### 5. Agents (`agents/`)

##### `file_summarizer_agent.py` (Layer 1)
**Purpose:** Generate high-level file summaries

**Input:** Raw C# source code
**Output:** `FileSummary` (summary, purpose, category, key_classes)
**Model:** Configurable (default: `codellama:7b`)
**Prompt:** `prompts/file_summarizer.md`
**Tools:** None (direct code analysis)

**Implementation:**
- LangChain `with_structured_output(FileSummary)` for type-safe JSON responses
- System/Human message pattern
- External prompt loading from markdown files

##### `detailing_agent.py` (Layer 2)
**Purpose:** Generate detailed class/method documentation

**Input:** File content + Layer 1 summary
**Output:** `DetailedDocs` (classes[], standalone_methods[])
**Model:** Configurable (default: `codellama:13b` - quality critical)
**Prompt:** `prompts/detailing_agent.md`
**Tools:** None

**Key Features:**
- Exhaustive method documentation (signature, description, parameters, returns)
- Class-level organization
- Standalone method detection

##### `relationship_mapper_agent.py` (Layer 3)
**Purpose:** Map cross-file dependencies and architectural patterns

**Input:** File content + Layer 1 + Layer 2
**Output:** `RelationshipMap` (dependencies[], dependents[], architectural_role)
**Model:** Configurable (default: `codellama:7b`)
**Prompt:** `prompts/relationship_mapper.md`
**Tools:** None

**Dependency Types:**
- Composition, Inheritance, Usage, Injection
- Bidirectional mapping (dependencies + dependents)
- Architectural role identification (Service, Repository, Controller, etc.)

##### `validation_agent.py`
**Purpose:** Hybrid validation (programmatic + LLM semantic)

**Validation Strategies:**
1. **Programmatic Checks:**
   - Summary length validation
   - Required field presence
   - JSON schema compliance

2. **LLM Semantic Validation:**
   - Accuracy assessment
   - Completeness verification
   - Quality scoring

**Output:** `ValidationResult` with specific refinement instructions for failed validations

##### `documentation_agent.py` (Layer 4)
**Purpose:** Synthesize final markdown documentation

**Input:** layer1.json + layer2.json + layer3.json
**Output:** `DOCUMENTATION.md`
**Model:** Configurable (default: `mistral-nemo:latest`)
**Prompt:** `prompts/documentation_agent.md`

**Synthesis Strategy:**
- Aggregate all layer outputs
- Generate cohesive narrative
- Include architectural overview
- Cross-reference dependencies
- Add metadata (timestamps, validation status)

#### 6. Writers (`writers/`)

##### `json_writer.py`
Handles JSON serialization of layer outputs:

**Functions:**
- `save_layer_outputs()`: Saves all three layers to JSON files
- `serialize_file_state()`: Converts Pydantic models to JSON-safe dicts
- Path handling for nested Pydantic models

**Output Files:**
- `layer1_summaries.json`: All file summaries
- `layer2_details.json`: Detailed documentation
- `layer3_relationships.json`: Dependency mappings

## Implementation Patterns

### 1. Universal LLM Provider Support

**Design Decision:** Use LangChain's OpenAI-compatible abstraction

```python
# Supports: Ollama, OpenRouter, Together AI, OpenAI, LM Studio
from langchain_openai import ChatOpenAI

def create_chat_model(base_url, model_name, api_key_env, timeout):
    api_key = os.getenv(api_key_env) if api_key_env else "not-needed"

    return ChatOpenAI(
        base_url=base_url,  # e.g., "http://localhost:11434/v1"
        api_key=api_key,
        model=model_name,   # e.g., "codellama:7b" or "gpt-4"
        timeout=timeout,
        temperature=0  # Deterministic for documentation
    )
```

**Configuration (config.yaml):**
```yaml
llm:
  base_url: "http://localhost:11434/v1"  # Local Ollama
  # base_url: "https://openrouter.ai/api/v1"  # OpenRouter
  api_key_env: null  # or "OPENROUTER_API_KEY"
  timeout: 300
```

### 2. Structured Output Pattern

**All agents use LangChain structured output for type safety:**

```python
# Agent initialization
base_model = create_chat_model(...)
self.model = base_model.with_structured_output(FileSummary)

# Invocation (returns Pydantic object directly)
summary = self.model.invoke([
    SystemMessage(content=self.system_prompt),
    HumanMessage(content=user_message)
])
# summary is FileSummary instance, not raw text
```

**Benefits:**
- Automatic JSON parsing and validation
- Type safety throughout pipeline
- Schema compliance guaranteed by LangChain
- No manual JSON parsing or error handling

### 3. External Prompt Management

**All prompts stored as markdown files in `prompts/`:**

```
prompts/
├── file_summarizer.md         # Layer 1 system prompt
├── detailing_agent.md         # Layer 2 system prompt
├── relationship_mapper.md     # Layer 3 system prompt
├── documentation_agent.md     # Layer 4 system prompt
├── validation_layer1.md       # L1 validation prompt
├── validation_layer2.md       # L2 validation prompt
└── validation_layer3.md       # L3 validation prompt
```

**Loading Pattern:**
```python
def _load_prompt(self) -> str:
    with open(self.prompt_path, 'r') as f:
        return f.read()
```

**Benefits:**
- Prompts are version-controlled
- Easy A/B testing and refinement
- Non-developers can modify prompts
- Clear separation of concerns

### 4. Validation Loop with Iteration Limits

**Prevents infinite refinement loops:**

```python
def _should_retry_layer1(state: FileState) -> Literal["proceed", "retry", "flag"]:
    if state.layer1_validation.passed:
        return "proceed"  # Move to Layer 2

    if state.layer1_iterations >= self.config.max_iterations:
        state.flagged_for_review = True
        return "flag"  # Give up, flag for human review

    return "retry"  # Try again with refinement instructions
```

**Configuration:**
```yaml
validation:
  max_iterations: 3  # Configurable threshold (1-10)
```

**Graceful Degradation:**
- Flagged files continue through pipeline (best-effort)
- Final output includes flagged file list
- Manual review workflow supported

### 5. Error Handling Strategy

**Three-tier error handling:**

1. **Agent-level:** Try/catch in agent `invoke()` methods
   ```python
   except Exception as e:
       state.error_message = f"Layer 1 failed: {str(e)}"
       return state  # Partial state returned
   ```

2. **Orchestrator-level:** Pipeline-level error recovery
   ```python
   except Exception as e:
       initial_state.error_message = f"Pipeline failed: {str(e)}"
       initial_state.flagged_for_review = True
       return initial_state
   ```

3. **Batch-level:** Directory processing continues on file failures
   ```python
   for file_path in files:
       try:
           results[file_path] = self.process_file(file_path)
       except Exception as e:
           results[file_path] = FileState(error_message=str(e))
   ```

**Result:** No single file failure crashes entire pipeline

### 6. Logging Architecture

**Structured logging with loguru:**

```python
logger.info("Processing file", file=str(file_path), iteration=3)
logger.success("Validation passed", layer="layer2")
logger.warning("Max iterations reached", iterations=3)
logger.error("Agent failed", error=str(e))
```

**Benefits:**
- Structured fields for parsing
- Color-coded severity levels
- Configurable verbosity (INFO/DEBUG via `-v` flag)
- Automatic exception tracing with `logger.exception()`

## Configuration Reference

### Complete config.yaml Schema

```yaml
# LLM Connection (OpenAI-compatible)
llm:
  base_url: "http://localhost:11434/v1"  # Required (must end with /v1)
  api_key_env: null                      # Optional (e.g., "OPENAI_API_KEY")
  timeout: 300                           # Seconds

# Model Selection (per-agent)
models:
  default: "mistral-nemo:latest"        # General purpose
  summarizer: "qwen3:1.7b"              # Fast summaries (Layer 1)
  detailing: "granite3.3:latest"        # Quality docs (Layer 2, critical)
  relationship_mapper: "qwen3:1.7b"     # Dependency mapping (Layer 3)
  validation: "granite3.3:latest"       # Validation (defaults to detailing)

# Quality Validation
validation:
  max_iterations: 3                     # Retries per layer (1-10)
  min_summary_length: 50                # Characters
  require_all_public_methods: true      # Enforce completeness

# Output Settings
output:
  base_path: "./docs_output"            # Directory
  format: "markdown"                    # Currently only markdown
  include_metadata: true                # Timestamps, validation status

# Processing Options
processing:
  parallel_files: 4                     # Concurrent files (1-16)
  enable_incremental: true              # Re-process only changed files (NYI)
  supported_languages:
    - "csharp"                          # Currently C# only
```

### Model Selection Guidelines

**For local Ollama:**
- Layer 1 (speed): `codellama:7b`, `qwen3:1.7b`
- Layer 2 (quality): `codellama:13b`, `granite3.3:latest`, `deepseek-coder:6.7b`
- Layer 3 (speed): `codellama:7b`, `qwen3:1.7b`

**For cloud APIs (OpenRouter, OpenAI):**
- Layer 1: `meta-llama/llama-3.1-8b-instruct`
- Layer 2: `anthropic/claude-3-5-sonnet`, `gpt-4-turbo`
- Layer 3: `meta-llama/llama-3.1-8b-instruct`

**Memory Considerations:**
- 7B models: ~8GB RAM
- 13B models: ~16GB RAM
- Reduce `parallel_files` if memory-constrained

## Usage Examples

### 1. Full Pipeline Execution

```bash
# Generate documentation for entire codebase
docugen document -c config.yaml -i /path/to/csharp/code

# Dry run (validate config without processing)
docugen document -c config.yaml -i /path/to/code --dry-run

# Verbose logging for debugging
docugen document -c config.yaml -i /path/to/code -v
```

**Output:**
```
docs_output/
├── layer1_summaries.json         # All file summaries
├── layer2_details.json           # Detailed documentation
├── layer3_relationships.json     # Dependency mappings
└── DOCUMENTATION.md              # Final comprehensive docs
```

### 2. Testing Individual Layers

```bash
# Test Layer 1 (summaries)
docugen test layer1 -c config.yaml -i MyService.cs

# Test Layer 2 (detailed docs) - auto-runs L1 first
docugen test layer2 -c config.yaml -i MyService.cs

# Test Layer 3 (dependencies) - auto-runs L1+L2 first
docugen test layer3 -c config.yaml -i MyService.cs

# Process multiple files with limit
docugen test layer1 -c config.yaml -i src/Services -l 5

# Save JSON output
docugen test layer2 -c config.yaml -i src/ -l 3 -o layer2_test.json
```

### 3. Connection Testing

```bash
# Test LLM connectivity
docugen test-connection -c config.yaml

# Output:
# ✓ Connection successful!
# Response: Hello! How can I help?
```

### 4. Programmatic Usage

```python
from pathlib import Path
from src.modules.docugen.orchestrator import create_orchestrator
from src.modules.docugen.state import GraphConfig
from src.modules.docugen.core import DocuGenConfig

# Load configuration
config_path = Path("config.yaml")
doc_config = DocuGenConfig.from_yaml(config_path)

# Create graph config
graph_config = GraphConfig(
    summarizer_model=doc_config.models.summarizer,
    detailing_model=doc_config.models.detailing,
    relationship_model=doc_config.models.relationship_mapper,
    llm_base_url=doc_config.llm.base_url,
    llm_api_key_env=doc_config.llm.api_key_env,
    max_iterations=doc_config.validation.max_iterations
)

# Create orchestrator
orchestrator = create_orchestrator(graph_config)

# Process single file
file_path = Path("MyService.cs")
result = orchestrator.process_file(file_path)

# Process directory
results = orchestrator.process_directory(Path("src/"), pattern="*.cs")

# Access layer outputs
for file, state in results.items():
    print(f"File: {file}")
    print(f"Summary: {state.layer1_summary.summary}")
    print(f"Classes: {[c.name for c in state.layer2_details.classes]}")
    print(f"Dependencies: {len(state.layer3_relationships.dependencies)}")
```

## Development Guidelines

### 1. Adding a New Agent

**Steps:**
1. Create `src/modules/docugen/agents/my_agent.py`
2. Define output model in `state.py`
3. Create prompt in `prompts/my_agent.md`
4. Implement agent class with `invoke()` method
5. Add node function for LangGraph
6. Wire into orchestrator graph

**Template:**
```python
from ..state import FileState, MyOutput, GraphConfig
from ..core import create_chat_model

class MyAgent:
    def __init__(self, config: GraphConfig):
        base_model = create_chat_model(
            config.llm_base_url,
            config.my_model,
            config.llm_api_key_env,
            config.llm_timeout
        )
        self.model = base_model.with_structured_output(MyOutput)
        self.system_prompt = self._load_prompt()

    def invoke(self, state: FileState) -> FileState:
        try:
            result = self.model.invoke([
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=self._prepare_context(state))
            ])
            state.my_output = result
            return state
        except Exception as e:
            state.error_message = f"MyAgent failed: {str(e)}"
            return state

# Node function for LangGraph
def my_agent_node(state: FileState, config: GraphConfig) -> FileState:
    agent = MyAgent(config)
    return agent.invoke(state)
```

### 2. Adding Language Support

**Current:** C# only (`.cs` files)

**To add Python support:**

1. Update `ProcessingConfig` in `core.py`:
   ```python
   supported_languages: list[str] = Field(
       default=["csharp", "python"]
   )
   ```

2. Update prompts to handle Python syntax:
   - `prompts/file_summarizer.md`: Add Python examples
   - `prompts/detailing_agent.md`: Python method signatures
   - `prompts/relationship_mapper.md`: Python import patterns

3. Update CLI file pattern matching:
   ```python
   # In cli.py
   if lang == "python":
       files = list(input_path.rglob("*.py"))
   elif lang == "csharp":
       files = list(input_path.rglob("*.cs"))
   ```

4. Update state models if needed (e.g., Python-specific metadata)

### 3. Testing Strategy

**Unit Tests:**
```python
# tests/unit/test_file_summarizer_agent.py
def test_summarizer_agent(sample_csharp_file):
    config = GraphConfig(summarizer_model="codellama:7b")
    agent = FileSummarizerAgent(config)
    state = FileState(file_path=sample_csharp_file, file_content=...)
    result = agent.invoke(state)

    assert result.layer1_summary is not None
    assert len(result.layer1_summary.summary) > 50
    assert result.error_message is None
```

**Integration Tests:**
```python
# tests/integration/test_orchestrator.py
def test_full_pipeline(sample_directory):
    orchestrator = create_orchestrator()
    results = orchestrator.process_directory(sample_directory)

    assert len(results) > 0
    for state in results.values():
        assert state.layer3_relationships is not None
```

**Test Data:**
- Store sample C# files in `data/sample_codebase/`
- Include edge cases (empty files, large files, complex inheritance)

### 4. Performance Optimization

**Current bottlenecks:**
1. **LLM latency:** Layer 2 (detailing) is slowest (~30s per file with 13B model)
2. **Sequential processing:** Layers are sequential (can't parallelize per-file)
3. **Memory:** Large models require significant RAM

**Optimization strategies:**

**1. Parallel file processing:**
```yaml
processing:
  parallel_files: 8  # Increase for multi-core systems
```

**2. Model selection:**
```yaml
models:
  summarizer: "qwen3:1.7b"      # Faster (7B → 1.7B)
  detailing: "codellama:13b"    # Keep quality here
  relationship_mapper: "qwen3:1.7b"  # Faster
```

**3. Cloud APIs for speed:**
```yaml
llm:
  base_url: "https://openrouter.ai/api/v1"
  api_key_env: "OPENROUTER_API_KEY"

models:
  summarizer: "meta-llama/llama-3.1-8b-instruct"  # Fast cloud model
  detailing: "anthropic/claude-3-5-sonnet"        # High quality
```

**4. Incremental processing (planned):**
- Track file hashes in SQLite DB
- Only re-process changed files
- Reuse existing layer outputs

**5. Batch requests (future):**
- Group multiple files in single LLM request
- Requires prompt engineering and output parsing changes

### 5. Customizing Validation Rules

**Location:** `prompts/validation_layer*.md`

**Example customization (stricter Layer 2 validation):**

```markdown
# Layer 2 Validation Prompt

You are validating detailed documentation for a C# file.

**Validation Criteria:**

1. **Completeness:**
   - ALL public methods must be documented (STRICT)
   - Private methods must be documented if complex (>10 lines)
   - Constructor documentation required

2. **Quality:**
   - Method descriptions must explain WHY, not just WHAT
   - Parameter descriptions required for all params
   - Return value descriptions required for non-void methods

3. **Accuracy:**
   - Method signatures must match source code exactly
   - Parameter types must be correct

**Output JSON:**
{
  "passed": boolean,
  "issues": ["specific issue 1", "issue 2", ...],
  "refinement_instructions": "How to fix the issues"
}

Respond with valid JSON only.
```

**Then adjust thresholds in config.yaml:**
```yaml
validation:
  max_iterations: 5  # More attempts for stricter validation
  require_all_public_methods: true
```

### 6. Prompt Engineering Best Practices

**Effective prompt structure for agents:**

```markdown
# Role Definition
You are a C# code analysis expert...

# Task Description
Your task is to analyze the following C# file and extract...

# Input Format
You will receive:
- File name: <name>
- File path: <path>
- Source code: <code>

# Output Schema
Respond with JSON matching this schema:
{
  "field1": "description",
  "field2": ["list", "of", "items"]
}

# Quality Guidelines
- Be concise (2-4 sentences for summaries)
- Focus on high-level purpose, not implementation details
- Identify key classes and their responsibilities

# Examples
<example input and output>

# Special Instructions
- Ignore generated code (auto-generated comments)
- Focus on business logic
- Identify design patterns
```

**Key principles:**
- Clear role assignment
- Specific task definition
- Explicit output schema
- Quality guidelines
- Examples (especially for complex tasks)
- Edge case handling

## Troubleshooting

### Common Issues

**1. Ollama connection errors**
```
Error: Ollama is not running
```
**Solution:**
```bash
ollama serve
ollama pull codellama:7b  # Ensure models exist
ollama list  # Verify models
```

**2. API key errors (cloud providers)**
```
ValueError: API key environment variable 'OPENROUTER_API_KEY' is not set
```
**Solution:**
```bash
# Create .env file
echo "OPENROUTER_API_KEY=your-key-here" > .env

# Or export directly
export OPENROUTER_API_KEY=your-key-here
```

**3. Out of memory errors**
```
Killed (OOM)
```
**Solution:**
```yaml
# Reduce parallelism in config.yaml
processing:
  parallel_files: 2  # Down from 4

# Or use smaller models
models:
  detailing: "codellama:7b"  # Down from 13b
```

**4. Timeout errors**
```
Request timed out after 300s
```
**Solution:**
```yaml
llm:
  timeout: 600  # Increase to 10 minutes
```

**5. Validation failures (all files flagged)**
```
⚠ Flagged for review: 50/50 files
```
**Solution:**
```yaml
# Relax validation in config.yaml
validation:
  max_iterations: 5  # More attempts
  min_summary_length: 30  # Lower threshold

# Or review prompts/validation_layer*.md
# Validation may be too strict
```

**6. Empty or malformed JSON output**
```
Error: Expecting value: line 1 column 1 (char 0)
```
**Solution:**
- Check model compatibility (some models don't support structured output well)
- Try different model (Claude, GPT-4 are most reliable)
- Review prompt clarity (ambiguous prompts → inconsistent JSON)

### Debug Workflow

**1. Enable verbose logging:**
```bash
docugen document -c config.yaml -i /path/to/code -v
```

**2. Test individual layers:**
```bash
# Isolate the failing layer
docugen test layer1 -c config.yaml -i failing_file.cs -v
```

**3. Check prompt rendering:**
```python
# In agent code, add debug logging
logger.debug(f"System prompt:\n{self.system_prompt}")
logger.debug(f"User message:\n{user_message}")
```

**4. Inspect intermediate state:**
```python
# After pipeline run
if state.error_message:
    logger.error(f"Error: {state.error_message}")
    logger.error(f"Last layer: {state.current_layer}")
    logger.error(f"L1 iterations: {state.layer1_iterations}")
```

**5. Test LLM connection:**
```bash
docugen test-connection -c config.yaml
```

### Performance Benchmarks

**Expected throughput (8-core, 16GB RAM, local Ollama):**
- Layer 1 (7B model): ~10 files/minute
- Layer 2 (13B model): ~2 files/minute (bottleneck)
- Layer 3 (7B model): ~8 files/minute
- **Overall:** ~100 files/hour

**Scaling recommendations:**
- <100 files: Default settings (`parallel_files: 4`)
- 100-1000 files: Reduce to `parallel_files: 2`, use smaller models
- 1000-5000 files: Cloud APIs (faster inference), batch processing
- 5000+ files: Incremental processing (only changed files)

## Extension Points

### 1. Custom Output Formats

**Current:** Markdown only

**To add HTML output:**

1. Create `writers/html_writer.py`:
   ```python
   def generate_html(layer1_data, layer2_data, layer3_data) -> str:
       # Convert JSON to HTML
       ...
   ```

2. Update `DocumentationAgent` to support HTML templates

3. Add format option to config:
   ```yaml
   output:
     format: "html"  # or "markdown"
   ```

### 2. Additional Validation Strategies

**Implement custom validators:**

```python
# In validation_agent.py

def validate_architecture_patterns(state: FileState) -> ValidationResult:
    """Validate architectural consistency (e.g., no repository calling services)."""
    issues = []

    role = state.layer3_relationships.architectural_role
    dependencies = state.layer3_relationships.dependencies

    # Rule: Repositories shouldn't depend on Services
    if "Repository" in role:
        for dep in dependencies:
            if "Service" in dep.file:
                issues.append(f"Repository depends on Service: {dep.file}")

    return ValidationResult(
        passed=len(issues) == 0,
        issues=issues
    )
```

### 3. Incremental Processing Implementation

**Strategy:**

1. Track file hashes in SQLite:
   ```python
   # state_tracker.py
   class FileStateTracker:
       def __init__(self, db_path: Path):
           self.conn = sqlite3.connect(db_path)
           self._create_schema()

       def has_changed(self, file_path: Path) -> bool:
           current_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
           stored_hash = self._get_stored_hash(file_path)
           return current_hash != stored_hash
   ```

2. Skip unchanged files in orchestrator:
   ```python
   def process_directory(self, directory: Path, incremental: bool = True):
       tracker = FileStateTracker(directory / ".docugen.db")
       files = [f for f in directory.rglob("*.cs") if tracker.has_changed(f)]
       # Process only changed files
   ```

### 4. Multi-Language Support

**Roadmap:**
- ✅ C# (implemented)
- ⏳ Java (planned)
- ⏳ Python (planned)
- ⏳ JavaScript/TypeScript (planned)

**Implementation checklist per language:**
- [ ] File pattern matching (e.g., `*.java`)
- [ ] Prompt updates (syntax examples, conventions)
- [ ] State model updates (language-specific metadata)
- [ ] Test data (sample files)
- [ ] Validation rules (language-specific quality checks)

## Project Structure

```
ai-dev-environment/
├── config.yaml                       # Main configuration (gitignored in production)
├── .env.example                      # Environment variable template
├── pyproject.toml                    # Project metadata and dependencies
├── README.md                         # Project overview
│
├── src/modules/docugen/              # Main package
│   ├── __init__.py
│   ├── cli.py                        # Click CLI (entry point)
│   ├── core.py                       # Configuration models + utilities
│   ├── state.py                      # Pydantic state models
│   ├── orchestrator.py               # LangGraph orchestration
│   ├── logger.py                     # Loguru configuration
│   │
│   ├── agents/                       # Five agent implementations
│   │   ├── __init__.py
│   │   ├── file_summarizer_agent.py     # Layer 1
│   │   ├── detailing_agent.py           # Layer 2
│   │   ├── relationship_mapper_agent.py # Layer 3
│   │   ├── validation_agent.py          # Validation for all layers
│   │   └── documentation_agent.py       # Layer 4 (synthesis)
│   │
│   ├── writers/                      # Output generation
│   │   ├── __init__.py
│   │   └── json_writer.py            # JSON serialization
│   │
│   ├── prompts/                      # External prompt templates
│   │   ├── file_summarizer.md
│   │   ├── detailing_agent.md
│   │   ├── relationship_mapper.md
│   │   ├── documentation_agent.md
│   │   ├── validation_layer1.md
│   │   ├── validation_layer2.md
│   │   └── validation_layer3.md
│   │
│   ├── config/
│   │   └── config.example.yaml       # Configuration template
│   │
│   ├── tests/                        # Module-level tests
│   │   ├── test_cli.py
│   │   └── test_core.py
│   │
│   └── README.md                     # Module documentation
│
├── tests/                            # Project-level tests
│   ├── unit/
│   │   ├── test_file_summarizer_agent.py
│   │   ├── test_detailing_agent.py
│   │   ├── test_relationship_mapper_agent.py
│   │   ├── test_validation_agent.py
│   │   └── test_output_generation.py
│   │
│   └── integration/
│       └── test_orchestrator.py
│
├── data/                             # Test data
│   └── sample_codebase/
│       └── RepoScribe-master/        # Sample C# project
│
├── docs_output/                      # Generated documentation (gitignored)
│   ├── layer1_summaries.json
│   ├── layer2_details.json
│   ├── layer3_relationships.json
│   └── DOCUMENTATION.md
│
└── ai-docs/                          # Project documentation
    ├── 0-brainstorming/
    ├── 1-prd/
    ├── 2-specs/
    └── 3-resources/
        └── langgraph/                # LangGraph documentation
```

## Key Files Reference

| File | Purpose | Key Functions/Classes |
|------|---------|----------------------|
| `cli.py` | CLI entry point | `main()`, `document()`, `test_layer{1,2,3}()`, `test_connection()` |
| `core.py` | Configuration | `DocuGenConfig`, `create_chat_model()`, `validate_config_path()` |
| `state.py` | State models | `FileState`, `GraphConfig`, `FileSummary`, `DetailedDocs`, `RelationshipMap` |
| `orchestrator.py` | LangGraph orchestration | `DocuGenOrchestrator`, `create_orchestrator()`, `process_directory()` |
| `agents/file_summarizer_agent.py` | Layer 1 agent | `FileSummarizerAgent`, `summarize_file()` |
| `agents/detailing_agent.py` | Layer 2 agent | `DetailingAgent`, `generate_details()` |
| `agents/relationship_mapper_agent.py` | Layer 3 agent | `RelationshipMapperAgent`, `map_relationships()` |
| `agents/validation_agent.py` | Validation logic | `validate_layer{1,2,3}()` |
| `agents/documentation_agent.py` | Final synthesis | `DocumentationAgent`, `invoke()` |
| `writers/json_writer.py` | JSON output | `save_layer_outputs()`, `serialize_file_state()` |

## Next Steps for Development

### Short-term (v0.5.0)
- [ ] Implement `status` command (job monitoring)
- [ ] Implement `resume` command (interrupted job recovery)
- [ ] Add progress bar for batch processing
- [ ] Improve error messages with actionable suggestions

### Medium-term (v0.6.0)
- [ ] Incremental processing (track file hashes)
- [ ] Java language support
- [ ] Python language support
- [ ] HTML output format
- [ ] Custom validation rules API

### Long-term (v1.0.0)
- [ ] Web UI (Streamlit or Gradio)
- [ ] Batch LLM requests (multiple files per request)
- [ ] Distributed processing (Celery or Ray)
- [ ] Real-time file watching (auto-regenerate on changes)
- [ ] TypeScript/JavaScript support
- [ ] Plugin system for custom agents

## License

MIT License - See LICENSE file for details

---

**Generated with DocuGen v0.4.0**
**Last Updated:** 2025-10-20
