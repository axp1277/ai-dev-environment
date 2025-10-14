---
Session: 5
Created: 2025-10-13
Inputs:
  - Brainstorming: session5.md
  - PRD: prd5.md
  - User Stories: stories-5.md
  - Specs: specs-5.md
Test Coverage Goal: 90%
Status: Draft
---

# London Session Profile Study - Validation and Acceptance Criteria

## Testing Overview

### Test Strategy

**Approach**: Mixed (Manual + Automated where feasible)
**Platform**: TradingView PineScript v5
**Primary Validation Method**: Manual verification with chart visualization and statistical comparison

**Coverage Goals**:
- Core Functionality: 100% (all 30 tasks validated)
- Unit-Level Logic: 90% (individual functions tested)
- Integration Testing: 100% (library integration validated)
- End-to-End Scenarios: 95% (user workflows validated)

### Test Environments

- **Development**: TradingView chart with indicator applied, 1-year historical data (ES futures)
- **Validation**: Multiple instruments (ES, NQ, CL) across different timeframes (1m, 5m, 15m, 1h)
- **Production**: TradingView public library after passing all validation

### Test Data Requirements

- Historical intraday price data: Minimum 252 trading days (1 year)
- Multiple instruments: ES, NQ, CL for cross-validation
- Various timeframes: 1-minute, 5-minute, 15-minute, 1-hour bars
- Coverage of different market conditions: Trending, ranging, volatile
- Inclusion of edge cases: Gaps, holidays, DST transitions, zero-range sessions

### Testing Tools

- **TradingView Platform**: Primary testing environment
- **PineScript Debugger**: Built-in plot and label functions for validation
- **Manual Calculation**: Spreadsheet for probability verification
- **Statistical Frequency Engine**: Library used for frequency counting
- **Reference Implementation**: Existing script demonstrating library usage

---

# Feature 1: Session Configuration and Detection

**Feature Description**: Configurable session times for London, NY AM, and NY PM sessions with automatic detection logic
**Related User Stories**: Story 1.1 (Configure Session Times), Story 1.2 (View Current Session Status)
**Related Specs**: Task 2.0 (Session Time Configuration), Task 3.0 (Session Detection Logic)
**Priority**: Critical

## Test Scenario 1.1: Configure Default Session Times

**Objective**: Verify default session times are correctly set and editable
**Preconditions**:
- Indicator is loaded on TradingView chart
- Settings panel is accessible

**Test Steps**:
1. Open indicator settings
2. Navigate to "Session Configuration" group
3. Verify default values are displayed
4. Note each session time input

**Expected Results**:
- ✓ London Session: 01:00-08:00 EST (default)
- ✓ NY AM Session: 08:00-12:00 EST (default)
- ✓ NY PM Session: 12:00-16:00 EST (default)
- ✓ All inputs accept time format "HHMM-0000"
- ✓ Settings persist after chart reload

**Acceptance Criteria**:
- [ ] Given I open settings, when I view Session Configuration, then London start is "0100-0000" and end is "0800-0000"
- [ ] Given I open settings, when I view Session Configuration, then NY AM start is "0800-0000" and end is "1200-0000"
- [ ] Given I open settings, when I view Session Configuration, then NY PM start is "1200-0000" and end is "1600-0000"
- [ ] Given I change session times, when I reload chart, then custom times persist

**Test Type**: Manual
**Automation**: No
**Priority**: Critical (P0)

---

## Test Scenario 1.2: Modify Session Times

**Objective**: Verify custom session times are accepted and applied correctly
**Preconditions**:
- Indicator is loaded on chart
- Settings panel is open

**Test Steps**:
1. Change London session to 02:00-09:00 EST
2. Change NY AM session to 09:00-13:00 EST
3. Change NY PM session to 13:00-17:00 EST
4. Save settings
5. Observe session detection on chart

**Expected Results**:
- ✓ Custom times are accepted without error
- ✓ Session detection adjusts to new times
- ✓ "London Session Active" label appears during 02:00-09:00
- ✓ "NY AM Session Active" label appears during 09:00-13:00
- ✓ "NY PM Session Active" label appears during 13:00-17:00

**Acceptance Criteria**:
- [ ] Given I set custom times, when I save settings, then no error messages appear
- [ ] Given custom London time is 02:00-09:00, when chart time is 03:00, then "London Session Active" displays
- [ ] Given custom NY AM time is 09:00-13:00, when chart time is 10:00, then "NY AM Session Active" displays
- [ ] Given custom times are saved, when I switch timeframes, then custom times remain applied

**Test Type**: Manual/Integration
**Automation**: No
**Priority**: High (P1)

---

## Test Scenario 1.3: Session Detection Accuracy

**Objective**: Verify session detection functions correctly identify active sessions
**Preconditions**:
- Indicator loaded with default session times
- Chart showing intraday data across multiple sessions

**Test Steps**:
1. Navigate to bar at 03:00 AM EST
2. Check session status indicator
3. Navigate to bar at 10:00 AM EST
4. Check session status indicator
5. Navigate to bar at 14:00 PM EST
6. Check session status indicator
7. Navigate to bar at 18:00 PM EST
8. Check session status indicator

**Expected Results**:
- ✓ At 03:00 AM: "London Session Active"
- ✓ At 10:00 AM: "NY AM Session Active"
- ✓ At 14:00 PM: "NY PM Session Active"
- ✓ At 18:00 PM: "No Active Session"
- ✓ Session transitions are accurate to the minute

**Acceptance Criteria**:
- [ ] Given chart time is within London session (01:00-08:00), when I check status, then I see "London Session Active"
- [ ] Given chart time is within NY AM (08:00-12:00), when I check status, then I see "NY AM Session Active"
- [ ] Given chart time is within NY PM (12:00-16:00), when I check status, then I see "NY PM Session Active"
- [ ] Given chart time is outside all sessions, when I check status, then I see "No Active Session"
- [ ] Given session transition occurs (e.g., 08:00), when bar closes, then status updates immediately

