# Seams

Where a module's interface lives, and how the module is tested there. Read when deciding where a seam goes, whether a new one is justified, or how to test a module across its dependencies.

## Terms

**Seam** (Michael Feathers): a place where behaviour can be altered without editing in that place. It is where a module's interface lives, and where tests sit. Where to put the seam is a decision separate from what goes behind it.

**Adapter**: a concrete thing that satisfies an interface at a seam: a Postgres repository, an in-memory fake, an HTTP client. The word names the role, not the size.

## Principles

- **The interface is the test surface.** Callers and tests cross the same seam. If a test has to reach past the interface, the module is the wrong shape.
- **One adapter means a hypothetical seam; two adapters mean a real one.** Introduce a seam only when something actually varies across it (typically production and test). A single-adapter seam is just indirection.
- **Internal seams stay internal.** A module may have seams inside its implementation for its own tests. Don't expose them through the interface because a test uses them.
- **Prefer existing seams, and the highest one that still observes the behaviour.**

## Dependency categories

Classify a module's dependencies; the category decides how it is tested across its seam.

1. **In-process**: pure computation or in-memory state. Test through the interface directly; no adapter needed.
2. **Local-substitutable**: has a local stand-in (PGLite for Postgres, an in-memory filesystem). Run the stand-in in the test suite. The seam stays internal.
3. **Remote but owned**: your own services across a network. Define a port at the seam; production gets an HTTP/gRPC/queue adapter, tests get an in-memory one.
4. **True external**: third-party services (Stripe, Twilio). Inject them as a port; tests provide a mock adapter.

## Designing for testability

- **Accept dependencies; don't construct them.** `processOrder(order, paymentGateway)` can be tested; a `processOrder(order)` that news up a `StripeGateway` cannot.
- **Return results rather than mutating.** `calculateDiscount(cart): Discount` can be asserted on; `applyDiscount(cart): void` has to be inspected from the side.
- **Keep the surface small.** Fewer entry points mean fewer tests; fewer parameters mean simpler setup.

## Replace, don't layer

When a cluster is deepened, write tests at the new interface and delete the old tests on the shallow modules it absorbed. Tests assert on observable outcomes through the interface, so they survive internal refactors. A test that has to change when only the implementation changed is testing past the interface.
