# Standalone Prompts — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-chat%20prompts-5b3cc4)

## Overview

This folder holds prompts that are pasted into a chat with a model. None is a slash command and nothing installs them; each is used by copying its text. Two of them are generators: they ask a model to design a reusable template, and they produced the first versions of the software blueprint and the n8n workflow blueprint now kept in `.agents/templates/`. The other three are working prompts: a system prompt for a second model that reviews a first model's engineering work, a prompt that reorders a plan around external-service setup, and a one-line instruction for continuing a document in its own voice.

## Key Features

- Generator prompts whose outputs became maintained templates, so the lineage of the templates is visible
- A two-model review setup with a structured report and a follow-up prompt written for the first model
- Short, single-purpose prompts that compose with any conversation

## Documents

Each item below is a file in this folder.

- [`blueprint_template_generator.md`](blueprint_template_generator.md): **Blueprint template generator** — a first-person brief from a non-technical product manager asking a model to build a reusable project-blueprint template that prompts for up-front questions, future-proofs the design and plans an MVP-first delivery. Paste as the first message when a new template of this kind is wanted.
- [`n8n_workflow_template_generator.md`](n8n_workflow_template_generator.md): **n8n workflow template generator** — the same brief specialised for n8n workflow projects stored in git and deployed through CI/CD; it ends by asking for the template alone. Paste as the first message.
- [`senior_engineer_reviewer.md`](senior_engineer_reviewer.md): **Senior engineer reviewer** — a system prompt for a second model acting as a senior software engineer who reviews a junior model's work, reports in a fixed format with a confidence check, and writes the follow-up prompt to send back. Use as the reviewing model's system prompt.
- [`group_external_service_setup.md`](group_external_service_setup.md): **Group external service setup** — asks a model to revise an implementation plan so that configuring external services interrupts coding as little as possible, with a non-technical setup guide per service. Paste after the plan, in the same chat.
- [`match_existing_style.md`](match_existing_style.md): **Match existing style** — one line instructing a model to continue a document in the tone, structure and formatting of its existing text, as if the original author had written it. Prefix it to an editing request.

## Maintenance

When adding or changing files in this folder:

- Keep this README list in sync with the files present.
- Name each file for what the prompt does, not for the tool or project it was first used with.
- When a generator's output is adopted as a template, keep the generator here and note the template it produced in its entry.
