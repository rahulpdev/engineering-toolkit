---
description: Audit ignore lists and scan for secrets in the current codebase; produce a structured agent handoff with all required fixes for a downstream agent to execute.
argument-hint: "<report-path> (required - path to change-review report YAML file)"
allowed-tools: Read, Glob, Grep, Bash(git:*), AskUserQuestion
---

# /hygiene-review: Pre-Merge Ignore List & Secrets Audit

## Philosophy (Why this exists)

Ignore lists can drift out of alignment with the codebase over time, and secrets can inadvertently appear in changed files. This command catches those gaps. It is purely diagnostic — it operates on the structured output of `/change-review`, which establishes the scope of changes in the codebase, and it produces a structured handoff for a downstream agent to execute any required fixes. This creates a clean separation of concerns: this command diagnoses, another command fixes.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/hygiene-review .agents/reports/review/change-review-2026-03-30-143022.yaml`

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

1. **Load and validate the change-review report.**
   - Read the YAML report file at `$ARGUMENTS`.
   - Validate it is a well-formed change-review report (has `status`, `changed_files`, etc.).

2. **Confirm no secrets in changed files.**
   - Read the contents of all changed files from the report and scan for plaintext secrets, API keys, tokens, or credentials. Secrets can appear in any file type.
   - If secrets are found, stop and alert the user immediately. Do not proceed to subsequent steps. Do not produce a structured handoff.

3. **Audit ignore lists.**
   - Locate `.gitignore` in the repo root (and `.dockerignore` if the project uses Docker, e.g., a `Dockerfile` or `docker-compose.yml` exists). If a required ignore file does not exist, record its creation in the handoff.
   - For each changed file path from the report, determine whether that file should be ignored:
     - Sensitive configuration files (e.g., `.env`, credentials, private keys).
     - Auto-generated files and build artifacts.
     - Data files (e.g., `.csv`, `.xlsx`).
     - Temporary, system-generated, and environment-specific files.
   - For any flagged file, check whether it is already covered by the relevant ignore list:
     - For `.gitignore`: run `git check-ignore` to verify coverage.
     - For `.dockerignore` (if applicable): read the file and compare against its patterns.
   - Record all required changes: ignore list entries to add and system commands to execute.

4. **Produce the structured agent handoff.**
   - Review all recorded changes from Step 3.
   - Do **not** apply any changes.
   - Do **not** write any files or create any artifacts. This step produces a response only.
   - Package **all** required changes into the **Structured Agent Handoff** format below.
   - If no issues were found, produce the handoff with `status: success` and a summary indicating no issues were found.

**Decision discipline**

- If you must make assumptions: list them explicitly and keep them minimal.
- If blocked by missing info: stop and ask targeted questions.

**Quality/Safety constraints**

- Do not modify any files. This command is read-only.
- Stage nothing and commit nothing.

## Output (OUTPUT)

### Structured Agent Handoff (for AI agents)

Return a single structured block that another agent can execute without conversation context.

**Required format (YAML)**
Include only non-empty fields. Omit empty lists/objects entirely.

```yaml
source_review: hygiene-review
status: # success | partial | blocked
summary: # one sentence describing what was audited and what needs to happen next

file_changes:
  # File edits the downstream agent must apply, in order (omit if none)
  - path: # relative path to the file to edit
    change_type: # create | modify
    instructions:
      -  # explicit edit instruction (e.g., "Add '.env' to .gitignore")
      -  # one instruction per discrete change

actions:
  # System commands the downstream agent must execute, in order (run after file_changes)
  # Examples: git rm --cached, git clean, git add --renormalize
  - cwd: # working directory (repo-relative or absolute)
    run: # exact shell command to execute
    expected_outcome: # what success looks like (exit code, file updated, output pattern)
    on_failure: # what to check or do if the command fails


# Optional (include only when relevant)

# assumptions:
#   - # assumption made during the audit

# blockers:
#   - # what is blocking and what input is needed
```
