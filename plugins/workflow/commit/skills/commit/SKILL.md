---
name: commit
description: Use when the user asks to create a commit, make a commit, or commit changes. Produces git commits with imperative-mood titles, a context paragraph, a bulleted "Changes:" section, and a closing impact statement. Never adds "Generated with" or "Co-Authored-By" trailers.
---

# Commit Style

## Overview

Create git commits that follow a consistent, professional format with imperative mood titles, detailed context, specific change listings, and impact summaries. The style uses past tense descriptions in the body and never includes "Generated with" or "Co-Authored-By" tags.

## Workflow

Follow this workflow when creating commits:

### 1. Gather Git Information

Run these git commands in parallel to understand the current state:

```bash
git status        # See all untracked and modified files
git diff          # See unstaged changes
git diff --cached # See staged changes
git log -3 --format="%h %s"  # See recent commit message style
```

### 2. Analyze the Changes

Review all changes (both staged and unstaged) to understand:

- What files were modified and why
- What functionality changed
- What impact these changes have
- Any patterns or groupings in the changes

### 3. Draft the Commit Message

Construct the commit message following the style guide in `references/commit-style.md`:

**Title Line:**
- Use imperative mood verbs (Refactor, Add, Fix, Migrate, Remove, Clean up)
- Keep under 60 characters
- Capitalize first word
- No period at the end

**Body:**
1. Opening paragraph explaining the overall change and context
2. "Changes:" section with bulleted specifics:
   - Use "-" for bullets
   - List specific files, functions, components modified
   - Show renames with arrow notation: "oldName → newName"
   - Include line reductions with percentages when relevant
3. Closing line with impact or "Fixes [what]" if applicable

**Language:**
- Body uses past tense (Removed, Updated, Fixed)
- Specific and technical (mention exact file names, function names)
- Explain what changed AND why it matters
- NEVER include "Generated with" or "Co-Authored-By" tags

### 4. Stage and Commit

Stage relevant files and create the commit:

```bash
# Stage files
git add file1.ts file2.tsx file3.json

# Create commit with HEREDOC for proper formatting
git commit -m "$(cat <<'EOF'
Title line here

Opening paragraph explaining the change and context.

Changes:
- Specific change 1 in component-name
- Specific change 2: oldName → newName
- Specific change 3 in file-name

Closing impact statement.
EOF
)"

# Verify commit was created
git status
```

### 5. Confirm Success

After committing, confirm the commit was created successfully and display:
- The commit hash
- The title
- How many files were changed
- Branch status (ahead/behind remote)

## References

- `references/commit-style.md` - Complete style guide with examples and patterns

## Notes

- Always check if files should be committed (avoid secrets, .env files, credentials)
- Group related changes logically in the "Changes:" section
- When multiple independent changes exist, ask if they should be separate commits
- Keep commit messages short and concise in title, detailed and specific in body
