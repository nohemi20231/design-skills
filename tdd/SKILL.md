---
name: tdd
description: Use when implementing a feature or fixing a bug test-first: red-green-refactor cycles, choosing the next test, test doubles, and testing levels.
---

# Test-Driven Development

Work in small red-green-refactor cycles. The `clean-code` skill governs the refactor step and the quality of the test code itself.

## Before coding
1. Restate the behavior as concrete examples: inputs, expected outputs, and edge cases.
2. Write a test list of behaviors to cover, simplest first. Keep it visible and update it as you learn.
3. For a bug, write a test that reproduces the bug before you touch any code.

## The cycle
1. **Red**: write one small failing test for the next behavior on the list.
   - Run it and confirm it fails for the expected reason, not because of a compile error or a typo.
2. **Green**: write the minimum code that passes.
   - Faking the result or hard-coding a value is fine when it keeps the step small.
   - Run the whole relevant suite.
3. **Refactor**: with all tests green, remove duplication and improve names and structure. Apply `clean-code`.
   - Refactor the test code too.
   - Don't add behavior during this step.
4. Repeat. Each cycle should take minutes. If a step gets large, back out and pick a smaller test.

## Choosing the next test
- Start with the degenerate case: empty input, zero, null, or the simplest happy path.
- Then add one dimension of variation at a time.
- **Triangulate**: add a second example to force out the fake implementation.
- Leave error paths and boundaries for after the core behavior works, but before you call the feature done.

## Good tests
- Test observable behavior through the public API, never private methods or internals.
- Each test checks one behavior and is named for it (`shouldRejectOrder_whenStockIsInsufficient`).
- Structure each test as Arrange-Act-Assert. Keep tests independent and deterministic.
- Control time, randomness, and IDs by injecting them.
- A test that is hard to write is design feedback. Fix the design rather than forcing the test.

## Test doubles
- Prefer real objects and in-memory fakes.
- Mock only at architectural boundaries: external services, messaging, and the clock. Don't mock what you don't own.
  - Wrap third-party code in an adapter and test the adapter with integration tests.
- Verify interactions only when the interaction is the behavior, such as sending an event or an email.

## Testing levels
- **Unit tests** cover domain logic. These are the bulk of the suite.
- **Integration tests** cover adapters: repositories, HTTP clients, and messaging.
- **Contract tests** cover service-to-service APIs (consumer-driven).
- **End-to-end tests** cover a few critical user journeys only.
- Outside-in (double loop) for features:
  1. Start with a failing acceptance test.
  2. Drive the inner pieces with unit-level TDD.
  3. Finish when the acceptance test passes.

## Java / Spring Boot notes
- Use JUnit 5 and AssertJ. Use Mockito sparingly, and only at boundaries.
- Unit-test domain and service classes without Spring. Construct them directly.
- Use slice tests for adapters: `@WebMvcTest` for controllers and `@DataJpaTest` for repositories.
- Use Testcontainers for real databases and brokers in integration tests. Don't use H2 as a stand-in for Postgres.
- Reserve `@SpringBootTest` for a few wiring and acceptance tests.
- Use Spring Cloud Contract or Pact for contract tests.

## When reporting work
Show the test list and mark which items are done. For each cycle, show the test, why it failed, and the change that made it pass.
