# Simplify — Python

Apply these on top of the general principles. The project's `AGENTS.md` /
`CLAUDE.md` still wins over anything here.

> Tuned to your preferences — opinions about *clarity*, not a restatement of
> PEP 8 (the model already knows that). Edit freely.

- **Guard clauses over nesting.** Return early on the invalid/edge case instead
  of wrapping the happy path in `if`.
- **Comprehensions: one level only.** A single `[x for x in xs if ...]` is clear;
  a nested or multi-`for` comprehension is not — use an explicit loop.
- **Explicit type hints** on public functions and dataclass fields. Skip them on
  obvious locals.
- **Error handling, mixed by context.** Use EAFP (try/except) for I/O and
  genuinely exceptional cases; use LBYL (check first) for cheap, predictable
  conditions. Always catch the **specific** exception — never bare `except:` —
  and don't swallow errors to make code look cleaner.
- Prefer a **`dataclass` or `NamedTuple`** over passing around tuples/dicts whose
  fields carry meaning.
- **f-strings** over `%`, `.format()`, or concatenation.
- Avoid clever one-liners (walrus chains, dense lambdas, `reduce`) when a named
  loop or helper reads better.
- Use `switch`-like `match` statements or `if`/`elif` chains for multi-branch
  logic — no ternary stacking.
