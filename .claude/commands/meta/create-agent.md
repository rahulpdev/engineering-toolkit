---
description: Create a new sub-agent in `.claude/agents/` from the standard sub-agent template, using one required argument and three optional mode arguments
argument-hint: "<agent-spec: required, quote if it contains spaces> [invocation-mode: optional trailing arg, default=manual, values=autonomous|manual|hybrid] [handoff-mode: optional trailing arg, default=stop-and-wait, values=act-immediately|stop-and-wait|conditional] [artifact-mode: optional trailing arg, default=none, values=report|none]"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(ls:*), Bash(test:*), AskUserQuestion
---

# /create-agent: Create a Sub-Agent

## Philosophy (Why this exists)

Sub-agents are most effective when they are narrow, predictable, and reusable. Because they run in isolated contexts, the handoff back to the primary agent is a critical context-compression boundary: the new agent must make its output structure explicit so that the primary agent does not infer missing meaning. This command enforces that by requiring the use of a shared template, and explicit mode decisions, to draft every new agent build.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/create-agent "Review newly written TypeScript API code for auth and error-handling issues"`
- `/create-agent "Validate a completed PRP against repository conventions before implementation" manual act-immediately`
- `/create-agent "Research third-party SDK upgrade risks and summarize migration concerns" hybrid conditional report`

**Arguments received**

- Positional: `$1`, `$2`, `$3`, `$4`
- All args as a single string: `$ARGUMENTS`

**Arguments policy**

- **Optional**: `$1` is required. `$2`, `$3`, and `$4` are optional trailing arguments with defaults.

**Argument contract**

- Required args:
  - `$1` = agent spec or extra context for the agent to create. Quote this argument if it contains spaces.
- Optional args:
  - `$2` = invocation mode. Allowed values: `autonomous`, `manual`, `hybrid`
  - `$3` = output handoff mode. Allowed values: `act-immediately`, `stop-and-wait`, `conditional`
  - `$4` = artifact mode. Allowed values: `report`, `none`
- Defaults (if any):
  - If `$2` is omitted, use `manual`
  - If `$3` is omitted, use `stop-and-wait`
  - If `$4` is omitted, use `none`
- Validation rules:
  - At least `$1` must be present.
  - If provided, `$2`, `$3`, and `$4` must match the allowed enum values exactly.
  - Defaults apply only to omitted trailing arguments.
  - `$1` must be specific enough to derive a focused agent name, mission, scope boundary, and minimum viable tool set.

**If arguments are missing/invalid**

- If `$1` is missing, stop and ask the user to re-run `/create-agent` with an agent spec.
- If any provided value for `$2`, `$3` or `$4` is invalid, stop before writing files, explain which value is invalid, and ask the user to re-run the command with valid arguments.

## Context to Load (INPUT)

**Read these files (auto-load into context)**

- @.agents/reference/subagent_template.md

**Optional: capture live state (auto-run bash, if allowed)**

- !`ls -1 .claude/agents 2>/dev/null || echo "(agents directory not yet created)"`

## Process (PROCESS)

Follow these steps in order:

1. Validate `$1`, `$2`, `$3`, and `$4` against the Argument contract above.
2. Derive the new sub-agent spec from the current conversation context plus `$1`.
   - Infer a kebab-case agent name.
   - Define one narrow area of expertise, one clear mission, and clear out-of-scope boundaries.
   - If `$2` is `autonomous` or `hybrid`, write the `description` principally for an AI primary agent; imperative, unambiguous, and precise.
   - Determine the minimum tool set (least privilege) and the most appropriate model.
3. Stop-and-ask gate (do not write files yet).
   - If any of the following are unclear, stop and ask targeted questions:
     - The spec does not provide enough concrete standards to make the agent self-contained.
     - Any tools that must be allowed (and why).
4. Ensure the target directory exists by running `mkdir -p .claude/agents`.
5. Check whether `.claude/agents/<agent-name>.md` already exists.
   - If it exists, stop and ask before overwriting.
   - If it does not exist, continue.
6. Design the primary-agent handoff contract as a first-class design problem.
   - If the primary agent may branch conditionally, make that rule explicit and observable from the sub-agent’s output alone, and ensure the output is sufficient for that decision.
   - Instruct the primary agent to state any assumptions or material inferences if the handoff contract allows it to proceed.
   - Specify precise next-action instructions the primary agent should follow, avoid vague instructions such as "report back", "summarize findings", or "continue if appropriate".
7. Draft the new sub-agent using `@.agents/reference/subagent_template.md`. Do not draft freehand.
   - Remove the template instruction comment block before saving.
   - Replace every placeholder with concrete, project-specific content derived from the current context and `$1`.
   - Embed concrete standards from the current context and `$1` when they materially shape the sub-agent’s behavior, including tool restrictions, missing-context policy, exact path conventions, naming rules, severity levels, output fields, artifact structure and other materially relevant project constraints.
   - Do not rely on generic phrases such as "follow project standards", "use existing patterns", or "review against best practices" unless the generated agent makes those standards explicit enough to execute.
   - Apply `$2` exactly as the template requires for Decision 1.
   - Apply `$3` exactly as the template requires for Decision 2.
   - Apply `$4` exactly as the template requires for Decision 3.
   - If `$4` is `report` and the current context does not imply a stronger location, use the default artifact path pattern `.agents/reports/<agent-name>-<timestamp>-<scope>.md`.
   - Keep the sub-agent self-contained. Do not rely on unstated chat history inside the generated sub-agent.
   - Remove any sections that do not apply — no empty stubs.
8. Validate the draft before writing it.
   - Confirm the agent YAML frontmatter is valid (`name`, `description`, optional `model`, `tools`, `color`)
   - Confirm the `description` field aligns with the chosen invocation mode.
   - Confirm the `tools` field (if present) is sufficient to execute every step in the generated process.
   - Confirm the `Invocation Policy`, `Artifact Contract`, `Output`, and `Primary-Agent Handoff Policy` sections are internally consistent with `$2`, `$3`, and `$4`.
   - Confirm there are no leftover `{{...}}` placeholders.
   - Confirm the process steps are single, verifiable actions in dependency order.
   - Confirm the generated agent is understandable and executable without relying on unstated repository knowledge or the spec that created it.
   - Confirm the new sub-agent is specialized rather than generic.
   - Confirm the primary agent can choose the next action from the sub-agent’s output alone, without inferring missing context, (if it may act or branch conditionally) and any assumptions or inferences made by the primary agent are clearly stated.
   - Confirm the output section preserves the template’s YAML handoff contract, including `status`, `summary`, `artifacts`, `assumptions`, and `recommended_next_action`.
9. Write the final file to `.claude/agents/<agent-name>.md`.
10. Return the final response using the Human-Readable Report section below.

**Decision discipline**

- Make the fewest assumptions necessary and list them explicitly.
- Prefer a narrow, reusable sub-agent over a broad catch-all agent.
- If the current context and `$1` conflict, surface the conflict instead of silently choosing one.

**Quality/Safety constraints**

- Do not create or modify files outside `.claude/agents/` while running this command, except for reading the required reference files.
- Do not overwrite an existing sub-agent without explicit user approval.
- Keep the new agent’s system prompt focused on a single area of expertise.
- Keep `tools` for the new agent minimal (only what the agent truly needs).
- Keep the generated sub-agent aligned to the common standard enforced by `@.agents/reference/subagent_template.md`.

## Output (OUTPUT)

### Human-Readable Report

Return a concise, easy-to-scan summary in plain language at a 16-year-old reading level:

- **Status**: Success | Blocked
- **What you understood**: 1-3 bullets covering the requested agent, its scope, and the three selected modes
- **Artifact**: `.claude/agents/<agent-name>.md` (or intended path if blocked)
- **How to run**: exact `/create-agent` invocation used, plus the created agent name
- **Key design choices**: chosen model, allowed tools rationale, notable scope boundaries, and any artifact path convention used
- **Questions (only if needed)**: numbered list (only if blocked)

## Notes

- The template at `@.agents/reference/subagent_template.md` is mandatory. If it feels insufficient, improve the template rather than bypassing it.
