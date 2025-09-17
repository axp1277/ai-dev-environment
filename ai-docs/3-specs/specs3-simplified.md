# Multi-Timeframe Level Detector with License Management - Technical Specification

## Vision

Create a Rust-based multi-timeframe level detector with simple license management that enables secure distribution of trading indicators. The system uses Rust for computational processing and allows integration with Python for visualization and C# for NinjaScript strategies.

### Objectives
- Build multi-timeframe level detection algorithm in Rust
- Implement simple license management with function-level access control
- Create compiled libraries (DLL) for Python and C# integration
- Develop CLI tool for license key management
- Establish modular architecture for adding indicators
- Support future cloud database migration

### Success Metrics
- Compile Rust indicators into DLL format
- Integrate with Python for Plotly chart visualization
- Implement working license verification with SQLite database
- Create functional CLI for license management
- Demonstrate multi-language compatibility (Python, C#)

## Tasks

⏳ Task 1.0: Database Schema Implementation
* ⏳ 1.1: Create SQLite database with three tables (functions, licenses, license_function_map)
* ⏳ 1.2: Define functions table (id, name) for indicator function names
* ⏳ 1.3: Define licenses table (id, key, tier) for license keys and optional tiers
* ⏳ 1.4: Define license_function_map table (license_id, function_id) for associations
* ⏳ 1.5: Implement basic database initialization functions

⏳ Task 2.0: License Checker Module
* ⏳ 2.1: Create license_checker.rs module with rusqlite connectivity
* ⏳ 2.2: Implement check_license function accepting function_name parameter
* ⏳ 2.3: Create database query to verify function access permissions
* ⏳ 2.4: Add basic error handling for invalid licenses
* ⏳ 2.5: Support both tier-based and individual function licenses

⏳ Task 3.0: Global Configuration
* ⏳ 3.1: Create config.rs module for license key storage
* ⏳ 3.2: Implement global license key access pattern
* ⏳ 3.3: Design configuration loading from compiled sources

⏳ Task 4.0: Indicator Functions
* ⏳ 4.1: Define standard signature (ohlc_data: &[Ohlc], index: usize)
* ⏳ 4.2: Create OHLC data structure
* ⏳ 4.3: Implement bullish_imbalance function with license checking
* ⏳ 4.4: Implement bearish_imbalance function with license checking
* ⏳ 4.5: Create order_block functions (bullish and bearish)
* ⏳ 4.6: Return Boolean results for indicator conditions

⏳ Task 5.0: CLI License Management
* ⏳ 5.1: Create separate Rust binary for CLI tool
* ⏳ 5.2: Implement "lk new" command for generating license keys
* ⏳ 5.3: Implement "lk add-function" command for adding functions
* ⏳ 5.4: Implement "lk remove" command for removing keys/functions
* ⏳ 5.5: Implement "lk list" command for viewing mappings
* ⏳ 5.6: Support tier-based license creation

⏳ Task 6.0: Multi-Language Integration
* ⏳ 6.1: Configure Rust project for DLL compilation
* ⏳ 6.2: Create Python bindings for indicator functions
* ⏳ 6.3: Create C-compatible exports for NinjaScript integration
* ⏳ 6.4: Test DLL generation and function calling

⏳ Task 7.0: Modular Architecture
* ⏳ 7.1: Create indicators directory structure
* ⏳ 7.2: Organize functions in separate files (imbalance.rs, order_block.rs)
* ⏳ 7.3: Establish consistent license_checker imports
* ⏳ 7.4: Create template for adding new indicators

⏳ Task 8.0: Python Integration
* ⏳ 8.1: Create Python module to read JSON output from Rust
* ⏳ 8.2: Implement Plotly candlestick chart rendering
* ⏳ 8.3: Add indicator overlay functionality on charts
* ⏳ 8.4: Define JSON format for indicator results

⏳ Task 9.0: Cloud Migration Preparation
* ⏳ 9.1: Design cloud database schema matching SQLite
* ⏳ 9.2: Create database abstraction for local vs cloud
* ⏳ 9.3: Add configuration for cloud license validation

## Development Guidelines

### Basic Requirements
1. Use Rust standard practices with cargo fmt and clippy
2. Implement basic error handling with Result types
3. Use rusqlite for SQLite database operations
4. Keep license keys secure in compiled binaries
5. Use consistent function naming across languages

### Database Operations
1. Use rusqlite with prepared statements
2. Simple table structure with basic queries
3. Handle database connection errors gracefully

### CLI Tool Usage
- Install: `cargo install --path ./license-cli`
- Create license: `lk new --tier tier1`
- Add function: `lk add-function order_block`
- Associate: `lk associate tier1 order_block`

### Function Structure
Each indicator function:
1. Accepts OHLC data vector and current index
2. Calls check_license("function_name") at start
3. Returns Result<bool, &str> for indicator condition
4. Keeps license checking logic separate from indicator logic

```rust
// Example indicator function
pub fn bullish_imbalance(ohlc_data: &[Ohlc], index: usize) -> Result<bool, &str> {
    check_license("bullish_imbalance")?;
    // Indicator logic here
    Ok(true)
}
```

### Integration Pattern
1. Rust functions compiled to DLL
2. Python imports DLL and calls functions
3. Results output as JSON for Python processing
4. Python renders charts with Plotly
5. C# uses P/Invoke for NinjaScript integration

This simplified specification focuses on the core requirements discussed in the brainstorming session without unnecessary complexity or features that weren't requested.