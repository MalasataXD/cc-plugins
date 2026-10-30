# Code Review Scoring Rubric

Score the pinned target, not the repository around it, from 0 to 100 in each category. A category the target doesn't touch scores `N/A`. Every score below 90 names the findings that cost it.

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

### 2. Performance (Weight: 15%)

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

### 3. Quality & Maintainability (Weight: 20%)

**Score Range:**
- **90-100**: Clear, well-structured, and easy to change.
- **75-89**: High quality code with minor readability or structure improvements possible.
- **60-74**: Adequate quality but needs refactoring for better maintainability.
- **40-59**: Poor code organization, difficult to understand or modify.
- **20-39**: Serious code quality issues (deeply nested logic, unclear intent).
- **0-19**: Unmaintainable code (spaghetti code, no structure).

**Key Factors:**
- The `code-smells` baseline

### 4. Complexity (Weight: 10%)

**Score Range:**
- **90-100**: Deep interfaces; nothing a cold reader must know is left unstated.
- **75-89**: Minor obscurity (an unstated invariant, an unexplained unit) with local impact.
- **60-74**: A change here forces edits in several places, or callers carry knowledge the implementation should absorb.
- **40-59**: High cognitive load: correct use requires knowledge the code does not surface.
- **20-39**: Unknown unknowns likely: it is not evident which code must change or what must be known to change it safely.
- **0-19**: Pervasive tactical shortcuts; every future change is amplified and unsafe.

**Key Factors:**
- Change amplification: one conceptual change, how many edit sites
- Cognitive load: what a developer must hold in their head to use this correctly
- Unknown unknowns: invariants or coupling nothing in the code reveals
- Dependencies: fewer, simpler, more obvious
- Obscurity: names, units, and invariants evident from the code itself
- Complexity pulled downwards: hard parts absorbed by the implementation, not exported to callers

### 5. Style & Standards (Weight: 10%)

**Score Range:**
- **90-100**: Perfectly follows style guide and coding standards.
- **75-89**: Mostly compliant with minor style inconsistencies.
- **60-74**: Some style violations but generally consistent.
- **40-59**: Frequent style violations affecting readability.
- **20-39**: Inconsistent style throughout, difficult to read.
- **0-19**: No adherence to any coding standards.

**Key Factors:**
- Naming conventions (variables, functions, classes)
- Code organization and file structure
- Language-specific idioms and best practices
- Consistency with existing codebase patterns
- Use of modern language features appropriately

### 6. Architecture & Design (Weight: 10%)

**Score Range:**
- **90-100**: Responsibilities sit in the right place and dependencies point the right way.
- **75-89**: Good design with minor architectural improvements possible.
- **60-74**: Acceptable design, but it departs from the codebase's established shape.
- **40-59**: Poor architectural choices or misuse of design patterns.
- **20-39**: Architectural anti-patterns present.
- **0-19**: No discernible architecture, chaotic design.

**Key Factors:**
- Separation of concerns
- Dependency direction
- Seams justified by a real need
- Layer separation (presentation, business logic, data access)
- Consistency with existing codebase architecture
- Interface design and contracts

### 7. Documentation (Weight: 10%)

**Score Range:**
- **90-100**: Public interfaces and non-obvious behaviour are documented, and nothing restates the code.
- **75-89**: Good documentation with minor gaps.
- **60-74**: Basic documentation present but incomplete.
- **40-59**: Minimal documentation, key areas undocumented.
- **20-39**: Sparse or misleading documentation.
- **0-19**: No documentation or completely incorrect documentation.

**Key Factors:**
- Public interface documentation
- Class and module documentation
- Complex logic explanation
- API documentation
- Inline comments for non-obvious code
- README or usage documentation
- Documentation accuracy and clarity

## Overall Score Calculation

Take the weighted average of the scored categories, dividing by the sum of their weights so an `N/A` adds nothing to the total. Round to the nearest whole number.
