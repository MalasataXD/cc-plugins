---
name: review
description: Use when the user asks for a code review, quality check, or improvement suggestions on a file, directory, or recent changes (e.g., "review my changes", "check this file for issues", "how can I improve this method"). Analyzes security, performance, quality, style, architecture, and documentation, and returns actionable feedback with a consistent 0–100 score.
---

# Code Review

## Overview

This skill provides a structured approach to conducting thorough code reviews. It analyzes code for security vulnerabilities, performance issues, code quality, style compliance, architectural patterns, and documentation quality. The review produces actionable feedback with a consistent 0-100 score to help developers improve their code.

## When to Use This Skill

Activate this skill when the user requests:
- "Review my changes"
- "Check this [directory/file/method] for code quality issues"
- "How can I improve this [file/method]?"
- "Code review this [directory/file]"
- Any variation requesting code analysis, quality checks, or improvement suggestions

## Code Review Workflow

Follow this workflow for every code review:

### 1. Identify the Scope

Determine what needs to be reviewed:
- **Single file**: Review the specified file
- **Directory**: Review all code files in the directory
- **Recent changes**: Use `git diff` or `git log` to identify changed files
- **Specific method/function**: Focus the review on that code section

### 2. Identify the Language and Style Guide

Before analyzing the code:
1. Identify the programming language(s) in the code
2. Search the codebase for style guides or coding standards:
   - Look for files like `.eslintrc`, `.prettierrc`, `style.md`, `CONTRIBUTING.md`, `.editorconfig`
   - Check for linter configuration files specific to the language
   - Look in `docs/` or root directory for coding standards
3. If no style guide exists:
   - Ask the user: "No style guide found for [language]. Would you like me to create one based on these files?"
   - If yes, create a style guide based on observed patterns in the codebase
   - If no, use language-specific best practices and community standards

### 3. Analyze the Code

Systematically examine the code across six categories:

#### Security Analysis
Review the code for security vulnerabilities using `references/security-checklist.md`:
1. Read the security checklist: `references/security-checklist.md`
2. Check for common security issues relevant to the language
3. Look for:
   - Hardcoded API keys, passwords, or secrets
   - Injection vulnerabilities (SQL, command, XSS, path traversal)
   - Insecure authentication or authorization
   - Sensitive data exposure
   - Insecure cryptographic practices
   - Poor error handling that leaks information
4. Note any security issues with severity assessment

#### Performance Analysis
Evaluate performance characteristics:
1. Analyze algorithm time complexity (Big O notation)
2. Assess space complexity and memory usage
3. Identify inefficient operations:
   - Nested loops that could be optimized
   - N+1 query problems
   - Unnecessary computations
   - Missing caching opportunities
4. Check for resource management issues (unclosed connections, memory leaks)

#### Code Quality & Maintainability
Assess code quality:
1. Evaluate readability and clarity
2. Check function/method length and complexity
3. Verify adherence to SOLID principles
4. Identify code duplication (DRY violations)
5. Look for magic numbers and hardcoded values
6. Assess cyclomatic complexity
7. Check for proper abstraction levels

#### Style & Standards Compliance
Compare code against the identified style guide:
1. Verify naming conventions (variables, functions, classes)
2. Check indentation and formatting consistency
3. Evaluate code organization and file structure
4. Ensure language-specific idioms are used correctly
5. Verify consistency with existing codebase patterns
6. Check appropriate use of modern language features

#### Architecture & Design Patterns
Evaluate architectural decisions:
1. Identify design patterns used and assess appropriateness
2. Check separation of concerns
3. Evaluate dependency management and injection
4. Assess layer separation (presentation, business logic, data)
5. Verify consistency with existing codebase architecture
6. Review interface design and contracts

#### Documentation Quality
Review documentation completeness:
1. Check function/method documentation (JSDoc, docstrings, etc.)
2. Verify class and module documentation
3. Assess inline comments for complex logic
4. Evaluate API documentation if applicable
5. Check README or usage documentation
6. Verify documentation accuracy and clarity

### 4. Calculate the Score

Use `references/scoring-rubric.md` to calculate a consistent score:
1. Read the scoring rubric: `references/scoring-rubric.md`
2. Score each category independently (0-100)
3. Apply the weighted calculation:
   - Security: 25%
   - Performance: 20%
   - Code Quality & Maintainability: 20%
   - Style & Standards: 15%
   - Architecture & Design Patterns: 10%
   - Documentation: 10%
4. Calculate the overall weighted score
5. Round to the nearest whole number

### 5. Prepare the Review

Organize findings into a clear, actionable review:
1. Start with the overall score and category breakdown
2. List key strengths (what the code does well)
3. List areas for improvement with brief explanations
4. Prioritize the top 3-5 most critical issues
5. For each critical issue:
   - Explain why it's problematic
   - Show a code example of the issue
   - Suggest how to fix it
   - Keep explanations short and concise

## Output Format

Present the code review using this structure:

```markdown
# Code Review: [File/Directory Name]

## Overall Score: X/100

### Category Breakdown:
- **Security**: X/100 (Weight: 25%)
- **Performance**: X/100 (Weight: 20%)
- **Code Quality & Maintainability**: X/100 (Weight: 20%)
- **Style & Standards**: X/100 (Weight: 15%)
- **Architecture & Design Patterns**: X/100 (Weight: 10%)
- **Documentation**: X/100 (Weight: 10%)

---

## Key Strengths

- [Specific strength with brief explanation]
- [Specific strength with brief explanation]
- [Specific strength with brief explanation]

---

## Areas for Improvement

### Security
- [Issue with brief explanation]

### Performance
- [Issue with brief explanation]

### Code Quality
- [Issue with brief explanation]

### Style & Standards
- [Issue with brief explanation]

### Architecture
- [Issue with brief explanation]

### Documentation
- [Issue with brief explanation]

---

## Priority Issues

### 1. [Most Critical Issue Title]
**Category**: [Security/Performance/etc.]
**Impact**: [Brief explanation of why this matters]

**Current Code**:
```[language]
[Code snippet showing the issue]
```

**Suggested Fix**:
```[language]
[Code snippet showing the improvement]
```

**Explanation**: [Concise explanation of the fix]

### 2. [Second Critical Issue Title]
[Same format as above]

### 3. [Third Critical Issue Title]
[Same format as above]

---

## Summary

[2-3 sentence summary of overall code quality and next steps]
```

## Guiding Principles

1. **Be objective**: Base assessments on measurable code characteristics
2. **Be specific**: Always provide concrete examples from the actual code
3. **Be actionable**: Focus on what can be improved and how
4. **Be concise**: Keep explanations short and to the point
5. **Be balanced**: Acknowledge both strengths and weaknesses
6. **Be consistent**: Use the scoring rubric for every review
7. **Be thorough**: Review all six categories systematically

## Resources

### references/security-checklist.md
Comprehensive checklist of common security vulnerabilities organized by category and language. Read this file at the start of the security analysis phase to ensure thorough coverage of potential security issues.

### references/scoring-rubric.md
Detailed scoring criteria for each of the six review categories with weighted calculation formula. Read this file when calculating scores to ensure consistent, fair scoring across all reviews.
