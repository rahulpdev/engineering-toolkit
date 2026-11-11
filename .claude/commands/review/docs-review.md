---
description: Audit README.md against the current codebase changes; produce a structured agent handoff with all required updates for a downstream agent to execute.
argument-hint: "<report-path> (required - path to change-review report YAML file)"
allowed-tools: Read, Glob, Grep, AskUserQuestion
---

# /docs-review: Pre-Merge README Audit

## Philosophy (Why this exists)

README.md can drift out of alignment with the codebase over time. This command catches those gaps. It is purely diagnostic — it operates on the structured output of `/change-review`, which establishes the scope of changes in the codebase, and it produces a structured handoff for a downstream agent to execute any required fixes. This creates a clean separation of concerns: this command diagnoses, another command fixes.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/docs-review .agents/reports/review/change-review-2026-03-30-143022.yaml`

**Arguments received**

- All args as a single string: `$ARGUMENTS`

**Arguments policy**

- **Mandatory**: `$ARGUMENTS` is required. If missing or invalid, stop and ask.

**Argument contract**

- Required args: `$ARGUMENTS` = path to a change-review report YAML file (produced by `/change-review`)
- Optional args: None
- Defaults: None
- Validation rules: File must exist and be a valid change-review YAML report

**If arguments are missing/invalid**

- Stop and ask the user for the report path. Suggest running `/change-review` first if no report exists.

## Context to Load (INPUT)

**Read these files (auto-load into context)**

- The change-review report file at the path provided in `$ARGUMENTS`
- @.agents/reference/repo_change_hygiene.md

## Process (PROCESS)

Follow these steps in order:

1. **Load scope from change-review report.**
   - Read the YAML report file at `$ARGUMENTS`.
   - Validate it is a well-formed change-review report (has `status`, `changed_files`, etc.).
   - From the flat list of changed file paths, exclude files that definitively cannot affect documentation (e.g., lockfiles, ignore files, generated files).
   - If all changed files are excluded, skip subsequent steps and produce the handoff with `status: success` and a summary indicating no documentation updates are needed.

2. **Assess README.md state.**
   - Check whether `README.md` exists in the repo root. If it does not exist, record its creation in the handoff and note that a comprehensive project documentation review may be needed beyond the scope of the changed files.
   - If it exists, read its contents in full.
   - Identify which sections are present (e.g., overview, installation, setup, usage, API reference, CLI usage, FAQs, contributions, license).

3. **Compare changes against README.md.**
   - For each changed file not excluded in Step 1, read its contents and determine what documentation impact it has.
   - Flag:
     - New features, commands, or APIs not documented in README.md.
     - Setup or installation steps that have changed but README.md still reflects the old process.
     - Removed or renamed features still referenced in README.md.
     - New dependencies or configuration requirements not mentioned.
     - Code examples or paths in README.md that no longer match the codebase.
   - Record all required changes: specific sections to add, update, or remove, with concrete edit instructions.

4. **Produce the structured agent handoff.**
   - Review all recorded changes from Step 3.
   - Do **not** apply any changes.
   - Do **not** write any files or create any artifacts. This step produces a response only.
   - Package **all** required changes into the **Structured Agent Handoff** format below.
   - If no issues were found, produce the handoff with `status: success` and a summary indicating no documentation updates are needed.

**Decision discipline**

- If you must make assumptions: list them explicitly and keep them minimal.
- If blocked by missing info: stop and ask targeted questions.
- If a change's documentation impact is unclear, err on the side of flagging it with a note explaining the uncertainty.

**Quality/Safety constraints**

- Do not modify any files. This command is read-only.
- Do not add speculative or unverified content to edit instructions — flag uncertainties for the downstream agent or user to resolve.
- Stage nothing and commit nothing.

## Output (OUTPUT)

### Structured Agent Handoff (for AI agents)

Return a single structured block that another agent can execute without conversation context.

**Required format (YAML)**
Include only non-empty fields. Omit empty lists/objects entirely.

```yaml
source_review: docs-review
status: # success | partial | blocked
summary: # one sentence describing what was audited and what needs to happen next

file_changes:
  # File edits the downstream agent must apply, in order (omit if none)
  - path: # relative path to the file to edit (e.g., "README.md")
    change_type: # create | modify
    instructions:
      -  # explicit edit instruction (e.g., "Add a 'Configuration' section after 'Installation' documenting the new ENV variables")
      -  # one instruction per discrete change


# Optional (include only when relevant)

# assumptions:
#   - # assumption made during the audit

# blockers:
#   - # what is blocking and what input is needed
```
