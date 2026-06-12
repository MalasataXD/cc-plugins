# Your Commit Message Style

## Structure:
- Title Line: Imperative mood, concise (typically under 60 characters), no period
- Blank line
- Body: Detailed description with context and specifics

## Title Characteristics:
- Uses imperative verbs: "Refactor", "Add", "Fix", "Migrate", "Remove", "Clean up"
- Describes WHAT was done (not what "will be" done)
- Capitalizes first word
- Examples: "Refactor PDF services and types for unified job model", "Fix calendar mode switching synchronization"

## Body Format:
1. Opening paragraph: Provides context and explains the overall change/purpose
2. "Changes:" section (when applicable): Bulleted list with specific modifications:
   - Uses "-" for bullets
   - Lists specific file/component changes
   - Shows renames with arrow notation: "oldName → newName"
   - Mentions deletions, additions, and updates
   - Includes line count reductions with percentages when relevant
3. Closing line (optional): "Fixes [what issue]" or summary of impact

## Language Style:
- Body uses past tense: "Removed", "Updated", "Replaced", "Fixed"
- Specific and technical: mentions exact file names, function names, component names
- Groups related changes together logically
- Explains both what changed AND why it matters
- Never includes "Generated with" or "Co-Authored-By" tags

## Example patterns:
- Function renames: "useJobNavigation → useShippingNavigation"
- Before/after props count: "Reduce props from 9 to 5"
- Code reduction: "Reduce EventCalendar from ~575 to ~380 lines (34% reduction)"
