<!--
TEMPLATE — template_readme.md
Produces the repository's README.md. Keep every section, heading, ordering and
formatting exactly as written. Text in [square brackets] is a slot: replace it
with this application's content from the PRD, the TAD and the code, then remove
the brackets. A slot of the form [Stack block: name] is replaced by the block of
that name in the appendix of the codebase setup specification, and that block's
own slots are filled the same way. Everything outside brackets is kept as
written, with one exception: the samples in the API Reference section (the
endpoint or operation sample and any sample header in its stack block, the
lifecycle diagram and the `BILLING_PROVIDER_TIMEOUT` row) show the form the
slots beside them take, and are replaced by this application's content. The
README describes the product the PRD and TAD define, and states nothing
beyond them. Delete this comment block from the finished file.
-->

# [Application name]

> [One-sentence description of what the application does for its user.]

[One badge per item in the tech stack, each of the form `![Tool](https://img.shields.io/badge/[tool]-[version]-[colour]?logo=[logo]&logoColor=white)`, followed by:]
![License](https://img.shields.io/badge/license-[licence]-lightgrey)

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Getting Started](#getting-started)
5. [Running the Application](#running-the-application)
6. [API Reference](#api-reference)
7. [CLI Usage](#cli-usage)
8. [Testing](#testing)
9. [Configuration](#configuration)
10. [Disclosures](#disclosures)
11. [FAQs](#faqs)
12. [Contributing](#contributing)
13. [License](#license)

---

## Overview

[What the application does and for whom; its main flow, as a numbered list where it has stages; and any retention or lifecycle fact a user must know. Written from the PRD.]

---

## Key Features

- **[Feature name]** — [what it does and the concrete guarantee: an endpoint or a command, a limit, a timing target]
- [One bullet per feature in the same form]
[Stack block: standard features]

---

## Architecture

[Stack block: architecture diagram]

---

## Getting Started

### Prerequisites

[One bullet per tool needed before the Installation steps, each of the form `- [Tool](link to its install page) — what it is for`, with the tools a user needs listed before the tools only a developer needs.]

### Installation

[Stack block: installation]

---

## Running the Application

[Stack block: running]

### Health checks

[Stack block: health checks]

---

## API Reference

[Stack block: API reference]

### Status lifecycle

[The status transitions as a plain-text diagram; name any value that is deliberately not valid.]

```
queued → processing → succeeded
                    → failed
```

### Error codes

[Stack block: error codes]

---

## CLI Usage

[Who the command-line interface is for, what it does, one example invocation in a `bash` block, and where its full contract is documented. With no command-line interface: None.]

---

## Testing

Test locations, conventions and commands are in [`CLAUDE.md`, Sections 6 and 9](CLAUDE.md).

---

## Configuration

[Stack block: configuration]

---

## Disclosures

[Stack block: disclosures]

---

## FAQs

[One entry per question a first-time user is likely to ask: the question in bold, a blank line, then a short answer in plain prose.]

**[Question?]**

[Answer.]

**Where can I find logs and diagnostics?**

[Stack block: logs answer]

---

## Contributing

[Who may contribute, in one sentence, e.g. "This is a private project. Contributions are by invitation only."]

Conventions for working on this codebase — architecture, branch naming, commit messages, pre-commit checks, tests — are in [`CLAUDE.md`](CLAUDE.md).

---

## License

[The licence statement, e.g. "Proprietary. All rights reserved.", one sentence on what that permits, and any third-party licence obligation the application carries.]
