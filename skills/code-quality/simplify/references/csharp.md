# Simplify — C# / .NET

Apply these on top of the general principles. The project's `AGENTS.md` /
`CLAUDE.md` still wins over anything here.

> Tuned to your preferences — opinions about *clarity*, not a restatement of the
> standard C# conventions the model already knows. Edit freely.

- **Guard clauses over nesting.** Validate and return/throw early; keep the happy
  path unindented.
- **Readable LINQ only.** A short, single-purpose chain is fine; break a long or
  multi-stage pipeline into named steps, or use a `foreach` when it reads better.
  Avoid deeply nested or side-effecting LINQ.
- **Honest nullability.** Enable nullable reference types and model intent in the
  signatures; avoid the null-forgiving `!` unless you can justify it right there.
- **Async done right.** No `async` over sync, no `.Result` / `.Wait()` /
  `.GetAwaiter().GetResult()`. Propagate `CancellationToken`s; follow the
  project's `ConfigureAwait` stance.
- **Pattern matching / `switch` expressions** for multi-branch logic — never
  nested ternaries.
- **Expression-bodied members** only when the body stays trivially readable; use
  a block body for anything with real logic.
- **`var` when the type is obvious** from the right-hand side (`new()`, casts,
  clear factory calls); use an explicit type when it isn't.
- **Reach for modern features that cut ceremony:** `record` / `record struct` for
  data-carrying types (over classes with boilerplate, and over tuples whose
  elements carry meaning), **primary constructors** to trim constructor noise, and
  **collection expressions** (`[..]`) / target-typed `new` where they read
  cleanly. Defer to the project on namespace style.
- Naming: `PascalCase` members/types, `_camelCase` private fields (or the
  project's existing convention).
