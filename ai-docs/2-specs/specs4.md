# Vision
Create a TradingView (Pine Script v5) indicator that models futures trades end to end: position sizing, baseline risk/reward math, and scaling scenarios (in and out) while rendering a clear on-chart visualization of entry, stop, and target performance.

## Objectives
- Provide modular input groups so traders can toggle between fixed contracts, percentage-of-capital sizing, manual price entries, and Fib-derived entry templates.
- Calculate per-contract and total P&L, risk, reward, and R-multiples using tick size, tick value, and contract size for any futures symbol.
- Model scale-in and scale-out behaviors that keep cumulative risk at or below the initial exposure while highlighting reward impact.
- Draw an intuitive trade box with labeled lines (price, % move, P&L) that auto-adjusts for long or short orientation and respects scaling events.

## Success Metrics
- Users can switch sizing modes and see the same initial risk reproduced numerically and visually within ±1 tick.
- Scale-in and scale-out toggles update combined P&L math without exceeding the configured max risk.
- Visual overlays remain accurate when price levels invert (short trades) or when inputs change intrabar.

# Tasks
=4 Task 1.0: Build input groups for trade configuration
* =4 1.1: Implement contract size group with dropdown for `Fixed contracts` vs `Risk % of capital`, persisting both inputs with validation.
* =4 1.2: Add standard entry/stop/target group that infers long/short from price ordering and supports enable/disable behavior.
* =4 1.3: Create Fib-extension entry group with editable 0.66 and 0.33 offsets plus configurable reward-to-risk defaulting to 2R.

=4 Task 2.0: Implement core risk & reward engine
* =4 2.1: Normalize tick size/value and compute per-contract and aggregated P&L for entry, stop, and target points.
* =4 2.2: Derive R-multiple, reward-to-risk ratio, and percentage move metrics for baseline trade scenarios.
* =4 2.3: Surface a summary panel/table showing contract count, capital at risk, and projected reward totals.

=4 Task 3.0: Add scaling scenarios without exceeding initial risk
* =4 3.1: Calculate scale-in price level(s) from percent risk reduction input and recompute blended average entry and risk.
* =4 3.2: Model scale-out at 1R with break-even stop relocation and adjust remaining position metrics.
* =4 3.3: Reflect scaling impacts in displayed P&L, R-multiples, and summary data when toggles are enabled.

=4 Task 4.0: Render on-chart visualization
* =4 4.1: Draw trade rectangle and horizontal lines for stop, entry, and target that reorient for long vs short setups.
* =4 4.2: Attach labels including price, % move from entry, and P&L (reward or risk) at each key level.
* =4 4.3: Highlight scale-in/out trigger levels and ensure graphics respect indicator bar index updates.

=4 Task 5.0: Harden usability and documentation
* =4 5.1: Add guardrails for invalid inputs (e.g., entry between stop/target, capital percentage bounds) with user-facing warnings.
* =4 5.2: Document sizing assumptions and scaling math inside the script header for trader reference.
* =4 5.3: Smoke-test against both long and short scenarios and note findings in QA checklist.

# Development Conventions

## Pine Script Standards
1. Target Pine Script v5 with `indicator()` setup configured for overlay visuals and inline grouping of inputs via the `group` parameter.
2. Encapsulate pricing math in pure functions (e.g., `calcRiskReward`) and keep state mutations minimal.
3. Derive instrument metadata (`syminfo.mintick`, currency) but fall back to user overrides when needed.
4. Only emit drawings/labels on confirmed data (e.g., `barstate.islast`) unless live bar updates are expressly required.

## Risk Math & UX
1. Use consistent rounding: tick-aligned for price outputs, currency-formatted for P&L.
2. Keep risk comparisons in base currency; display percent-of-capital when the corresponding sizing mode is active.
3. When scaling toggles are disabled, ensure baseline metrics remain unaffected and labels hide derived levels.
4. Annotate complex calculations briefly so downstream agents can follow the reasoning without re-deriving formulas.

## Testing Expectations
1. Validate indicator on at least two symbols with different tick values (e.g., ES, NQ) and both long/short cases.
2. Confirm risk cap is respected when combining scale-in contracts with original position size.
3. Verify that toggling between sizing modes or entry templates updates visuals and summaries without requiring reload.
