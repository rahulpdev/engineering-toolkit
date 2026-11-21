# Templates — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-project%20kickoff-5b3cc4)

## Overview

This folder holds the documents a new project is started from, and the two templates that every slash command and sub-agent is generated from. Each is copied into the project and filled in there; none is edited in place. The project documents form a chain: the idea intake captures a hypothesis, the blueprint turns it into a brief for Product Management and Engineering (who write the PRD, the product requirements document, and the TAD, the technical architecture document, from it), and a codebase setup specification, kept in `.agents/reference/` because an agent reads it as instructions and it is never filled in, then tells a planning agent and an implementation agent how to build the repository's foundation in validated, committed steps before any feature is written. The README and `CLAUDE.md` templates are used at the last step of that build. They are shared by every kind of project, and each setup specification's appendix supplies the parts that belong to its own stack. The folder installs into a project as `.agents/templates/`; `/draft-project-document` copies the software blueprint from that path, and each setup specification's Day-0 kit names the README and `CLAUDE.md` templates by that path. `/meta:create-command` and `/meta:create-agent` load the slash-command and sub-agent templates from that path too.

## Key Features

- A kickoff chain from idea intake to a built foundation, with each document feeding the next
- A software blueprint that separates what the client wants (intent) from how to build it (design), marking the rare deliberate mechanism explicitly
- README and `CLAUDE.md` templates that divide descriptive from normative content so the two never restate each other
- Two generation templates that give every slash command and sub-agent the same shape

## Documents

Each item below is a file in this folder. The project documents come first, in the order a project uses them, followed by the two generation templates.

- [`idea_template.md`](idea_template.md): **OKR idea intake** — twenty-three questions that capture a new idea's problem, users, outcomes, scope, constraints, risks and focus before any planning.
- [`template_software_blueprint.md`](template_software_blueprint.md): **Software project blueprint** — Sections 1-4 define context, requirements, scope and exclusions as question-and-answer prompts; Section 5 is the agency's own questions, NFRs and risk register; Sections 6-10 instruct Product Management and Engineering on writing the PRD and TAD. Blueprint wording is intent unless marked **Deliberate**.
- [`workflow_blueprint.md`](workflow_blueprint.md): **n8n workflow blueprint** — the same kickoff shape for an n8n automation: triggers, inputs, steps, outputs, external services, edge cases, a Mermaid diagram, NFRs and a question log.
- [`template_readme.md`](template_readme.md): **README template** — the section order, headings, formatting and voice of an application's `README.md`, for every kind of project; descriptive only, pointing to `CLAUDE.md` for commands and conventions. Its stack-specific parts are stack blocks filled from the setup specification's appendix, and a section with no equivalent for a stack keeps a "Not applicable" line. Its API samples are placeholders to replace.
- [`template_claude_md.md`](template_claude_md.md): **CLAUDE.md template** — the application's global rules for coding agents, for every kind of project: principles, stack, architecture, code style, logging, testing, error handling, development commands, communication standard and agent instructions. Its stack-specific parts, including the fixed code examples, are stack blocks filled from the setup specification's appendix; real code is pointed to through the reference table in Section 8, never copied.
- [`custom_command_template.md`](custom_command_template.md): **Slash-command template** — the copy/paste template every command is generated from, with instructions to the creating agent on argument handling, process-step writing and the choice between a human-readable report and a structured agent handoff.
- [`subagent_template.md`](subagent_template.md): **Sub-agent template** — the template every sub-agent is generated from, with three decisions resolved before writing (invocation mode, handoff mode, artefact mode) and a YAML handoff schema the primary agent acts on.

## Maintenance

When adding or changing files in this folder:

- Keep this README list in sync with the files present, with the project documents in the order a project uses them.
- A change to the slash-command or sub-agent template changes every command or sub-agent created afterwards; re-check `/meta:create-command` or `/meta:create-agent`, whichever loads it.
- Each setup specification lists its Day-0 kit and expected final layout; when a template is renamed or moved, update both specifications in `.agents/reference/` and `/draft-project-document`.
- A change to the README or `CLAUDE.md` template that adds, renames or removes a stack block is made to every setup specification's appendix in the same commit.
