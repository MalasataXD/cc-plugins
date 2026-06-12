# Simplify — TypeScript / React

Apply these on top of the general principles. The project's `AGENTS.md` /
`CLAUDE.md` still wins over anything here.

## TypeScript

- **ES modules** with sorted imports and explicit file extensions.
- Prefer the **`function` keyword** over arrow functions for top-level and named
  declarations. Arrow functions are fine for short inline callbacks.
- **Explicit return-type annotations** on exported / top-level functions. Let
  inference handle locals.
- Prefer **error handling without `try/catch`** when a cleaner path exists
  (result types, narrow guards, validating at the boundary). Keep `try/catch`
  where it genuinely belongs.
- Replace `any` with a real type or `unknown` + narrowing.
- Use `switch` or `if`/`else` chains for multiple conditions — **never nested
  ternaries**.
- Consistent naming: `camelCase` values, `PascalCase` types/components.

## React

- **Explicit `Props` type** for every component; no inline anonymous prop shapes
  on non-trivial components.
- Keep components focused — split when a component juggles too many concerns.
- Derive state instead of duplicating it; lift only when genuinely shared.
- Keep effects honest: correct dependency arrays, no logic that belongs in render
  or an event handler.
- Extract a hook or helper when the same logic repeats — but don't abstract a
  one-off.
