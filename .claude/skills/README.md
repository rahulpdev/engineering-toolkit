# Claude Code Skills — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-skills-5b3cc4)

## Overview

This folder contains Claude Code skills: one folder per skill, each holding a `SKILL.md` with YAML frontmatter and any supporting files it links to. Claude reads a supporting file only when `SKILL.md` tells it to, so long or verbatim material can sit in its own file. The frontmatter names the skill and describes when to use it. It can also stop Claude from starting the skill on its own (`disable-model-invocation: true`), so that it runs only when invoked as `/<name>`, and can run the skill in a separate agent that has not seen the conversation (`context: fork`).

## Key Features

- One folder per skill, with `SKILL.md` as the entry point and supporting files beside it
- Frontmatter that controls whether Claude may start a skill on its own or only when the user invokes it
- Verbatim text kept in its own file, so every use copies the same words
- One skill for several variants of a task, with the steps that differ kept in a file per variant
- Skills that run in a separate agent, so the work is done without sight of the conversation and its detail stays out of it

## Documents

Each item below is a skill folder in this directory.

- [`check-ignore-comments/`](check-ignore-comments/SKILL.md): **Check Ignore Comments** (`/check-ignore-comments`) — finds every `noqa` and `type: ignore` comment in the codebase, investigates why each exists, and writes a dated report to `.agents/reports/` giving, per comment, the code, the reason it exists, resolution options with effort and impact, trade-offs, and a Remove / Keep / Refactor recommendation. The document-reviewer sub-agent then reads the report, and its findings are corrected. Runs in a separate agent that has not seen the conversation (`context: fork`).
- [`merge-worktrees/`](merge-worktrees/SKILL.md): **Merge Worktrees** (`/merge-worktrees`) — finalises a single piece of work by collapsing its worktree and branch back into the local `main` or `integration` branch. It takes a required kebab-case name, an optional base branch (default `main`) and an optional type (`feature`, `fix`, `chore` or `docs`, default `feature`), prepares a `--no-ff` merge of `<type>/<name>` without committing, validates the merged working tree with the checks of the project's tool set, read from [`python.md`](merge-worktrees/python.md) or [`pnpm.md`](merge-worktrees/pnpm.md), commits the merge only on success, then removes the worktree and deletes the work branch.
- [`new-worktree/`](new-worktree/SKILL.md): **New Worktree** (`/new-worktree`) — creates a single git worktree branched off the local `main` or `integration` branch on a branch named `<type>/<name>`. It takes a required kebab-case name, an optional base branch (default `main`) and an optional type (`feature`, `fix`, `chore` or `docs`, default `feature`), validates the name against reserved values, runs the preflight checks of the project's tool set, read from [`python.md`](new-worktree/python.md) or [`pnpm.md`](new-worktree/pnpm.md), checks the `worktrees/` ignore-rule, the base branch, existing worktree/branch, and remote freshness, creates the worktree at `worktrees/<type>-<name>`, installs dependencies, and confirms the resulting branch.
- [`task-structuring/`](task-structuring/SKILL.md): **Task Structuring** (`/task-structuring`) — turns an unstructured or incomplete request into a tightly scoped work brief for another LLM. It recaps the request, lists any clarifications needed, then writes the brief under six fixed headings from [`schema.md`](task-structuring/schema.md), ending with the conduct reminders copied verbatim from [`conduct-reminders.md`](task-structuring/conduct-reminders.md), and repeats the brief in one Markdown block for copying. Manual only (`disable-model-invocation: true`).
- [`technical-code-review/`](technical-code-review/SKILL.md): **Technical Code Review** (`/technical-code-review`) — audits scoped code changes for real technical issues via Git. It accepts optional context such as one or more commit hashes, a commit range, or a directory focus, reviews the resolved scope for logic, security, performance, and maintainability issues, verifies each finding against the actual code, writes a human-readable Markdown report with numbered findings to `.agents/reports/review/`, and has the document-reviewer sub-agent read the report before correcting its wording. Runs in a separate agent that has not seen the conversation (`context: fork`).

## Maintenance

When adding or changing skills in this folder:

- Keep this `README.md` list in sync with the skill folders present.
- Place each skill folder directly in this folder; Claude Code does not find a skill inside a group subfolder.
- Draft a skill by converting an existing command.
- Give every `SKILL.md` a `name` and a `description` that says when to use the skill, and link every supporting file from `SKILL.md`.
- Set `disable-model-invocation: true` for a skill that should run only when the user invokes it.
