# Custom Slash Commands vs Custom Skills

## Conceptual Difference

- **Slash command** — a user-invoked prompt template. You type `/name` and the file's contents get injected as a prompt. One-way, always user-initiated.
- **Skill** — a capability bundle Claude can auto-invoke when the task matches its description, OR you can invoke explicitly. Can include supporting files, scripts, and reference docs.

## How To Create Each

### Slash Command

Single markdown file:

- Project: `.claude/commands/<name>.md`
- Personal: `~/.claude/commands/<name>.md`
- Subdirectories namespace the command (`.claude/commands/git/commit.md` → `/git:commit`)

```markdown
---
description: What this does
allowed-tools: Read Grep Bash(git *)
argument-hint: [file] [format]
---

Your prompt here. Use $ARGUMENTS, $1, $2 for placeholders.
Use !`command` to inject bash output before Claude sees it.
```

Frontmatter is optional — content alone works.

### Skill

A **directory** containing `SKILL.md` plus optional supporting files:

- Project: `.claude/skills/<skill-name>/SKILL.md`
- Personal: `~/.claude/skills/<skill-name>/SKILL.md`

```
my-skill/
├── SKILL.md          # required
├── reference.md      # optional
└── scripts/helper.py # optional
```

```yaml
---
name: my-skill
description: What this does and WHEN to use it. Critical — Claude reads this to decide auto-invocation.
disable-model-invocation: true # optional: turns off auto-invoke
user-invocable: false # optional: only Claude can load it
allowed-tools: Read Grep
paths: src/**/*.ts # optional: only relevant when editing matching files
---
Instructions here. Reference @other-file.md to pull in supporting docs on demand.
```

The `description` field is the single most important part for auto-invocation — it's what Claude scans to decide whether to load the skill autonomously.

## Key Behavioral Differences

|                         | Slash command           | Skill                                            |
| ----------------------- | ----------------------- | ------------------------------------------------ |
| Invocation              | User types `/name` only | Auto-invoked by Claude **or** user types `/name` |
| Always-loaded footprint | None                    | Just the description (so Claude knows it exists) |
| Bundled files/scripts   | No (single `.md`)       | Yes (whole directory)                            |

## When To Choose Which

- **Slash command** — quick prompt template you'll always trigger yourself; no risk of accidental invocation.
- **Skill** — you want Claude to recognize "this task fits" and apply it without you remembering to type the command, or you need to bundle scripts/reference docs alongside the instructions.

Skills are the modern, recommended format; slash commands still work and are simpler when you just want a manual shortcut.

## How A Skill Invokes A Script

There are two distinct mechanisms:

**A) Preprocessing — runs before Claude sees the skill**
The `` !`command` `` syntax in SKILL.md is executed once, and the output is substituted into the prompt. Claude never sees the command itself, only its output. Useful for injecting fresh context (current branch, file list, etc.).

**B) Runtime invocation — Claude executes the script during the task**
This is the more common case. SKILL.md contains instructions like _"Run `python scripts/analyze.py <file>` to extract dependencies"_. Claude reads that, then uses its **Bash tool** to actually run it during the conversation. The script isn't auto-executed by the skill system — Claude is the executor.

For both:

- Scripts live anywhere in the skill directory (convention: `scripts/`)
- Reference paths via `${CLAUDE_SKILL_DIR}` to be path-safe
- `allowed-tools: Bash` (or a narrower pattern like `Bash(python *)`) in frontmatter pre-approves execution

There are **no auto-run hooks** in skills themselves — if you want something to fire on a Claude Code event, that's the hooks system in `settings.json`, separate from skills.

## The `paths` Frontmatter Field

`paths` is a glob filter that gates **Claude's automatic invocation** of the skill:

```yaml
paths: src/**/*.ts, src/**/*.tsx
```

When set, Claude only auto-considers the skill when working with files matching those globs. It does **not**:

