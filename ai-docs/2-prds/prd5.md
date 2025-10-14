# London Session Profile Study - Product Requirements Document

## Executive Summary

The London Session Profile Study is a statistical analysis tool for TradingView that quantifies the probability of London session highs and lows being reached during New York trading sessions. The tool builds upon an existing TradingView indicator that visualizes London and New York sessions as boxes on charts, extending it with comprehensive statistical analysis capabilities. By analyzing where price closes within the London session (divided into four 25% percentile quadrants) and incorporating conditional filters like VWAP bias, traders can make data-driven decisions about target probability during specific New York time windows. The study will leverage an existing Statistical Frequency Engine library (PineScript) to compute and display these probabilities, providing traders with quantifiable insights into intraday trading opportunities.

## Document Version
- Version: 1.0
- Date: 2025-10-13
- Source Session: session5.md

## Problem Statement

### Current State
Traders currently use session-based indicators that visualize London and New York trading sessions but lack quantitative data on the probability of London session targets (highs/lows) being reached during New York sessions. While the visual session boxes provide temporal context, traders must rely on subjective experience or manual backtesting to estimate whether London extremes will be challenged during New York trading hours. This creates uncertainty in target setting and trade management decisions.

### Desired State
Traders should have access to statistical probability data that quantifies the likelihood of London highs or lows being reached during specific New York time windows, conditional on:
- Which quadrant (0-25%, 25-50%, 50-75%, 75-100%) of the London session range price closed at
- The time of day during the New York session (AM vs PM session)
- Optional filters such as VWAP bias (above/below VWAP anchored at New York midnight)

This probabilistic approach transforms subjective guesswork into data-driven decision making.

### Value Proposition
By providing quantifiable probability metrics for London high/low target achievement during New York sessions, traders can:
- Set realistic profit targets based on statistical likelihood
- Filter trading opportunities based on probability thresholds
- Understand how starting quadrant position affects target probability
- Incorporate bias filters (VWAP) to refine conditional probabilities
- Make more informed decisions about trade entry, exit, and position sizing

## Target Users

### Primary User Personas

1. **Intraday Futures Trader**
   - Role: Day trader focusing on ES, NQ, and other futures contracts
   - Goals: Identify high-probability setups during New York session based on London session structure
   - Pain Points: Difficulty quantifying when London targets will be reached; uncertainty about optimal entry timing
   - Success Criteria: Ability to view probability percentages for London high/low raids during specific NY time windows based on quadrant positioning

2. **Systematic Strategy Developer**
   - Role: Quantitative trader building algorithmic trading systems
   - Goals: Incorporate session-based probability statistics into automated trading strategies
   - Pain Points: Lack of historical probability data for London/NY session relationships; manual backtesting is time-consuming
   - Success Criteria: Access to statistical frequency data that can be programmatically queried and used in strategy logic

3. **Market Structure Analyst**
   - Role: Technical analyst studying intraday market behavior patterns
   - Goals: Understand and document how price behaves across different session transitions
   - Pain Points: Need quantitative evidence to support session-based analysis theories
   - Success Criteria: Statistical data showing probability distributions across different quadrant starting positions and time windows

### Use Cases

1. **Morning Session Trade Planning**
   - Actor: Intraday Futures Trader
   - Scenario: At 8:00 AM EST (London close/NY open), trader observes price closed in the top 75-100% quadrant of London session range and wants to know probability of London low being raided during NY AM session
   - Expected Outcome: Study displays historical probability percentage (e.g., "65% probability London low raided when starting from top quadrant during NY AM session")

2. **VWAP Bias Filtering**
   - Actor: Systematic Strategy Developer
   - Scenario: Developer wants to filter trade signals to only take setups when price is below VWAP (anchored at NY midnight) and starting from bottom 0-25% quadrant, targeting London high raid
   - Expected Outcome: Study provides conditional probability statistics filtered by VWAP position (e.g., "42% probability when below VWAP vs 68% when above VWAP")

3. **Time-Based Target Windows**
   - Actor: Intraday Futures Trader
   - Scenario: Trader wants to know if London high is more likely to be hit during NY AM session (8AM-12PM) or NY PM session (12PM-4PM)
   - Expected Outcome: Study provides time-windowed probability data showing different likelihood across AM vs PM sessions

## Requirements

### Functional Requirements

