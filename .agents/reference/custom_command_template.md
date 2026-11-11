## Custom Slash-Command Template (Copy/Paste Ready)

````markdown
<!--
  TEMPLATE INSTRUCTIONS (for the creating agent — remove before saving the final command):

  - Read the user-provided spec/source in full before drafting.
  - Populate, adapt, or delete sections intentionally; do not leave placeholders.
  - Default to omission: if a section does not apply, remove it entirely (do not leave an empty stub).

  Argument handling:
  - If the command accepts NO arguments: omit `argument-hint` and do not reference `$ARGUMENTS` or `$1/$2/...`.
  - If the command accepts ONE argument blob: use `$ARGUMENTS`.
  - If the command accepts MULTIPLE distinct arguments: use `$1`, `$2`, `$3`, ... and define each.
  - If arguments are OPTIONAL: state defaults and what happens when omitted.
  - argument-hint examples:
    - Required: <file-path> <name> (required - target file, tool name)
    - Optional: [scope] (optional - limits analysis to that directory)
    - Mixed:    <file-path> [--flag] (required - target file, optional - enables verbose output)

  Process writing rules:
  - Each step should be a single, verifiable action.
  - State what to DO, not what to think about.
  - If a step has sub-actions, use a nested list.
  - If a step depends on a previous step's output, state the dependency (and step number) explicitly.
  - If a step requires judgment, state the criteria for that judgment.
  - If a step can fail, state the failure path before moving to the next step.

  Output consumer:
  - If the output is for HUMANS: keep the human section and delete the agent section.
  - If the output is for AI AGENTS: keep the agent section and delete the human section.
  - If the consumer is not specified: stop and ask before proceeding. Do not guess.
-->

---

description: {{ONE_SENTENCE_DESCRIPTION_OF_WHAT_THIS_COMMAND_DOES}}
argument-hint: {{ARGUMENT_HINT}}
allowed-tools: {{COMMA_SEPARATED_LIST_OF_ALLOWED_TOOLS}}

---

# {{/command-name}}: {{Human-Friendly Title}}

## Philosophy (Why this exists)

{{Philosophy = principles/constraints that guide judgment when the process doesn’t specify.}}
{{Not philosophy = rephrasing the frontmatter description.}}
{{Keep it 1–3 sentences; decision-shaping, not feature summary.}}

## Invocation & Arguments (INPUT) (omit if no arguments)

**Usage examples**

- `{{/command-name}}` {{(if no arguments)}}
- `{{/command-name}} {{EXAMPLE_REQUIRED_ARGS}}` {{(if required)}}
- `{{/command-name}} {{EXAMPLE_OPTIONAL_ARGS}}` {{(if optional)}}

**Arguments received**

- Positional: `$1`, `$2`, `$3`, ...
- All args as a single string: `$ARGUMENTS`

**Arguments policy (choose ONE)**

- **Mandatory**: Arguments are required. If missing/invalid, stop and ask.
- **Optional**: Arguments may be omitted. If omitted, apply defaults.
- **None**: This command must be invoked with no arguments. If provided, stop and ask to re-run without args.

**Argument contract**

- Required args: {{LIST_REQUIRED_ARGS_OR_WRITE_NONE}}
- Optional args: {{LIST_OPTIONAL_ARGS_OR_WRITE_NONE}}
- Defaults (if any): {{DEFAULTS}}
- Validation rules: {{E.G._MUST_BE_EXISTING_FILEPATH__ALLOWED_ENUM_VALUES__ETC}}

**If arguments are missing/invalid**

- {{EXPLICIT_BEHAVIOR}} (e.g., “Stop and ask for the missing value”, or “Return an error-style report and do not proceed”.)

## Context to Load (INPUT) (omit if none)

{{List everything the agent must see to succeed. Prefer explicit file references and concrete constraints. Keep this as context, not instructions.}}

**Read these files (auto-load into context)**

- @{{path/to/relevant_reference_1.md}}
- @{{path/to/relevant_reference_2.md}}

**Optional: capture live state (auto-run bash, if allowed)**

- !`{{command_that_captures_context_1}}`
- !`{{command_that_captures_context_2}}`

## Process (PROCESS)

Follow these steps in order:

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}
4. {{STEP_4}}
5. {{STEP_5}}

**Decision discipline**

- If you must make assumptions: list them explicitly and keep them minimal.
- If blocked by missing info: stop and ask targeted questions (unless the argument contract says to fail fast).

**Quality/Safety constraints**

- {{CONSTRAINT_1}} (e.g., “Do not change unrelated files.”)
- {{CONSTRAINT_2}} (e.g., “Avoid large refactors.”)
- {{CONSTRAINT_3}} (e.g., “Do not introduce new dependencies.”)

## Output (OUTPUT)

**Output consumer (choose ONE)**

- Keep exactly one of the two sections below and delete the other. Do not mix formats.

---

### Human-Readable Report (for humans)

Return a concise, easy-to-scan summary in plain language at a 16-year-old reading level that lets a human verify you “got it”:

- **Status**: {{Success|Partial|Blocked}}
- **What you understood**: {{1–3 bullets}}
- **What you did**: {{bullets, in execution order}}
- **Key results**: {{bullets; include locations like `file:line` when relevant}}
- **Risks / gotchas**: {{bullets, only if real}}
- **Next steps**: {{bullets}}
- **Questions (only if needed)**: {{numbered list}}

---

### Structured Agent Handoff (for AI agents; no ambiguity)

Return a single structured block that another agent can execute without conversation context.

**Required format (YAML)**
Include only non-empty fields. Omit empty lists/objects entirely.

```yaml
status: {{success|partial|blocked}}
summary: {{one_sentence}}

arguments:
  raw: "$ARGUMENTS"

artifacts:
  # Files created/updated by running this command (or files the next agent must read)
  - path: "{{relative/or/absolute/path}}"
    purpose: "{{why it exists / what to do with it}}"

next_action:
  # Exactly what the consuming agent should do next (command or slash command), with all required parameters.
  run: "{{exact_command_or_next_slash_command}}"

# Optional extensions (include only when relevant)

# parsed_arguments:
#   arg1: "{{value}}"
#   arg2: "{{value}}"
#   # add more as needed
#
# assumptions:
#   - "{{assumption_1}}"
#   - "{{assumption_2}}"
#
# actions:
#   # Exact commands to run, in order (include cwd if non-default)
#   - run: "{{exact_shell_command}}"
#   - cwd: "{{optional}}"
#     run: "{{exact_shell_command}}"
#
# file_changes:
#   - path: "{{file_path}}"
#     change_type: "{{create|modify|delete}}"
#     instructions:
#       - "{{explicit_edit_1}}"
#       - "{{explicit_edit_2}}"
#
# acceptance_criteria:
#   - "{{criterion_1}}"
#   - "{{criterion_2}}"
#
# validation:
#   - "{{exact_validation_command_1}}"
#   - "{{exact_validation_command_2}}"
#
# blockers:
#   - "{{what_is_blocking_and_what_input_is_needed}}"
```

## Notes (Optional) (omit if empty)

- {{NOTES_FOR_FUTURE_MAINTAINERS_OR_WHEN_TO_USE_THIS_COMMAND}}
- {{LINKS_OR_REFS_IF_RELEVANT}}
````
