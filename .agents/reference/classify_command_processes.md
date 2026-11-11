# Classifying Command Processes by Determinism

## Philosophical Approach

### The core distinction

Code is **deterministic** — given the same inputs, it produces the same outputs every time. AI is **probabilistic** — usually produces what you want, sometimes doesn't. Code is a recipe; AI is a cook. Code is predictable but brittle; AI is flexible but fuzzy.

### The atomic task is the unit of analysis

A command should correspond to one coherent task with one input shape and one output shape. Don't decompose further: chopping every probabilistic moment into its own command, chained with deterministic scripts, creates more coordination overhead than the work itself. The atomic task is the level at which the unit is useful on its own — to a human, to another command, or to a script chaining several together.

### The three buckets

**Bucket 1 — Genuinely probabilistic.** The whole process requires judgment, interpretation, or natural-language reasoning end-to-end. No script could do it because the inputs are fuzzy and "correct" depends on context. Belongs as an AI command.

**Bucket 2 — Deterministic in disguise.** Written as an AI process with heavy guardrails (numbered steps, validation rules, strict output formats) precisely because the underlying task is mechanical. If the guardrails are doing all the work, the AI is doing none. Belongs as code.

**Bucket 3 — Mixed.** The process has a judgment spine with mechanical scaffolding around it. Keep it as an AI command (so the judgment can flow naturally) but factor the deterministic scaffolding into one or more scripts the command calls.

### The judgment spine filter

For each command, ask: does the process have a judgment spine — a place where the AI is actually deciding something — or is the "judgment" just guardrails dressed up to look like judgment?

- Genuine spine → bucket 1 or 3.
- No spine, just guardrails → bucket 2.
- Spine plus mechanical scaffolding → bucket 3.

### Step-level diagnostic

For each individual step inside a process:

1. **Is the input shape predictable?** Predictable (file path, number, enum) → leans code. Natural-language input → leans AI.
2. **Would two competent humans produce the same output?** Yes → code can do it. No → judgment is involved.
3. **Is the rule explicit, or does the AI need to "know what you mean"?** Explicit rule → code. Tacit knowledge → AI.
4. **Are the guardrails essentially re-implementing an `if` statement or a regex?** Yes → that step is bucket-2 leakage.

A step that fails tests 1–3 is a judgment step. A step that passes all four is a deterministic step. If different steps in the same process answer differently, the command is bucket 3.

### Bucket 3 implication: multiple deterministic regions are possible

A bucket 3 command may contain multiple distinct deterministic regions inside its process — not just one. Each contiguous deterministic region maps to its own separate script. One bucket 3 command might call one script (one deterministic phase), or several (multiple phases interleaved with judgment steps), depending on how the determinism is distributed across the process.

## Context For Building The Meta Command

### Purpose

Build a meta command that classifies existing custom commands or skills by determinism. Given one or more paths to command or skill files, the meta command must analyze each file's PROCESS section, assign it to bucket 1, 2, or 3, and — for bucket 3 — identify precisely which steps should be extracted into deterministic code.

### Inputs

One or more paths to existing command or skill files. Accept multiple paths in a single invocation so several commands can be classified together.

Expected locations:

- Custom slash commands: `.claude/commands/**/*.md`
- Claude skills: `.claude/skills/<name>/SKILL.md`
- Codex skills: `.agents/skills/<name>/SKILL.md`

### What to read inside each file

Focus on the PROCESS section only. In files using the project's `custom_command_template.md`, this is the section headed `## Process (PROCESS)` containing the numbered steps. Other sections (Philosophy, Invocation & Arguments, Context to Load, Output) may be read for context but are not the subject of classification.

If a file lacks a clearly demarcated PROCESS section, infer the equivalent procedural steps from the body and note the ambiguity in the output.

### Classification logic

Apply the philosophical approach above:

1. Determine whether the process has a judgment spine.
2. Apply the four-question step-level diagnostic to each step.
3. Assign one bucket per command:
   - **Bucket 1** if every step requires judgment.
   - **Bucket 2** if no step requires judgment.
   - **Bucket 3** if some steps require judgment and others are mechanical.

### Output requirements

The meta command must return a structured report for each input file. Per-file output must include:

- **File path** classified.
- **Bucket** (1, 2, or 3).
- **Reasoning**: short justification grounded in the step-level diagnostic.
- **Recommendation**:
  - Bucket 1 → keep as-is.
  - Bucket 2 → convert to code; suggest a script outline.
  - Bucket 3 → keep as an AI command, but extract the deterministic phases into separate scripts (see next section).

### Bucket 3 output: enumerate every deterministic region

For each bucket 3 command, the output must clearly enumerate the deterministic regions inside the process. The user must be able to tell, without re-reading the original command, exactly which steps go into which script.

For each region, include:

- The step numbers (or step range) covered by the region.
- A one-sentence summary of what the region does.
- A proposed script name and a one-sentence description of its purpose.
- The expected inputs and outputs of the proposed script, so the AI command can call it cleanly.

Multiple regions per command are expected and must each be listed separately. Do not collapse non-contiguous regions into a single script — preserve the interleaving of judgment and mechanical steps as it exists in the source process.

Illustrative shape (not prescriptive):

```yaml
file: ".claude/commands/foo.md"
bucket: 3
reasoning: "Steps 1–2 require judgment about scope; steps 3–5 are mechanical file edits; step 6 requires judgment about the final report."
deterministic_regions:
  - steps: "3-5"
    summary: "Apply a fixed set of formatting transformations to the captured files."
    proposed_script:
      name: "apply_formatting.py"
      purpose: "Apply the fixed formatting ruleset to a list of file paths."
      inputs: "list of file paths"
      outputs: "modified files, JSON manifest of changes"
```

