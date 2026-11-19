<!--
TEMPLATE — template_claude_md.md
Produces the repository's CLAUDE.md. Keep every section, heading, ordering and
formatting exactly as written. Text in [square brackets] is a slot: replace it
with this application's content from the PRD and TAD, then remove the brackets.
A slot of the form [Stack block: name] is replaced by the block of that name in
the appendix of the codebase setup specification, and that block's own slots
are filled the same way. Everything outside brackets is kept as written. The
finished file states every rule in its own words: no line names the PRD or the
TAD or cites a section of either. The code examples are kept as written too:
they show format, and their customer and order names are placeholders. Only
their error codes change, and only where this application's error-code format
differs from the one they use. Delete this comment block from the finished
file.
-->

# [Application name] — Global Agent Rules

## 1. Core Principles

**VERBOSE NAMING IS NON-NEGOTIABLE**

- Clarity over brevity, always

**STRUCTURED JSON LOGGING IS MANDATORY**

- Every operation logs start + completion (or failure) with contextual fields
- Dotted namespace events: `domain.component.action_state`
- [Stack block: correlation-ID rule]

**SECURITY AND DATA HANDLING ARE NON-NEGOTIABLE**

- Never read, modify, or commit files containing API keys, tokens, credentials, or private certificates
- Never commit sensitive configuration files, private data files, or files with embedded plaintext secrets
- [Stack block: secret storage rule]
- Ensure compliance with relevant data protection regulations (e.g., GDPR, CCPA)

**TYPE SAFETY IS REQUIRED**

[Stack block: type safety rules]

**REQUIREMENT ALIGNMENT IS REQUIRED**

- Maintain a three-way match between: the requirements the implementation plan was written from, the implementation plan, and the final code
- When a change makes any statement in this file untrue, correct this file in the same change

[Stack block: documentation comment rule]

**KISS** (Keep It Simple, Stupid)

- Prefer simple, readable solutions over clever abstractions
- Commands and scripts never bring in a second programming language or an undeclared package; general command-line tools such as `git`, `grep` and `curl` are allowed, and a further package becomes a declared dependency first

**YAGNI** (You Aren't Gonna Need It)

- Defer building features until they're actually needed

**SOLUTIONS MUST BE GROUNDED**

- Demonstrate solutions are grounded in project docs, existing code, or verified research.

---

## 2. Tech Stack

[Stack block: tech stack]

---

## 3. Architecture

[Stack block: architecture]

---

## 4. Code Style

Code examples in this file show format only. Their customer and order names are placeholders, not part of this application; the files to imitate are listed in Section 8.

### Size limits

- **Files:** [the file size limit from Section 2.3 of the codebase setup specification] lines max — refactor into modules when approaching this limit
- **Functions:** 50 lines max — extract helpers if a function grows beyond this
- **Parameters:** Move constants, configurations, and long strings to separate files.

### Naming

[Stack block: naming]

[Stack block: documentation comments]

### ORM models — always use shared mixins

[Stack block: ORM models]

### Schemas

[Stack block: schemas]

---

## 5. Logging

[Stack block: logger setup]

**Event name format:** `domain.component.action_state`

- Good: `orders.checkout.validation_started`, `billing.invoice.generation_failed`
- Bad: `validation_started`, `failed`, `checkout`

**States:** `_started`, `_completed`, `_failed` (general); `_validated`, `_rejected` (validation operations)

**Always include contextual fields; never log bare messages.**

[Stack block: logging example]

---

## 6. Testing

### Test locations

[Stack block: test locations]

### Rules

- Tests must cover happy paths, edge cases, boundary conditions, and failure/error paths
[Stack block: test rules]

### Unit test example

[Stack block: unit test example]

[Stack block: second test example]

---

## 7. Error Handling

**Error code format:** [the error-code format for this application and its domain list] -- e.g., `ORDERS_INPUT_EMPTY_CART`, `BILLING_PROVIDER_TIMEOUT`

[Stack block: error model]

---

## 8. Common Patterns

Each pattern has one reference implementation in the repository. Read the file for the pattern you are about to write before writing it, and add a row when a pattern first appears.

| Pattern | Reference file |
| ------- | -------------- |
[One row per pattern the repository already implements, each naming a file that exists: at minimum [Stack block: minimum patterns]. A pattern with no implementation yet has no row.]

- [Where reference material for recurring patterns lives under `.agents/reference/`, or that it is to come.]

---

## 9. Development Commands

```bash
# Setup — NEVER edit dependency declarations directly, always use the package manager's add / remove commands
# Dependencies — update as part of the same change whenever packages are introduced or removed
[Stack block: development commands]
```

---

## 10. Communication Standard

If the text of the file named below is not already in your context, read it in full before your first message to the user.

@.agents/reference/communication-standard.md

---

## 11. AI Agent Instructions

<!-- Rebuild this list from the sections present in the finished file; every item must point at a section that exists. -->

1. **Match the vertical slice** per Section 3
2. **Log every operation** per Section 5
3. **Use verbose field names** per Section 4
4. [Stack block: fourth agent instruction]
5. [Stack block: fifth agent instruction]
6. **Write colocated tests** per Section 6
7. **Run linters and type checkers before finishing** per Section 9
8. **No suppression comments without a documented reason** per Section 1
9. **Never import across feature slices** per Section 3
10. **Imitate the reference implementations** per Section 8
11. **Never use git commands:** `git add .`, `git add -A` or `git add --all`
12. **Communicate with the user** per Section 10
