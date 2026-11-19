# Agent Reference Files — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-standards%20and%20guides-5b3cc4)

## Overview

This folder holds the files that commands and sub-agents read while they run, and the guides that explain the thinking behind them. It installs into a project as `.agents/reference/`, and the path matters: `/meta:create-command` and `/meta:create-agent` load the two templates from here, the four review-chain audits load `repo_change_hygiene.md` from here, `/draft-project-document` and `/drafting:seamless-edit` load `communication-standard.md` from here and stop if it is missing, and every command, skill and sub-agent that starts the document reviewer hands it that file's path. Two files are design documents whose tooling has not been built; they are marked as such below. The vertical-slice architecture guide that the codebase setup specifications and `/plan:set-heading` can use is not in this folder, because it is Rasmus Widing's work; a project that needs it places the author's copy at `.agents/reference/vertical-slice-architecture-setup-guide.md`.

## Key Features

- The two generation templates that give every command and sub-agent the same shape
- A communication standard for an agent's messages to the user and the documents it writes
- The repository hygiene rules the pre-merge review chain audits against
- The eight-stage planning framework the planning chain implements
- One-time setup instructions for the worktree workflow

## Documents

Each item below is a file in this folder.

- [`custom_command_template.md`](custom_command_template.md): **Slash-command template** — the copy/paste template every command is generated from, with instructions to the creating agent on argument handling, process-step writing and the choice between a human-readable report and a structured agent handoff.
- [`subagent_template.md`](subagent_template.md): **Sub-agent template** — the template every sub-agent is generated from, with three decisions resolved before writing (invocation mode, handoff mode, artefact mode) and a YAML handoff schema the primary agent acts on.
- [`communication-standard.md`](communication-standard.md): **Communication standard** — who the reader is and the rules for writing messages to the user and documents, with short examples.
- [`repo_change_hygiene.md`](repo_change_hygiene.md): **Repository change hygiene** — the README, dependency, ignore-file, configuration and secrets rules that `/review:hygiene-review`, `/review:deps-review`, `/review:config-review` and `/review:docs-review` audit against.
- [`integration_branch_setup.md`](integration_branch_setup.md): **Integration branch setup** — the workflow behind `/new-worktree integration` and `/merge-worktrees integration`, the eleven one-time steps that satisfy their preconditions, and which steps still apply without an integration branch.
- [`structured_solution_planning.md`](structured_solution_planning.md): **Structured solution planning** — an eight-stage problem-solving framework (frame, build context, define, generate options, evaluate, structure, validate, plan) mapped onto the planning chain, with the competencies and failure modes of each stage.
- [`piv_loop_reference.md`](piv_loop_reference.md): **PIV loop reference** — a summary of the Plan, Implement, Validate development loop, its command system, the five-level validation pyramid and the practice of evolving commands and rules from each loop's friction.
- [`classify_command_processes.md`](classify_command_processes.md): **Classifying command processes by determinism** — a framework for deciding which steps of a command need an AI's judgement and which should be a script, plus specifications for two meta commands that would apply it. Specification only: neither meta command has been built.
- [`convert_command_to_skill.md`](convert_command_to_skill.md): **Commands versus skills** — how Claude Code slash commands and skills differ, how a skill is ported to Codex, and specifications for two conversion scripts with error codes and rollback rules. The reference section predates three facts: commands and skills are now one feature, a skill inside a group subfolder is not found, and a skill can run in a separate agent. The two scripts have not been built.
- [`external_services.md`](external_services.md): **Third-party external services** — rules for requesting, validating and storing credentials and for integrating an external service.
- [`delivery_and_deployment.md`](delivery_and_deployment.md): **CI/CD and deployment** — digest-pinned image deployment to DigitalOcean App Platform with Terraform, and Python module resolution inside Docker.
- [`LLM_docs.md`](LLM_docs.md): **Documentation links** — the official Claude Code and Codex pages on skills and sub-agents.

## Maintenance

When adding or changing files in this folder:

- Keep this README list in sync with the files present.
- A change to either template changes every command or sub-agent created afterwards; re-check the meta commands that load it.
- A change to `communication-standard.md` or `repo_change_hygiene.md` changes the behaviour of the commands and skills that read it at run time; re-read them.
- Mark any file that specifies unbuilt tooling as such in its entry here.
