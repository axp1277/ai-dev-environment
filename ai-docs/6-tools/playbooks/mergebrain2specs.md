# Command: mergebrain2specs.md
# Description: Merges new brainstorming ideas into an existing specification document
# Usage: merge-specs <session_number> <spec_number>

BRAINSTORMING_FILE="session$1.md"
SPEC_FILE="specs$2.md"

echo "Merging brainstorming session $BRAINSTORMING_FILE into specification document $SPEC_FILE..."

Analyze the content in the brainstorming file "$BRAINSTORMING_FILE" and the specification file "$SPEC_FILE". 

Your task is to:
1. Identify new features, tasks, or enhancements in the brainstorming file that are not present in the specification document
2. Determine where each new item should be placed in the specification document based on relevance to existing sections
3. Update the specification document by adding these new items in appropriate sections
4. If a brainstorming item is similar to an existing spec item but contains new details, merge the information rather than creating duplicates
5. Maintain the original formatting and structure of the specification document
6. Add a note at the end of each new/updated section indicating it was updated from the brainstorming session

Return the updated specification document with all changes highlighted or marked. 