**Test Type**: Integration
**Automation**: Partial (via debug plots)
**Priority**: Critical (P0)

---

## Test Scenario 1.4: Invalid Session Time Handling

**Objective**: Verify system validates and handles invalid session time inputs
**Preconditions**:
- Indicator settings panel is open

**Test Steps**:
1. Attempt to set London end time before London start time
2. Attempt to set NY AM start before London end
3. Attempt to set invalid time format (e.g., "2500-0000")
4. Observe error handling

**Expected Results**:
- ✓ System prevents illogical time ordering
- ✓ Error message displays on chart: "Invalid session times: Check configuration"
- ✓ Invalid format inputs are rejected or corrected
- ✓ Indicator does not execute with invalid configuration

**Acceptance Criteria**:
- [ ] Given London end < London start, when I apply settings, then error message displays
- [ ] Given NY AM start < London end, when I apply settings, then error message displays
- [ ] Given invalid time format, when I save, then PineScript rejects input or displays error
- [ ] Given invalid configuration, when indicator runs, then chart shows error label clearly

**Test Type**: Manual/Validation
**Automation**: No
**Priority**: Medium (P2)

---

# Feature 2: London Session Tracking and Quadrant Calculation

**Feature Description**: Track London session high/low and calculate four 25% percentile quadrants
**Related User Stories**: Story 2.1 (View London Session Quadrants), Story 2.2/2.3 (View Probabilities)
**Related Specs**: Task 4.0 (London High/Low Tracking), Task 5.0 (Quadrant Division)
**Priority**: Critical

## Test Scenario 2.1: London Session High/Low Tracking

**Objective**: Verify London session high and low are correctly identified and locked at session close
**Preconditions**:
- Indicator loaded on chart with intraday data
- London session is complete (past 08:00 AM)

**Test Steps**:
1. Identify a completed London session on chart
2. Manually note the highest and lowest prices during 01:00-08:00
3. Check indicator's displayed London high and low values
4. Verify values remain locked throughout NY sessions

**Expected Results**:
- ✓ London high matches observed highest price during 01:00-08:00
- ✓ London low matches observed lowest price during 01:00-08:00
- ✓ Values are locked at 08:00 and don't change during NY sessions
- ✓ London high and low are visually marked on chart with horizontal lines

**Acceptance Criteria**:
- [ ] Given London session ended at 08:00, when I check London high, then it matches the highest price between 01:00-08:00
- [ ] Given London session ended at 08:00, when I check London low, then it matches the lowest price between 01:00-08:00
- [ ] Given London session closed, when NY session is active, then London high/low values do not change
- [ ] Given I observe chart, when London session completes, then horizontal lines mark London high and low

**Test Type**: Manual/Visual
**Automation**: Partial (via plot verification)
**Priority**: Critical (P0)

---

## Test Scenario 2.2: Quadrant Boundary Calculation

**Objective**: Verify quadrant boundaries are correctly calculated at 25%, 50%, 75%
**Preconditions**:
- Indicator loaded on chart
- London session is complete with identifiable high/low

**Test Steps**:
1. Note London high and low (e.g., High=4200, Low=4180)
2. Calculate expected quadrant boundaries manually:
   - Range = 4200 - 4180 = 20
   - Q1 upper = 4180 + (20 * 0.25) = 4185
   - Q2 upper = 4180 + (20 * 0.50) = 4190
   - Q3 upper = 4180 + (20 * 0.75) = 4195
   - Q4 upper = 4200
3. Check indicator's displayed quadrant lines
4. Compare with manual calculations

**Expected Results**:
- ✓ Q1 boundary line at 4185 (25% level)
- ✓ Q2 boundary line at 4190 (50% level)
- ✓ Q3 boundary line at 4195 (75% level)
- ✓ Q4 boundary at London high (4200)
- ✓ All boundaries calculated accurately to 2 decimal places

**Acceptance Criteria**:
- [ ] Given London range is 20 points, when I check Q1 upper boundary, then it is London low + 5 points (25%)
- [ ] Given London range is 20 points, when I check Q2 upper boundary, then it is London low + 10 points (50%)
- [ ] Given London range is 20 points, when I check Q3 upper boundary, then it is London low + 15 points (75%)
- [ ] Given I manually calculate boundaries, when I compare to indicator, then values match within 0.01 points

**Test Type**: Manual/Calculation
**Automation**: Partial (via debug output)
**Priority**: Critical (P0)

---

## Test Scenario 2.3: Quadrant Classification at London Close

**Objective**: Verify price is correctly classified into the appropriate quadrant at London close (08:00)
**Preconditions**:
- Indicator loaded on chart
- London session has just closed at 08:00

**Test Steps**:
1. Identify closing price at 08:00 (e.g., 4187)
2. Determine expected quadrant based on boundaries:
   - 4180-4185 = Q1
   - 4185-4190 = Q2
   - 4190-4195 = Q3
   - 4195-4200 = Q4
3. Check indicator's displayed "Starting Quadrant" label
4. Test with multiple sessions covering all 4 quadrants

**Expected Results**:
- ✓ Closing price 4187 classified as Quadrant 2 (25-50%)
- ✓ "Starting Quadrant: Q2 (25-50%)" label displays correctly
- ✓ Quadrant classification is accurate for all test cases
- ✓ Edge case: Exact boundary prices handled consistently (e.g., 4185 classified as Q2)

**Acceptance Criteria**:
- [ ] Given close price is 4187 and Q1 upper is 4185, Q2 upper is 4190, when classified, then Starting Quadrant is Q2
- [ ] Given close price is exactly on boundary (4185), when classified, then consistent rule applies (e.g., belongs to upper quadrant)
- [ ] Given I test 10 different sessions, when I verify each classification, then all are mathematically correct
- [ ] Given quadrant is determined, when I check display, then label shows correct quadrant number and percentage range

**Test Type**: Manual/Calculation
**Automation**: Partial
**Priority**: Critical (P0)

---

## Test Scenario 2.4: Quadrant Visualization

