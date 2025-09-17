# Command: report_updates
# Description: Generate a client-friendly update report based on git changes
# Usage: report_updates

# Instruct the AI to create a comprehensive update report for clients

Create a professional update report that communicates recent changes to clients:

1. **Get Current Version**: 
   - Read the current version from `pyproject.toml`
   - Use this version for the report header

2. **Analyze Recent Changes**:
   - Run `git status` to see current state
   - Run `git diff HEAD~1` to get changes from the last commit
   - If there are uncommitted changes, also run `git diff` to include them
   - Analyze the diff output to identify meaningful changes

3. **Categorize Changes**:
   Based on the git diff analysis, categorize changes into:
   
   **🆕 New Features**: 
   - New functionality added
   - New commands, modules, or capabilities
   - New integrations or connections
   
   **🔧 Improvements**: 
   - Enhanced existing functionality
   - Performance optimizations
   - Better error handling
   - UI/UX improvements
   
   **🐛 Bug Fixes**: 
   - Resolved issues or errors
   - Fixed broken functionality
   - Corrected logic or calculations
   
   **📊 Configuration & Settings**: 
   - New configuration options
   - Updated default settings
   - Environment or deployment changes
   
   **🔐 Security & Stability**: 
   - Security enhancements
   - Stability improvements
   - Dependency updates

4. **Generate Report**:
   Create a markdown file named `UPDATE_REPORT.md` in the project root with:
   
   ```markdown
   # Update Report - Version [VERSION]
   
   **Generated**: [CURRENT_TIMESTAMP]
   **Version**: [CURRENT_VERSION]
   
   ## Summary
   
   [Brief 1-2 sentence overview of what was updated in this version]
   
   ## 🆕 New Features
   
   - [Feature 1]: [Brief description of what it does and why it's useful]
   - [Feature 2]: [Brief description of what it does and why it's useful]
   
   ## 🔧 Improvements
   
   - [Improvement 1]: [What was enhanced and the benefit]
   - [Improvement 2]: [What was enhanced and the benefit]
   
   ## 🐛 Bug Fixes
   
   - [Fix 1]: [What was broken and how it was resolved]
   - [Fix 2]: [What was broken and how it was resolved]
   
   ## 📊 Configuration & Settings
   
   - [Config 1]: [What setting was added/changed and its purpose]
   - [Config 2]: [What setting was added/changed and its purpose]
   
   ## 🔐 Security & Stability
   
   - [Security 1]: [What was improved for security/stability]
   - [Security 2]: [What was improved for security/stability]
   
   ---
   
   *This report was automatically generated from git changes analysis.*
   ```

5. **Report Guidelines**:
   
   **Language Style**:
   - Use clear, non-technical language when possible
   - Focus on client benefits rather than technical implementation
   - Keep each bullet point concise but informative
   - Use active voice ("Added new feature" not "New feature was added")
   
   **Content Rules**:
   - Only include sections that have actual changes
   - Skip internal code refactoring unless it impacts performance
   - Ignore minor formatting or comment changes
   - Focus on user-facing improvements
   - Include relevant file paths only if they help explain the change
   
   **Prioritization**:
   - Lead with the most impactful changes
   - Group related changes together
   - Use clear, benefit-focused descriptions
   
   **Examples of Good vs Poor Descriptions**:
   
   ✅ **Good**: "Enhanced Discord bot with new !logs command to easily download trading log files directly from chat"
   
   ❌ **Poor**: "Modified src/discord_bot/commands.py to add logs function with file upload capability"
   
   ✅ **Good**: "Improved strategy logging to provide clearer visibility into why trades are filtered or entered"
   
   ❌ **Poor**: "Added enable_messaging parameter and enhanced logging in strategy.py"

6. **Validation**:
   - Ensure the report is client-ready (no technical jargon)
   - Verify all sections have content or are omitted
   - Check that the version and timestamp are correct
   - Confirm the summary accurately reflects the changes

7. **Discord Notification**:
   After generating the report, send an update notification to Discord:
   
   - Check if `DISCORD_UPDATES_CHANNEL_ID` exists in `.env` file
   - If the environment variable exists, use the Discord bot to send an update message
   - Create a Discord embed with:
     - Title: "📋 Update Report - Version [VERSION]"
     - Description: The summary section from the report
     - Color: Green for successful update
     - Fields for each category that has content (New Features, Improvements, etc.)
     - Footer with timestamp
   - Use the existing Discord bot structure in `src/discord_bot/`
   - Send the message to the updates channel specified by `DISCORD_UPDATES_CHANNEL_ID`
   
   **Discord Integration Steps**:
   1. Import necessary Discord modules from `src/discord_bot/`
   2. Load the `DISCORD_UPDATES_CHANNEL_ID` from environment variables
   3. Initialize a Discord client connection (reuse existing bot structure)
   4. Create a professional embed message with the update information
   5. Send the embed message to the updates channel
   6. Handle any Discord connection errors gracefully
   
   **Discord Message Format**:
   ```
   📋 **Update Report - Version 1.54.4**
   
   🔄 **Summary**: [Brief overview of changes]
   
   🆕 **New Features** (if any):
   • [Feature descriptions]
   
   🔧 **Improvements** (if any):
   • [Improvement descriptions]
   
   🐛 **Bug Fixes** (if any):
   • [Fix descriptions]
   
   📊 **Configuration** (if any):
   • [Config descriptions]
   
   🔐 **Security & Stability** (if any):
   • [Security descriptions]
   ```

8. **Final Output**:
   - Create/overwrite the `UPDATE_REPORT.md` file
   - Send Discord notification to updates channel (if configured)
   - Confirm both the report was generated and Discord message was sent
   - Provide a brief summary of what was included in the report and notification status