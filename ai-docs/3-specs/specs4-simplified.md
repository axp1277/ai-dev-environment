# Vision
Ship a Pine Script v5 indicator that lets futures traders define a trade (entry, stop, target) and immediately see the resulting risk, reward, and visual trade box, with optional scale-in and scale-out helpers that respect the original risk profile.

## Objectives
- Group user inputs so contract sizing, price levels, and optional templates (Fib entry, scaling) can be toggled independently.
- Compute per-contract and total P&L using tick size, tick value, and contract size for both long and short trades.
- Offer scale-in and scale-out calculations that never exceed the starting risk and show how reward-to-risk shifts.
- Draw a box plus labeled lines for stop, entry, and target so traders can read prices, % moves, and P&L at a glance.

## Success Metrics
- Switching between fixed contracts and risk-% sizing keeps the calculated max loss within 1 tick of the expected value.
- Enabling scaling modules updates blended entry/stop math while reported max risk stays ≤ baseline risk.
- Visual overlays remain accurate when trade direction flips or input values change mid-session.

# Tasks
=4 Task 1.0: Configure user inputs
* =4 1.1: Build contract size group with dropdown for `Fixed contracts` vs `Risk % of capital`, validating both inputs.
* =4 1.2: Add standard entry/stop/target group with enable toggle and automatic long/short detection from price order.
* =4 1.3: Provide Fib-entry template group with editable 0.66% and 0.33% offsets plus a reward-to-risk default of 2R.

=4 Task 2.0: Calculate baseline risk and reward
* =4 2.1: Normalize tick size/value and compute per-contract risk, reward, and R-multiples for the configured trade.
* =4 2.2: Output total P&L and percentage move figures tied to stop and target levels for the active sizing mode.

=4 Task 3.0: Model scaling scenarios within the same risk budget
* =4 3.1: Derive scale-in level from the percent risk reduction input and recalc blended entry and position size.
* =4 3.2: Implement scale-out at 1R with break-even stop shift and update remaining position metrics.
* =4 3.3: Ensure scaling toggles refresh displayed R-multiples and P&L without altering baseline numbers when off.

=4 Task 4.0: Render chart visuals
* =4 4.1: Draw rectangle plus stop/entry/target lines that orient correctly for long versus short trades.
* =4 4.2: Attach labels to each line showing price, % move from entry, and corresponding P&L.
* =4 4.3: Indicate scale-in/out trigger levels when enabled so traders can see planned adjustment points.

# Development Conventions

## Pine Script Practices
1. Target Pine Script v5 overlay mode and group related inputs with the `group` argument for clarity.
2. Keep risk math in helper functions so scale scenarios reuse the same calculations.
3. Use instrument tick metadata when available; allow manual overrides only if a symbol lacks values.
4. Update drawings on the latest bar (`barstate.islast`) to avoid stale labels when inputs change.

## Risk & Scaling Notes
1. Validate that entry lies between stop and target; show warnings instead of computing inverted trades.
2. Clamp risk-% inputs to sensible bounds (e.g., 0.1%–10%) to prevent accidental oversized exposure.
3. Display scale-derived metrics only when the relevant toggle is on to avoid misleading numbers.