**Objective**: Verify quadrant lines and labels are clearly displayed on chart without clutter
**Preconditions**:
- Indicator loaded with "Show Quadrant Lines" enabled

**Test Steps**:
1. Observe London session quadrant visualization
2. Check that all 4 quadrant boundary lines are visible
3. Check that quadrant labels (Q1, Q2, Q3, Q4) are readable
4. Verify current quadrant is highlighted or distinguished

**Expected Results**:
- ✓ Four horizontal lines mark quadrant boundaries
- ✓ Labels display "Q1 (0-25%)", "Q2 (25-50%)", "Q3 (50-75%)", "Q4 (75-100%)"
- ✓ Current starting quadrant is visually emphasized (bold, color, or marker)
- ✓ Lines persist through NY sessions
- ✓ Visualization is clear and does not obscure price action

**Acceptance Criteria**:
- [ ] Given quadrant lines are enabled, when I view chart, then I see 4 distinct horizontal lines
- [ ] Given I look at quadrant labels, when I read them, then text is clear and properly positioned
- [ ] Given current quadrant is Q3, when I view chart, then Q3 is visually distinguished from others
- [ ] Given multiple sessions on chart, when I scroll, then old quadrant lines are cleaned up appropriately

**Test Type**: Manual/Visual/UX
**Automation**: No
**Priority**: High (P1)

---

## Test Scenario 2.5: Edge Case - Zero Range Session

**Objective**: Verify system handles London sessions where high equals low (zero range)
**Preconditions**:
- Access to historical data with extremely low volatility or flat sessions

**Test Steps**:
1. Identify or simulate a London session where high == low (range = 0)
2. Check indicator behavior
3. Verify error handling

**Expected Results**:
- ✓ Quadrant calculation returns `na` (not applicable)
- ✓ Message displays: "Zero range session - No quadrants"
- ✓ Probabilities display "N/A" or "Insufficient data"
- ✓ Indicator does not crash or show errors
- ✓ Session resumes normal operation on next valid session

**Acceptance Criteria**:
- [ ] Given London high == London low, when quadrants are calculated, then result is `na`
- [ ] Given zero range session, when I view chart, then appropriate error message displays
- [ ] Given zero range occurs, when next valid session appears, then indicator resumes normal operation
- [ ] Given zero range, when probability calculation attempted, then system handles gracefully without errors

**Test Type**: Edge Case/Error Handling
**Automation**: Partial
**Priority**: Medium (P2)

---

# Feature 3: Probability Computation and Display

**Feature Description**: Compute and display probability of London high/low raids during NY AM/PM sessions based on starting quadrant
**Related User Stories**: Story 2.2 (View Probability - London High), Story 2.3 (View Probability - London Low), Story 2.4 (View All Quadrants)
**Related Specs**: Task 9.0 (Frequency Counting), Task 10.0 (Probability Calculation), Task 17-20 (Display)
**Priority**: Critical

## Test Scenario 3.1: Probability Calculation Accuracy

**Objective**: Verify probability calculations are mathematically correct and match manual backtest
**Preconditions**:
- Indicator loaded with at least 100 historical trading days
- Manual backtest completed for sample period (e.g., 100 days)

**Test Steps**:
1. Select specific quadrant/target/session combination (e.g., Q4 -> London Low Raid in NY AM)
2. Manually count occurrences:
   - Total sessions starting from Q4: X
   - Sessions where London low was raided during NY AM: Y
   - Manual probability = (Y / X) * 100%
3. Compare with indicator's displayed probability
4. Repeat for multiple scenarios

**Expected Results**:
- ✓ Indicator probability matches manual calculation within 2% margin of error
- ✓ Sample size (n) displayed matches manual count
- ✓ Success count / total count ratio is correct
- ✓ All 16 base probabilities validated (4 quadrants × 2 targets × 2 sessions)

**Acceptance Criteria**:
- [ ] Given manual calculation shows 65/100 = 65%, when I check indicator, then probability displays between 63-67%
- [ ] Given I manually count 100 sessions starting from Q4, when I check indicator sample size, then n=100 is displayed
- [ ] Given I verify 10 different scenarios, when I compare manual vs indicator, then all are within 2% margin
- [ ] Given I test all 16 base scenarios, when I verify each, then calculations are mathematically correct

**Test Type**: Manual/Calculation/Validation
**Automation**: Partial (via debug logs)
**Priority**: Critical (P0)

---

## Test Scenario 3.2: Sample Size Display

**Objective**: Verify sample size is displayed alongside probability values
**Preconditions**:
- Indicator loaded with historical data
- Probabilities are calculated

**Test Steps**:
1. Observe probability display on chart
2. Check format of probability values
3. Verify sample size is included

**Expected Results**:
- ✓ Probability displayed as "65.4% (n=87)" format
- ✓ Sample size is accurate and matches frequency counter
- ✓ Low sample size (n < 30) has visual warning (yellow color, asterisk)
- ✓ Insufficient data (n < 10) displays "Insufficient data (n=X)" instead of percentage

**Acceptance Criteria**:
- [ ] Given probability is 65.4% with 87 samples, when I view display, then I see "65.4% (n=87)"
- [ ] Given sample size is 25 (< 30), when I view display, then I see yellow color or asterisk warning
- [ ] Given sample size is 8 (< 10), when I view display, then I see "Insufficient data (n=8)" instead of percentage
- [ ] Given I hover over probability, when tooltip appears, then I see detailed breakdown (e.g., "57/87 = 65.5%")

**Test Type**: Manual/Visual
**Automation**: No
**Priority**: High (P1)

---

## Test Scenario 3.3: Raid Detection Accuracy

**Objective**: Verify system correctly identifies when London high/low was raided during NY sessions
**Preconditions**:
- Indicator loaded on chart
- Multiple complete NY sessions visible

**Test Steps**:
1. Identify a NY session where London high was clearly breached
2. Check if indicator counted this as a "raid"
3. Identify a NY session where London high was NOT breached
4. Check if indicator correctly did NOT count this as a raid
5. Test edge cases: exact touches, wicks vs body close