### Output consumer

The meta command's output is for a human reviewer. Use the human-readable report shape defined in `custom_command_template.md`. The classification is a judgment call the user will want to review before acting on it.

### Edge cases

- **No process section** → flag and skip classification rather than guess.
- **Trivially short process** (one or two steps) → still classify, but note the limited evidence.
- **Skill with bundled scripts already present** → note this; existing scripts do not by themselves change the bucket but may indicate partial bucket 3 implementation already underway.

### Constraints

- Read-only. The meta command must not modify any command or skill file. Its only output is the classification report.
- Do not propose specific code implementations beyond the script name, purpose, inputs, and outputs. Writing the actual script content is a separate downstream task.

## Context For Building The Process Editor Meta Command

### Purpose

Build a second meta command that consumes the classifier output and the actual scripts the user has subsequently written, and surgically edits the original command or skill file. Deterministic step regions identified by the classifier are replaced in-place with new process steps that invoke the user's scripts. Judgment steps are preserved. Everything outside the PROCESS section is preserved byte-for-byte.

This editor meta command runs *after* the classifier and *after* the scripts have been written. It is only meaningful for files the classifier assigned to bucket 3.

### Inputs

The editor meta command must be invoked with three things:

- **The path to the original command or skill file** — the same file the classifier analyzed.
- **The classifier output for that file** — the enumerated deterministic regions (step ranges, summaries, proposed script names, expected inputs/outputs). Accept this as a path to a YAML/JSON report, or as inline structured input.
- **For each deterministic region, the script that has been written to replace it.** Each script entry must include:
  - Path to the script file.
  - The exact invocation command (e.g., `python .claude/commands/scripts/foo.py <args>`).
  - The actual inputs the script accepts (these may differ from the classifier's proposed inputs; trust the actual script).
  - The actual outputs the script produces (stdout shape, files written, exit codes).
  - The step range in the source command that this script replaces (must match a region from the classifier output).

The relationship between deterministic regions and scripts must be one-to-one. Reject the invocation if a region has no script, or if a script has no region.

### Pre-edit validation

Before any file mutation:

- The command/skill file exists and is readable.
- The PROCESS section is locatable and parseable as a numbered list.
- Each step range cited in the inputs corresponds to existing steps in the current PROCESS section.
- Step ranges do not overlap with one another.
- The PROCESS section content for each step range still matches what the classifier saw — i.e., detect drift if the file has been edited since classification.
- Every referenced script file exists at the path provided.

If drift is detected, stop and ask the user whether to proceed, re-run the classifier, or abort. Do not silently edit against a stale classification.

### Edit logic

For each (deterministic region, script) pair:

- Locate the contiguous step range inside the PROCESS section.
- Remove those steps.
- Insert replacement step(s) in their place that instruct the AI to invoke the script. Each replacement step must:
  - State the script's purpose in one line, so the AI executing the command at runtime knows what the script is for.
  - Give the exact invocation command, with input placeholders made explicit (where the AI should source the arguments from earlier judgment steps).
  - State what the script returns and how the AI should consume the output for subsequent steps.
- Renumber all subsequent steps so the PROCESS section remains a clean numbered list.
- Preserve all other steps verbatim.

Outside the PROCESS section, change nothing. Frontmatter, philosophy, input/context sections, output sections, and notes must pass through byte-for-byte (modulo the unavoidable step renumbering inside PROCESS).

### Allowed-tools handling

If a script invocation requires Bash (or a narrower pattern) and the command/skill frontmatter's `allowed-tools` does not already permit it, propose the minimal addition needed. Do not silently change `allowed-tools` — surface the proposed change in the output and ask the user to confirm before applying.

### Output requirements

The editor meta command must return:

- **Status**: Success / Partial / Blocked.
- **File edited** (path).
- **Summary of edits**: for each replaced region, list the original step range, the replacement step number(s), and the script invoked.
- **Diff or rendered preview** of the PROCESS section before and after.
- **Allowed-tools change** (if proposed): show before and after, plus an explicit ask for confirmation.
- **Validation result**: confirm the edited file parses cleanly — frontmatter still valid YAML, PROCESS section still a clean numbered list, no orphaned or duplicated step numbers.

### Safety constraints

- Hold the original file contents in memory before editing.
- On any failure during edit or post-validation, rollback to the original contents and emit an error.
- Never edit any file other than the named command or skill file.
- Do not write or modify the scripts; assume they already exist as inputs to this command.
- Do not modify any section other than PROCESS (and `allowed-tools` only with explicit confirmation).

### Output consumer

The editor meta command's output is for a human reviewer. Use the human-readable report shape defined in `custom_command_template.md`. After editing, the user should be able to read the report and immediately see which steps were replaced, by which scripts, and whether any frontmatter changes are pending confirmation.

### Edge cases

- **File classified as bucket 1 or 2** → stop and explain; this editor is only meaningful for bucket 3.
- **Region step range matches but content has drifted** → stop and ask before editing.
- **Multiple regions with overlapping step ranges** → reject as invalid input.
- **Script expects inputs that no earlier judgment step produces** → flag in the output as a likely bug in the region-to-script mapping; do not edit.
- **PROCESS section uses non-numbered formatting** (e.g., narrative paragraphs) → stop and ask; the editor depends on a numbered list to locate step ranges.