- Block explicit `/skill-name` invocation (that always works)
- Restrict which tools the skill can use
- Affect anything beyond auto-invocation eligibility

Think of it as a relevance hint that prevents a frontend-only skill from being auto-loaded during backend work.

## Bash Injection With `!command`

Same syntax, same behavior as in slash commands. Inline `` !`git diff HEAD` `` and the multi-line ` ```! ` fenced form both work in SKILL.md. Output is substituted before Claude sees the rendered skill content.

Two caveats:

- A `shell:` frontmatter field can override the default (`bash`) — relevant on Windows with PowerShell.
- An org/user setting `"disableSkillShellExecution": true` can disable this feature entirely; commands then render as `[shell command execution disabled by policy]`.

## Path Resolution For Bundled Scripts

Claude's working directory is the **project root**, not the skill folder. So a bare `scripts/foo.py` in SKILL.md resolves to `<project_root>/scripts/foo.py`, which doesn't exist. The actual file lives at `<project_root>/.claude/skills/<skill-name>/scripts/foo.py`.

Two reasonable options for project-level skills:

**Option A — `${CLAUDE_SKILL_DIR}` (recommended):**

```markdown
Run `python ${CLAUDE_SKILL_DIR}/scripts/count_files.py`
```

Cleanest. Resolves correctly without hardcoding anything. Survives folder renames.

**Option B — explicit project-relative path:**

```markdown
Run `python .claude/skills/repo-analyzer/scripts/count_files.py`
```

Works because cwd is the project root. Downsides: hardcodes the skill name (rename the skill folder → all script references break), and bakes in the install location.

## No Equivalent For Slash Commands

There is **no** `${CLAUDE_COMMAND_DIR}` equivalent for slash commands. The variable only exists for skills. That's largely because slash commands are conceived as a single `.md` file with no expectation of bundled siblings, while skills are explicitly a directory bundle.

Workarounds if a slash command needs to reference a script:

- Hardcode the project-relative path: `.claude/commands/scripts/foo.py` (works because cwd is the project root, but breaks if you reorganize)
- Use an absolute path under `~/.claude/` if it's a personal command
- **Convert it to a skill** — same prompt content works, plus you get a directory bundle, `${CLAUDE_SKILL_DIR}`, and (optionally) auto-invocation

## Six-Step Conversion Walkthrough

Assumptions: command and skill both at the project repo level; no reference docs or scripts; existing slash command frontmatter includes `description`, `allowed-tools`, and `argument-hint`; `disable-model-invocation` should always be set to `true`.

1. Create the skill folder: `.claude/skills/foo/`
2. Move the file: `.claude/commands/foo.md` → `.claude/skills/foo/SKILL.md`
3. Update the frontmatter:
   - **Add** `name: foo` (must match the folder name)
   - **Add** `disable-model-invocation: true`
   - **Keep** `description`, `allowed-tools`, and `argument-hint` unchanged — since auto-invocation is off, the description can stay as a short label
4. Body stays as-is. `$ARGUMENTS`, `$1`, `` !`command` `` all still work.
5. Delete the old `.claude/commands/foo.md` to avoid a name collision.
6. Test: type `/foo` to confirm explicit invocation works.

## Porting Claude Skills To Codex Skills

Codex skills use the same broad Agent Skills pattern: a directory with `SKILL.md` plus optional supporting resources such as `scripts/`, `references/`, and `assets/`.

Codex also supports optional Codex-specific metadata:

```
my-skill/
├── SKILL.md
├── scripts/       # optional
├── references/    # optional
├── assets/        # optional
└── agents/
    └── openai.yaml