**Expected Results**:
- ✓ Price exceeding London high during NY session is detected as raid
- ✓ Price not reaching London high is not counted as raid
- ✓ Exact touch of London high (price == high) is handled consistently
- ✓ Wicks above/below London levels count as raids (not just body close)
- ✓ Raid detection works for both NY AM and NY PM sessions separately

**Acceptance Criteria**:
- [ ] Given price reaches 4201 and London high is 4200, when NY session ends, then raid is detected
- [ ] Given price reaches 4199 and London high is 4200, when NY session ends, then raid is NOT detected
- [ ] Given price exactly touches 4200 (London high), when NY session ends, then consistent rule applies (e.g., counted as raid)
- [ ] Given wick touches London high but body doesn't, when NY session ends, then raid is detected
- [ ] Given raid occurs at 10:00 AM (NY AM), when I check NY AM probability, then this event is counted in numerator

**Test Type**: Integration/Validation
**Automation**: Partial
**Priority**: Critical (P0)

---

## Test Scenario 3.4: Probability Display Formatting

**Objective**: Verify probabilities are displayed in clear, readable format
**Preconditions**:
- Indicator loaded with sufficient data
- Probabilities calculated for current quadrant

**Test Steps**:
1. Observe probability display layout
2. Check text formatting and positioning
3. Verify color coding if enabled
4. Check that display is not cluttered

**Expected Results**:
- ✓ Display shows current session status
- ✓ Starting quadrant clearly indicated
- ✓ Relevant probabilities displayed:
   - "London High Raid (NY AM): 42.3% (n=87)"
   - "London Low Raid (NY AM): 71.5% (n=87)"
   - "London High Raid (NY PM): 38.1% (n=87)"
   - "London Low Raid (NY PM): 68.2% (n=87)"
- ✓ High probability values (>60%) highlighted in green (if color coding enabled)
- ✓ Display positioned according to user setting (top-left, top-right, etc.)

**Acceptance Criteria**:
- [ ] Given I view probability display, when I read values, then format is consistent "XX.X% (n=YY)"
- [ ] Given color coding is enabled, when probability is >60%, then text is green
- [ ] Given color coding is enabled, when probability is 40-60%, then text is yellow
- [ ] Given color coding is enabled, when probability is <40%, then text is red
- [ ] Given display position is set to "Top Right", when I view chart, then display appears in top right corner

**Test Type**: Manual/Visual/UX
**Automation**: No
**Priority**: High (P1)

---

## Test Scenario 3.5: Multi-Quadrant View

**Objective**: Verify "Show All Quadrants" toggle displays probability table for all 4 quadrants simultaneously
**Preconditions**:
- Indicator loaded with sufficient data for all quadrants
- "Show All Quadrants" setting enabled

**Test Steps**:
1. Enable "Show All Quadrants" in settings
2. Observe probability table display
3. Verify all 16 probability values are shown
4. Check that current quadrant is highlighted

**Expected Results**:
- ✓ Table displays with 4 rows (quadrants) and 4 columns (LH-AM, LL-AM, LH-PM, LL-PM)
- ✓ All 16 probabilities visible and readable
- ✓ Current starting quadrant row is highlighted with distinct background color
- ✓ Sample sizes displayed for each value
- ✓ Table is formatted clearly without overlapping text

**Acceptance Criteria**:
- [ ] Given "Show All Quadrants" is enabled, when I view chart, then I see a table with 4 rows and 4 columns
- [ ] Given I count probability values, when all are visible, then I see exactly 16 values (4 × 2 × 2)
- [ ] Given current quadrant is Q3, when I view table, then Q3 row has distinct background highlighting
- [ ] Given I disable "Show All Quadrants", when I view chart, then only current quadrant probabilities display

**Test Type**: Manual/Visual
**Automation**: No
**Priority**: Medium (P2)

---

# Feature 4: VWAP Bias Filtering

**Feature Description**: Calculate VWAP anchored at NY midnight and provide conditional probabilities based on price position relative to VWAP
**Related User Stories**: Story 3.1 (Enable VWAP Filter), Story 3.2 (View Conditional Probabilities), Story 3.3 (Visualize VWAP)
**Related Specs**: Task 11.0 (VWAP Calculation), Task 12.0 (VWAP Conditional Counters), Task 13.0 (VWAP Visualization)
**Priority**: High

## Test Scenario 4.1: VWAP Calculation Accuracy

**Objective**: Verify VWAP is correctly calculated and anchored at NY midnight
**Preconditions**:
- Indicator loaded on chart
- VWAP filter enabled
- Compare against TradingView built-in VWAP indicator

**Test Steps**:
1. Add TradingView built-in VWAP indicator to chart, anchored at session (daily)
2. Enable VWAP filter in London Profile Study
3. Compare VWAP line from both indicators at various times during NY session
4. Verify they match exactly

**Expected Results**:
- ✓ VWAP values match TradingView built-in VWAP within 0.01 points
- ✓ VWAP resets at NY midnight (00:00 EST)
- ✓ VWAP line plots continuously throughout NY session
- ✓ VWAP calculation uses proper volume-weighted formula: Σ(price × volume) / Σ(volume)

**Acceptance Criteria**:
- [ ] Given I compare at 10:00 AM, when I check both VWAPs, then values match within 0.01 points
- [ ] Given I observe VWAP at 23:59, when clock transitions to 00:00, then VWAP resets
- [ ] Given I manually calculate VWAP for 3 sample bars, when I compare to indicator, then formula is correctly applied
- [ ] Given I test on different instruments (ES, NQ, CL), when I verify VWAP, then calculation is accurate across all

**Test Type**: Integration/Calculation
**Automation**: Partial (via comparison to built-in indicator)
**Priority**: Critical (P0)

---

## Test Scenario 4.2: VWAP Bias Determination

**Objective**: Verify system correctly determines if price is above or below VWAP at NY open (08:00)
**Preconditions**:
- VWAP filter enabled
- VWAP is calculated
- NY session is starting (08:00)

