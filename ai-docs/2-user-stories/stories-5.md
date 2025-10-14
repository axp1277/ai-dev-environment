---
Session: 5
Created: 2025-10-13
Inputs:
  - Brainstorming: session5.md
  - PRD: prd5.md
Status: Draft
---

# London Session Profile Study - User Stories

## User Personas

### Primary Persona: Intraday Futures Trader
**Role**: Active day trader focusing on ES, NQ, and other futures contracts during NY session

**Goals**:
- Identify high-probability trading setups based on London session structure
- Set realistic profit targets backed by statistical data
- Time trade entries and exits based on probability of London targets being hit
- Increase win rate by filtering low-probability setups

**Pain Points**:
- Cannot quantify when London highs or lows will be raided during NY session
- Relies on gut feeling or subjective experience for target setting
- Uncertainty about whether to target London high, London low, or both
- Difficulty determining optimal entry timing within NY session
- Manual backtesting is time-consuming and error-prone

**Technical Proficiency**: Intermediate - Comfortable with TradingView indicators and basic configuration

---

### Secondary Persona: Systematic Strategy Developer
**Role**: Quantitative trader building algorithmic trading systems

**Goals**:
- Incorporate session-based probability statistics into automated strategies
- Backtest strategies with historical probability data
- Filter trade signals based on statistical probability thresholds
- Develop robust rules-based trading systems

**Pain Points**:
- Lack of programmatically accessible historical probability data
- Manual backtesting of session relationships is inefficient
- Need quantitative filters to improve strategy performance
- Difficult to validate edge without statistical evidence

**Technical Proficiency**: Advanced - Can modify PineScript code and integrate libraries

---

### Tertiary Persona: Market Structure Analyst
**Role**: Technical analyst studying and documenting intraday market behavior

**Goals**:
- Understand how price behaves across session transitions
- Document probability distributions for different market conditions
- Validate session-based trading theories with quantitative evidence
- Educate other traders on session dynamics

**Pain Points**:
- Need quantitative evidence to support analysis theories
- Cannot easily demonstrate probability distributions to others
- Lack of tools to analyze session relationships statistically
- Manual data collection and analysis is tedious

**Technical Proficiency**: Intermediate - Understands technical analysis and can interpret statistical data

---

# Epic 1: Session Configuration and Setup

**Epic Goal**: Enable traders to configure London and New York session times to match their preferred markets and trading style

## User Story 1.1: Configure Session Times

**As an** intraday futures trader
**I want to** configure the start and end times for London, NY AM, and NY PM sessions
**So that** the study analyzes the correct time windows for my specific market

**Acceptance Criteria**:
- [ ] Given I open the indicator settings, when I view the session configuration section, then I see separate inputs for London session start/end, NY AM start/end, and NY PM start/end
- [ ] Given I want to change session times, when I enter new times in EST format (e.g., "01:00" for 1 AM), then the system accepts and validates the format
- [ ] Given I have configured custom session times, when I reload the chart, then my custom settings persist
- [ ] Given I enter invalid time format, when I save settings, then I see a clear error message explaining the correct format

**Priority**: High
**Story Points**: 2

---

## User Story 1.2: View Current Session Status

**As an** intraday futures trader
**I want to** see which session is currently active on my chart
**So that** I understand the context for the probability data being displayed

**Acceptance Criteria**:
- [ ] Given I am viewing the chart during London session, when I look at the indicator display, then I see "London Session Active"
- [ ] Given I am viewing the chart during NY AM session, when I look at the indicator display, then I see "NY AM Session Active"
- [ ] Given I am viewing the chart during NY PM session, when I look at the indicator display, then I see "NY PM Session Active"
- [ ] Given I am viewing the chart outside trading hours, when I look at the indicator display, then I see "No Active Session"

**Priority**: Medium
**Story Points**: 2

---

# Epic 2: Quadrant Analysis and Probability Computation

**Epic Goal**: Provide statistical probability data for London high/low targets based on quadrant positioning at London session close

## User Story 2.1: View London Session Quadrants

**As an** intraday futures trader
**I want to** see the London session range divided into four 25% quadrants
**So that** I can understand where price closed relative to the session range

**Acceptance Criteria**:
- [ ] Given London session has closed, when I view the chart, then I see the London session high and low clearly marked
- [ ] Given the London range is displayed, when I look at the visualization, then I see four equal quadrants marked at 0-25%, 25-50%, 50-75%, and 75-100%
- [ ] Given price closed in a specific quadrant, when NY session opens, then the current quadrant is highlighted or labeled (e.g., "Quadrant 4: 75-100%")
- [ ] Given I hover over quadrant markers, when I pause, then I see tooltip showing the price levels for that quadrant

**Priority**: High
**Story Points**: 5

---

## User Story 2.2: View Probability of London High Being Raided

