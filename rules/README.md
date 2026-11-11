# Global Rules And Personas — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-agent%20rules-5b3cc4)

## Overview

This folder holds two kinds of instruction for a model. `CLAUDE.md` is a stack-independent global-rules file for a coding agent: it is copied to the root of a repository that is not an application, such as a documentation or tooling repository, and governs how the agent works there. An application built with a codebase setup specification gets its `CLAUDE.md` generated from `.agents/templates/template_claude_md.md` instead, which carries the application's own stack and conventions. The three files under `personas/` are role instructions for a chat model, not Claude Code rules: each sets a mission, behaviours, tone and a fixed response format, and is pasted as the first message or system prompt of a chat.

## Key Features

- A lean global-rules file that covers operating principles, interaction, problem solving, code organisation, documentation, security, performance, testing, change management and git safety without naming a stack
- Persona prompts with fixed report formats, so a chat produces the same shape of output every time
- A clear rule for which `CLAUDE.md` a repository gets

## Documents

Each item below is a file in this folder.

- [`CLAUDE.md`](CLAUDE.md): **Global agent rules** — the rules a coding agent follows in a non-application repository: operating principles, user interaction, problem solving, task breakdown, code organisation and documentation, Python linting, security and secrets, performance, compliance, error handling, dependencies, testing, change management, assumption prevention and git safety.
- [`personas/qa_engineer.md`](personas/qa_engineer.md): **QA engineer** — a persona that finds bugs beyond the happy path, traces root causes, researches related issues, and reports in a fixed format with reproduction steps, environment, severity and a suggested fix.
- [`personas/ux_ui_strategist.md`](personas/ux_ui_strategist.md): **UX/UI strategist** — a persona that analyses competitors, trends and benchmarks and reports evidence-backed design implications in a fixed format.
- [`personas/community_post_writer.md`](personas/community_post_writer.md): **Community post writer** — a persona that turns frustrated developer notes into respectful, complete help requests shaped for Reddit, Stack Overflow, GitHub Issues or Discord.

## Maintenance

When adding or changing files in this folder:

- Keep this README list in sync with the files present.
- Keep `CLAUDE.md` stack-independent; stack-specific rules belong in `.agents/templates/template_claude_md.md`.
- Keep each persona's response format explicit so its output stays checkable.
