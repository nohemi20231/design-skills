---
name: refactor-proposal
description: Use when planning, writing, or reviewing a refactor. Covers writing a refactor proposal (the ask, the benefits, what changes), deciding whether a new requirement needs a refactor first, hunting duplicated code and duplicated payloads, replacing flags and hard-coded values, centralizing error handling, judging a refactor pull request by how the tests changed, and automating validation with sample data. Use it whenever someone says "refactor", "clean this up before we add X", "this isn't scalable", "too many if/else", "we keep copying this", or a new requirement does not fit the current design, even if they never say "refactor".
---

# Refactor Proposal

A refactor is justified by a concrete new ask, not by taste. The proposal exists to show that the current design cannot take the new ask cheaply, and that a specific set of changes will make it affordable. The `software-design` skill explains why affordability of change is the measure. The `clean-code` skill has the catalog of smells and refactorings. The `tdd` skill governs how to keep behavior pinned while you change structure.

## Write the proposal first

Keep it short. Someone should be able to read it in two minutes and either agree or push back on a specific line.

```
# Refactor proposal: <area>

## The ask
<the new requirement, in one or two sentences>

## Why the current design cannot take it
<what you would have to duplicate, flag, or special-case to bolt it on>

## Benefits
<the changes necessary to adapt the current design and convert it to the new ask>
<what becomes cheaper for the asks after this one>

## What changes
<the list of concrete changes, each small enough to be one pull request>

## Duplicated code found
<the places that mean the same thing, including payloads>

## Open questions
<decisions about data ownership or lifecycle that the refactor forces>

## Validation
<the sample data and the automated checks that prove behavior is preserved>
```

The "benefits" section is the heart. Phrase it the way the notes do: the refactor "makes the changes necessary to adapt our current design and convert it to the new ask of adding X to our Y process." If you cannot name the ask, you are not refactoring, you are rewriting.

## What to look for

### Duplicated code, including payloads

Duplication is not only duplicated logic. Duplicated payloads, request and response shapes, DTOs, and mapping code count too, and they are the kind most often missed because each copy looks slightly different. Find code that means the same thing with different values and collapse it to one place with the value as data.

When you remove duplication of *data*, you inherit a decision about its lifecycle. Example from a claims system: the policy owner is copied into several places and gets updated. Is the owner something that should be static, a snapshot at the time of the claim, or should an update flow through the whole claim? The refactor cannot be finished until that is answered. Put questions like that in "Open questions" and get an answer before you collapse the copies.

### Hard-coded values that should be dynamic

If the design works only for the values it was written with, it is not scalable. The sign is code that is structurally identical but differs in a literal: a name, a type, a limit, a status. Pull the value out as data, configuration, or a parameter so the next value does not need new code.

### Flags

Try not to use flags. A flag almost always exists to drive an if/else somewhere else, which means the behavior lives in two places and the reader has to find both. Instead, have the thing mean what it means: a named type, a strategy, a value object, or two well-named methods. If a flag survives, it should be the exception you can explain.

### Values whose meaning is unclear

Before a refactor, teams often struggle because they are required to know exactly what an "I don't know" value means: a null, an empty string, a sentinel, a default. Define it explicitly as part of the refactor. An unknown value with an explicit type and name is cheap. An unknown value that every caller interprets differently is the hidden duplication that breaks things.

### Error handling in one place

Put the error handling in a single place, so that when an exception is thrown you can see how it is handled. Scattered try/catch blocks around duplicated code are a sign that the duplication is hiding inconsistent failure behavior. Centralize first, then you will know what the refactor is allowed to change.

## Judging a refactor pull request by its tests

The test diff tells you what the refactor really did, often more honestly than the description:

- **Many existing tests had to change** and the behavior did not: this probably means the code is coupled to concrete classes where it should depend on interfaces. Tests that reach through the interface should survive an internal reshuffle. Treat it as a signal to introduce the interface, not to rewrite the tests.
- **Many new tests had to be added**: this is probably a sign of extracting code out into its own new method or class. That is usually good. Check that the new tests cover the extracted unit and that the old tests still cover the caller.
- **Tests did not change at all**: the behavior is pinned. This is the refactor you want.
- **Tests were deleted**: ask why, every time.

Count the tests changed, added, and deleted, and say what the numbers suggest in the review.

## Automate the validation

Get sample data of the real inputs and the questions the system has to answer about them. Then create a method (or a test harness) that you can ask those questions and that gives the answer automatically. With enough data and automated validation, making changes becomes faster, because you can trust the automation to know the answer and have it fast and ready instead of re-checking by hand.

Concretely:

1. Collect a representative sample of real inputs, including the odd ones.
2. Record the expected answer for each, from the current system or from a domain expert.
3. Turn that into a table-driven test that runs in seconds.
4. Only then start the refactor. Every step must keep the table green.

## Steps

1. Write the proposal using the template, with the ask named.
2. Gather sample data and build the automated validation.
3. Resolve the open questions about data ownership and lifecycle.
4. Centralize error handling.
5. Refactor in small steps: one duplication, one flag, or one extraction per pull request, behavior unchanged, tests green.
6. Only after the structure is in place, make the behavior change the ask requires, in its own pull request.
