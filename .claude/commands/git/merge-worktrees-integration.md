---
description: Merge the single work branch `<type>/<name>` into the local `integration` branch with a `--no-ff` merge commit, validate the result with pytest/mypy/pyright, and on success remove the worktree and delete the work branch.
argument-hint: [type] <name> (name required - short kebab-case work name; type optional - `feature`, `fix`, `chore` or `docs`, default `feature`; must match what was passed to `/new-worktree-integration`)
allowed-tools: Bash(git check-ref-format:*), Bash(git rev-parse:*), Bash(git show-ref:*), Bash(git for-each-ref:*), Bash(git status:*), Bash(git diff:*), Bash(git switch:*), Bash(git merge:*), Bash(git commit:*), Bash(git worktree:*), Bash(git branch:*), Bash(git fetch:*), Bash(git rev-list:*), Bash(git -C:*), Bash(test:*), Bash(grep:*), Bash(pwd:*), Bash(dirname:*), Bash(uv run:*)
---

# /merge-worktrees-integration: Merge Worktree Into Integration

## Philosophy (Why this exists)

This command finalises a single piece of work by collapsing its worktree and branch back into `integration` under one consistent pattern. It prepares a `--no-ff` merge of `<type>/<name>` into the local `integration` branch, validates the merged working tree against pytest/mypy/pyright, and only commits the merge once validation passes.

