# Claude Code Skills — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-skills-5b3cc4)

## Overview

This folder contains Claude Code skills: one folder per skill, each holding a `SKILL.md` with YAML frontmatter and any supporting files it links to. Claude reads a supporting file only when `SKILL.md` tells it to, so long or verbatim material can sit in its own file. The frontmatter names the skill, describes when to use it, and can stop Claude from starting it on its own (`disable-model-invocation: true`), so that it runs only when invoked as `/<name>`.

## Key Features

- One folder per skill, with `SKILL.md` as the entry point and supporting files beside it
- Frontmatter that controls whether Claude may start a skill on its own or only when the user invokes it
- Verbatim text kept in its own file, so every use copies the same words

## Documents

Each item below is a skill folder in this directory.

- [`task-structuring/`](task-structuring/SKILL.md): **Task Structuring** (`/task-structuring`) — turns an unstructured or incomplete request into a tightly scoped work brief for another LLM. It recaps the request, lists any clarifications needed, then writes the brief under six fixed headings from [`schema.md`](task-structuring/schema.md), ending with the conduct reminders copied verbatim from [`conduct-reminders.md`](task-structuring/conduct-reminders.md), and repeats the brief in one Markdown block for copying. Manual only (`disable-model-invocation: true`).

## Maintenance

When adding or changing skills in this folder:

- Keep this `README.md` list in sync with the skill folders present.
- Give every `SKILL.md` a `name` and a `description` that says when to use the skill, and link every supporting file from `SKILL.md`.
- Set `disable-model-invocation: true` for a skill that should run only when the user invokes it.