**Test Steps**:
1. At NY open (08:00), note closing price (e.g., 4195)
2. Note VWAP value at 08:00 (e.g., 4190)
3. Check indicator's displayed VWAP bias label
4. Verify bias is correctly identified

**Expected Results**:
- ✓ Price 4195 > VWAP 4190 → Bias: "Above VWAP"
- ✓ Price 4185 < VWAP 4190 → Bias: "Below VWAP"
- ✓ VWAP bias label displays clearly on chart
- ✓ Bias determination is accurate at exact NY open time

**Acceptance Criteria**:
- [ ] Given price is 4195 and VWAP is 4190 at 08:00, when I check bias label, then I see "VWAP Bias: Above"
- [ ] Given price is 4185 and VWAP is 4190 at 08:00, when I check bias label, then I see "VWAP Bias: Below"
- [ ] Given price equals VWAP exactly at 08:00, when I check bias, then consistent rule applies (e.g., "Neutral" or assigned to Above)
- [ ] Given I test across 20 sessions, when I verify each bias determination, then all are correct

**Test Type**: Integration/Validation
**Automation**: Partial
**Priority**: High (P1)

---

## Test Scenario 4.3: Conditional Probability Calculation

**Objective**: Verify VWAP filter produces distinct conditional probabilities
**Preconditions**:
- VWAP filter enabled
- Sufficient historical data (at least 50 samples for each VWAP condition)

**Test Steps**:
1. Enable VWAP filter
2. Observe probability display for specific quadrant/target/session (e.g., Q4 -> London Low in NY AM)
3. Note base probability and VWAP-conditional probabilities
4. Verify probabilities differ

**Expected Results**:
- ✓ Base probability displayed (e.g., "Base: 65%")
- ✓ Above VWAP probability displayed (e.g., "Above VWAP: 72%")
- ✓ Below VWAP probability displayed (e.g., "Below VWAP: 58%")
- ✓ Sample sizes shown for each (e.g., "n=87" for base, "n=45" above, "n=42" below)
- ✓ Conditional probabilities show statistical edge (differ from base by >5%)

**Acceptance Criteria**:
- [ ] Given VWAP filter is enabled, when I view probabilities, then I see three values: Base, Above VWAP, Below VWAP
- [ ] Given Above VWAP probability is 72%, when I compare to Base 65%, then I see 7 percentage point difference
- [ ] Given I check sample sizes, when I add Above (n=45) + Below (n=42), then sum equals Base (n=87)
- [ ] Given I test 5 different scenarios, when I verify conditional probabilities, then at least 3 show >5% difference from base

**Test Type**: Integration/Statistical Validation
**Automation**: Partial
**Priority**: High (P1)

---

## Test Scenario 4.4: VWAP Visualization

**Objective**: Verify VWAP line is clearly plotted on chart when filter is enabled
**Preconditions**:
- VWAP filter enabled
- VWAP customization settings accessible

**Test Steps**:
1. Enable VWAP filter
2. Observe VWAP line on chart
3. Verify it starts at NY midnight
4. Check that line is visible and not cluttered
5. Customize color and width

**Expected Results**:
- ✓ VWAP line plots starting from NY midnight (00:00)
- ✓ Line is continuous throughout NY session
- ✓ Default color is distinct from price (e.g., blue or purple)
- ✓ Line width is appropriate (1-2 pixels)
- ✓ Customization settings work (color, width)
- ✓ Disabling VWAP filter hides the line

**Acceptance Criteria**:
- [ ] Given VWAP filter is enabled, when I view chart, then I see a continuous line from midnight onward
- [ ] Given I change VWAP color to red, when I save settings, then line changes to red
- [ ] Given I change VWAP width to 3, when I save settings, then line becomes thicker
- [ ] Given I disable VWAP filter, when I view chart, then VWAP line is no longer visible

**Test Type**: Manual/Visual/UX
**Automation**: No
**Priority**: Medium (P2)

---

## Test Scenario 4.5: Insufficient VWAP Data Handling

**Objective**: Verify system handles cases where VWAP-filtered sample size is too small
**Preconditions**:
- VWAP filter enabled
- Historical data available but limited for certain VWAP conditions

**Test Steps**:
1. Identify scenario where VWAP-filtered data is insufficient (e.g., only 5 "Above VWAP" samples)
2. Check probability display
3. Verify warning or message appears

**Expected Results**:
- ✓ When Above VWAP n < 10, display "Insufficient data (n=5)" instead of percentage
- ✓ When Below VWAP has sufficient data, that probability still displays
- ✓ Warning message: "VWAP filter: Low sample size for some conditions"
- ✓ Base probability (unfiltered) still displays regardless

**Acceptance Criteria**:
- [ ] Given Above VWAP sample size is 5, when I view probability, then I see "Insufficient data (n=5)"
- [ ] Given Below VWAP sample size is 45, when I view probability, then percentage displays normally (e.g., "58% (n=45)")
- [ ] Given VWAP filter produces insufficient data, when I check display, then warning message appears
- [ ] Given I load more historical data, when sample size exceeds threshold, then percentage displays

**Test Type**: Edge Case/Error Handling
**Automation**: Partial
**Priority**: Medium (P2)

---

# Feature 5: Time-Based Target Window Filtering

**Feature Description**: Filter probability calculations to only include raids that occurred within specified time windows
**Related User Stories**: Story 4.1 (Enable Time Window Filter), Story 4.2 (Compare AM vs PM Probabilities)
**Related Specs**: Task 14.0 (Time Window Configuration), Task 15.0 (Time-Constrained Raid Detection), Task 16.0 (Window-Filtered Display)
**Priority**: Medium

## Test Scenario 5.1: Time Window Configuration

**Objective**: Verify time window filter can be enabled and configured correctly
**Preconditions**:
- Indicator settings panel is open

**Test Steps**:
1. Locate "Enable Time Window Filter" toggle
2. Enable the filter
3. Set custom time window (e.g., 09:30 - 11:00)
4. Save settings
5. Verify configuration is applied

