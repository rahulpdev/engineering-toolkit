# Claude Code Slash Commands — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-markdown-blue)
![Focus](https://img.shields.io/badge/focus-slash%20commands-5b3cc4)

## Overview

This folder contains Claude Code slash-command definitions: single-purpose Markdown files with YAML frontmatter that package reusable prompts into invokable workflows. Commands are organized by group, and the group folder is the command namespace: drafting utilities live under `drafting/`, git workflow commands under `git/`, helper utilities under `helper/`, implementation commands under `implement/`, command-building helpers under `meta/`, planning commands under `plan/`, review-chain commands under `review/`, and validation commands under `validate/`. A file `git/commit.md` is invoked as `/git:commit`.

Each active command should follow the INPUT -> PROCESS -> OUTPUT framework: declare its argument contract, identify context to load, define ordered process steps, state decision discipline, and produce exactly one output type, either a Human-Readable Report or a Structured Agent Handoff. To invoke these commands in Codex, use: "Read and follow in full `<command_path>` with this additional context:".

## Key Features

- Reusable prompts packaged as slash-command Markdown files with explicit argument contracts
- Folder-level organization for planning, execution, review, and meta-authoring workflows
- YAML frontmatter declaring descriptions, argument hints, and least-privilege tool access where needed
- Meta-commands for creating new commands and sub-agents from shared templates
- Strict INPUT -> PROCESS -> OUTPUT discipline so outputs can be checked by humans or handed to downstream agents

## Documents

Each item below is a command definition in this folder, grouped by subfolder.

### drafting

- [`check-congruity.md`](drafting/check-congruity.md): **`/drafting:check-congruity`** — reviews one recently edited file, passed as an optional path argument (defaulting to `plan.md` in `$ARTIFACTS_DIR` for Archon runs), for contradictions, inconsistencies, discrepancies, structural drift, duplicate claims, and missing connective logic. It itemizes findings, applies minimal fixes that preserve the author's voice and edit intent, then re-reads the file to verify the issues were resolved without introducing new ones.
- [`compare-docs.md`](drafting/compare-docs.md): **`/drafting:compare-docs`** — compares the document authored in the current conversation against another LLM's version at the required path argument. It rates both documents overall and section by section against the original instructions, proposes numbered surgical edits where the other version is stronger, performs root-cause analysis where both versions are weak, waits for explicit approval before applying edits, and treats the other LLM's file as read-only.
- [`draft-blueprint.md`](drafting/draft-blueprint.md): **`/drafting:draft-blueprint`** — copies the software blueprint template into the current project's `.agents/blueprint.md` and populates the header, Introduction, and Sections 1-5 from the conversation plus an optional reference document, written in the voice and vocabulary of a required sample blueprint. It settles framing (who the client is, what this delivery covers, how source recommendations are treated) before writing, shows gaps only through the template's own tools, leaves Sections 6-10 untouched, runs a two-way check against the template and the sample, and reports every judgement call as a numbered list for the user to confirm or reject.
- [`seamless-edit.md`](drafting/seamless-edit.md): **`/drafting:seamless-edit`** — applies the edits agreed in the current conversation to a target document, from an optional free-form argument naming the file and any scoping notes. It edits surgically so the result reads as if the original author drafted the passages from the start, with no additive bloat, no in-file rationale, and no over-fitting to the incident that triggered the edit.

### git

- [`commit.md`](git/commit.md): **`/git:commit`** — creates an atomic Git commit in Conventional Commit format. It accepts optional file arguments, defaults to all current changes when no files are supplied, reviews `git status` and `git diff`, stages the intended files, composes a type/scope/description message, commits, and reports the resulting commit hash and file stats.
- [`merge-worktrees.md`](git/merge-worktrees.md): **`/git:merge-worktrees`** — finalises a single piece of work by collapsing its worktree and branch back into the local `integration` branch. It takes a required kebab-case name and an optional type (`feature`, `fix`, `chore` or `docs`, default `feature`), prepares a `--no-ff` merge of `<type>/<name>` without committing, validates the merged working tree against pytest/mypy/pyright, commits the merge only on success, then removes the worktree and deletes the work branch.
- [`new-worktree.md`](git/new-worktree.md): **`/git:new-worktree`** — creates a single git worktree branched off the local `integration` branch on a branch named `<type>/<name>`. It takes a required kebab-case name and an optional type (`feature`, `fix`, `chore` or `docs`, default `feature`), validates the name against reserved values, performs preflight checks for `pyproject.toml`, `app/`, declared dev dependencies, `worktrees/` ignore-rule, `integration`, existing worktree/branch, and remote freshness, creates the worktree at `worktrees/<type>-<name>`, installs Python/uv dependencies, and confirms the resulting branch.

### implement

- [`execute.md`](implement/execute.md): **`/implement:execute`** — implements an existing plan from a required plan-file path. It reads the plan, executes tasks in order, follows the stated testing strategy, runs the validation commands exactly as specified, performs final verification, and reports completed tasks, tests added, validation results, and commit readiness.

### helper

- [`explain-simply.md`](helper/explain-simply.md): **`/helper:explain-simply`** — rewrites required pasted text as a plain language explanation a 16-year-old can read. It avoids jargon, preserves the source meaning, includes one example only when necessary, and returns only the rewrite.
- [`log-response.md`](helper/log-response.md): **`/helper:log-response`** — saves the complete previous AI response verbatim to a Markdown file in a required target folder. It accepts an optional filename as the second argument, requiring quotes when the filename contains spaces, normalizes the saved name to snake_case with a `.md` extension, refuses to overwrite existing files without confirmation, verifies the saved content by readback, and reports the actual target file path.
- [`revise-prompt.md`](helper/revise-prompt.md): **`/helper:revise-prompt`** — revises the user's original prompt into a self-contained, improved version based on feedback. It accepts optional feedback as the argument, falling back to the most recent user message, locates the original prompt and the AI response under critique, diagnoses the gap, plans surgical edits that preserve voice, structure, and intent, inlines context so the revised prompt stands alone, and returns only the revised prompt with no preamble or commentary.
- [`think-architect.md`](helper/think-architect.md): **`/helper:think-architect`** — answers the current technical question the way a senior software engineer and architect would. It accepts an optional question or context argument, falling back to the problem under discussion, inspects the existing architecture and decisions in the repository, reasons from first principles, builds the solution inside the current design or states deliberately what must change and why, checks the result against common standards and best practice, and reports in plain language with no metaphors, no jargon, and no unexplained code references.
- [`wwcd.md`](helper/wwcd.md): **`/helper:wwcd`** — thinks through a decision the way a senior engineer would. It accepts optional guidance, takes the decision from the agent's previous response, checks whether it must be decided now and whether it is easy to reverse, scores every option against seven lenses (standards, architectural fit, lock-in, lifecycle fit, maintenance burden, maintainability by the owner, security and failure modes), recommends one option with up to two runners-up, and names the judgement that produced the recommendation so the owner can challenge it.

### meta

- [`create-agent.md`](meta/create-agent.md): **`/meta:create-agent`** — creates a new sub-agent in `.claude/agents/` from `.agents/reference/subagent_template.md`. It takes one required agent-spec argument plus optional invocation, handoff, and artifact mode arguments, validates those modes, enforces least-privilege tools, and produces a human-readable creation report.
- [`create-command.md`](meta/create-command.md): **`/meta:create-command`** — creates a new slash command in `.claude/commands/` from `.agents/reference/custom_command_template.md`. It accepts optional free-form context about desired behavior, constraints, or examples, enforces correct argument handling and a single output section, and keeps generated commands aligned with the repository's INPUT -> PROCESS -> OUTPUT standard.

### plan

- [`chart-course.md`](plan/chart-course.md): **`/plan:chart-course`** — takes one required problem-definition path followed by two or more solution-option paths, spawns exactly one Navigator sub-agent to evaluate and rank the options, verifies the Navigator's reported artifact exists at the path it reported, and reports only the invoked agent type plus the `status` and `summary` handoff fields before stopping.
- [`find-position.md`](plan/find-position.md): **`/plan:find-position`** — accepts an optional free-form comment as current-turn context, reviews the current conversation, extracts the best implicit or explicit problem definition, checks that explicit user decisions affecting the current loop are preserved during assessment, tests the definition against problem slicing, constraint articulation, outcome clarity, and solution separation, labels reasoning gaps, reports settled decisions used just before the verdict, and returns a cleaner replacement definition for downstream planning.
- [`fix-position.md`](plan/fix-position.md): **`/plan:fix-position`** — saves the previous AI response verbatim to a markdown file. It accepts an optional slug (inferring one from the response if omitted), normalises it to kebab-case, creates `.agents/plans/artifacts/<slug>/`, writes the response to `<slug>-problem-definition.md` inside that folder, refuses to overwrite existing files without confirmation, verifies the saved content by readback, and reports the actual target file path.
- [`plan-feature.md`](plan/plan-feature.md): **`/plan:plan-feature`** — turns a feature request into an implementation-ready plan through feature understanding, codebase intelligence gathering, external documentation research, strategic analysis, and structured plan generation. The output includes context references, implementation phases, step-by-step tasks, testing strategy, validation commands, acceptance criteria, and a completion checklist.
- [`plot-routes.md`](plan/plot-routes.md): **`/plan:plot-routes`** — takes a required path to a problem-definition file, spawns multiple pathfinder sub-agents in parallel to produce independent solution options, saves each YAML report alongside the problem-definition file in `.agents/plans/artifacts/<slug>/` as `<slug>-option-<i>.yaml` (deriving the slug from the folder name), and presents a condensed preview without synthesis, ranking, merging, or interpretation.
- [`run-debate.md`](plan/run-debate.md): **`/plan:run-debate`** — takes two required absolute `.md` paths in the same folder (the problem file and a context file) and an optional `debate-config.json`, builds a `debate/` workspace beside them from symlinks so the originals stay the source of truth, and runs the orchestrate skill from the dialectic-agentic clone named by the environment variable `DIALECTIC_AGENTIC_DIR`.
- [`set-heading.md`](plan/set-heading.md): **`/plan:set-heading`** — takes the PRD path and the TAD path as required arguments and an architecture guide path as an optional third, infers the active prioritisation lens from those documents and recent `feat`/`fix` commits, then recommends one primary next feature and one alternate with the decision frame, signals, trade-offs, architecture fit, acceptance criteria, and done standard disclosed.

### review

- [`change-review.md`](review/change-review.md): **`/review:change-review`** — establishes the scope of recent codebase changes via Git. It accepts optional context such as a commit hash or directory focus, inspects status, diffs, and logs as needed, compiles a deduplicated list of changed files, and writes a structured report to `.agents/reports/review/` for downstream review commands.
- [`combine-change-review.md`](review/combine-change-review.md): **`/review:combine-change-review`** — consumes two required `/change-review` report paths plus optional context. It validates both source reports, deduplicates changed files across them, preserves file-origin and source metadata, records any context-driven scope adjustments, and writes one downstream-compatible combined scope report to `.agents/reports/review/`.
- [`config-review.md`](review/config-review.md): **`/review:config-review`** — consumes a required `/change-review` report path and audits runtime configuration definitions and usage across the scoped changes. It checks environment variables, config modules, compose/Helm/CI settings, defaults, naming consistency, environment mismatches, and missing documentation, then produces a structured handoff for downstream fixes.
- [`deps-review.md`](review/deps-review.md): **`/review:deps-review`** — consumes a required `/change-review` report path and audits dependency manifests plus lockfiles against the changed files. It flags undeclared imports, stale or missing lockfiles, unpinned production dependencies, dev/prod mismatches, and required regeneration commands in a structured handoff.
- [`docs-review.md`](review/docs-review.md): **`/review:docs-review`** — consumes a required `/change-review` report path and audits `README.md` against the scoped codebase changes. It identifies undocumented features or APIs, outdated setup steps, renamed or removed references, and examples or paths that no longer match the repository, then produces section-level edit instructions.
- [`hygiene-review.md`](review/hygiene-review.md): **`/review:hygiene-review`** — consumes a required `/change-review` report path, audits ignore lists, and scans changed files for plaintext secrets, API keys, tokens, and credentials. It halts and alerts the user when secrets are found; otherwise it emits a structured handoff for ignore-list updates and related repository-local actions.
- [`review-handoff.md`](review/review-handoff.md): **`/review:review-handoff`** — applies the complete set of structured review handoffs already present in conversation context from `hygiene-review`, `deps-review`, `config-review`, and `docs-review`. It validates source reviews, resolves overlapping instructions, applies file changes in grouped order, runs safe follow-up actions, and reports what changed without staging, committing, pushing, or merging.

### validate

- [`code-review.md`](validate/code-review.md): **`/validate:code-review`** — audits scoped code changes for real technical issues via Git. It accepts optional context such as one or more commit hashes, a commit range, or a directory focus, reviews the resolved scope for logic, security, performance, and maintainability issues, verifies each finding against the actual code, and writes a human-readable Markdown report with numbered findings to `.agents/reports/review/`.
- [`code-review-fix.md`](validate/code-review-fix.md): **`/validate:code-review-fix`** — consumes a required code review report path or manual issue description plus optional scope. It fixes actionable review findings one by one, adds or updates relevant tests, runs targeted verification and final validation, and reports exactly what changed without staging, committing, pushing, or merging.
- [`validate.md`](validate/validate.md): **`/validate:validate`** — runs comprehensive project validation by executing the pytest suite, mypy and pyright type checks, ruff linting, a local uvicorn server smoke test on port 8123, and a Docker Compose deployment check with endpoint and log verification. It then produces a summary report covering test, type-check, lint, local server, and Docker statuses with an overall PASS/FAIL health assessment.
- [`validate-obsidian-plugin.md`](validate/validate-obsidian-plugin.md): **`/validate:validate-obsidian-plugin`** — the plugin counterpart of `/validate:validate`: runs the pnpm test, typecheck, lint and format checks, builds the plugin and checks `main.js`, `manifest.json` and `versions.json` against the size budget and manifest rules, runs the end-to-end tests against the earliest and latest supported Obsidian versions, and produces a PASS/FAIL summary.
- [`check-ignore-comments.md`](validate/check-ignore-comments.md): **`/validate:check-ignore-comments`** — finds every `noqa` and `type: ignore` comment in the codebase, investigates why each exists, and writes a dated report to `.agents/reports/` giving, per comment, the code, the reason it exists, resolution options with effort and impact, trade-offs, and a Remove / Keep / Refactor recommendation.

## Maintenance

When adding or changing commands in this folder:

- Keep this `README.md` list in sync with active command files and their subfolders.
- Keep active commands in the smallest appropriate folder.
- Each active command file should declare its argument contract, context to load, ordered process steps, decision discipline, and exactly one output section: Human-Readable Report or Structured Agent Handoff.
- Update the description here whenever a command's arguments, inputs, process, output format, output consumer, or file path changes.
