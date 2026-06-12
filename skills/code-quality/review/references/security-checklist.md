# Security Checklist for Code Review

## General Security Issues

### Input Validation
- Validate and sanitize all user inputs
- Check for proper type checking and bounds checking
- Validate file uploads (type, size, content)
- Prevent injection attacks through input sanitization

### Injection Vulnerabilities

#### SQL Injection
- Use parameterized queries or prepared statements
- Avoid string concatenation for SQL queries
- Use ORM frameworks properly
- Validate and escape user input in database queries

#### Command Injection
- Avoid executing shell commands with user input
- Use safe APIs instead of shell execution when possible
- Properly escape and validate arguments if shell execution is necessary
- Use allowlists for permitted commands

#### Cross-Site Scripting (XSS)
- Encode output when rendering user-provided data
- Use Content Security Policy (CSP) headers
- Sanitize HTML input
- Avoid `innerHTML` and similar dangerous DOM methods

#### Path Traversal
- Validate file paths against allowlists
- Use path normalization and canonicalization
- Avoid user input in file system operations
- Check for `../` sequences and absolute paths

### Authentication & Authorization
- Implement strong password requirements
- Use secure password hashing (bcrypt, Argon2, scrypt)
- Never store passwords in plain text
- Implement proper session management
- Use secure session tokens (random, unpredictable, sufficient entropy)
- Implement proper access control checks
- Validate authorization on every request
- Avoid relying on client-side authorization

### Sensitive Data Exposure

#### API Keys & Secrets
- Never hardcode API keys, passwords, or secrets
- Use environment variables or secure vaults for secrets
- Check for secrets in configuration files
- Ensure secrets are not logged or exposed in error messages
- Use `.gitignore` to prevent committing secrets

#### Data Encryption
- Use HTTPS/TLS for data in transit
- Encrypt sensitive data at rest
- Use strong encryption algorithms (AES-256, RSA-2048+)
- Avoid deprecated encryption methods (MD5, SHA1 for passwords, DES)

#### Personal Identifiable Information (PII)
- Minimize collection of PII
- Implement proper data retention policies
- Ensure PII is properly encrypted
- Comply with privacy regulations (GDPR, CCPA)

### Cryptography
- Use well-established cryptographic libraries
- Avoid custom cryptographic implementations
- Use secure random number generators
- Properly manage cryptographic keys
- Use appropriate key sizes
- Implement proper IV/nonce generation for encryption

### Error Handling & Logging
- Avoid exposing sensitive information in error messages
- Log security-relevant events
- Sanitize log output to prevent log injection
- Avoid logging sensitive data (passwords, tokens, PII)
- Implement proper error handling (avoid generic catch-all)

### Session Management
- Use secure, httpOnly, and sameSite cookies
- Implement proper session timeout
- Regenerate session IDs after authentication
- Implement secure logout functionality
- Protect against session fixation attacks

### Cross-Site Request Forgery (CSRF)
- Implement CSRF tokens for state-changing operations
- Use SameSite cookie attribute
- Validate origin and referrer headers
- Require re-authentication for sensitive operations

### XML/JSON Processing
- Prevent XXE (XML External Entity) attacks
- Disable external entity processing in XML parsers
- Validate JSON schema
- Implement size limits for parsed data

### File Operations
- Validate file types and extensions
- Implement file size limits
- Scan uploaded files for malware
- Store uploaded files outside web root
- Use unique, non-guessable filenames

### API Security
- Implement rate limiting
- Use API authentication (OAuth, API keys, JWT)
- Validate API request parameters
- Implement proper CORS configuration
- Version APIs properly

### Dependency Management
- Keep dependencies up to date
- Scan for known vulnerabilities in dependencies
- Use dependency lock files
- Avoid dependencies with security issues
- Review dependency licenses

## Language-Specific Considerations

### JavaScript/TypeScript
- Avoid `eval()`, `Function()`, and similar dynamic code execution
- Use strict mode
- Validate JSON parsing input
- Sanitize DOM manipulation
- Use TypeScript for type safety

### Python
- Avoid `exec()`, `eval()`, `__import__()`
- Use parameterized queries with database libraries
- Validate pickle deserialization sources
- Be cautious with `subprocess` and `os.system()`

### Java
- Avoid deserialization of untrusted data
- Use prepared statements for SQL
- Validate XML input
- Be cautious with reflection APIs
- Use security manager appropriately

### C/C++
- Prevent buffer overflows
- Use safe string functions (`strncpy`, `snprintf`)
- Avoid format string vulnerabilities
- Prevent memory leaks
- Validate array bounds
- Use smart pointers (C++)

### PHP
- Disable dangerous functions (`eval`, `system`, `exec`)
- Use prepared statements
- Validate `include`/`require` paths
- Escape output properly
- Configure PHP securely (`display_errors=off` in production)

### Go
- Validate SQL queries (use parameterized queries)
- Be cautious with `os/exec`
- Properly handle errors
- Validate template inputs
- Use context for timeouts and cancellation

## Infrastructure & Configuration

### Server Configuration
- Disable directory listing
- Remove default/sample files
- Configure security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- Implement HTTPS with strong TLS configuration
- Keep server software updated

### Access Control
- Implement principle of least privilege
- Use role-based access control (RBAC)
- Regularly review permissions
- Implement multi-factor authentication for sensitive operations

### Monitoring & Alerting
- Implement security monitoring
- Set up alerts for suspicious activities
- Regular security audits
- Implement intrusion detection