1. **Session Definition and Configuration**
   - FR1.1: System shall allow configurable session time ranges:
     - London Session: Default 1:00 AM - 8:00 AM EST (configurable)
     - New York AM Session: Default 8:00 AM - 12:00 PM EST (configurable)
     - New York PM Session: Default 12:00 PM - 4:00 PM EST (configurable)
   - FR1.2: System shall persist session configuration settings across chart reloads

2. **Quadrant Calculation**
   - FR2.1: System shall divide London session range into four equal 25% percentile quadrants:
     - Quadrant 1: 0-25% (bottom quartile)
     - Quadrant 2: 25-50% (lower-middle quartile)
     - Quadrant 3: 50-75% (upper-middle quartile)
     - Quadrant 4: 75-100% (top quartile)
   - FR2.2: System shall determine which quadrant price closed in at London session close (8:00 AM default)
   - FR2.3: System shall calculate London session high and low for each trading day

3. **Probability Computation**
   - FR3.1: System shall compute probability of London high being raided during NY AM session for each starting quadrant
   - FR3.2: System shall compute probability of London low being raided during NY AM session for each starting quadrant
   - FR3.3: System shall compute probability of London high being raided during NY PM session for each starting quadrant
   - FR3.4: System shall compute probability of London low being raided during NY PM session for each starting quadrant
   - FR3.5: System shall use Statistical Frequency Engine library to maintain running statistics

4. **VWAP Bias Filter**
   - FR4.1: System shall calculate VWAP anchored at New York midnight open
   - FR4.2: System shall provide toggle to enable/disable VWAP filter
   - FR4.3: When VWAP filter enabled, system shall compute separate conditional probabilities for:
     - Price above VWAP at NY open
     - Price below VWAP at NY open
   - FR4.4: System shall display both filtered and unfiltered probabilities when filter is active

5. **Time-Based Target Windows**
   - FR5.1: System shall allow users to enable/disable time window filters
   - FR5.2: When enabled, system shall limit probability calculations to only include days where target was hit within specified time window
   - FR5.3: System shall support separate windows for NY AM session (8-12) and NY PM session (12-4)

6. **Statistical Frequency Engine Integration**
   - FR6.1: System shall import and utilize existing Statistical Frequency Engine PineScript library
   - FR6.2: System shall follow implementation patterns from reference scripts using the Statistical Frequency Engine
   - FR6.3: System shall maintain historical frequency counts for all probability calculations

7. **Visualization and Display**
   - FR7.1: System shall display probability percentages as text labels on chart
   - FR7.2: System shall show current quadrant position
   - FR7.3: System shall display relevant probabilities based on active filters
   - FR7.4: System shall provide clear indication of which filters are currently active

### Non-Functional Requirements

1. **Performance**
   - NFR1.1: Statistical calculations shall complete within TradingView PineScript execution time limits
   - NFR1.2: Historical data processing shall not cause script timeouts on charts with 1+ years of data
   - NFR1.3: Real-time probability updates shall occur within 1 bar of session close

2. **Usability**
   - NFR2.1: Filter toggles shall be easily accessible in TradingView indicator settings
   - NFR2.2: Probability displays shall be clearly readable without cluttering chart
   - NFR2.3: Session time configurations shall use standard EST time format
   - NFR2.4: Documentation shall include clear examples of how to interpret probability values

3. **Reliability**
   - NFR3.1: System shall handle missing data gracefully (gaps, holidays)
   - NFR3.2: Probability calculations shall be mathematically correct and verifiable
   - NFR3.3: System shall maintain accurate counts even after chart reloads

4. **Maintainability**
   - NFR4.1: Code shall follow PineScript best practices and naming conventions
   - NFR4.2: Statistical logic shall be modular and reusable
   - NFR4.3: Reference implementation shall be documented for future modifications

## Scope & Constraints

### In Scope
- London Session Profile statistical analysis for NY trading sessions
- Quadrant-based probability calculations (4 quadrants)
- VWAP bias conditional filtering
- Time-based target window filtering (NY AM vs NY PM)
- Integration with existing Statistical Frequency Engine library
- Basic visualization of probabilities on chart
- Configuration of session time ranges

### Out of Scope
- Analysis of other session pairs (Asian/London, etc.)
- Real-time alerting or notifications
- Integration with automated trading execution systems
- Mobile app or standalone application (TradingView platform only)
- Machine learning or predictive modeling
- Multi-timeframe analysis
- Backtesting framework or strategy automation
- Historical probability chart overlays or heatmaps