```

`SKILL.md` is the portable skill body. `agents/openai.yaml` is Codex-specific metadata for UI, invocation policy, and declared tool dependencies.

## Codex Skill Locations

Codex skills are usually created locally, either manually or with:

```text
$skill-creator
```

Codex discovers skills from locations such as:

```text
.agents/skills
~/.agents/skills
/etc/codex/skills
```

## Codex Frontmatter Requirements

For Codex, `name` and `description` are required:

```markdown
---
name: evaluation-report
description: Evaluate candidate options and produce an evaluation report.
---
```

Do not omit `name` in Codex. Claude Code can infer the name from the directory if omitted, but Codex requires it for supported skill discovery and validation.

Claude-specific frontmatter should not be copied directly into Codex `SKILL.md`.

## Claude To Codex Frontmatter Mapping

```text
name
  Keep in Codex SKILL.md.

description
  Keep in Codex SKILL.md.

disable-model-invocation
  Move to agents/openai.yaml as policy.allow_implicit_invocation: false.

allowed-tools
  No direct Codex SKILL.md equivalent. Re-express as written operational constraints in the skill body. Use Codex config/rules/hooks for enforcement.

argument-hint
  Translate into agents/openai.yaml interface.default_prompt.
```

## Codex Invocation Policy

Claude:

```yaml
disable-model-invocation: true
```

Codex:

```yaml
# agents/openai.yaml
policy:
  allow_implicit_invocation: false
```

When `allow_implicit_invocation` is `false`, Codex will not auto-select the skill based on the user's prompt. Explicit `$skill-name` invocation still works.

## Translating allowed-tools For Codex

Codex skills do not have a per-skill `allowed-tools` field.

For Codex, express the intended behavior directly in the skill body. Example:

```markdown
# Evaluation Report

## Operational Constraints

Operate read-first. Your only write operation is creating the evaluation report artifact. Do not modify existing files, including source code, option files, or the problem definition. All other operations must be read and search based.
```

Examples:

```markdown
Operate read-only. Use file reads and search to gather context. Do not create, edit, delete, rename, or move files.
```

```markdown
Use reads and search for all investigation. Write only the final requested artifact. Do not modify existing project files.
```

```markdown
Use shell only for read-only inspection commands such as `git status` and `git diff`. Do not run build, install, network, mutation, staging, commit, push, or deploy commands unless the user explicitly asks.
```

Actual enforcement in Codex belongs in runtime configuration, rules, hooks, sandboxing, app permissions, or approval policy, not in `SKILL.md`.

## agents/openai.yaml

`agents/openai.yaml` is optional Codex-specific metadata.

Example:

```yaml
interface:
  display_name: "Evaluation Report"
  short_description: "Compare options and write an eval report"
  default_prompt: "Use $evaluation-report to compare <problem-file> against <option-files>."

policy:
  allow_implicit_invocation: false

dependencies:
  tools:
    - type: "mcp"
      value: "github"
      description: "GitHub MCP server"
      transport: "streamable_http"
      url: "https://example.com/mcp"
```

## interface.default_prompt

`interface.default_prompt` is for the Codex UI/harness and indirectly for the user.

It is not hidden agent guidance. It is not an argument schema. It is not a validation layer.

The Codex app can show, suggest, or insert it when a user selects or invokes the skill. The agent only sees it if the UI inserts it into the actual conversation prompt.

Use it as a starter prompt that shows the expected invocation shape:

```yaml
interface:
  default_prompt: "Use $evaluation-report to compare <problem-file> against <option-files>."
```

## Recommended Codex Porting Shape

Keep Codex `SKILL.md` focused and portable:

```markdown
---
name: skill-name
description: Clear trigger description for when Codex should use this skill.
---

# Skill Name

## Operational Constraints

State translated tool/write/read constraints here.

## Instructions

