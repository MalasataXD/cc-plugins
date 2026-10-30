# Security Checklist

Trace the target, not the whole application. Find each trust boundary the change crosses, then follow untrusted data from its source to its sink. Untrusted data includes requests, files, webhooks, third-party responses, and model output. The sweep is done when every boundary has been traced. A control that may live outside the target, such as a gateway, is a question to raise, not a finding.

## Untrusted data reaching a sink

- **Queries**: Is data bound as parameters, including in raw ORM calls and dynamic `ORDER BY` clauses?
- **Commands**: Does the code pass an argument array rather than a shell string?
- **HTML**: Is output contextually encoded? Check raw-HTML paths such as `innerHTML` and `dangerouslySetInnerHTML`.
- **Paths**: Is the path canonicalized, then confirmed to sit inside the permitted root?
- **Outbound URLs**: Can the caller steer the destination, including through redirects? This is SSRF.
- **Redirects**: Is the target limited to known destinations?
- **Deserialization**: Can untrusted data reach `pickle`, unsafe YAML loading, Java object deserialization, or an XML parser with external entities enabled?
- **Code execution**: Can it reach `eval`, `exec`, `Function`, dynamic imports, or templates compiled from input?
- **Regular expressions**: Can input trigger catastrophic backtracking?
- **Object mapping**: Is input mapped to allowed fields only? Check mass assignment and prototype pollution.
- **Prompts and model output**: Can untrusted text steer an agent into using its tools? Is model output treated as untrusted before it reaches a sink?

## Who is acting

- **Object access**: Does each read and write confirm that this caller may touch this specific record, including tenant scope?
- **Function access**: Is authorization enforced server-side on every new route, job, and action?
- **Sessions and tokens**: Are cookies `Secure`, `HttpOnly`, and `SameSite`, and is the session rotated at login? Are a JWT's signature, algorithm, expiry, and audience verified?
- **Passwords**: Are they hashed with Argon2, scrypt, or bcrypt?
- **CSRF**: Do cookie-authenticated, state-changing requests carry a CSRF defence?
- **Webhooks**: Is the signature verified against the raw body?
- **Races**: Can a check-then-act sequence be raced, such as a balance check or a single-use token?

## Secrets and sensitive data

- **Secrets**: Are they kept out of code and config? Treat a committed secret as compromised and rotate it.
- **Logs and errors**: Do secrets, tokens, and personal data stay out of logs, traces, and error responses?
- **Responses**: Does each response return only the fields this caller may see?
- **Personal data**: Is new collection or sharing necessary, and is the data protected at rest?

## Cryptography

- Does the code use established libraries and authenticated encryption, such as AES-GCM or ChaCha20-Poly1305?
- Do tokens, keys, and nonces come from a secure random source, with nonces never reused?
- Are MD5 and SHA-1 absent from security-sensitive use?
- Are secrets compared in constant time?

## Files and resource limits

- **Uploads**: Are size and content type checked, with files stored outside the web root under non-guessable names?
- **Limits**: Do parsing, pagination, and new expensive or authentication endpoints have limits?

## Supply chain and configuration

- **Dependencies**: Is each new package needed, maintained, spelled correctly, and locked? Do lockfile changes match the manifest?
- **CI**: Does untrusted pull request data stay out of `run:` steps? Check `pull_request_target`, actions pinned to a commit SHA, and token permissions.
- **Configuration**: Check changed CORS rules, security headers, debug flags, TLS settings, and default credentials.

## C and C++

- Are copies bounded, using `snprintf`, `std::string`, or `std::span`?
- Are format strings constant?
- Check object lifetimes, use-after-free, and integer overflow before allocation.
