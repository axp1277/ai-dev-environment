# Futures Reward-to-Risk Indicator - Product Requirements Document

## Executive Summary
Active futures traders currently stitch together spreadsheets, broker calculators, and chart annotations to understand their risk/reward profile for a trade. This process is slow, error-prone, and makes it difficult to evaluate how scaling in or out of a position changes exposure.

The Futures Reward-to-Risk Indicator streamlines this workflow inside TradingView. Traders configure contract sizing, entry/stop/target levels, and optional Fibonacci-based entries, then immediately see calculated risk, reward, and R-multiples. Optional scale-in and scale-out modules show how adjustments affect outcomes while keeping total risk within the original budget. A chart overlay draws the trade box and labels to make the plan obvious at a glance.

## Document Version
- Version: 1.0
- Date: 2025-09-17
- Source Session: session4.md

## Problem Statement

### Current State
- Traders calculate risk/reward manually or in external tools, breaking focus from the chart.
- Determining contract size based on fixed lots versus percentage of capital requires separate math.
- Scaling scenarios are rarely explored because recomputing blended entries and risk is tedious.

### Desired State
- Traders describe a potential trade directly inside TradingView and instantly see risk and reward metrics.
- Contract sizing, scaling, and entry templates can be toggled without rebuilding the entire setup.
- Visual cues on the chart communicate the trade box and adjustment levels for rapid decision making.

### Value Proposition
- Reduces calculation time and errors by centralizing risk math in one indicator.
- Encourages disciplined risk management by enforcing that scaling actions never exceed initial exposure.
- Improves situational awareness with clear on-chart annotations tied to the configured trade.

## Target Users

### Primary User Personas
1. **Active Futures Trader**
   - Role: Individual day or swing trader using futures contracts.
   - Goals: Size positions accurately, plan exits, and maintain consistent reward-to-risk ratios.
   - Pain Points: Manual calculators, misaligned contract sizing, difficulty modeling scaling actions.
   - Success Criteria: Trustworthy on-chart metrics that match manual calculations and update instantly.

2. **Trading Coach / Mentor**
   - Role: Guides traders on risk management best practices.
   - Goals: Provide repeatable frameworks for sizing trades and scaling decisions.
   - Pain Points: Coaching often relies on static examples that traders fail to apply in real time.
   - Success Criteria: Indicator that communicates structure clearly and reinforces adherence to the plan.

### Use Cases
1. **Plan Baseline Trade**
   - Actor: Active Futures Trader
   - Scenario: Inputs entry, stop, target, and contract-size mode to view risk/reward metrics.
   - Expected Outcome: Receives per-contract and total P&L, R-multiple, and visual trade box.

2. **Evaluate Scale-In Opportunity**
   - Actor: Active Futures Trader
   - Scenario: Enables scale-in module, sets percent risk reduction, and reviews new blended entry level.
   - Expected Outcome: Sees updated reward figure while overall risk stays within the original budget.

3. **Lock in Gains with Scale-Out**
   - Actor: Active Futures Trader
   - Scenario: Activates scale-out at 1R to move stop to break-even and partially close position.
   - Expected Outcome: Indicator displays revised position metrics and the new protective stop level.

## Requirements

### Functional Requirements
1. **Input Configuration**
   - FR1.1: Provide dropdown for contract sizing mode (`Fixed contracts`, `Risk % of capital`) with corresponding inputs.
   - FR1.2: Offer toggleable standard entry/stop/target group that auto-detects long vs short from price order.
   - FR1.3: Supply Fibonacci entry template with adjustable 0.33% and 0.66% offsets and a default 2R ratio.

2. **Risk & Reward Calculations**
   - FR2.1: Calculate per-contract risk, reward, and R-multiples using tick size, tick value, and contract size.
   - FR2.2: Summarize total P&L, percent moves, and capital-at-risk for the active sizing mode.

3. **Scaling Modules**
   - FR3.1: Scale-in logic derives the additional entry price from percent risk reduction while keeping risk ≤ baseline.
   - FR3.2: Scale-out module triggers at 1R, shifts stop to break-even, and recomputes remaining position metrics.

4. **Visualization**
   - FR4.1: Draw trade rectangle with labeled stop, entry, and target lines showing price, % move, and P&L.
   - FR4.2: Indicate scale-in/out trigger levels on the chart when modules are enabled.

### Non-Functional Requirements
1. **Performance**
   - Indicator updates risk calculations and drawings without noticeable lag on real-time bars.

2. **Usability**
   - Inputs are grouped with clear labels; invalid configurations generate human-readable warnings.

3. **Compatibility**
   - Works on TradingView Pine Script v5 across common futures symbols; respects tick size per instrument.

4. **Maintainability**
   - Core calculations are encapsulated to simplify future mode additions.

## Scope & Constraints

### In Scope
- Manual entry/stop/target configuration with auto direction detection.
- Contract sizing via fixed contracts or risk percentage of capital.
- Fibonacci-based entry suggestions with configurable offsets.
- Scale-in and scale-out modules that keep risk at or below the initial exposure.
- Chart overlays for trade box and scaling levels, including price/P&L labels.

### Out of Scope
- Automated order placement or broker integration.
- Multiple simultaneous trade plans on one chart.
- Advanced scaling strategies beyond single scale-in and single scale-out templates.

### Constraints
- TradingView settings panes are static; inputs for unused modes remain visible even when the mode is inactive.
- Accurate risk math requires correct tick value/tick size information, which may vary by instrument.
- Pine Script label limits restrict the number of concurrent annotations per bar.

## Success Metrics

### Key Performance Indicators (KPIs)
1. Risk calculations match manual spreadsheet results within 1 tick difference in back-testing samples.
2. ≥80% of beta users report improved clarity around scaling decisions during simulated trades.

### Acceptance Criteria
1. Enabling each module (standard, Fib, scale-in, scale-out) updates displayed metrics without requiring indicator reload.
2. Visual trade box correctly reorients for short trades (target below entry) with accurate labels.

## Dependencies & Risks

### Dependencies
- TradingView Pine Script v5 environment and overlay rendering capabilities.
- Accurate instrument metadata (`syminfo.mintick`, tick value) from TradingView data.

### Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Users misunderstand static input groups | Medium | Medium | Provide inline descriptions and default values clarifying when to use each mode. |
| Tick value discrepancies across brokers | Medium | High | Allow manual override inputs and document verification steps. |
| Pine label limits exceeded on lower timeframes | Low | Medium | Reuse labels where possible and gate optional drawings behind toggles. |

## Timeline & Phases

### Proposed Phases
**Phase 1: Core Indicator (2 weeks)**
- Deliver contract sizing, standard entry/stop/target group, baseline risk calculations, and trade box visualization.
- Validate calculations against sample trades and document usage instructions.

**Phase 2: Scaling Enhancements (2 weeks)**
- Implement Fib-entry template, scale-in, and scale-out modules with updated metrics and visuals.
- Conduct user dry runs to confirm risk cap adherence and adjust messaging.

### Milestones
- Week 1: Contract sizing + baseline risk engine completed.
- Week 2: Trade box visualization and QA sign-off for Phase 1.
- Week 3: Scaling modules implemented.
- Week 4: Final validation, documentation, and beta release.