Write the workflow Codex should follow.
```

Put Codex-specific UI and invocation metadata in:

```text
agents/openai.yaml
```

Use runtime config, rules, hooks, sandboxing, and approvals for real enforcement.

## Python Claude Command to Skill Conversion Script: PRD

### Purpose

Automate steps 2–5 of the Six-Step Conversion Walkthrough. Transform a project-level slash command (`.claude/commands/<name>.md`) into a project-level skill (`.claude/skills/<name>/SKILL.md`) with required frontmatter additions, pre- and post-conversion validation, and deletion of the original command file. Steps 1 (folder creation) and 6 (manual test) remain manual or implicit.

### Invocation

```text
python convert_command_to_skill.py <command-filename>
```

Argument:

- `<command-filename>` — Accepts both `foo` and `foo.md`. The script strips a trailing `.md` if present. The resulting basename becomes the skill folder name and the value of the `name` frontmatter field.

Working directory: Script must be run from the project root. It does not attempt to discover the project root.

### Source And Destination Paths

- Source: `.claude/commands/<basename>.md` (relative to cwd)
- Destination directory: `.claude/skills/<basename>/`
- Destination file: `.claude/skills/<basename>/SKILL.md`

### Pre-Conversion Validation

All checks must pass before any file mutation. On failure: emit error JSON, exit 1, make no changes.

| Check                                                                     | Error code                   |
| ------------------------------------------------------------------------- | ---------------------------- |
| `<basename>` matches `^[a-z0-9-]{1,64}$`                                  | `E_INVALID_NAME`             |
| Source file exists at expected path                                       | `E_SOURCE_NOT_FOUND`         |
| Source file is readable as UTF-8 text                                     | `E_SOURCE_UNREADABLE`        |
| Source begins with YAML frontmatter delimited by `---`                    | `E_NO_FRONTMATTER`           |
| Frontmatter parses as valid YAML                                          | `E_FRONTMATTER_INVALID_YAML` |
| Frontmatter contains non-empty `description`                              | `E_MISSING_DESCRIPTION`      |
| Frontmatter contains non-empty `allowed-tools`                            | `E_MISSING_ALLOWED_TOOLS`    |
| Frontmatter contains non-empty `argument-hint`                            | `E_MISSING_ARGUMENT_HINT`    |
| If frontmatter has `name`, its value equals `<basename>`                  | `E_NAME_MISMATCH`            |
| Destination directory `.claude/skills/<basename>/` does not already exist | `E_DEST_DIR_EXISTS`          |

### Conversion Steps

Execute in order. Hold the original source file contents in memory throughout for rollback. On any failure after step 1, run rollback (see below) and exit 2.

1. Create destination directory `.claude/skills/<basename>/`. Failure: `E_DEST_DIR_CREATE_FAILED`.
2. Write destination file `.claude/skills/<basename>/SKILL.md` — a copy of source with frontmatter modified:
   - Add `name: <basename>` if absent
   - Add or override `disable-model-invocation: true` (boolean, not string)
   - Preserve all other existing fields and values (`description`, `allowed-tools`, `argument-hint`, and any unknown fields)
   - Preserve body content byte-for-byte after the closing `---`
   - Recommended key order: `name` first, `disable-model-invocation` last, all others in original order
   - Failure: `E_DEST_WRITE_FAILED`
3. Delete source file `.claude/commands/<basename>.md`. Failure: `E_SOURCE_DELETE_FAILED`.

### Post-Conversion Validation

Run all checks before reporting success. On failure: rollback and exit 2.

| Check                                                      | Error code                          |
| ---------------------------------------------------------- | ----------------------------------- |
| Destination file exists and is readable                    | `E_POST_DEST_MISSING`               |
| Destination frontmatter parses as YAML                     | `E_POST_FRONTMATTER_INVALID`        |
| Destination has `name` equal to `<basename>`               | `E_POST_NAME_INVALID`               |
| Destination has `disable-model-invocation: true` (boolean) | `E_POST_DISABLE_INVOCATION_INVALID` |
| Destination has non-empty `description`                    | `E_POST_MISSING_DESCRIPTION`        |
| Destination has non-empty `allowed-tools`                  | `E_POST_MISSING_ALLOWED_TOOLS`      |
| Destination has non-empty `argument-hint`                  | `E_POST_MISSING_ARGUMENT_HINT`      |
| Source file no longer exists                               | `E_POST_SOURCE_STILL_EXISTS`        |

### Rollback Behavior

Triggered by any failure in Conversion Steps 1–3 or Post-Conversion Validation.

1. If destination SKILL.md was written, delete it.
2. If destination directory was created and is now empty, delete it.
3. If source was deleted, restore from the in-memory copy held since step 0.
4. Emit the original triggering error (not the rollback steps).
5. Exit 2.

If rollback itself fails at any step: emit `E_ROLLBACK_FAILED` with `original_error` and `rollback_failure` both in `context`, and exit 3. Manual intervention required.

### Error Output Format

All errors emit a single JSON object to stderr, then exit non-zero. Schema:

```json
{
  "error_code": "E_SOURCE_NOT_FOUND",
  "message": "Source file '.claude/commands/foo.md' not found.",
  "context": {
    "expected_path": ".claude/commands/foo.md",
    "cwd": "/Users/example/project"
  },
  "remediation": "Verify the command file exists at the expected path and that the script is run from the project root."
}
```

Required fields: `error_code`, `message`, `context`, `remediation`. `context` keys vary per error code but must always be machine-parseable (no embedded prose).

### Success Output Format

On success: single JSON object to stdout, exit 0.

```json
{
  "status": "ok",
  "source_deleted": ".claude/commands/foo.md",
  "destination_created": ".claude/skills/foo/SKILL.md",
  "fields_added": ["name", "disable-model-invocation"],
  "fields_preserved": ["description", "allowed-tools", "argument-hint"]
}
```

### Exit Codes

| Code | Meaning                                                               |
| ---- | --------------------------------------------------------------------- |
| 0    | Success                                                               |
| 1    | Pre-conversion validation failed (no file changes)                    |
| 2    | Conversion or post-validation failed; rollback completed successfully |
| 3    | Rollback failed; filesystem may be in inconsistent state              |
| 64   | Invalid invocation (missing argument, wrong arg count)                |

### Idempotency

The script is **not** idempotent by design. Re-running on an already-converted skill will fail at `E_SOURCE_NOT_FOUND`. To re-convert, the user must manually remove `.claude/skills/<basename>/` first. This prevents silent overwrites.

### Dependencies

- Python 3.9+
- `PyYAML` (declared via `# /// script` PEP 723 metadata or a sibling `requirements.txt`)
- Standard library only beyond PyYAML: `pathlib`, `shutil`, `json`, `sys`, `re`
- No network calls
- No shell-out

