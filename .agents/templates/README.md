# Project Templates — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-project%20kickoff-5b3cc4)

## Overview

This folder holds the documents a new project is started from. Each is copied into the project and filled in there; none is edited in place. They form a chain: the idea intake captures a hypothesis, the blueprint turns it into a brief for Product Management and Engineering (who write the PRD, the product requirements document, and the TAD, the technical architecture document, from it), and a codebase setup specification then tells a planning agent and an implementation agent how to build the repository's foundation in validated, committed steps before any feature is written. The README and `CLAUDE.md` templates are used at the last step of that build. The folder installs into a project as `.agents/templates/`; `/drafting:draft-blueprint` copies the software blueprint from that path, and each setup specification's Day-0 kit names the README and `CLAUDE.md` templates by that path.

## Key Features

- A kickoff chain from idea intake to a built foundation, with each document feeding the next
- A software blueprint that separates what the client wants (intent) from how to build it (design), marking the rare deliberate mechanism explicitly
- Two foundation specifications, one for a Python backend and one for an Obsidian plugin, each with fixed conventions, a Decision Register for the few project-specific choices, and a definition of done
- README and `CLAUDE.md` templates that divide descriptive from normative content so the two never restate each other

## Documents

Each item below is a file in this folder, in the order a project uses them.

- [`idea_template.md`](idea_template.md): **OKR idea intake** — twenty-three questions that capture a new idea's problem, users, outcomes, scope, constraints, risks and focus before any planning.
- [`template_software_blueprint.md`](template_software_blueprint.md): **Software project blueprint** — Sections 1-4 define context, requirements, scope and exclusions as question-and-answer prompts; Section 5 is the agency's own questions, NFRs and risk register; Sections 6-10 instruct Product Management and Engineering on writing the PRD and TAD. Blueprint wording is intent unless marked **Deliberate**.
- [`workflow_blueprint.md`](workflow_blueprint.md): **n8n workflow blueprint** — the same kickoff shape for an n8n automation: triggers, inputs, steps, outputs, external services, edge cases, a Mermaid diagram, NFRs and a question log.
- [`ai_optimized_codebase_setup.md`](ai_optimized_codebase_setup.md): **Codebase setup specification, Python** — twelve sequential steps that build a Python 3.12, FastAPI, Supabase and Docker foundation with Ruff, MyPy, Pyright and pytest, structured JSON logging with correlation IDs and a canonical error model; fixed conventions, a Decision Register resolved from the PRD and TAD, a Day-0 kit, a suppression loop after every step from Step 8, and a definition of done. Needs the vertical-slice architecture guide, which the project owner supplies.
- [`ai_optimized_codebase_setup_obsidian_plugin.md`](ai_optimized_codebase_setup_obsidian_plugin.md): **Codebase setup specification, Obsidian plugin** — the same shape for a TypeScript plugin: compiler and type-aware lint as the type-safety layers, a core separated from the Obsidian host through ports so it can be tested without Obsidian, bundle and release checks in place of containers, and tests inside a real Obsidian. Needs the same guide and the Obsidian plugin development reference the specification names.
- [`template_readme.md`](template_readme.md): **README template** — the section order, headings, formatting and voice of an application's `README.md`; descriptive only, pointing to `CLAUDE.md` for commands and conventions. Its API samples are placeholders to replace.
- [`template_claude_md.md`](template_claude_md.md): **CLAUDE.md template** — the application's global rules for coding agents: principles, stack, architecture, code style, logging, testing, error handling, development commands, human-communication rules and agent instructions. Code examples are fixed format samples; real code is pointed to through the reference table in Section 8, never copied.
- [`template_readme_obsidian_plugin.md`](template_readme_obsidian_plugin.md): **README template, Obsidian plugin** — mirrors `template_readme.md` section for section, departing only where a plugin cannot follow a service, and adds the Disclosures section the Obsidian community directory requires.
- [`template_claude_md_obsidian_plugin.md`](template_claude_md_obsidian_plugin.md): **CLAUDE.md template, Obsidian plugin** — mirrors `template_claude_md.md` section for section for a TypeScript plugin; sections with no plugin equivalent keep a "Not applicable" line.

## Maintenance

When adding or changing files in this folder:

- Keep this README list in sync with the files present and in the order a project uses them.
- Each setup specification lists its Day-0 kit and expected final layout; when a template is renamed or moved, update both specifications and `/drafting:draft-blueprint`.
- Keep the Python and Obsidian pairs aligned section for section; a change to one template's structure is made to its pair in the same commit.
- Bump the version line in a specification whenever its steps change.