**As an** intraday futures trader
**I want to** see the probability of London high being raided during NY session based on my current quadrant
**So that** I can decide whether to target the London high

**Acceptance Criteria**:
- [ ] Given I closed London session in Quadrant 1 (0-25%), when NY AM session opens, then I see "London High Raid Probability (NY AM): X%" displayed on chart
- [ ] Given I closed London session in Quadrant 4 (75-100%), when NY AM session opens, then I see a different probability percentage reflecting lower likelihood
- [ ] Given NY AM session ends, when NY PM session begins, then the probability updates to show NY PM session probability
- [ ] Given I have historical data loaded, when the study calculates probabilities, then values are based on at least 100 historical sessions

**Priority**: High
**Story Points**: 8

---

## User Story 2.3: View Probability of London Low Being Raided

**As an** intraday futures trader
**I want to** see the probability of London low being raided during NY session based on my current quadrant
**So that** I can decide whether to target the London low

**Acceptance Criteria**:
- [ ] Given I closed London session in Quadrant 4 (75-100%), when NY AM session opens, then I see "London Low Raid Probability (NY AM): X%" displayed on chart
- [ ] Given I closed London session in Quadrant 1 (0-25%), when NY AM session opens, then I see a different probability percentage reflecting lower likelihood
- [ ] Given NY AM session ends, when NY PM session begins, then the probability updates to show NY PM session probability
- [ ] Given probabilities are displayed, when I compare them across different quadrants, then I can see how starting position affects probability

**Priority**: High
**Story Points**: 8

---

## User Story 2.4: View All Quadrant Probabilities Simultaneously

**As a** market structure analyst
**I want to** view probability statistics for all four quadrants at once
**So that** I can compare probability distributions and understand patterns

**Acceptance Criteria**:
- [ ] Given I enable "Show All Quadrants" setting, when I view the chart, then I see a probability table showing all 4 quadrants × 2 targets (high/low) × 2 sessions (AM/PM) = 16 probability values
- [ ] Given the probability table is displayed, when I read the values, then they are organized in a clear, readable format (e.g., table or structured list)
- [ ] Given I want to focus on current quadrant only, when I disable "Show All Quadrants", then only the current quadrant's probabilities are shown
- [ ] Given the table is displayed, when I compare probabilities, then higher probability values are visually emphasized (e.g., bold or colored)

**Priority**: Medium
**Story Points**: 5

---

# Epic 3: VWAP Bias Filtering

**Epic Goal**: Enable conditional probability analysis based on VWAP position to refine trading setups

## User Story 3.1: Enable VWAP Filter

**As a** systematic strategy developer
**I want to** enable a VWAP filter that shows conditional probabilities based on price position relative to VWAP
**So that** I can filter setups to only trade when VWAP bias aligns with my strategy

**Acceptance Criteria**:
- [ ] Given I open indicator settings, when I view the filter section, then I see a toggle for "Enable VWAP Filter"
- [ ] Given VWAP filter is disabled, when I view probabilities, then I see base probabilities without VWAP conditioning
- [ ] Given I enable VWAP filter, when NY session opens, then the system calculates VWAP anchored at NY midnight
- [ ] Given VWAP filter is enabled, when I save settings, then the setting persists across chart reloads

**Priority**: High
**Story Points**: 3

---

## User Story 3.2: View Conditional Probabilities with VWAP Filter

**As a** systematic strategy developer
**I want to** see separate probability statistics for when price is above vs below VWAP at NY open
**So that** I can quantify how VWAP bias affects target probability

**Acceptance Criteria**:
- [ ] Given VWAP filter is enabled and price is above VWAP at NY open, when I view probabilities, then I see "Above VWAP: X%" and "Below VWAP: Y%" displayed
- [ ] Given VWAP filter is enabled and price is below VWAP at NY open, when I view probabilities, then the "Below VWAP" percentage is highlighted as the current condition
- [ ] Given conditional probabilities are shown, when I compare them, then I can see if VWAP position creates a statistical edge
- [ ] Given insufficient data exists for VWAP conditioning, when probabilities are calculated, then I see "Insufficient data for VWAP filter" message

**Priority**: High
**Story Points**: 8

---

## User Story 3.3: Visualize VWAP on Chart

**As an** intraday futures trader
**I want to** see VWAP (anchored at NY midnight) plotted on my chart
**So that** I can visually confirm price position relative to VWAP

**Acceptance Criteria**:
- [ ] Given VWAP filter is enabled, when NY session begins, then VWAP line is plotted on the chart starting at NY midnight
- [ ] Given VWAP is plotted, when price crosses VWAP, then I can clearly see the crossover point
- [ ] Given I want to customize VWAP display, when I access settings, then I can change VWAP line color and thickness
- [ ] Given I disable VWAP filter, when I view the chart, then VWAP line is hidden

