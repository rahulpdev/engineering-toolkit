---
description: Create a new custom slash command in `.claude/commands/` using the standard template
argument-hint: "[extra-context] (optional - description, constraints, or examples for the command you want to create)"
allowed-tools: Read, Edit, Write, Glob, Grep, Agent, Bash(mkdir:*), Bash(ls:*), Bash(test:*), AskUserQuestion
---

# /create-command: Create a Custom Slash Command

## Philosophy (Why this exists)

This command exists to enforce a single standard and common structure for a growing command library by requiring the use of a shared template to draft every new command build.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/create-command`
- `/create-command Create a command that reviews a PR for security issues and produces an agent-readable checklist.`

**Arguments received**

- All args as a single string: `$ARGUMENTS`

**Arguments policy**

- **Optional**: `$ARGUMENTS` may be omitted. If omitted, rely on the current conversation context.

**Argument contract**

- Required args: None
- Optional args: `$ARGUMENTS` = extra context (desired behavior, constraints, examples, edge cases)
- Defaults (if any): Empty string
- Validation rules: None (free-form text)

**If arguments are missing/invalid**

- If the command-to-create’s specification is not clear from current context + `$ARGUMENTS`, stop and ask targeted questions (command name, audience, arguments, and allowed tools) before writing any files.

## Context to Load (INPUT)

**Read these files (auto-load into context)**

- @.agents/templates/custom_command_template.md

**Optional: capture live state (auto-run bash, if allowed)**

- !`ls -1 .claude/commands 2>/dev/null || echo "(commands directory not yet created)"`

## PROCESS

Follow these steps in order:

1. **Derive the new command’s spec from current context + `$ARGUMENTS`.**
   - Determine all required fields:
     - Command name (kebab-case; becomes both invocation `/name` and filename `name.md`)
     - Human-friendly title
     - 1-2 sentence frontmatter `description` written for an AI agent; imperative, unambiguous, and precise
     - Argument policy for the new command (None / Optional / Mandatory) and `argument-hint` (omit both if none)
     - Minimal `allowed-tools` set for the new command (least privilege)
     - Whether the new command saves a new file or edits an existing one
     - For a saved file: its path and naming rule, who it is written for, what to do if the file already exists, and its layout
     - Output consumer of the final response: **Human-Readable Report** or **Structured Agent Handoff** (ask if not explictly stated)
2. **Stop-and-ask gate (do not write files yet).**
   - If any of the following are unclear, stop and ask targeted questions:
     - The new command’s name (cannot be safely inferred)
     - Whether the new command saves a file
     - Where the saved file goes and what to do if it already exists (cannot be safely inferred)
     - The output consumer (human vs agent)
     - Any required arguments (and their validation rules)
     - Any tools that must be allowed (and why)
3. **Ensure the target directory exists.**
   - Run `mkdir -p .claude/commands`.
4. **Important: Draft the new command using the required template (do not draft freehand).**
   - Start by copying the template from `@.agents/templates/custom_command_template.md`.
   - Remove the template’s internal instruction comment before saving the final command.
   - Replace all placeholders with concrete content.
   - Delete any sections that do not apply (do not leave empty stubs).
   - Implement correct argument handling:
     - No args → omit `argument-hint` and do not reference `$ARGUMENTS` / `$1..$N`.
     - One argument blob → use `$ARGUMENTS`.
     - Multiple distinct args → use `$1`, `$2`, `$3`, ... and define each.
   - Write file paths so the new command runs from any repository on any machine:
     - Files inside the project the command runs in → paths relative to that project's root (e.g. `docs/blueprint.md`).
     - Files outside that project → home-relative paths with forward slashes (e.g. `~/Workspaces/engineering-toolkit/.agents/templates/template_software_blueprint.md`). Never write a drive letter, a user name, or backslashes.
     - Do not auto-load a home-relative path with `@`; list it as a file to read in full and have a process step read it, expanding `~` to the home folder.
     - In shell commands, leave a home-relative path unquoted so the shell expands `~`.
5. **Choose and keep exactly one output section for the new command’s final response.**
   - If the final response is for humans: keep **Human-Readable Report** and delete **Structured Agent Handoff**.
   - If the final response is for agents: keep **Structured Agent Handoff** and delete **Human-Readable Report**.
   - If the consumer is still not specified: stop and ask (do not guess).
6. **Validate the draft before saving.**
   - Confirm the new command contains:
     - Valid YAML frontmatter (`description`, optional `argument-hint`, `allowed-tools`)
     - A clear **Context to Load** section (only if needed)
     - A step-by-step **Process** where each step is verifiable
     - A **Saved File** section (only if the command saves a file)
     - An **Output** section that describes the final response only
     - No leftover placeholders (e.g., `{{...}}`) or template instructions
     - No absolute or machine-specific file paths (every path is project-relative or home-relative)
7. **Write the new command file as this command’s own SAVED FILE section below describes.**
8. **Run the document review.**
   - Start the `document-reviewer` sub-agent once, using the agent spawning tool with `subagent_type|agent_type: "document-reviewer"`, and pass it two paths and nothing else: the communication standard at `.agents/reference/communication-standard.md` and the file written in Step 7.
   - Follow the instruction that closes its response, except that you ignore any finding against a heading the template fixes.
   - After the edits, repeat the checks in Step 6 once.
9. **Handoff: produce the final response using this command’s own OUTPUT section below.**

**Decision discipline**

- If you must make assumptions: list them explicitly and keep them minimal.
- If blocked by missing info: stop and ask targeted questions (unless the new command’s argument contract says to fail fast).

**Quality/Safety constraints**

- Do not create or modify files outside `.claude/commands/` (except reading the required template) unless explicitly requested.
- Do not overwrite existing command files without explicit confirmation.
- Keep `allowed-tools` for the new command minimal (only what the command truly needs).
- Ensure the new command is internally consistent and ready to run without extra undocumented context.

## SAVED FILE

- **Path**: `.claude/commands/<command-name>.md`
- **Naming rule**: `<command-name>` is the new command’s kebab-case name from Step 1.
- **Written for**: the user, who reads it to check what the new command will do. The agent that runs the new command reads it too.
- **If the file already exists**: Stop and ask before overwriting.

**Layout**

The template at `.agents/templates/custom_command_template.md`, with its instruction comment removed, every placeholder replaced and every section that does not apply deleted.

## OUTPUT

### Human-Readable Report

Return a concise, easy-to-scan summary:

- **Status**: Success | Blocked
- **File**: the path of the new command file (or intended path if blocked)
- **Assumptions**: any assumption made while drafting, or `None`
- **Document review**: what the document-reviewer's closing instruction says to tell the user
- **Questions (only if blocked)**: numbered list

Repeat nothing that is in the new command file.

## Notes

- The template is the standard. If it seems insufficient for a particular command, the right move is to improve the template — not to bypass it.
- The `document-reviewer` sub-agent must be present in `.claude/agents/`, or the document review in Step 8 cannot run.
