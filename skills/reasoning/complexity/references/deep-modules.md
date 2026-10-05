# Deep modules

How to shape a module so it pulls complexity downwards. Read when proposing a new module, shaping its interface, or judging whether an existing one is shallow.

## Terms

**Module**: anything with an interface and an implementation. Scale-agnostic: a function, a class, a package, a slice spanning tiers.

**Interface**: everything a caller must know to use the module correctly. That is the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics. It is wider than the `interface` keyword or a class's public methods.

**Depth**: leverage at the interface, meaning the behaviour a caller (or test) gets per unit of interface it has to learn. A module is **deep** when a lot of behaviour sits behind a small interface, and **shallow** when the interface is nearly as complex as the implementation.

```
Deep                         Shallow
┌──────────────┐             ┌──────────────────────────┐
│  interface   │             │        interface         │
├──────────────┤             ├──────────────────────────┤
│              │             │  implementation          │
│implementation│             └──────────────────────────┘
│              │
└──────────────┘
```

Depth pays out twice: **leverage** for callers (one implementation serves N call sites and M tests) and **locality** for maintainers (change, bugs, and verification concentrate in one place; fix once, fixed everywhere).

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be built from small, swappable parts inside. They just aren't part of its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through: fold it into its caller. If complexity reappears across its callers, it was earning its keep.
- **Depth is leverage, not a line ratio.** Padding the implementation doesn't make a module deeper; hiding more of what callers would otherwise have to know does.

## Shaping an interface

Ask, in order:

1. Can I reduce the number of entry points?
2. Can I simplify the parameters, or give the common case defaults?
3. Can I hide more complexity inside: an ordering constraint, an error the module could handle, configuration it could derive?

Before settling, sketch a second interface that differs in kind (fewer entry points, or one built around the most common caller) and keep whichever is deeper. The first idea is rarely the best one.

## Deepening moves

- **Merge a shallow cluster.** Several small modules that must be understood together, and change together, become one module with one interface.
- **Fold a pass-through into its caller.** When the deletion test says it carries nothing.
- **Absorb what callers repeat.** Setup, validation, or error handling copied across call sites moves behind the interface.

How the deepened module is tested depends on its dependencies: see [seams.md](seams.md).