### Non-Goals

- Discovering or resolving the project root
- Editing the body of the file
- Migrating reference docs or bundled scripts
- Personal-scope (`~/.claude/`) conversion
- Re-conversion / overwrite of existing skills
- Verifying the converted skill works at runtime

## Python Claude Skill to Codex Skill Conversion Script: PRD

### Purpose

Build a one-way, copy-only converter from project Claude skill `.claude/skills/<skill-name>/` to project Codex skill `.agents/skills/<skill-name>/`. Preserve the Claude skill unchanged; convert Claude metadata into Codex `SKILL.md`, `agents/openai.yaml`, and body guidance. This is Part 2 of the modular pipeline: no slash-command conversion, bidirectional sync, Git authority detection, or semantic convergence.

### Invocation

```text
python convert_claude_skill_to_codex_skill.py <skill-name>
```

Accept exactly one argument: a folder name such as `foo` for `.claude/skills/foo/SKILL.md`. Reject `.md`, `SKILL.md`, paths, absolute paths, slashes, backslashes, empty or whitespace-only strings, extra args, and names not matching `^[a-z0-9-]{1,64}$`. Run only from project root; do not discover root.

### Paths

Use source dir `.claude/skills/<skill-name>/`, source file `.claude/skills/<skill-name>/SKILL.md`, destination root `.agents/skills/`, destination dir `.agents/skills/<skill-name>/`, destination file `.agents/skills/<skill-name>/SKILL.md`, and metadata file `.agents/skills/<skill-name>/agents/openai.yaml`. Create `.agents/skills/` if missing. Never create output outside `.agents/skills/<skill-name>/`.

