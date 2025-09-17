# Product Requirements Document

## Executive Summary
This project aims to develop a high-performance multi-timeframe level detector algorithm implemented in Rust, featuring a sophisticated license management system for controlled distribution to multiple clients. The solution addresses the critical business problem of code duplication across programming languages while enabling secure, tiered access to proprietary trading algorithms.

## Vision Statement
Create a unified, cross-platform algorithmic trading framework that eliminates code duplication while providing granular license control for intellectual property protection and monetization.

## Objectives
- Eliminate code duplication by consolidating trading algorithm logic into a single Rust codebase
- Enable cross-language compatibility (Python, C#, native Rust) through compiled libraries
- Implement granular license management for tiered access control to proprietary functions
- Maximize performance through Rust's speed advantages for intensive data processing
- Maintain intellectual property protection through compiled binary distribution
- Streamline client delivery workflow for freelance development services

## Target Users
- **Freelance Developer (Primary User)**: Needs to serve multiple clients with different technical requirements and licensing needs while minimizing code maintenance overhead
- **Trading Algorithm Clients**: Require access to specific trading indicators and algorithms based on their subscription tier or individual function licensing
- **Multi-Platform Users**: Need to integrate trading algorithms across different environments (Python for visualization, C# for NinjaTrader, native Rust for performance)

## Key Features

### Core Features (Must-Have)
1. **Multi-Timeframe Level Detection Algorithm**: Core Rust implementation for analyzing candlestick data and extracting trading levels with high performance
2. **Cross-Language Compatibility**: Compile Rust code to DLL format for C# integration and Python module for seamless cross-platform usage
3. **License-Based Function Access Control**: Runtime license validation system that controls access to specific algorithm functions without requiring recompilation
4. **SQLite-Based License Management Database**: Local database storage for license keys, function mappings, and tier associations with cloud migration capability
5. **CLI License Management Tool**: Command-line interface for creating, managing, and associating license keys with specific functions or tiers

### Secondary Features (Should-Have)
1. **Tier-Based Licensing System**: Support for both individual function licenses and tier-based access (e.g., "tier1" granting access to multiple functions)
2. **Centralized Configuration Management**: Global license key configuration to eliminate the need for passing license keys to individual functions
3. **Function Name Mapping System**: Automatic mapping between function names and license requirements for streamlined protection
4. **Database Migration Utilities**: Tools to migrate from local SQLite to cloud-based database solutions
5. **Error Handling and Validation**: Comprehensive error messages for license violations and invalid access attempts

### Future Features (Could-Have)
1. **Cloud-Based License Validation**: Real-time license checking against cloud database for dynamic access control
2. **License Analytics and Usage Tracking**: Monitor function usage patterns and license utilization across clients
3. **Automated License Expiration Management**: Time-based license control with automatic expiration handling
4. **Web-Based License Management Interface**: GUI alternative to CLI for non-technical license management
5. **Advanced Encryption for License Keys**: Enhanced security measures for license key generation and validation

## Technical Considerations
- **Primary Language**: Rust for core algorithm implementation and performance optimization
- **Database**: SQLite for local development with PostgreSQL/MySQL migration path for cloud deployment
- **Cross-Platform Compilation**: DLL generation for C# integration, Python module creation via PyO3
- **CLI Framework**: Rust-based command-line interface using standard argument parsing libraries
- **Database Connectivity**: rusqlite for SQLite operations with future support for cloud database drivers
- **Modular Architecture**: Separate .rs files for different indicators to maintain code organization and extensibility

## Success Criteria
- **Code Duplication Elimination**: Achieve single-source-of-truth for all trading algorithm logic across languages
- **Performance Benchmark**: Rust implementation demonstrates measurable performance improvement over Python equivalents
- **License Control Effectiveness**: 100% of protected functions require valid license validation before execution
- **Cross-Platform Compatibility**: Successful integration with Python (Plotly visualization) and C# (NinjaTrader strategies)
- **Development Efficiency**: Reduce client-specific development time by minimum 60% through code reuse
- **Intellectual Property Protection**: Zero exposure of source code in distributed binaries

## Out of Scope
- **Real-time Trading Execution**: Focus on algorithm development and licensing, not trade execution systems
- **Market Data Feed Integration**: Assumes external data sources provide OHLC data streams
- **User Interface Development**: CLI-only approach, no graphical user interfaces for end users
- **Performance Optimization Beyond Rust**: No additional performance tuning beyond native Rust capabilities
- **Multi-User License Server**: Single-developer license management, not enterprise multi-user systems

## Dependencies
- **Rust Ecosystem**: Access to rusqlite, PyO3, and CLI development crates
- **Development Environment**: Rust compiler with cross-compilation capabilities for target platforms
- **Client Integration Requirements**: Ability to consume DLLs in C# and Python modules in target environments
- **Database Infrastructure**: SQLite for development with optional cloud database for production deployment
- **Algorithm Knowledge Transfer**: Existing algorithm logic and trading expertise to guide Rust implementation

## Database Schema Requirements
- **Functions Table**: Store algorithm function names with unique identifiers
- **Licenses Table**: Manage license keys with optional tier associations
- **License-Function Mapping Table**: Many-to-many relationship between licenses and accessible functions
- **Migration Support**: Schema designed for easy cloud database migration

## CLI Command Structure
- **License Creation**: `lk new` command for generating new license keys with tier or function-specific associations
- **Function Management**: Commands to add, remove, and list available algorithm functions
- **Association Management**: Tools to link license keys with specific functions or tiers
- **Database Operations**: Utilities for database maintenance and migration preparation

## Security and Intellectual Property Protection
- **Compiled Binary Distribution**: All algorithm logic compiled into non-readable binary format
- **Runtime License Validation**: No hardcoded access control, all validation performed at execution time
- **Secure License Storage**: License mappings compiled into binary to prevent external configuration file exposure
- **Function Name Obfuscation**: Internal function name mapping to prevent reverse engineering attempts