The validation step here is **integration validation**, not feature validation.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/merge-worktrees-integration feature-a`
- `/merge-worktrees-integration pdf-table-detection`
- `/merge-worktrees-integration fix login-timeout`
- `/merge-worktrees-integration chore bump-deps`

**Arguments received**

- All args as a single string: `$ARGUMENTS`

**Arguments policy**

- **Mandatory**: `$ARGUMENTS` is required and must hold a name, optionally preceded by a type. If missing or invalid, stop and ask.

**Argument contract**

- Required args: `$ARGUMENTS` = work name in kebab-case (e.g. `feature-a`), given as the last token. Must match exactly the name passed to `/new-worktree-integration`.
- Optional args: a type before the name. It is one of `feature`, `fix`, `chore` or `docs`. Must match exactly the type passed to `/new-worktree-integration`.
- Defaults: the type is `feature` when omitted.
  - Fixed conventions (not user-configurable): the merge target is always the local `integration` branch. The merge always uses `--no-ff`.
- Derived values, computed in Step 1 and used by every later step:
  - `TYPE`: the type given, or `feature` when none was given.
  - `NAME`: the name.
  - `BRANCH`: `TYPE/NAME`.
  - `FOLDER`: `TYPE-NAME`. The worktree path is `worktrees/FOLDER`.
- Validation rules:
  - Must be non-empty after trimming whitespace.
  - Must be either one token (the name) or two tokens (a type, then the name).
  - When two tokens are given, the first must be exactly `feature`, `fix`, `chore` or `docs`.
  - `NAME` must satisfy every rule below:
    - Must not contain shell metacharacters: `;`, `&`, `|`, `` ` ``, `$`, `(`, `)`, `<`, `>`, `*`, `?`, `[`, `]`, `{`, `}`, `\`, `'`, `"`, `!`.
    - Must not start with `/` or `-`.
    - Must not contain `..`, `@{`, or `/` (single segment only).
    - Must not equal (case-insensitively) any git pseudo-ref: `HEAD`, `FETCH_HEAD`, `ORIG_HEAD`, `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `BISECT_HEAD`.
    - Must not equal (case-insensitively) any workflow-reserved name: `main`, `master`, `integration`, `feature`, `fix`, `chore`, `docs`.
    - Must match strict kebab-case: regex `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` (lowercase letter start, then dash-separated lowercase-alphanumeric segments; no underscores, no uppercase, no leading digit or hyphen, no trailing hyphen, no consecutive hyphens).
  - `refs/heads/$BRANCH` must pass `git check-ref-format`.

**If arguments are missing/invalid**

- Stop before running any git mutations. Explain the problem, ask for a valid name and show a valid example. If the type is not allowed, list the allowed types.

## Process (PROCESS)

Follow these steps in order:

1. **Parse and validate `$ARGUMENTS`.**
   - Trim surrounding whitespace.
   - Split on whitespace. Set `TYPE` and `NAME` from the tokens, then compute `BRANCH` and `FOLDER` as defined in _Argument contract_.
   - Reject the value if any rule in _Validation rules_ is violated. On reject, stop and tell the user which validation rule was violated.
   - Run `git check-ref-format "refs/heads/$BRANCH"` (no `--branch` — running with `--branch` would first expand `@{-N}` "previous checkout" shortcuts against your current state, which is not what we want for literal-string validation). If exit code is non-zero, stop and tell the user the branch name fails git's ref-format check.
2. **Confirm cwd is the main repo root.** Run each check in order; on the first that fails, stop and tell the user the matching message.
   - **Not in a git repo**: run `git rev-parse --is-inside-work-tree`. If exit code is non-zero, stop with "cwd is not inside a git repository; cd into the repo and re-run."
   - **Bare repo**: run `git rev-parse --is-bare-repository`. If output is `true`, stop with "bare repos are not supported by this command."
   - **Linked worktree (covers both the worktree root and any subdirectory of one)**: run `git rev-parse --path-format=absolute --git-dir` and capture as `GD`; run `git rev-parse --path-format=absolute --git-common-dir` and capture as `GCD`. If `GD` != `GCD`, compute `MAIN_ROOT` as `dirname "$GCD"`, then stop with "you are in a linked worktree; cd $MAIN_ROOT and re-run."
   - **Subdirectory of main repo**: run `pwd -P` and capture as `CWD`; run `git rev-parse --show-toplevel` and capture as `TOPLEVEL`. If `CWD` != `TOPLEVEL`, stop with "you are in a subdirectory of the main repo; cd $TOPLEVEL and re-run."
3. **Confirm `pyproject.toml` exists at the repo root.**
   - Run: `test -f pyproject.toml`.
   - If it does not exist, stop and tell the user that this is not a uv-managed project.
4. **Confirm the `app/` directory exists at the repo root.**
   - Run: `test -d app`.
   - If it does not exist, stop and tell the user that an `app/` directory is required at the repo root.
5. **Confirm `pytest`, `mypy`, and `pyright` are declared in `pyproject.toml`.**
   - Run: `grep -q '"pytest"' pyproject.toml && grep -q '"mypy"' pyproject.toml && grep -q '"pyright"' pyproject.toml`.
   - If any of the three is missing, stop and tell the user which tool(s) are missing and to add them with `uv add --dev pytest mypy pyright`.
6. **Confirm the local `integration` branch exists.**
   - Run: `git show-ref --verify --quiet refs/heads/integration`.
   - If it does not exist, stop and tell the user that a local `integration` branch is required.
7. **Confirm the work branch exists (exact case).**
   - Run: `git show-ref --verify --quiet "refs/heads/$BRANCH"`. If missing, stop and tell the user that the `$BRANCH` branch does not exist.
   - Then run: `grep -ix "refs/heads/$BRANCH" <<< "$(git for-each-ref --format='%(refname)' refs/heads/)"`. If the matched refname differs in case from `refs/heads/$BRANCH`, stop and tell the user that a different-case variant of the branch exists and refuse to merge.
8. **Confirm the worktree folder `worktrees/$FOLDER` exists and is checked out on the right branch.**
   - Run: `test -d "worktrees/$FOLDER"`. If missing, stop and tell the user that `worktrees/$FOLDER` does not exist.
   - Run: `git -C "worktrees/$FOLDER" branch --show-current`. If the output is empty (detached HEAD) or differs from `$BRANCH`, stop and tell the user to `cd worktrees/$FOLDER && git switch $BRANCH` before re-running.
9. **Confirm the worktree has no uncommitted or untracked changes from the user.**
   - Run: `git -C "worktrees/$FOLDER" status --porcelain`.
   - Allow `.venv/` and `uv.lock` lines in the output; treat any other non-empty line as user state. If any user state exists, stop and tell the user to commit or discard those changes before re-running.
10. **Confirm the main repo working tree is clean and is not mid-merge.**
    - Run: `git rev-parse -q --verify MERGE_HEAD`. If exit code is 0, stop and tell the user that a merge is already in progress and they should either `git merge --abort` to restore `integration`, or finish the merge manually with `git commit`, before re-running.
    - Run: `git status --porcelain`. If non-empty, stop and tell the user the list of dirty paths so they can commit, stash, or ignore them.
11. **Check whether local `integration` is behind its remote (warn-only).**
    - Always include the outcome under "What you did" in the final report; never silently skip, never stop the process.
    - Run: `git fetch origin integration`. If it exits non-zero (no network, no `origin` remote, or no remote branch), substitute the git error as the outcome and proceed to Step 12.
    - Otherwise run: `git show-ref --verify --quiet refs/remotes/origin/integration`. If the ref does not exist (e.g. custom `remote.origin.fetch` refspec), substitute "refs/remotes/origin/integration is not present locally" as the outcome and proceed to Step 12.
    - Otherwise run: `git rev-list --count integration..origin/integration`. If the count is 0, substitute "integration is up to date with origin/integration" as the outcome; if greater than 0, substitute "integration is N commit(s) behind origin/integration" as the outcome and also add that line under **Risks / gotchas**.
12. **Switch the main repo to `integration`.**
    - Run: `git switch integration`. If this fails, stop and tell the user the git error.
13. **Prepare the merge without committing.**
    - Run: `git merge "$BRANCH" --no-ff --no-commit`.
    - If the merge reports conflicts, capture the conflicting files via `git diff --name-only --diff-filter=U`, run `git merge --abort` to restore integration, and stop and tell the user the conflict list.
14. **Run integration validation on the prepared merge.**
    - Run, in order:
      - `uv run pytest -v --ignore=worktrees`
      - `uv run mypy app/`
      - `uv run pyright app/`
    - If any exits non-zero, capture which command failed and the last lines of its output, run `git merge --abort`, and stop and tell the user which command failed and its output.
15. **Commit the prepared merge.**
    - Run: `git commit -m "merge: $BRANCH into integration"`. If this fails, stop and tell the user the git error, and that the prepared merge is still in place — they can either fix and commit manually or run `git merge --abort` to abandon.
16. **Remove the worktree.**
    - Run: `git worktree remove --force "worktrees/$FOLDER"`.
    - If this fails, capture the git error and add it under **Risks / gotchas** in the final report, mark `Status: Partial`, **skip Step 17 entirely** and proceed directly to Step 18. Include in the report the exact recovery commands: `git worktree remove --force "worktrees/$FOLDER"` (try again manually), then `git branch -d "$BRANCH"`.
17. **Delete the work branch.** (Skipped if Step 16 failed.)
    - Run: `git branch -d "$BRANCH"`.
    - If `-d` refuses, capture the git error and add it under **Risks / gotchas** in the final report, and mark `Status: Partial`.
18. **Produce the final response using the OUTPUT section.** Include the Step 11 outcome under "What you did" verbatim.

**Decision discipline**

- Never auto-resolve merge conflicts; always hand control back to the user.
- `--force` is permitted **only** on Step 16. Never use `git branch -D` anywhere in this command.
- Never run `git push` in this command; pushing `integration` is out of scope.
- If validation fails, abort the prepared merge with `git merge --abort`.
- If re-invoked after a stopped run where the worktree has already been removed or the work branch already deleted, refuse and report; do not attempt to repair or resume.

**Quality/Safety constraints**

- Always merge into the local `integration` branch; never into `main`, `master`, a remote-tracking branch, or whatever branch happens to be checked out.
- Always use `--no-ff` so every piece of work lands as a distinct merge commit on `integration`.
- Cleanup (Steps 16–17) runs only after Steps 13, 14, and 15 succeed.
- Do not start any server, run any health check, reserve ports, or kill server processes; this project has no web server.
- Do not modify files outside git's own state and the worktree's metadata.

## Output (OUTPUT)

### Human-Readable Report

Return a concise, easy-to-scan summary in plain language at a 16-year-old reading level:

- **Status**: Success | Partial | Blocked
- **What you understood**: 1–3 bullets restating the type, name, source branch, and merge target.
- **What you did**: bullets, in execution order (e.g. switched to `integration`, merged with `--no-ff`, ran pytest/mypy/pyright, removed worktree, deleted work branch, plus the Step 11 freshness outcome verbatim).
- **Key results**:
  - Merge: `<type>/<name>` → `integration` (include merge commit hash if available)
  - Validation: pytest / mypy / pyright outcomes
  - Worktree removed: `worktrees/<folder>`
  - Work branch deleted: `<type>/<name>`
- **Risks / gotchas**: bullets, only when real (e.g. freshness behind, merge conflicts, validation failure + merge aborted, residual worktree files).
- **Next steps**: exact command(s) the user can run next (e.g. start the next piece of work, or perform their separate process to merge `integration` into `main`).
- **Questions (only if blocked)**: numbered list of what is needed to unblock.

## Notes

- Hardcoded assumptions: project uses Python + `uv`; the user manually verifies the work inside the worktree before invoking this command; project has no web server; project source lives under `app/`; `pytest`, `mypy`, and `pyright` are declared as dev dependencies.
- Validation layering: pre-merge validation is owned by other commands in the worktree. This command only runs the integration-validation layer on the merged tree.
- Known limitation: between Steps 13 and 15 the main repo is in a mid-merge state. Do not run other git operations on the main repo during this window — `git merge --abort` on failure would undo any unrelated changes staged in another shell.
- Known limitation: the warn-only fetch in Step 11 always emits an outcome under "What you did" (skipped / up-to-date / behind), but the check itself is best-effort — on network or remote failure it substitutes the git error and proceeds.
- Known limitation: `pyproject.toml` presence and dev-dependency declarations are checked, but the file's contents are not otherwise validated. In particular, if `[tool.pytest.ini_options].testpaths` resolves into `worktrees/`, Step 14's `--ignore=worktrees` is overridden and pytest will fail mid-merge with a collection error. Keep test discovery roots out of `worktrees/`.
