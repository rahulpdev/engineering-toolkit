# Claude Code Output Styles — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-output%20styles-5b3cc4)

## Overview

This folder contains Claude Code output styles: Markdown files with YAML frontmatter that replace how Claude Code behaves and responds for a whole session. Each file's frontmatter gives the style's `name`, a one-line `description`, and `keep-coding-instructions`, which says whether Claude Code keeps its built-in software engineering instructions alongside the style. The body is the style's instructions. A style is chosen per session from Claude Code's output style setting.

## Key Features

- Session-wide roles for work that is not coding, such as shaping an idea before any planning starts
- Frontmatter that names each style and states whether the coding instructions stay in force
- Plain Markdown bodies that can be edited like any other prompt

## Documents

Each item below is an output style in this folder.

- [`project-ideator.md`](project-ideator.md): **Project Ideator** — turns a vague software idea into one Objective with three to five measurable Key Results. It questions the idea in rounds across problem, value, scope and risk, explains likely technical blockers in plain English, keeps an assumption ledger and a decision log, and delivers the final OKR package in one Markdown block for the next stage of planning. Drops Claude Code's coding instructions (`keep-coding-instructions: false`).

## Maintenance

When adding or changing output styles in this folder:

- Keep this `README.md` list in sync with the output style files present.
- Give every style the three frontmatter fields `name`, `description` and `keep-coding-instructions`.
- Set `keep-coding-instructions: true` only for a style meant to be used while writing code.
