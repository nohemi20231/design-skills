---
name: software-design
description: Use when deciding how to design code or a change before writing it, reviewing a pull request for design quality, or judging whether a design is "good". Covers what design actually is, just-in-time design, the economics of change, minimalism versus extensibility, cohesion and coupling, readability, non-functional requirements, and analysis versus design. Use it whenever someone asks "is this good design?", "should I make this extensible?", "how should I structure this?", "is this over-engineered?", or pauses to think about how to approach a change, even if they never say the word "design".
---

# Software Design

This skill is about the *reasoning* behind design decisions at any level. The `clean-code` skill gives the rules for functions, classes, and modules. The `software-architecture` skill covers structure above the class level (layers, services, data ownership). Use this skill to decide *whether* a design is good and *why*, and to keep the other two skills from being applied blindly.

## What design is

Design is the mapping of the requirements to the underlying languages, libraries, and frameworks to solve a given problem.

Three consequences follow, and they shape everything else in this skill:

- **If the requirements change, or the language, library, or framework changes, the design changes accordingly.** A library that evolves and gains a feature can make a simpler solution possible, so the design should move with it.
- **Two engineers given the same problem produce different designs**, because each has a different understanding of the requirements and of the tools. Neither is automatically wrong. Judge a design against the requirements and the tools, not against your own habits.
- **Design always happens.** A developer cannot code without designing. The pause when you stop typing and think, or when your pair goes quiet for a few seconds before answering, is design happening in the code. That is *just-in-time design*. The real question is never "did we design?" but "did we do good design, or accidental design?"

### Analysis versus design

Analysis is taking the time to understand, refine, define, and explain the requirements, often in a technology-independent or technology-agnostic way. Design is done with regard to the underlying technology. Do the analysis first. Most bad designs are good designs of the wrong problem.

## What good design is

### The economics of change

A good design is not one that correctly predicts the future. It is the one that makes accommodating future needs more affordable. When the requirements evolve, the design has to evolve, and it all comes down to the economic impact of that change.

Code gets harder to maintain as it grows. Creating a simple design takes a lot more effort than creating a complex one. So:

- **Minimalism is the key criterion for a good design.** A minimal design is easier to evolve than a complex, overreaching one.
- **Extensibility is a slippery slope.** In the name of extensibility we may overly complicate solutions and actually make it harder to extend in the future.
- **When the requirements change, your design has to evolve.** The skill is to keep that change to a minimum, not to have predicted it.
- **Do not apply principles for their own sake.** Emphasize the context and how you benefit from a principle. If applying it leaves you with unnecessary complexity, you have misused it.

### Characteristics of a good design

When you look at a pull request and ask "is this good, is it OK, does it need improvement?", check these, roughly in order of weight:

| Characteristic | What to ask |
|---|---|
| Simple, fewer moving parts | Is there anything here the requirements do not need? |
| Relevant | Does it meet the requirements and the use cases, no more and no less? |
| High cohesion | Does each unit do one thing and one thing only? |
| Low, loose coupling | Does it depend on stable things (interfaces) rather than unstable ones (concrete classes)? |
| Readable, understandable | Can a teammate with similar background read the intent without asking? |
| Easy to test | If you catch yourself saying "hmm, this code is hard to test", the design needs to change. Hard to test is a design signal, not a testing problem. |
| Easy to change, maintainable | How much would the obvious next requirement cost? |
| Right level of abstraction | Are details hidden where they belong, and nothing abstracted that has only one use? |
| Robust | How does it handle errors and failure? Is the error handling in one place? |
| Good structure | Is the code organized so the reader finds things where they expect them? |
| Flexible, extensible, reusable | Treat these as *warnings*, not goals. Each is a slippery slope toward complexity. Only pursue them when a requirement asks for them. |

### Cohesion

Cohesion means code that does one thing and one thing only: narrow and focused. That is the same idea as the Single Responsibility Principle. The short form is: **like things are together, and unlike things are apart.**

Care about cohesion because it minimizes the code, and the frequency of change over time. Every change to a low-cohesion unit risks the other things it does. Cohesion has an economic impact, which is why it ranks above most other characteristics.

### Coupling

Aim for low coupling and loose coupling.

Loose coupling means **depend on what is more stable.** An interface is more stable than a class, so depend on the interface. If what you depend on is less stable, such as a concrete class, that dependency will drag you along every time it changes. This is the practical form of the Dependency Inversion Principle.

### Readability

Readability is the measure of how easy it is for *others* to understand the code, where "others" means people with a similar background and the necessary skills. It is not about the least experienced reader imaginable.

So if everybody on a team has the same level of understanding and the code still does not communicate its intent, that is when the code is unreadable. The fix is to make the code communicate intent, not to add comments explaining what it does.

## Design principles

The notes below are the principles in their shortest form. Use them as lenses, with the context warning above in mind. `clean-code` has the full rules and refactorings.

- **Single Responsibility (SRP)**: a class should have only one reason to change, meaning a single well-defined responsibility.
- **Open/Closed (OCP)**: software entities (classes, modules) should be open for extension but closed for modification. Extend functionality without altering the correctness of the program.
- **Liskov Substitution (LSP)**: subtypes (derived classes) must be substitutable for their base types (parent classes) without altering the correctness of the program.
- **Interface Segregation (ISP)**: clients should not be forced to depend on interfaces they don't use. Prefer smaller, focused interfaces.
- **Dependency Inversion (DIP)**: high-level modules should not depend on low-level modules; both should depend on abstractions. This decouples components through abstractions and interfaces.
- **YAGNI and DRY** are the fundamental principles under all of the above. YAGNI keeps the design minimal. DRY keeps one piece of knowledge in one place.
- **Object-oriented design and inheritance**: inheritance is one tool for extension. Reach for it when there is a real "is-a" relationship and the LSP holds. Otherwise prefer composition.

## Non-functional requirements

Non-functional requirements are the characteristics of an application rather than its features. The design has to account for the ones that matter for this system, and ignoring them is how a "good" design fails in production:

- scalability
- performance
- security
- reliability
- portability
- configurability
- upgradability

Before designing, ask which of these are real requirements here and which are not. Designing for a non-functional requirement nobody has is the extensibility slippery slope in another costume.

## How to apply

### Before coding (the just-in-time design pause)

1. Restate the requirement in one or two sentences. If you cannot, do analysis first.
2. Name the non-functional requirements that actually apply.
3. Sketch the smallest design that meets the requirement with the tools you have. Say what it depends on and whether those things are stable.
4. Ask what the next likely change is and what it would cost. Do not build for it. Make sure it would be affordable.
5. If the design is hard to test, change the design, not the tests.

### Reviewing a pull request

Walk the characteristics table. For each finding, give:

- the characteristic it weakens
- the economic consequence (what future change gets more expensive, or what breaks)
- the smaller alternative

Order findings by cost of leaving them: cohesion and coupling first, then testability and robustness, then readability. Finish by naming anything in the change that exists for a requirement nobody has, and recommend removing it.

### When tempted to add extensibility

Ask: which requirement asks for this? If none does, write down the simpler design and note the one place a future change would touch. That note is cheaper than the abstraction and usually enough.
