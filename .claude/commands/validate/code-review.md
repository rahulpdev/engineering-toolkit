---
description: Audit scoped code changes for real technical issues via Git, then write a human-readable code review report with verified findings and concrete fix suggestions.
argument-hint: '[additional context] (optional - e.g., "review git commit abc123", "review git commit abc123 def456", "review git range abc123..def456", "focus on backend/")'
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(mkdir:*), Bash(date:*), Write, AskUserQuestion
---

# /code-review: Technical Code Review

## Philosophy (Why this exists)

Code can drift away from quality, security, and performance standards as it changes. This command catches those gaps by reviewing Git diffs together with full file context. Reviews favor readability, simplicity, and earned complexity, and flag only issues backed by evidence — not stylistic preferences.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/code-review`
- `/code-review review git commit abc123`
- `/code-review review git commit abc123 def456`
- `/code-review review git range abc123..def456`
- `/code-review focus on backend/`

**Arguments received**

- All args as a single string: `$ARGUMENTS`

**Arguments policy**

- **Optional**: `$ARGUMENTS` may be omitted. If omitted, review current working-tree, staged, and untracked changes.

**Argument contract**

- Required args: None
- Optional args: `$ARGUMENTS` = additional context to identify review scope, such as one or more commit hashes, one commit range, directories, or focus areas
- Defaults: When omitted, use current Git state
- Validation rules:
  - Free-form text is allowed.
  - Any referenced commit or range must resolve in Git.
  - Do not combine commit-list mode and range mode in one invocation unless the user explicitly clarifies the intended scope.

**If arguments are missing/invalid**

- If omitted, proceed using current Git state.
- If a referenced commit or range cannot be resolved, stop and ask for a valid commit, range, or scope.
- If the requested scope is ambiguous, stop and ask a targeted question before reviewing.

## Context to Load (INPUT)

**Capture live state**

!`git status`

## Process (PROCESS)

Follow these steps in order:

1. **Gather codebase and Git context.**
   - Run `git status`, `git diff --name-only`, and `git diff --staged --name-only` to identify uncommitted changes, staged changes, and untracked files.
   - If `$ARGUMENTS` references one or more commits, run `git show --stat --name-status <commit...>` and `git show <commit...>`.
   - If `$ARGUMENTS` references a range, run `git diff --stat --name-status <range>` and `git diff <range>`.
   - If no commit or range is provided, run `git diff HEAD`, `git diff --stat HEAD`, and `git ls-files --others --exclude-standard`.
   - If `$ARGUMENTS` references directories or focus areas, use them to narrow whichever scope mode applies.
   - If `$ARGUMENTS` is empty and Git shows no uncommitted changes, run `git log --oneline -10` and ask the user which recent commit(s) to review. Do not assume the codebase is clean.
   - If the repo is not a Git repo or Git data is unavailable, state the limitation and ask the user which files to review.

2. **Determine review scope.**
   - If one or more commits are provided, review only files changed by those commits.
   - If a range is provided, review only files changed by that range.
   - If no commit or range is provided, review current staged, unstaged, and untracked changes.
   - Do not include unrelated staged, unstaged, or untracked changes when one or more commits or a range was provided unless the user explicitly asks for them.
   - If focus context is provided, narrow the selected scope to that focus.
   - Use the selected Git diff/stat output to identify changed lines, deleted lines, removed behavior, file status, and line churn.
   - Exclude files that definitively cannot be subject to technical code review, such as binary assets, images, lockfiles, or generated artifacts.
   - If all changed files are excluded, skip analysis steps and proceed to Step 5 with `Status: Success`.
   - Read each review-scope file in full when it exists.
   - Note imports, exports, and call sites that connect changed code to the rest of the codebase.
   - Read narrowly relevant neighboring files only when needed to understand imports, call sites, data contracts, tests, or framework conventions.

3. **Review for technical issues.**
   - Analyze each review-scope file for:
     - **Logic errors:** incorrect conditionals, off-by-one mistakes, missing error handling, race conditions, state bugs, and broken data flow.
     - **Security issues:** injection risks, XSS, authorization bypasses, unsafe deserialization, insecure secret handling, and exposed credentials.
     - **Performance problems:** N+1 queries, inefficient algorithms on hot paths, avoidable repeated work, memory leaks, and unbounded resource use.
     - **Code quality issues:** only when they create a concrete maintainability or correctness risk, such as unclear naming that hides a bug, unsafe duplication, overly complex control flow, or missing types around ambiguous interfaces.
     - **Adherence to known codebase standards and existing patterns**.
   - Focus on changed behavior and real risk. Do not report subjective style preferences.

4. **Verify findings before reporting them.**
   - For each candidate issue, re-read the exact file and line range that supports it.
   - For type or syntax claims, confirm against the actual code, not from memory.
   - For security concerns, validate with surrounding context.
   - For performance concerns, confirm the affected path is meaningful, such as a hot path, large input, or repeated invocation.
   - Confirm the issue is not explained by nearby code, tests, framework behavior, or established project conventions.
   - Include only findings with a concrete failure mode and an actionable fix.
   - If a concern cannot be verified from the available code context, omit it or list it under "Review Notes" rather than as a finding.

5. **Write the code review report.**
   - Ensure the `.agents/reports/review/` directory exists.
   - Use the **Human-Readable Report** format below.
   - Populate `**Review scope:**` with the Git source reviewed, such as current working tree, commit hash list, range, or focused directory.
   - Write the report to `.agents/reports/review/code-review-<YYYY-MM-DD-HHMMSS>.md`.
   - If no issues are found, the report must include: `Code review passed. No technical issues detected.`

6. **Return a concise summary.**
   - Report the absolute path to the created code review file on its own line.
   - Summarize the number of findings by severity, change stats, and any skipped files.
   - Do not apply fixes, stage files, commit files, or modify code.

**Decision discipline**

- If you must make assumptions: list them explicitly and keep them minimal.
- If blocked by missing info: stop and ask targeted questions.
- If a finding is plausible but unproven, do not promote it to an issue.

**Quality/Safety constraints**

- Do not modify source files. Only write the code review report.
- Derive review scope only from `$ARGUMENTS` and Git state.
- Do not include unrelated staged, unstaged, or untracked changes when commit or range scope is provided unless explicitly requested.
- Do not run tests, builds, or arbitrary code execution.
- Suggest concrete fixes; do not just identify problems.
- Flag security findings as critical severity.
- Stage nothing and commit nothing.

## Output (OUTPUT)

### Human-Readable Report (for humans)

Write the following Markdown structure to `.agents/reports/review/code-review-<timestamp>.md`.

````markdown
# Code Review Report

**Review scope:** <current working tree | commits <hashes> | range <range> | focused scope>
**Status:** Success | Partial | Blocked
**Summary:** <one paragraph describing what was reviewed and the result>

## Stats

- Files Modified: <count>
- Files Added: <count>
- Files Deleted: <count>
- New lines: <count>
- Deleted lines: <count>

## Scope Reviewed

- Files reviewed: <count>
- Files skipped: <count>
- Skipped files:
  - <path>: <reason>

## Findings

- Critical findings: <count>
- High findings: <count>
- Medium findings: <count>
- Low findings: <count>

<!--For each finding, write one block. Number findings sequentially.-->

```text
issue number: 1
severity: critical|high|medium|low
file: path/to/file.py
line: 42
issue: <one-line description>
detail: <why this is a concrete problem>
suggestion: <specific fix>
```

If no issues are found, write:

Code review passed. No technical issues detected.

<!--Omit Review Notes section if list is empty-->

## Review Notes

- <non-blocking observations or verification limits, only if relevant>

<!--Omit Blockers section if list is empty-->

## Blockers

- <what blocked the review and what input is needed, only if relevant>

<!--Omit Assumptions section if list is empty-->

## Assumptions

- <assumption, only if relevant>
````

## Notes

- This command reviews Git diffs together with full file context.