### Source Contract

Source must be a real directory containing a real UTF-8 `SKILL.md` with YAML frontmatter delimited by `---`, parsed as a mapping, and a non-empty body. Required frontmatter: `name` non-empty and equal to `<skill-name>`; `description` non-empty string; `disable-model-invocation` boolean `true`; `allowed-tools` non-empty scalar or list; `argument-hint` non-empty string.

Reject source symlinks anywhere in the tree. Reject source `agents/openai.yaml` as a metadata conflict.

### Output Contract

Copy the full source directory recursively into a temporary destination, preserving regular file bytes, names, directories, bundled `scripts/`, `references/`, `assets/`, and executable bits. Do not delete, move, rename, edit, chmod, or otherwise mutate `.claude/skills/<skill-name>/`.

Destination `SKILL.md` frontmatter must contain exactly:

```yaml
---
name: <skill-name>
description: <source description>
---
```

It must not contain Claude-only fields, including `disable-model-invocation`, `allowed-tools`, `argument-hint`, `user-invocable`, `paths`, or `shell`. Preserve the source body except for deterministic insertion or replacement of `## Operational constraints`.

Destination `agents/openai.yaml` must contain only:

```yaml
interface:
  default_prompt: "Use $<skill-name> <argument-hint>."

policy:
  allow_implicit_invocation: false
```

`default_prompt` must include `$<skill-name>` and the trimmed source `argument-hint`; escape YAML strings correctly. `allow_implicit_invocation` must be boolean `false`.

### Operational Constraints

Translate `allowed-tools` into a generated plain-language `## Operational constraints` section. It must be the first H2 outside fenced code blocks. If the source body already has an `Operational constraints` H2, remove that entire H2 section first. Insert before the first H2; if none exists, insert after the opening H1 block and following blanks; if no H1 exists, insert at body start.

Normalize `allowed-tools` deterministically: if YAML list, normalize and flatten each item; if scalar with top-level commas, split on commas outside parentheses; otherwise split on whitespace outside parentheses. Trim entries, preserve source order, and reject empty entries or unbalanced parentheses. Generate no YAML, JSON, tables, code fences, or LLM-written prose. Include the normalized original tool list in one sentence, state the guidance is not runtime enforcement, and end with: `Do not broaden tool use beyond these source Claude Code tool constraints unless the user explicitly authorizes it.`

Tool prose mapping: `Read`/`LS`/`Glob`/`Grep` -> read, list, and search project files as needed; `Write`/`Edit`/`MultiEdit` -> create or modify files only when required; `Bash` -> shell only for command families allowed by the Claude skill; `Bash(...)` -> shell only when matching listed Claude Bash patterns; `WebSearch`/`WebFetch` -> web access only for allowed lookup behavior; `AskUserQuestion` -> ask only for missing input, ambiguity, or permission; `Agent`/`Task` -> delegate only when required and supported; `Skill` -> invoke other skills only when required; unknown or MCP/tool-specific entries -> preserve the literal source tool name in prose.

### Validation And Error Codes

All pre-validation failures emit JSON to stderr and make no changes. Invalid invocation/name exits 64; other pre-validation exits 1.