**Priority**: Medium
**Story Points**: 3

---

# Epic 4: Time-Based Target Window Filtering

**Epic Goal**: Allow filtering of probability calculations to specific time windows within NY session

## User Story 4.1: Enable Time Window Filter

**As an** intraday futures trader
**I want to** enable a time window filter that only counts targets hit within specific time ranges
**So that** I can focus on setups that reach targets during my preferred trading window

**Acceptance Criteria**:
- [ ] Given I open indicator settings, when I view the filter section, then I see a toggle for "Enable Time Window Filter"
- [ ] Given time window filter is disabled, when probabilities are calculated, then all target hits during NY session are counted regardless of time
- [ ] Given I enable time window filter, when probabilities are calculated, then only targets hit within the specified window are counted
- [ ] Given I want to specify a custom window, when I access settings, then I can enter start and end times for the window (e.g., "9:30 AM - 11:00 AM")

**Priority**: Medium
**Story Points**: 5

---

## User Story 4.2: Compare AM vs PM Target Probabilities

**As a** market structure analyst
**I want to** see separate probability statistics for NY AM session (8-12) vs NY PM session (12-4)
**So that** I can understand when London targets are most likely to be hit

**Acceptance Criteria**:
- [ ] Given I am viewing probabilities, when NY AM session is active, then I see both "NY AM Probability: X%" and "NY PM Probability: Y%"
- [ ] Given the probabilities are displayed, when I compare AM vs PM, then I can see which session has higher probability for my current quadrant
- [ ] Given I want to focus on one session only, when I adjust time window filter, then I can limit calculations to only AM or only PM
- [ ] Given historical patterns are available, when comparing sessions, then I can identify consistent time-based patterns

**Priority**: Medium
**Story Points**: 5

---

# Epic 5: Statistical Engine Integration and Data Display

**Epic Goal**: Integrate with Statistical Frequency Engine library and display reliable probability data

## User Story 5.1: View Sample Size for Probability Calculations

**As a** market structure analyst
**I want to** see the sample size (number of historical sessions) used to calculate each probability
**So that** I can assess the statistical reliability of the data

**Acceptance Criteria**:
- [ ] Given probabilities are displayed, when I look at each probability value, then I see the sample size in parentheses (e.g., "65% (n=120)")
- [ ] Given sample size is less than 30, when probability is displayed, then I see a warning indicator (e.g., asterisk or yellow color)
- [ ] Given I want more details, when I hover over a probability value, then I see tooltip with full statistics (sample size, confidence interval if available)
- [ ] Given I enable "Show Statistics" setting, when viewing probabilities, then I see additional metrics like success count / total count (e.g., "78/120 = 65%")

**Priority**: Medium
**Story Points**: 3

---

## User Story 5.2: Handle Insufficient Historical Data

**As an** intraday futures trader
**I want to** be clearly informed when there is insufficient historical data for a probability calculation
**So that** I don't make trading decisions based on unreliable statistics

**Acceptance Criteria**:
- [ ] Given a specific quadrant/target/session combination has fewer than 10 historical samples, when probability is displayed, then I see "Insufficient data (n=X)" instead of a percentage
- [ ] Given multiple probabilities have insufficient data, when I view the study, then I see a summary message like "Low data availability: Load more historical data"
- [ ] Given I add more historical bars to my chart, when the study recalculates, then previously unavailable probabilities appear if threshold is now met
- [ ] Given I hover over "Insufficient data" message, when I pause, then tooltip explains minimum sample size requirement (e.g., "Minimum 10 samples required")

**Priority**: High
**Story Points**: 3

---

## User Story 5.3: Verify Statistical Accuracy

**As a** systematic strategy developer
**I want to** manually verify that probability calculations are mathematically correct
**So that** I can trust the data for building trading strategies

**Acceptance Criteria**:
- [ ] Given I want to audit calculations, when I enable "Debug Mode" in settings, then I see detailed logs showing frequency counts for each condition
- [ ] Given I perform manual backtest on a sample period, when I compare results to study probabilities, then they match within 2% margin of error
- [ ] Given probability is displayed as 65%, when I check the underlying data, then approximately 65 out of 100 historical instances resulted in target being hit
- [ ] Given the study uses Statistical Frequency Engine library, when I review the implementation, then it follows the reference patterns correctly

**Priority**: High
**Story Points**: 5

---

# Epic 6: Usability and Configuration

**Epic Goal**: Provide intuitive controls and clear visual presentation of probability data

## User Story 6.1: Customize Probability Display

**As an** intraday futures trader
**I want to** customize how probabilities are displayed on my chart
**So that** the study fits my chart layout and personal preferences