**Expected Results**:
- ✓ Toggle switches on successfully
- ✓ Custom time inputs accept valid time format
- ✓ Start time < End time validation works
- ✓ Settings persist after chart reload
- ✓ Window boundaries display on chart or in label

**Acceptance Criteria**:
- [ ] Given I enable time window filter, when I check toggle, then it shows "Enabled"
- [ ] Given I set window to 09:30-11:00, when I save, then no error messages appear
- [ ] Given I set window start after window end, when I save, then error message displays
- [ ] Given I reload chart, when I check settings, then custom window times persist

**Test Type**: Manual/Configuration
**Automation**: No
**Priority**: Medium (P2)

---

## Test Scenario 5.2: Time-Constrained Raid Detection

**Objective**: Verify system only counts raids that occurred within specified time window
**Preconditions**:
- Time window filter enabled (e.g., 09:00 - 11:00)
- Historical data shows various raid times

**Test Steps**:
1. Identify session where London low was raided at 10:30 (within window)
2. Identify session where London low was raided at 13:00 (outside window)
3. Check probability calculation
4. Verify only in-window raids are counted

**Expected Results**:
- ✓ Raid at 10:30 is counted in numerator
- ✓ Raid at 13:00 is NOT counted
- ✓ Total count (denominator) remains the same
- ✓ Probability is lower than full-session probability
- ✓ Display shows window boundaries: "Window: 09:00 - 11:00"

**Acceptance Criteria**:
- [ ] Given window is 09:00-11:00 and raid at 10:30, when probability calculated, then this raid is counted
- [ ] Given window is 09:00-11:00 and raid at 13:00, when probability calculated, then this raid is NOT counted
- [ ] Given I compare full session prob (65%) vs window prob (52%), when window is enabled, then window probability is displayed
- [ ] Given window filter is active, when I view display, then I see "Window: 09:00-11:00" label

**Test Type**: Integration/Validation
**Automation**: Partial
**Priority**: Medium (P2)

---

## Test Scenario 5.3: AM vs PM Probability Comparison

**Objective**: Verify system displays separate probabilities for NY AM and NY PM sessions correctly
**Preconditions**:
- Sufficient data for both AM and PM sessions
- No time window filter applied (or full session window)

**Test Steps**:
1. Observe probability display for specific quadrant/target
2. Note NY AM probability
3. Note NY PM probability
4. Verify both are displayed and can be compared

**Expected Results**:
- ✓ Both probabilities displayed:
   - "London High Raid (NY AM): 42.3% (n=87)"
   - "London High Raid (NY PM): 38.1% (n=87)"
- ✓ Sample sizes may differ if data varies
- ✓ Probabilities can be compared to identify best time window
- ✓ Display is clear and not cluttered

**Acceptance Criteria**:
- [ ] Given I view probabilities, when I look for NY AM, then I see "NY AM: XX.X% (n=YY)"
- [ ] Given I view probabilities, when I look for NY PM, then I see "NY PM: XX.X% (n=YY)"
- [ ] Given NY AM prob is 42.3% and NY PM is 38.1%, when I compare, then I can clearly see AM has higher probability
- [ ] Given I test 5 different quadrant/target combinations, when I check display, then AM and PM are always separated

**Test Type**: Manual/Visual
**Automation**: No
**Priority**: Medium (P2)

---

# Non-Functional Requirements

## Performance Validation

### Test Scenario NFR-P1: Script Execution Performance

**Objective**: Verify script executes without timeout on large datasets
**Preconditions**:
- Chart loaded with 252+ trading days (1 year of data)

**Test Steps**:
1. Load chart with 1 year of intraday data (1-minute bars)
2. Apply indicator
3. Wait for script to execute
4. Monitor for timeout or errors

**Expected Results**:
- ✓ Script loads successfully without timeout
- ✓ Execution completes within TradingView limits
- ✓ No memory errors occur
- ✓ Probability calculations complete for all scenarios

**Acceptance Criteria**:
- [ ] Given chart has 252 trading days, when I apply indicator, then script executes without timeout error
- [ ] Given I load 5000 bars, when I apply indicator, then script completes execution successfully
- [ ] Given script is running, when I check browser console, then no memory warnings appear
- [ ] Given execution completes, when I check probabilities, then all 16 base values are calculated

**Test Type**: Performance
**Priority**: Critical (P0)

---

### Test Scenario NFR-P2: Real-Time Update Performance

**Objective**: Verify probability updates occur smoothly in real-time
**Preconditions**:
- Indicator applied to live chart
- Market is open

**Test Steps**:
1. Apply indicator to live chart during market hours
2. Observe updates as new bars close
3. Monitor for lag or delays
4. Verify session transitions are smooth

**Expected Results**:
- ✓ Probabilities update within 1 bar close after session end
- ✓ No visible lag or freezing
- ✓ Session status updates immediately at transition times
- ✓ Chart remains responsive

**Acceptance Criteria**:
- [ ] Given NY AM session ends at 12:00, when 12:00 bar closes, then probabilities update within 1 minute
- [ ] Given I interact with chart, when I pan or zoom, then chart remains responsive
- [ ] Given session transitions occur, when I observe updates, then no lag or delay is visible
- [ ] Given real-time updates occur, when I check CPU usage, then indicator doesn't cause excessive load

**Test Type**: Performance/Integration
**Priority**: High (P1)

---

## Security and Data Integrity Validation

### Test Scenario NFR-S1: Data Integrity Across Chart Reloads

**Objective**: Verify frequency counters persist correctly across chart reloads
**Preconditions**:
- Indicator has been running with historical data
- Probabilities calculated

**Test Steps**:
1. Note current probability values and sample sizes
2. Reload chart (F5 or close/reopen)
3. Check probability values after reload
4. Verify they match pre-reload values

**Expected Results**:
- ✓ Probability values identical before and after reload
- ✓ Sample sizes (n) identical before and after reload
- ✓ No data loss occurs
- ✓ Frequency counters maintain accuracy