| Pre-check | Error |
| --- | --- |
| Wrong arg count | `E_INVALID_INVOCATION` |
| Name fails `^[a-z0-9-]{1,64}$` | `E_INVALID_NAME` |
| Source dir missing | `E_SOURCE_SKILL_NOT_FOUND` |
| Source dir not real dir | `E_SOURCE_DIR_INVALID` |
| Source `SKILL.md` missing | `E_SOURCE_SKILL_MD_NOT_FOUND` |
| Source `SKILL.md` not real file | `E_SOURCE_SKILL_MD_INVALID` |
| Source tree contains symlink | `E_SOURCE_SYMLINK_UNSUPPORTED` |
| Source contains `agents/openai.yaml` | `E_SOURCE_OPENAI_METADATA_CONFLICT` |
| Source unreadable as UTF-8 | `E_SOURCE_UNREADABLE` |
| Missing `---` frontmatter | `E_NO_FRONTMATTER` |
| Invalid YAML mapping | `E_FRONTMATTER_INVALID_YAML` |
| Missing/empty `name` | `E_MISSING_NAME` |
| `name` mismatch | `E_NAME_MISMATCH` |
| Missing/empty `description` | `E_MISSING_DESCRIPTION` |
| Missing `disable-model-invocation` | `E_MISSING_DISABLE_MODEL_INVOCATION` |
| `disable-model-invocation` not boolean `true` | `E_DISABLE_MODEL_INVOCATION_NOT_TRUE` |
| Missing/empty `allowed-tools` | `E_MISSING_ALLOWED_TOOLS` |
| Invalid `allowed-tools` shape/normalization | `E_ALLOWED_TOOLS_INVALID` |
| Missing/empty `argument-hint` | `E_MISSING_ARGUMENT_HINT` |
| Empty body | `E_EMPTY_BODY` |
| `.agents/skills/` is file or symlink | `E_DEST_ROOT_INVALID` |
| Destination already exists | `E_DEST_DIR_EXISTS` |
| Canonical destination escapes expected path | `E_DEST_PATH_UNSAFE` |

Conversion failures exit 2 after successful rollback, or 3 if rollback fails.

| Step | Failure |
| --- | --- |
| Create `.agents/skills/` | `E_DEST_ROOT_CREATE_FAILED` |
| Create temp destination under `.agents/skills/` | `E_TEMP_DEST_CREATE_FAILED` |
| Copy source tree | `E_SOURCE_COPY_FAILED` |
| Write transformed `SKILL.md` | `E_DEST_SKILL_WRITE_FAILED` |
| Create `agents/` | `E_OPENAI_METADATA_DIR_CREATE_FAILED` |
| Write `agents/openai.yaml` | `E_OPENAI_METADATA_WRITE_FAILED` |
| Rename temp dir to final destination | `E_DEST_FINALIZE_FAILED` |

Post-validation failures also exit 2 after rollback.

| Post-check | Error |
| --- | --- |
| Source dir missing | `E_POST_SOURCE_DIR_MISSING` |
| Source `SKILL.md` missing | `E_POST_SOURCE_SKILL_MD_MISSING` |
| Source manifest changed | `E_POST_SOURCE_CHANGED` |
| Destination dir missing | `E_POST_DEST_DIR_MISSING` |
| Destination wrong canonical location | `E_POST_DEST_WRONG_LOCATION` |
| Destination `SKILL.md` missing/unreadable | `E_POST_DEST_SKILL_MD_MISSING` |
| Destination frontmatter invalid | `E_POST_FRONTMATTER_INVALID` |
| Destination frontmatter not exactly `name`, `description` | `E_POST_FRONTMATTER_FIELDS_INVALID` |
| Destination name invalid | `E_POST_NAME_INVALID` |
| Destination description differs from source | `E_POST_DESCRIPTION_INVALID` |
| Claude fields still present | `E_POST_CLAUDE_FIELDS_PRESENT` |
| Operational constraints missing/duplicated | `E_POST_OPERATIONAL_CONSTRAINTS_INVALID` |
| Operational constraints not first H2 | `E_POST_OPERATIONAL_CONSTRAINTS_ORDER` |
| `agents/openai.yaml` missing/unreadable | `E_POST_OPENAI_METADATA_MISSING` |
| `agents/openai.yaml` invalid YAML | `E_POST_OPENAI_METADATA_INVALID_YAML` |
| `allow_implicit_invocation` not boolean `false` | `E_POST_INVOCATION_POLICY_INVALID` |
| `default_prompt` missing or lacks `$<skill-name>` | `E_POST_DEFAULT_PROMPT_INVALID` |
| Copied non-transformed files differ | `E_POST_COPIED_FILES_INVALID` |

