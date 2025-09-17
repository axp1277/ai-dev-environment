# Multi-Timeframe Level Detector with License Management - Technical Specification

## Vision

Build a Rust-based multi-timeframe level detector with license management that enables secure distribution of proprietary trading indicators. The system uses Rust for computational processing with Python for visualization and C# integration for NinjaTrader strategies.

### Objectives
- Implement multi-timeframe level detection algorithm in Rust
- Create license management system with function-level access control
- Enable cross-language integration through compiled DLL
- Build CLI tool for license key management
- Support local SQLite database
- Maintain code reusability across Python, C#, and Rust

### Success Metrics
- Compile Rust indicators into DLL format
- Implement license verification with SQLite backend
- Achieve Python integration with Plotly visualization
- Demonstrate C# compatibility for NinjaTrader integration
- Create functional CLI for license management
- Validate licensing with individual function access controls

## Tasks

⏳ Task 1.0: Core Database Schema
* ⏳ 1.1: Create SQLite database with three tables: functions, licenses, license_function_map
* ⏳ 1.2: Define functions table (id PRIMARY KEY, name TEXT UNIQUE)
* ⏳ 1.3: Define licenses table (id PRIMARY KEY, key TEXT UNIQUE, tier TEXT)
* ⏳ 1.4: Define license_function_map table (license_id INTEGER, function_id INTEGER, FOREIGN KEYS)

⏳ Task 2.0: License Checker Module
* ⏳ 2.1: Create license_checker.rs module with rusqlite connectivity
* ⏳ 2.2: Implement check_license function accepting function_name parameter
* ⏳ 2.3: Support tier-based and individual function licensing
* ⏳ 2.4: Basic error handling for invalid licenses

⏳ Task 3.0: Global Configuration
* ⏳ 3.1: Create config.rs module for license key storage
* ⏳ 3.2: Implement global license key access using lazy_static

⏳ Task 4.0: OHLC Data Structure
* ⏳ 4.1: Define basic OHLC data structure (open, high, low, close)
* ⏳ 4.2: Create JSON serialization for output

⏳ Task 5.0: Indicator Functions
* ⏳ 5.1: Define standard function signature (ohlc_data: &[Ohlc], index: usize) -> Result<bool, &str>
* ⏳ 5.2: Implement bullish_imbalance indicator with license verification
* ⏳ 5.3: Implement bearish_imbalance indicator with license verification
* ⏳ 5.4: Create order_block indicators (bullish and bearish)

⏳ Task 6.0: CLI License Management
* ⏳ 6.1: Create separate Rust binary for CLI tool
* ⏳ 6.2: Implement "lk new" command for generating license keys
* ⏳ 6.3: Implement "lk add-function" command for registering functions
* ⏳ 6.4: Implement "lk remove" command for removing licenses/functions
* ⏳ 6.5: Implement "lk list" command for viewing mappings
* ⏳ 6.6: Implement "lk associate" command for linking licenses to functions

⏳ Task 7.0: Multi-Language Integration
* ⏳ 7.1: Configure Rust project for DLL compilation
* ⏳ 7.2: Create Python bindings using PyO3
* ⏳ 7.3: Implement C-compatible exports for C# P/Invoke
* ⏳ 7.4: JSON-based data exchange format

⏳ Task 8.0: Code Organization
* ⏳ 8.1: Create indicators directory structure (indicators/imbalance.rs, indicators/order_block.rs)
* ⏳ 8.2: Establish license_checker imports across modules

⏳ Task 9.0: Python Visualization
* ⏳ 9.1: Create Python module for reading JSON output
* ⏳ 9.2: Implement Plotly candlestick chart rendering
* ⏳ 9.3: Add indicator overlay functionality

## Development Conventions

### Code Quality
1. Follow Rust best practices using cargo fmt and clippy
2. Use Result types for error handling
3. Keep functions modular and short
4. Use descriptive variable and function names

### Dependencies
- Rust: rusqlite for SQLite, clap for CLI, PyO3 for Python bindings
- Python: plotly for charts, json for data exchange
- Database: SQLite 3.x

### Environment Setup
- Rust: Latest stable toolchain
- Python: 3.8+ for visualization
- SQLite: Local database file

### CLI Tool Usage Examples
```bash
# Create new license
lk new

# Add function
lk add-function order_block

# Associate license with function
lk associate license_key order_block

# List all licenses and functions
lk list

# Remove license or function
lk remove license_key
```

### Indicator Function Template
```rust
use crate::license_checker::check_license;

pub fn bullish_imbalance(ohlc_data: &[Ohlc], index: usize) -> Result<bool, &str> {
    check_license("bullish_imbalance")?;

    if index >= ohlc_data.len() || index < 1 {
        return Err("Invalid index");
    }

    let current = &ohlc_data[index];
    let previous = &ohlc_data[index - 1];

    // Simple gap detection logic
    Ok(current.low > previous.high)
}
```

This specification captures the core requirements discussed in the brainstorming session: multi-timeframe level detector in Rust, license management with SQLite, CLI tool, Python visualization, and C# integration.