**Acceptance Criteria**:
- [ ] Given probability is 65.4% (n=87) before reload, when I reload chart, then probability is 65.4% (n=87) after reload
- [ ] Given I reload chart 5 times, when I check probabilities, then values remain consistent
- [ ] Given frequency counters are persisted, when I verify via debug output, then counts match expected historical accumulation
- [ ] Given chart is reloaded, when I check calculation speed, then counters don't need full recalculation (use `var` keyword)

**Test Type**: Data Integrity/Reliability
**Priority**: High (P1)

---

## Usability Validation

### Test Scenario NFR-U1: Settings Accessibility and Clarity

**Objective**: Verify all settings are easily accessible and understandable
**Preconditions**:
- Indicator is applied to chart

**Test Steps**:
1. Open indicator settings
2. Review all input groups and options
3. Check for tooltips and help text
4. Verify organization is logical

**Expected Results**:
- ✓ Settings organized into logical groups (Session Configuration, Filters, Display)
- ✓ Each input has tooltip explaining its purpose
- ✓ Default values are sensible and work out of the box
- ✓ Input labels are clear and unambiguous

**Acceptance Criteria**:
- [ ] Given I open settings, when I view inputs, then they are organized into groups (Session Configuration, Filters, Display)
- [ ] Given I hover over an input, when tooltip appears, then explanation is clear and helpful
- [ ] Given I apply indicator with defaults, when I view chart, then probabilities display without any configuration needed
- [ ] Given I am new user, when I read input labels, then I understand what each setting does without external documentation

**Test Type**: Usability/UX
**Priority**: Medium (P2)

---

### Test Scenario NFR-U2: Error Messages Clarity

**Objective**: Verify error messages are clear and actionable
**Preconditions**:
- Various error conditions can be triggered

**Test Steps**:
1. Trigger invalid session time configuration
2. Trigger insufficient data scenario
3. Trigger zero-range session
4. Check error messages for each

**Expected Results**:
- ✓ Error messages are clear and specific
- ✓ Messages suggest corrective action
- ✓ Errors display prominently on chart
- ✓ No technical jargon or PineScript error codes exposed

**Acceptance Criteria**:
- [ ] Given invalid session times, when error displays, then message says "Invalid session times: Check configuration" (not generic error)
- [ ] Given insufficient data, when warning displays, then message says "Load more historical data" (actionable)
- [ ] Given zero-range session, when message displays, then it says "Zero range session - No quadrants" (clear explanation)
- [ ] Given errors occur, when I read messages, then I understand problem and how to fix it without external help

**Test Type**: Usability/Error Handling
**Priority**: Medium (P2)

---

# Edge Cases and Error Scenarios

## Feature: Session Detection

### Edge Case 1: DST Transitions

**Test**: Verify session detection during Daylight Saving Time transitions
**Expected**: Session times adjust correctly or user is warned to update manually
**Priority**: Medium

**Test Steps**:
1. Test indicator behavior during spring DST transition (clocks forward)
2. Test indicator behavior during fall DST transition (clocks back)
3. Verify session times remain accurate

**Acceptance Criteria**:
- [ ] Given DST transition occurs, when I check session detection, then times are still accurate OR warning message appears
- [ ] Given manual adjustment is needed, when DST occurs, then clear instructions are provided

---

### Edge Case 2: Market Holidays

**Test**: Verify indicator handles market holidays gracefully
**Expected**: No errors, probabilities not calculated for holiday days, indicator resumes normally after holiday
**Priority**: Low

**Test Steps**:
1. Load chart that includes market holiday (e.g., Christmas, Thanksgiving)
2. Verify indicator behavior on holiday
3. Verify indicator resumes normally after holiday

**Acceptance Criteria**:
- [ ] Given chart includes holiday, when indicator runs, then no errors or crashes occur
- [ ] Given it's a holiday, when I check probabilities, then holiday data is excluded from calculations
- [ ] Given market reopens after holiday, when indicator resumes, then normal operation continues

---

## Feature: Probability Calculation

### Error Scenario 1: Insufficient Historical Data

