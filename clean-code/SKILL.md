---
name: clean-code
description: Use when writing, refactoring, or reviewing code at the function, class, and module level: naming, function design, SOLID, error handling, tests, and code smells.
---

# Clean Code

Apply this skill whenever you produce or review code. System structure questions (service boundaries, layering across the system, data ownership) belong to the `software-architecture` skill. For the test-first workflow, use the `tdd` skill. For the reasoning behind a design choice (is this good design, is it over-engineered, which non-functional requirements matter), use the `software-design` skill. When planning or reviewing a refactor, use the `refactor-proposal` skill.

## How to apply
1. Make it correct and covered by tests first. Then clean it.
2. Walk every section below. Fix what matters and don't gold-plate.
3. When principles conflict, choose deliberately and state the trade-off in one line (see **Tensions**).
4. When reviewing, order findings by severity: correctness, then design, then readability, then style. Name the principle and show the fix in code.

## Naming
- Names reveal intent: what it is and why it exists, not how it works.
- Avoid abbreviations, type encodings, and noise words (`Manager`, `Data`, `Info`, `Helper`) unless they are real domain terms.
- Classes are nouns, methods are verbs, and booleans read as predicates (`isActive`, `hasExpired`).
- Use one word per concept across the codebase. Pick one of `get`, `fetch`, or `retrieve`.
- Name length grows with scope. Short names are fine for tiny scopes, and wide scopes need descriptive names.

## Functions
- A function does one thing at one level of abstraction. Read top-down (stepdown rule).
- Keep functions small. If you need a comment or blank line to separate sections, extract a function.
- Use three parameters or fewer. Group related ones into a parameter object.
- Don't use boolean flag arguments. Split into two well-named methods.
- Avoid hidden side effects. Apply command-query separation: a function either changes state or returns a value.
- Prefer returning new values to mutating arguments.

## Classes and modules
**SOLID**
- **SRP**: one reason to change, meaning one actor or stakeholder.
- **OCP**: extend behavior by adding types or strategies, not by editing switch statements.
- **LSP**: subtypes honor the base contract. Don't override a method only to throw `UnsupportedOperationException`.
- **ISP**: prefer small, client-specific interfaces to fat ones.
- **DIP**: depend on abstractions. High-level policy never imports low-level detail.

**Also**
- High cohesion inside a unit, low coupling between units.
- Law of Demeter: talk to direct collaborators. Avoid chains like `a.getB().getC().doX()`.
- Prefer composition to inheritance.
- Tell, don't ask: put behavior next to the data it uses. Getters and setters that expose internals are fine only on DTOs.
- Prefer immutability: final fields and value objects.
- Avoid primitive obsession. Introduce value types such as `EmailAddress`, `Money`, and `OrderId`.

## General principles
- **DRY** applies to knowledge, not text. Two similar code blocks that change for different reasons are not duplication.
- **KISS**: use the simplest design that works.
- **YAGNI**: don't build for requirements you don't have yet.
- **Least astonishment**: code does what its name and signature suggest.
- **Boy Scout rule**: leave code cleaner than you found it. Keep refactors in separate commits from behavior changes.
- No magic numbers or strings. Use named constants or enums.

## Comments
- Code explains *how*. Comments explain *why*: constraints, non-obvious decisions, warnings, and public API contracts.
- Delete commented-out code, redundant comments, and change-log comments.
- Every TODO needs an owner or a ticket.

## Error handling
- Throw exceptions rather than returning error codes.
- Don't return null. Return `Optional`, an empty collection, or a Null Object.
- Fail fast and validate input at boundaries.
- Throw specific exception types with useful context.
- Never swallow exceptions. Catch generic `Exception` only at a top-level boundary.
- Keep try blocks small and separate error handling from the happy path.
- Don't use exceptions for control flow.

## Tests
- Follow FIRST: fast, independent, repeatable, self-validating, and timely.
- Each test covers one behavior, uses Arrange-Act-Assert, and has a descriptive name (`shouldRejectOrder_whenStockIsInsufficient`).
- Test behavior through the public API, not implementation details.
- Hold test code to production standards.
- Design for testability: inject dependencies and avoid static or global state.

## Formatting
- Follow the project's formatter and linter. Consistency beats personal preference.
- Keep related code close together and order it top-down, callers before callees.

## Concurrency (when relevant)
- Minimize shared mutable state. Prefer immutable data and thread confinement.
- Keep concurrency mechanics separate from business logic.

## Code smells and refactorings
| Smell | Refactoring |
|---|---|
| Long method | Extract Method |
| Large class / god service | Extract Class, split by use case |
| Long parameter list | Introduce Parameter Object |
| Feature envy | Move Method |
| Data clumps, primitive obsession | Introduce Value Object |
| Switch on type | Replace Conditional with Polymorphism |
| Shotgun surgery | Move related logic together |
| Divergent change | Split by reason to change |
| Message chains | Hide Delegate |
| Speculative generality, dead code | Delete it |

## Tensions between principles
- **DRY vs. decoupling**: across module or service boundaries, accept duplication rather than create shared coupling.
- **Small functions vs. readability**: don't fragment logic into one-line wrappers that force constant jumping between functions.
- **Abstraction vs. YAGNI**: introduce an abstraction at the second or third concrete case (rule of three), not the first.
- **Performance vs. clarity**: write for clarity first. Optimize measured hotspots and comment why.

## Java / Spring Boot notes
- Use constructor injection with `final` fields. Don't use field `@Autowired`.
- Keep controllers thin: map HTTP to DTOs and delegate to services.
- Never expose JPA entities through the API. Map them to DTOs, and use `record`s for DTOs and value objects.
- Put `@Transactional` at the service or use-case boundary, not on controllers.
- Use `Optional` only as a return type, never for fields or parameters.
- Centralize exception-to-HTTP mapping in `@RestControllerAdvice`.
- Split god services by use case.

## Review output format
For each finding, give:
- the location
- the principle it violates
- the problem
- the suggested fix, in code

End with the top three priorities. Skip anything the formatter already handles.
