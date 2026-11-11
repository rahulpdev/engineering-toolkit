# Claude Code Sub-Agents — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-sub%20agents-5b3cc4)

## Overview

This folder contains Claude Code sub-agent definitions: single-purpose Markdown files (with YAML frontmatter) that a primary agent can delegate to for specialized reasoning tasks during PIV Layer 2 planning. Each sub-agent encapsulates a distinct role — framed with an explicit philosophy, invocation policy, INPUT → PROCESS → OUTPUT contract, decision discipline, and primary-agent handoff policy — so that it can be invoked deterministically and its output consumed downstream without ambiguity. Use sub-agents when you want to run a task in parallel worktrees or you want a focused agent to execute a narrowly scoped task and are prepared to lose its context at the end of the task.

## Key Features

- Role-separated sub-agents for cognitively independent reasoning (e.g., generation vs. evaluation)
- Explicit invocation policies stating when to invoke and when not to invoke each agent
- Structured INPUT → PROCESS → OUTPUT contracts for predictable, chainable handoffs
- YAML frontmatter declaring model, effort, tool permissions, and color for the harness
- Strict decision discipline (minimize assumptions, stay in scope, cite `path:line` evidence)
- Stop-and-wait handoff policies that keep the human in the decision loop

## Documents

Each item below is a sub-agent definition in this folder.

- [`document-reviewer.md`](document-reviewer.md): **Document Reviewer** — takes the path to the writing standard and the path to one document, reads the standard and then the document once from start to finish as a first-time reader with no drafting context, and returns every place that reader stumbles as a YAML handoff: location, exact quote, what could not be understood, the standard's rule where one applies, and a plainer wording where one is apparent. Reads nothing else, never edits, and does no fact-checking or mechanical checks. Writes no artifact itself; its handoff tells the primary agent to save the YAML to `docs/reports/reviews/document-reviewer-<YYYYMMDD-HHmmss>-<document>.yaml` (gitignored) and then apply or refuse each finding, without re-invoking the reviewer on the same version. Runs on `sonnet` with high effort and read-only tools (Read, Glob, Grep). Satisfies the writing standard's Writing review, which requires a reader who took no part in drafting.
- [`navigator.md`](navigator.md): **Navigator** — takes a problem definition file and multiple solution option files as input, derives testable evaluation criteria from the problem definition, assesses each option against every criterion using a `strong` / `partial` / `weak` scale with `path:line` evidence, performs comparative analysis, assesses reversibility, surfaces unstated premises, and produces a complete best-to-worst ranking. Writes an evaluation report artifact alongside the problem-definition file in `.agents/plans/artifacts/<slug>/` as `<slug>-options-evaluation-<YYYYMMDD-HHmmss>.md` (deriving the slug from the folder name) and returns a structured YAML handoff; explicitly does not advocate for any option or generate new ones. Runs on `opus` with high effort and read/search-only tools (Read, Write, Glob, Grep). Maps to Stage 5 (Option evaluation) of the structured planning framework.
- [`pathfinder.md`](pathfinder.md): **Pathfinder** — takes a well-defined problem definition (problem, constraints, success criteria, scope) plus the project files named in the invocation (typically the PRD, the TAD, `CLAUDE.md` and `README.md`; it stops if none are named) and produces exactly one concrete, implementation-ready solution option. Surveys at least three structurally distinct approaches before selecting and developing the strongest candidate into a full option with design decisions, components, implementation outline, fitness assessment, trade-offs, risks, reversibility, decision sensitivity, and neutral observations on alternatives considered. Runs on `sonnet` with high effort and read/inspect-only tools (Read, Glob, Grep, Bash); performs no file mutations. Maps to Stage 4 (Option generation) of the structured planning framework.

## Maintenance

When adding or changing sub-agents in this folder:

- Keep this `README.md` list in sync with the sub-agent files present.
- Each sub-agent file should declare its role, invocation policy, INPUT → PROCESS → OUTPUT contract, decision discipline, and primary-agent handoff policy.
- Update the description here whenever a sub-agent's responsibilities, inputs, outputs, or handoff policy change.