**Acceptance Criteria**:
- [ ] Given I want to adjust display, when I open settings, then I can choose text size (Small/Medium/Large)
- [ ] Given I want to position probabilities, when I access settings, then I can choose display location (Top Left, Top Right, Bottom Left, Bottom Right)
- [ ] Given I want to color-code probabilities, when I configure settings, then I can set color thresholds (e.g., >60% green, 40-60% yellow, <40% red)
- [ ] Given my chart is cluttered, when I minimize the study, then only the most critical probability (current quadrant, current session) is shown

**Priority**: Low
**Story Points**: 5

---

## User Story 6.2: Access Clear Documentation

**As an** intraday futures trader
**I want to** access clear documentation explaining how to interpret probability values
**So that** I can use the study effectively without confusion

**Acceptance Criteria**:
- [ ] Given I need help, when I click "Documentation" link in settings, then I see a guide explaining what each probability means
- [ ] Given I am confused about quadrants, when I read documentation, then I see clear examples showing how quadrant is determined
- [ ] Given I want to understand filters, when I read documentation, then I see examples of how VWAP and time window filters affect probabilities
- [ ] Given I need interpretation guidance, when I read documentation, then I see suggested probability thresholds for trade filtering (e.g., "Consider setups >60%")

**Priority**: Medium
**Story Points**: 3

---

## User Story 6.3: Reset to Default Settings

**As an** intraday futures trader
**I want to** easily reset all settings to defaults
**So that** I can start fresh if my custom configuration becomes problematic

**Acceptance Criteria**:
- [ ] Given I want to reset, when I click "Reset to Defaults" button in settings, then all session times revert to defaults (London 1-8 AM, NY AM 8-12, NY PM 12-4)
- [ ] Given I confirm reset, when settings are restored, then all filters are disabled and display options return to defaults
- [ ] Given I accidentally click reset, when the button is pressed, then I see a confirmation dialog asking "Are you sure?"
- [ ] Given settings are reset, when I view the chart, then I see a notification "Settings restored to defaults"

**Priority**: Low
**Story Points**: 2

---

# Story Map

## Release 1 - Core MVP
**Goal**: Deliver basic quadrant-based probability analysis without filters

- **Epic 1: Session Configuration and Setup**
  - Story 1.1: Configure Session Times
  - Story 1.2: View Current Session Status

- **Epic 2: Quadrant Analysis and Probability Computation**
  - Story 2.1: View London Session Quadrants
  - Story 2.2: View Probability of London High Being Raided
  - Story 2.3: View Probability of London Low Being Raided

- **Epic 5: Statistical Engine Integration**
  - Story 5.2: Handle Insufficient Historical Data
  - Story 5.3: Verify Statistical Accuracy

**Estimated Duration**: 2-3 weeks
**Story Points Total**: 36

---

## Release 2 - Enhanced Filtering
**Goal**: Add VWAP and time window conditional filtering

- **Epic 3: VWAP Bias Filtering**
  - Story 3.1: Enable VWAP Filter
  - Story 3.2: View Conditional Probabilities with VWAP Filter
  - Story 3.3: Visualize VWAP on Chart

- **Epic 4: Time-Based Target Window Filtering**
  - Story 4.1: Enable Time Window Filter
  - Story 4.2: Compare AM vs PM Target Probabilities

**Estimated Duration**: 1-2 weeks
**Story Points Total**: 24

---

## Release 3 - Analytics and Usability
**Goal**: Add advanced analytics and improve user experience

- **Epic 2: Quadrant Analysis and Probability Computation**
  - Story 2.4: View All Quadrant Probabilities Simultaneously

- **Epic 5: Statistical Engine Integration**
  - Story 5.1: View Sample Size for Probability Calculations

- **Epic 6: Usability and Configuration**
  - Story 6.1: Customize Probability Display
  - Story 6.2: Access Clear Documentation
  - Story 6.3: Reset to Default Settings

**Estimated Duration**: 1 week
**Story Points Total**: 18

---

## Total Project Estimate
**Total Story Points**: 78
**Estimated Timeline**: 4-6 weeks with iterative development
**Team Size**: 1 developer with AI assistance + 1 product owner for oversight

---

## Notes on Story Prioritization

**High Priority Stories (MVP Critical)**:
- Basic session configuration and quadrant display
- Core probability calculations for London high/low raids
- VWAP filter implementation (key differentiator)
- Data quality handling (insufficient data warnings)
- Statistical accuracy verification

**Medium Priority Stories (Important but not blocking)**:
- Time window filtering
- Session comparison (AM vs PM)
- Sample size display
- Documentation

**Low Priority Stories (Nice to have)**:
- Advanced display customization
- Reset functionality
- Multi-quadrant simultaneous view

**Dependencies**:
- Statistical Frequency Engine library must be integrated before any probability calculations
- VWAP calculation required before VWAP filtering can work
- Session configuration must work before probabilities can be calculated
- All core stories (Release 1) must complete before filters (Release 2) are added
