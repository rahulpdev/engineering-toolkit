# Claude Code Sub-Agents — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-sub%20agents-5b3cc4)

## Overview

This folder contains Claude Code sub-agent definitions: single-purpose Markdown files (with YAML frontmatter) that a primary agent can delegate to for specialized tasks. Each sub-agent encapsulates a distinct role — framed with an explicit philosophy, invocation policy, INPUT → PROCESS → OUTPUT contract, decision discipline, and primary-agent handoff policy — so that it can be invoked deterministically and its output consumed downstream without ambiguity. Use sub-agents when you want to run a task in parallel worktrees or you want a focused agent to execute a narrowly scoped task and are prepared to lose its context at the end of the task.

## Key Features

- Role-separated sub-agents for cognitively independent reasoning (e.g., generation vs. evaluation)
- Explicit invocation policies stating when to invoke and when not to invoke each agent
- Structured INPUT → PROCESS → OUTPUT contracts for predictable, chainable handoffs
- YAML frontmatter declaring model, effort, tool permissions, and color for the harness
- Strict decision discipline (minimize assumptions, stay in scope, cite `path:line` evidence)
- Explicit handoff policies stating whether the primary agent acts on the result or waits for the user

## Documents

Each item below is a sub-agent definition in this folder.

- [`document-reviewer.md`](document-reviewer.md): **Document Reviewer** — takes the path to the communication standard and the path to a document, reads the standard and then the document as the user the standard describes, with no knowledge of the conversation that produced it, and records every place where the document breaks a rule of the standard: location, exact quote, how the rule is broken, the rule's number and name, and a suggested wording where the meaning is clear enough to offer one. Reads nothing else, changes no existing file, and does not check whether the document's claims are true. Writes its findings to `docs/reviews/` as `document-reviewer-<YYYY-MM-DD>-<document name>.md` and returns them as a YAML handoff that tells the primary agent to correct each finding or leave it without waiting for the user, to tell the user about any finding it left that affects what the user would understand, and not to re-invoke the reviewer on the same document unless the user asks. Runs on `sonnet` with high effort and two tools (Read, Write).
- [`navigator.md`](navigator.md): **Navigator** — takes a problem definition file and multiple solution option files as input, derives testable evaluation criteria from the problem definition, assesses each option against every criterion using a `strong` / `partial` / `weak` scale with `path:line` evidence, performs comparative analysis, assesses reversibility, surfaces unstated premises, and produces a complete best-to-worst ranking. Writes an evaluation report alongside the problem-definition file in `docs/options/` as `<slug>-options-evaluation.md` (deriving the slug from the problem-definition filename), reads the communication standard before writing that report, has the document-reviewer sub-agent read it and corrects its wording without changing any ranking, score or rating, and returns a structured YAML handoff; explicitly does not advocate for any option or generate new ones. Runs on `opus` with high effort and tools limited to reading, searching, writing and correcting its own report, and starting the reviewer (Read, Write, Edit, Glob, Grep, Agent). Maps to Stage 5 (Option evaluation) of the structured planning framework.
- [`pathfinder.md`](pathfinder.md): **Pathfinder** — takes a well-defined problem definition (problem, constraints, success criteria, scope) plus the project files named in the invocation (typically the PRD, the TAD, `CLAUDE.md` and `README.md`; it stops if none are named) and produces exactly one concrete, implementation-ready solution option. Surveys at least three structurally distinct approaches before selecting and developing the strongest candidate into a full option with design decisions, components, implementation outline, fitness assessment, trade-offs, risks, reversibility, decision sensitivity, and neutral observations on alternatives considered. Runs on `opus` with xhigh effort and read/inspect-only tools (Read, Glob, Grep, Bash); performs no file mutations. Maps to Stage 4 (Option generation) of the structured planning framework.

## Maintenance

When adding or changing sub-agents in this folder:

- Keep this `README.md` list in sync with the sub-agent files present.
- Each sub-agent file should declare its role, invocation policy, INPUT → PROCESS → OUTPUT contract, decision discipline, and primary-agent handoff policy.
- Update the description here whenever a sub-agent's responsibilities, inputs, outputs, or handoff policy change.
