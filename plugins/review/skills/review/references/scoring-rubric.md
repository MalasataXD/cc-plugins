# Code Review Scoring Rubric

Provide a consistent 0-100 score based on the following categories. Calculate the overall score as a weighted average of these categories.

## Scoring Categories

### 1. Security (Weight: 25%)

**Score Range:**
- **90-100**: No security issues detected. Follows all security best practices.
- **75-89**: Minor security considerations that pose low risk.
- **60-74**: Some security issues present that should be addressed.
- **40-59**: Multiple security vulnerabilities or one critical issue.
- **20-39**: Serious security vulnerabilities that could be exploited.
- **0-19**: Critical security flaws that pose immediate risk.

**Key Factors:**
- Input validation and sanitization
- Authentication and authorization
- Sensitive data handling (API keys, passwords, PII)
- Injection vulnerability prevention
- Secure cryptographic practices
- Proper error handling without information leakage

### 2. Performance (Weight: 20%)

**Score Range:**
- **90-100**: Optimal time/space complexity. Efficient algorithms and data structures.
- **75-89**: Good performance with minor optimization opportunities.
- **60-74**: Acceptable performance but noticeable inefficiencies exist.
- **40-59**: Performance issues that could impact user experience.
- **20-39**: Significant performance problems (e.g., O(n²) where O(n) is achievable).
- **0-19**: Severe performance issues (e.g., O(2ⁿ) or worse, memory leaks).

**Key Factors:**
- Algorithm time complexity
- Space complexity and memory usage
- Database query efficiency (N+1 queries, missing indexes)
- Unnecessary computations or redundant operations
- Caching strategies
- Resource management (connection pooling, file handles)

### 3. Code Quality & Maintainability (Weight: 20%)

**Score Range:**
- **90-100**: Exemplary code quality. Clear, well-structured, and follows SOLID principles.
- **75-89**: High quality code with minor readability or structure improvements possible.
- **60-74**: Adequate quality but needs refactoring for better maintainability.
- **40-59**: Poor code organization, difficult to understand or modify.
- **20-39**: Serious code quality issues (deeply nested logic, unclear intent).
- **0-19**: Unmaintainable code (spaghetti code, no structure).

**Key Factors:**
- Code readability and clarity
- Function/method length and complexity
- Single Responsibility Principle adherence
- DRY (Don't Repeat Yourself) compliance
- Proper abstraction levels
- Cyclomatic complexity
- Magic numbers and hardcoded values

### 4. Style & Standards Compliance (Weight: 15%)

**Score Range:**
- **90-100**: Perfectly follows style guide and coding standards.
- **75-89**: Mostly compliant with minor style inconsistencies.
- **60-74**: Some style violations but generally consistent.
- **40-59**: Frequent style violations affecting readability.
- **20-39**: Inconsistent style throughout, difficult to read.
- **0-19**: No adherence to any coding standards.

**Key Factors:**
- Naming conventions (variables, functions, classes)
- Indentation and formatting
- Code organization and file structure
- Language-specific idioms and best practices
- Consistency with existing codebase patterns
- Use of modern language features appropriately

### 5. Architecture & Design Patterns (Weight: 10%)

**Score Range:**
- **90-100**: Excellent architecture. Appropriate design patterns used correctly.
- **75-89**: Good design with minor architectural improvements possible.
- **60-74**: Acceptable design but doesn't follow established patterns well.
- **40-59**: Poor architectural choices or misuse of design patterns.
- **20-39**: Architectural anti-patterns present.
- **0-19**: No discernible architecture, chaotic design.

**Key Factors:**
- Appropriate use of design patterns
- Separation of concerns
- Dependency injection and inversion
- Layer separation (presentation, business logic, data access)
- Consistency with existing codebase architecture
- Interface design and contracts

### 6. Documentation Quality (Weight: 10%)

**Score Range:**
- **90-100**: Comprehensive, clear documentation for all public interfaces.
- **75-89**: Good documentation with minor gaps.
- **60-74**: Basic documentation present but incomplete.
- **40-59**: Minimal documentation, key areas undocumented.
- **20-39**: Sparse or misleading documentation.
- **0-19**: No documentation or completely incorrect documentation.

**Key Factors:**
- Function/method documentation (JSDoc, docstrings, etc.)
- Class and module documentation
- Complex logic explanation
- API documentation
- Inline comments for non-obvious code
- README or usage documentation
- Documentation accuracy and clarity

## Overall Score Calculation

```
Overall Score = (Security × 0.25) + (Performance × 0.20) + (Quality × 0.20) +
                (Style × 0.15) + (Architecture × 0.10) + (Documentation × 0.10)
```

## Score Interpretation

- **90-100**: Excellent - Production-ready code with minimal issues
- **80-89**: Very Good - High quality with some minor improvements needed
- **70-79**: Good - Solid code but notable improvements recommended
- **60-69**: Acceptable - Functional but needs refactoring before production
- **50-59**: Below Average - Multiple issues need to be addressed
- **40-49**: Poor - Significant problems, not ready for production
- **30-39**: Very Poor - Major refactoring required
- **0-29**: Critical - Code needs to be rewritten

## Presentation Format

When presenting the score, use this format:

```
## Code Review Score: X/100

### Category Breakdown:
- Security: X/100 (Weight: 25%)
- Performance: X/100 (Weight: 20%)
- Code Quality: X/100 (Weight: 20%)
- Style & Standards: X/100 (Weight: 15%)
- Architecture: X/100 (Weight: 10%)
- Documentation: X/100 (Weight: 10%)

### Key Strengths:
- [Bullet point]
- [Bullet point]

### Areas for Improvement:
- [Bullet point with brief explanation]
- [Bullet point with brief explanation]

### Priority Issues:
1. [Most critical issue with example]
2. [Second most critical issue with example]
```

## Scoring Guidelines

1. **Be objective**: Base scores on observable code characteristics, not subjective preferences
2. **Be consistent**: Use the same criteria across all reviews
3. **Be fair**: Consider the context (prototype vs production, complexity of domain)
4. **Be specific**: Provide concrete examples for score deductions
5. **Be actionable**: Focus on what can be improved
6. **Be balanced**: Acknowledge both strengths and weaknesses
