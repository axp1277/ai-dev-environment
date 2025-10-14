# London Session Profile Study - User Workflow

**Session**: 5
**Created**: 2025-10-13
**Description**: Trader workflow from session observation through probability analysis to trading decision

---

## Workflow Diagram

This diagram illustrates the complete user journey for a trader using the London Session Profile Study indicator, from initial chart setup through probability analysis to trading decisions.

```mermaid
graph TD
    Start((Trader Opens<br/>Chart)) --> LoadIndicator[Load London Profile<br/>Study Indicator]
    LoadIndicator --> ConfigSession{Configure<br/>Session Times?}

    ConfigSession -->|Yes| CustomConfig[Set Custom Times<br/>London/NY AM/NY PM]
    ConfigSession -->|No| DefaultConfig[Use Default Times<br/>01:00-08:00, 08:00-12:00, 12:00-16:00]

    CustomConfig --> WaitLondon[Wait for London<br/>Session Close]
    DefaultConfig --> WaitLondon

    WaitLondon --> LondonClose[London Session Closes<br/>at 08:00 AM]
    LondonClose --> IdentifyQuadrant[System Identifies<br/>Closing Quadrant<br/>Q1/Q2/Q3/Q4]

    IdentifyQuadrant --> DisplayProb[Display Probabilities<br/>for Current Quadrant]

    DisplayProb --> TraderAnalysis{Trader<br/>Analyzes<br/>Probabilities}

    TraderAnalysis --> EnableFilters{Want to<br/>Apply Filters?}

    EnableFilters -->|VWAP Filter| CheckVWAP[Enable VWAP Filter<br/>Check Bias Above/Below]
    EnableFilters -->|Time Window| SetTimeWindow[Set Custom Time Window<br/>e.g., 09:30-11:00]
    EnableFilters -->|No Filter| ViewBaseProb[View Base<br/>Probabilities]

    CheckVWAP --> ViewConditional[View Conditional<br/>Probabilities<br/>Above/Below VWAP]
    SetTimeWindow --> ViewWindowProb[View Time-Window<br/>Filtered Probabilities]

    ViewConditional --> DecideTarget
    ViewWindowProb --> DecideTarget
    ViewBaseProb --> DecideTarget

    DecideTarget{High Probability<br/>Target Identified?}

    DecideTarget -->|Yes >60%| PlanTrade[Plan Trade<br/>Target: London High/Low<br/>Timeframe: NY AM/PM]
    DecideTarget -->|No <40%| NoTrade[Skip Trade<br/>Low Probability]
    DecideTarget -->|Borderline 40-60%| ReviewMore[Review Additional<br/>Analysis]

    PlanTrade --> MonitorSession[Monitor NY Session<br/>Track Target Progress]
    ReviewMore --> MonitorSession

    MonitorSession --> TargetHit{Target<br/>Reached?}

    TargetHit -->|Yes| TradeSuccess[Trade Success<br/>Exit Position]
    TargetHit -->|No| SessionEnd[NY Session Ends<br/>Re-evaluate]

    NoTrade --> WaitNext[Wait for Next<br/>London Session]
    TradeSuccess --> WaitNext
    SessionEnd --> WaitNext

    WaitNext --> NextDay{Continue<br/>Trading?}
    NextDay -->|Yes| WaitLondon
    NextDay -->|No| End((End))

    classDef userAction fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    classDef systemProcess fill:#ffe1e1,stroke:#cc0000,stroke-width:2px
    classDef decision fill:#fff4e1,stroke:#cc6600,stroke-width:2px
    classDef success fill:#e1ffe1,stroke:#00cc00,stroke-width:2px

    class LoadIndicator,CustomConfig,CheckVWAP,SetTimeWindow,PlanTrade,MonitorSession userAction
    class LondonClose,IdentifyQuadrant,DisplayProb,ViewConditional,ViewWindowProb,ViewBaseProb systemProcess
    class ConfigSession,TraderAnalysis,EnableFilters,DecideTarget,TargetHit,NextDay decision
    class TradeSuccess success
```

## Key Workflow Steps

### 1. Initial Setup
- Trader loads the indicator on TradingView chart
- Optionally configures custom session times or uses defaults

### 2. Session Observation
- Wait for London session to close at 08:00 AM EST
- System automatically identifies closing quadrant (Q1, Q2, Q3, or Q4)

### 3. Probability Analysis
- System displays probability data for current quadrant
- Trader can apply optional filters:
  - **VWAP Filter**: View conditional probabilities based on price position relative to VWAP
  - **Time Window Filter**: Focus on specific time ranges within NY session
  - **No Filter**: View base probabilities

### 4. Trading Decision
- **High Probability (>60%)**: Plan trade targeting London high or low during NY session
- **Low Probability (<40%)**: Skip trade due to low statistical likelihood
- **Borderline (40-60%)**: Review additional analysis before deciding

### 5. Trade Execution & Monitoring
- If trade is planned, monitor NY session for target achievement
- Track whether London high/low is reached
- Exit position if target is hit, or re-evaluate at session end

### 6. Next Session
- Wait for next London session to repeat the process
- Continue daily trading loop or end session

## Color Legend

- **Blue (User Action)**: Actions performed by the trader
- **Red (System Process)**: Automated system calculations and displays
- **Orange (Decision)**: Decision points in the workflow
- **Green (Success)**: Successful trade outcome

## Related Documents

- **PRD**: ai-docs/2-prds/prd5.md
- **User Stories**: ai-docs/2-user-stories/stories-5.md
- **Technical Specs**: ai-docs/2-specs/specs-5.md
- **Validation**: ai-docs/2-validation/validation-5.md
- **Architecture Diagram**: ai-docs/2-diagrams/architecture-5.md