### Conversion And Rollback

Before destination mutation, create a complete source backup and manifest of every source path, size, executable bit, and SHA-256 hash. Then create destination root, temp destination, copy source, transform temp `SKILL.md`, write temp `agents/openai.yaml`, validate temp output, atomically rename temp destination to final path, and validate final source preservation plus final destination identity.

Rollback deletes temp destination, deletes final destination only if this run created it, restores source from backup if its manifest changed, rechecks the source manifest, emits the original error, and exits 2. If rollback fails, emit `E_ROLLBACK_FAILED` with `original_error`, `rollback_failure`, `source_backup_path`, and `manual_intervention_required: true`; exit 3.

### Error Output

Emit exactly one JSON object to stderr for errors; no tracebacks, logs, warnings, progress text, or human-only prose.

Required fields: `status: "error"`, `error_code`, `message`, `phase`, `context`, `remediation`. `context` must contain machine-parseable JSON only. Frontmatter errors include `field`, `expected`, and `actual_type`; filesystem errors include relevant expected and actual paths. Example message for `E_SOURCE_SKILL_NOT_FOUND`: `Claude skill 'foo' was not found at '.claude/skills/foo/SKILL.md'.`

### Success Output

Emit exactly one JSON object to stdout and exit 0. Required fields: `status: "ok"`, `skill_name`, `source_preserved`, `destination_created`, `openai_metadata_created`, `fields_kept_in_skill_md: ["name", "description"]`, `fields_removed_from_skill_md: ["disable-model-invocation", "allowed-tools", "argument-hint"]`, `fields_translated_to_body: ["allowed-tools"]`, `fields_translated_to_openai_yaml: ["disable-model-invocation", "argument-hint"]`, `source_manifest_unchanged: true`, `copied_file_count`.

### Exit Codes

`0` success; `1` pre-validation failed with no changes; `2` conversion/post-validation failed and rollback succeeded; `3` rollback failed and manual repair may be needed; `64` invalid invocation or skill name.

### Idempotency

Non-overwriting by design. First run succeeds only if `.agents/skills/<skill-name>/` is absent. Re-run after success fails with `E_DEST_DIR_EXISTS`. Retry after failed conversion is safe if rollback succeeded. Never silently merge or overwrite a Codex skill.

### Acceptance Tests

Cover: minimal success; success preserving `scripts/`, `references/`, `assets/`; missing source; missing/mismatched `name`; missing `description`; missing or false `disable-model-invocation`; missing/empty/invalid `allowed-tools`; missing/empty `argument-hint`; invalid YAML; malformed invocation; path traversal like `../foo`; existing destination; symlink rejection; source `agents/openai.yaml` conflict; Claude field removal; `agents/openai.yaml` creation; boolean `allow_implicit_invocation: false`; operational constraints insertion before first H2, replacement of existing section, and no-H2 body behavior; rollback after simulated destination write failure and post-validation failure; source manifest unchanged after success.

### Dependencies

Python 3.9+ with `PyYAML` declared via PEP 723 metadata or sibling `requirements.txt`. Standard library only beyond PyYAML: `pathlib`, `tempfile`, `shutil`, `hashlib`, `stat`, `json`, `sys`, `re`. No network calls, shell-out, Git commands, or LLM calls.

### Non-Goals

Claude slash-command conversion; deleting or moving Claude skills; bidirectional sync; Git authority detection; semantic diff/convergence after independent edits; runtime enforcement through Codex config/rules/hooks/sandbox/approvals; personal-scope `~/.claude/skills`; admin `/etc/codex/skills`; plugin packaging; skill renaming; overwriting or merging existing Codex skills.