### Constraints
- **Technical**:
  - Must work within TradingView PineScript v5 limitations
  - Subject to PineScript execution time and memory constraints
  - Limited to data available through TradingView data feed
  - Must use existing Statistical Frequency Engine library architecture
- **Business**:
  - Requires TradingView Pro/Premium subscription for real-time data
  - Limited to markets with active London and NY session trading
- **Timeline**:
  - Implementation follows AI-assisted development workflow
  - Development will be broken into incremental, testable tasks

## Success Metrics

### Key Performance Indicators (KPIs)

1. **Accuracy**: Probability calculations match manual backtest results within 2% margin of error (verified on sample of 100 trading days)

2. **Completeness**: All four quadrants × two targets (high/low) × two NY sessions (AM/PM) = 16 base probability values successfully computed

3. **Filter Functionality**: VWAP filter produces distinct conditional probabilities that differ from base probabilities by statistically significant margin

4. **Performance**: Script executes without timeout on 252+ trading days of historical data

5. **Usability**: User can configure all session times and enable/disable filters through TradingView settings interface without code modification

### Acceptance Criteria

1. Study successfully imports Statistical Frequency Engine library and follows reference implementation patterns
2. London session range correctly identified with high, low, and four quadrants calculated
3. Probability values display on chart for all 16 base scenarios (4 quadrants × 2 targets × 2 NY sessions)
4. VWAP filter toggle functions correctly and produces conditional probability splits
5. Time window filters correctly limit probability calculations to specified windows
6. Session time ranges are configurable and persist across sessions
7. Documentation includes implementation guide and interpretation examples
8. Code passes review by AI coder with oversight from project owner
9. Manual verification confirms probability calculations match expected statistical frequencies

## Dependencies & Risks

### Dependencies
- **External Systems**:
  - TradingView platform and PineScript v5 runtime
  - Statistical Frequency Engine PineScript library (existing)
  - TradingView real-time and historical data feed

- **Teams**:
  - AI Planner (specification document generation)
  - AI Coder (PineScript implementation with human oversight)

- **Prerequisites**:
  - Statistical Frequency Engine library must be accessible and functional
  - Reference implementation script demonstrating library usage must be available
  - TradingView account with appropriate data access

### Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| PineScript execution timeout on large datasets | Medium | High | Optimize statistical calculations; limit lookback period if necessary; implement incremental processing |
| Statistical Frequency Engine library limitations | Low | High | Review library capabilities early; verify it supports required statistical operations; have fallback custom implementation plan |
| VWAP filter produces non-significant probability differences | Medium | Medium | Accept as valid result if no statistical edge exists; document findings; consider alternative bias filters |
| Session time configuration doesn't account for DST changes | Medium | Low | Document DST handling requirements; provide user guidance on manual adjustments; consider automatic DST handling if feasible |
| Insufficient historical data to compute reliable probabilities | Low | Medium | Define minimum sample size requirements (e.g., 100 days); display confidence intervals or sample size alongside probabilities |
| Chart clutter from displaying too many probability values | Medium | Low | Implement selective display options; allow users to choose which probabilities to show; use compact formatting |
| Integration complexity with existing session indicator | Low | Medium | Build as standalone study initially; document integration steps as optional enhancement |
| AI implementation deviates from specification | Medium | Medium | Human oversight at each task completion; incremental review and testing; clear specification document with examples |

## Implementation Approach

### Development Workflow
The implementation will follow an AI-assisted development workflow:
1. **Brainstorming** (Complete): Session 5 captures requirements and approach
2. **PRD Generation** (Current): Formal product requirements documentation
3. **Specification Planning**: AI Planner converts PRD to detailed technical specification with numbered tasks
4. **Implementation**: AI Coder implements specification incrementally with human oversight
5. **Testing & Validation**: Manual verification of probability calculations and functionality

### Phased Delivery
- **Phase 1**: Core functionality (session detection, quadrant calculation, basic probability computation)
- **Phase 2**: VWAP filter implementation
- **Phase 3**: Time-based target window filters
- **Phase 4**: Visualization optimization and configuration options

### Reference Materials
- Existing TradingView session indicator (London/NY boxes visualization)
- Statistical Frequency Engine PineScript library
- Reference script demonstrating Statistical Frequency Engine usage
- PineScript v5 documentation and best practices