**Trigger**: Apply indicator to chart with less than 10 days of data
**Expected Error Handling**:
- Display: "Insufficient historical data: Load at least 10 days"
- Logging: N/A (PineScript doesn't have logging to external files)
- Recovery: System displays message but doesn't crash; probabilities show "N/A"

**Acceptance Criteria**:
- [ ] Given chart has only 5 days of data, when indicator runs, then message "Insufficient historical data" displays
- [ ] Given insufficient data, when I check probabilities, then they show "N/A" or "Insufficient data"
- [ ] Given I add more data, when chart reloads, then indicator calculates probabilities normally

---

### Error Scenario 2: Missing Volume Data

**Trigger**: Apply indicator to instrument with no volume data (Forex, some indices)
**Expected Error Handling**:
- Display: "VWAP requires volume data: VWAP filter disabled" (if VWAP filter was enabled)
- Recovery: Indicator continues with VWAP filter automatically disabled; base probabilities still work

**Acceptance Criteria**:
- [ ] Given instrument has no volume data and VWAP enabled, when indicator runs, then warning message displays
- [ ] Given VWAP filter is disabled due to missing volume, when I check probabilities, then base probabilities still calculate correctly
- [ ] Given I switch to instrument with volume, when indicator runs, then VWAP filter works normally

---

# Traceability Matrix

| User Story | Technical Spec | Test Scenario | Status |
|------------|----------------|---------------|---------|
| Story 1.1: Configure Session Times | Task 2.0 | TS 1.1, 1.2, 1.4 | ⏳ Pending |
| Story 1.2: View Current Session Status | Task 3.0 | TS 1.3 | ⏳ Pending |
| Story 2.1: View London Quadrants | Task 4.0, 5.0, 6.0 | TS 2.1, 2.2, 2.3, 2.4, 2.5 | ⏳ Pending |
| Story 2.2: View London High Raid Prob | Task 7.0, 8.0, 9.0, 10.0 | TS 3.1, 3.2, 3.3, 3.4 | ⏳ Pending |
| Story 2.3: View London Low Raid Prob | Task 7.0, 8.0, 9.0, 10.0 | TS 3.1, 3.2, 3.3, 3.4 | ⏳ Pending |
| Story 2.4: View All Quadrants | Task 20.0 | TS 3.5 | ⏳ Pending |
| Story 3.1: Enable VWAP Filter | Task 11.0 | TS 4.1 | ⏳ Pending |
| Story 3.2: View Conditional Probabilities | Task 12.0 | TS 4.2, 4.3, 4.5 | ⏳ Pending |
| Story 3.3: Visualize VWAP | Task 13.0 | TS 4.4 | ⏳ Pending |
| Story 4.1: Enable Time Window Filter | Task 14.0 | TS 5.1 | ⏳ Pending |
| Story 4.2: Compare AM vs PM | Task 15.0, 16.0 | TS 5.2, 5.3 | ⏳ Pending |
| Story 5.1: View Sample Size | Task 19.0 | TS 3.2 | ⏳ Pending |
| Story 5.2: Handle Insufficient Data | Task 19.0 | TS 3.2, 4.5 | ⏳ Pending |
| Story 5.3: Verify Accuracy | Task 25.0 | TS 3.1 | ⏳ Pending |
| Story 6.1: Customize Display | Task 21.0 | TS 3.4, 4.4 | ⏳ Pending |

**Coverage**: 15 user stories mapped to 30 technical tasks validated by 25+ test scenarios

---

# Test Execution Summary

**Test Run Date**: Not yet executed
**Environment**: TradingView Development
**Build Version**: v1.0.0 (not yet implemented)

| Feature | Total Tests | Passed | Failed | Blocked | Pass Rate |
|---------|-------------|--------|--------|---------|-----------|
| Session Configuration | 4 | 0 | 0 | 0 | N/A |
| London Tracking & Quadrants | 5 | 0 | 0 | 0 | N/A |
| Probability Computation | 5 | 0 | 0 | 0 | N/A |
| VWAP Filtering | 5 | 0 | 0 | 0 | N/A |
| Time Window Filtering | 3 | 0 | 0 | 0 | N/A |
| Non-Functional (Performance) | 2 | 0 | 0 | 0 | N/A |
| Non-Functional (Usability) | 2 | 0 | 0 | 0 | N/A |
| Edge Cases | 2 | 0 | 0 | 0 | N/A |

**Overall Pass Rate**: 0% (Not yet executed)
**Total Test Scenarios**: 28
**Critical Priority Tests**: 10
**High Priority Tests**: 8
**Medium Priority Tests**: 10

---

# Testing Recommendations

## Priority Order for Testing

1. **Phase 1 - Core Functionality (P0 Tests)**:
   - Session detection accuracy (TS 1.3)
   - London high/low tracking (TS 2.1)
   - Quadrant calculation accuracy (TS 2.2, 2.3)
   - Probability calculation accuracy (TS 3.1)
   - Raid detection accuracy (TS 3.3)
   - VWAP calculation accuracy (TS 4.1)
   - Script execution performance (NFR-P1)

2. **Phase 2 - User Features (P1 Tests)**:
   - Session configuration (TS 1.1, 1.2)
   - Quadrant visualization (TS 2.4)
   - Sample size display (TS 3.2)
   - Probability display formatting (TS 3.4)
   - VWAP bias determination (TS 4.2)
   - Conditional probability calculation (TS 4.3)
   - Data integrity (NFR-S1)
   - Real-time performance (NFR-P2)

3. **Phase 3 - Enhanced Features (P2 Tests)**:
   - Time window filtering (TS 5.1, 5.2, 5.3)
   - Multi-quadrant view (TS 3.5)
   - VWAP visualization (TS 4.4)
   - Edge cases (TS 2.5, EC1, EC2)
   - Usability (NFR-U1, NFR-U2)
   - Insufficient data handling (TS 4.5, Error scenarios)

## Acceptance Criteria for Release

**Minimum requirements for v1.0 release**:
- [ ] All Critical (P0) tests pass: 10/10
- [ ] At least 90% of High (P1) tests pass: 7/8 minimum
- [ ] No blocking issues remain unresolved
- [ ] Manual verification confirms probability calculations accurate within 2% margin
- [ ] Script executes without timeout on 1 year of data
- [ ] User documentation complete with usage examples
- [ ] Known limitations documented clearly

**Definition of Done**:
- [ ] All test scenarios in Phase 1 and Phase 2 executed and passed
- [ ] Code review completed by human oversight
- [ ] Statistical accuracy validated against manual backtest
- [ ] Performance validated on large datasets
- [ ] User acceptance testing completed
- [ ] Documentation published
- [ ] Ready for TradingView library publication

---

# Appendix: Manual Verification Procedure

## Probability Calculation Manual Verification

To manually verify probability calculations:

1. **Select Sample Period**: Choose 100 consecutive trading days
2. **For Each Day**:
   - Identify London session high and low
   - Calculate quadrant boundaries
   - Determine closing quadrant at 08:00
   - Track if London high/low was raided during NY AM (08:00-12:00)
   - Track if London high/low was raided during NY PM (12:00-16:00)
3. **Calculate Probabilities**:
   - For Q4 → London Low in NY AM:
     - Count: Days starting from Q4 = X
     - Count: Of those X days, how many had London low raided in NY AM = Y
     - Probability = (Y / X) * 100%
4. **Compare to Indicator**:
   - Indicator probability should be within 2% of manual calculation
   - Sample size should match manual count

**Example Spreadsheet Columns**:
- Date
- London High
- London Low
- London Range
- Close at 08:00
- Quadrant (1-4)
- High Raided NY AM (Y/N)
- Low Raided NY AM (Y/N)
- High Raided NY PM (Y/N)
- Low Raided NY PM (Y/N)

Use pivot tables or formulas to calculate probabilities for each quadrant/target/session combination.
