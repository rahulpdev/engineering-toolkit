---
description: Perform an adversarial review of a feature plan against the full defect category set, verifying cited references against the codebase and writing a human-readable review with a Findings Summary to the target directory (the folder a workflow names in `$ARTIFACTS_DIR` when it runs this command, `docs/reviews/` otherwise), then have the document-reviewer sub-agent read the review and correct its wording.
argument-hint: <plan-filepath> (required - path to the feature plan markdown file to review)
allowed-tools: Read, Write, Edit, Grep, Glob, Agent, Bash(mkdir:*), Bash(test:*), Bash(basename:*)
---

# /plan-review: Adversarial Plan Review

## Philosophy (Why this exists)

The agent that carries out a plan does what the plan says, word for word. This command exists to look hard for weak points in a plan before implementation by surfacing gaps the author cannot see themselves: capabilities the plan promises but silently drops, tests that pass while the feature is broken, and cures (the fixes a review proposes for its findings) that quietly remove something the plan promised. Coverage requires an explicit statement per category; silence is not coverage. Cures must be audited against the plan's own Problem Statement and User Story, because closing a finding by removing a promised capability is the most common way this loop (the repeated rounds of review and fix, each round called a cycle) degrades a plan, and the cost is invisible when the reviewer stops at `finding cleared`, the note that a finding has been dealt with.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/plan-review docs/plans/add-user-authentication.md`
- `/plan-review docs/plans/detect-pdf-table-plan.md`

**Arguments received**

- Argument: `$ARGUMENTS`, the text typed after the command's name

**Arguments policy**

- **Mandatory**: `$ARGUMENTS` is required.

**Rules for the argument**

- Required arguments: `$ARGUMENTS` = path to the plan markdown file.
- Optional arguments: None.
- Validation rules:
  - `$ARGUMENTS` must be a path to an existing readable file.
  - `$ARGUMENTS` must end in `.md`.

**If arguments are missing/invalid**

- If `$ARGUMENTS` is absent, stop and ask for the plan file path.
- If `$ARGUMENTS` does not exist or is unreadable, stop and ask for a valid path.

## Process (PROCESS)

Follow these steps in order:

1. **Validate the plan file.**
   - Capture the artifacts directory, the folder where a workflow run keeps the files it produces, into a shell variable, a named value the shell keeps for the commands that follow: `DIR="$ARTIFACTS_DIR"`. `$ARTIFACTS_DIR` is an environment variable (a named setting a program is started with) which Archon, the tool that runs commands like this one as steps of a workflow, sets to that folder.
   - If `$DIR` is non-empty, confirm the plan exists with `test -f "$DIR/plan.md"` (Archon workflow context); the plan source is `$DIR/plan.md`.
   - Otherwise, confirm the plan exists with `test -f "$ARGUMENTS"` (a person typed the command); the plan source is `$ARGUMENTS`, and derive `<plan-name>`, the plan's file name without its folder or its `.md` ending, from `basename "$ARGUMENTS" .md` for the review filename.
   - If the check fails, stop: if a person typed the command, ask for a valid path; under Archon, report the missing plan input and halt.

2. **Read the plan in full.**
   - Read the plan source from top to bottom.
   - Extract the Problem Statement, User Story, Solution Statement, Feature Description, Feature Metadata, Task list, Test list, Acceptance Criteria, Validation Commands, Confidence Score, and any NOTES entries recording finding classes the author has considered and rejected on prior cycles.
   - Track every claim, cited file, cited symbol (the name of a function, class or constant), cited API field (a field in the reply an outside service sends; a service's API is the set of requests it answers), cited CLI flag (an option typed after a command's name at the command line, the CLI), cited line number, cited task number, and cited test name.

3. **Verify cited references against the codebase.**
   - For every file the plan cites, use `Read`, `Grep`, or `Glob` (the tools that read a file, search files for a piece of text, and find files by name) to confirm the file exists and contains what the plan asserts.
   - For every symbol, function, field, or flag the plan cites, `Grep` for it in the referenced file or the wider codebase.
   - When the plan proposes replacing a pattern fixed in the code (path, piece of text the code gives a special meaning, value of a setting, repeated block) in a cited file, `Grep` the file for every occurrence of that pattern and confirm the plan's tasks address all of them. Partial substitutions (some occurrences addressed, others left alone) are a defect class the plan itself will not surface.
   - Do not take the plan's word for what its cited files contain.
   - Where verification is impossible (external API, file not in the repository), state that explicitly in the relevant finding.

4. **Prepare the target review file.**
   - Capture the artifacts directory into a shell variable: `DIR="$ARTIFACTS_DIR"`.
   - If `$DIR` is non-empty, create it with `mkdir -p "$DIR"` and set the target path to `$DIR/plan-review.md` (Archon workflow context).
   - Otherwise, create `docs/reviews/` with `mkdir -p docs/reviews/` and set the target path to `docs/reviews/<plan-name>-plan-review.md` (a person typed the command).

5. **Review the plan against every category defined below.**
   - Produce findings in each category listed below. State `no findings` explicitly for any category with zero findings. Silence is not coverage.
   - For every finding, state the affected behaviour or claim concretely; do not speculate broadly.
   - If the plan's NOTES rejection log records this finding class as considered and rejected on a prior cycle, either name what has changed since that rejection OR acknowledge the prior rejection in the finding itself. Do not silently raise the same class of finding again.
   - Tag each finding as **[material]** (requires plan changes) or **[cosmetic]** (only the plan's wording is off, or less exact than it should be).
   - For every finding, propose a cure AND audit it against the plan's stated Problem Statement and User Story.
   - **Removal-first cure discipline.** Before proposing an additive cure (new test, new rule, new validator that rejects input that is not valid, new guard that refuses a dangerous action before it runs), explicitly consider whether _removing_ the thing the finding attaches to resolves the finding. If removal resolves the finding without cost to the Problem Statement, the removal cure is the correct one; additive cures require justification for why removal was rejected. Record the removal-consideration outcome on every finding. Rationale: additive cures pile up extra checks and rules around a weakness in the design underneath; removal cures get rid of the weakness. Without this discipline the repeated rounds of review and fixing reliably compound over-specification rather than resolving it.
   - If the cure removes a capability the Problem Statement promises, mark it **value-prop-amputating** (the label for a cure that removes part of what the plan promises to deliver; value-prop is short for value proposition, meaning that promise) and either propose an alternative that preserves the promise OR state `no preserving cure in scope, operator decision needed`, the line telling the User (the operator) that only they can settle this trade-off, with the trade-off laid out. Do not decide for the author when the cure is value-prop-amputating.

   **The categories:**
   1. **Implementation contradicts the plan's own claims**: code, task placement, or the point in the order of the code's steps where something runs does the opposite of the narrative (e.g. `fires every cycle` while the code sits behind a check that skips most cycles; `covers X` while no test exercises X; `uses Y` while Y isn't actually called from any of the code shown); observability claims (claims about what the system will log or report) not reflected in the code that would produce those records.
   2. **Promised in narrative, missing from tasks/tests**: capabilities the Feature Description, User Story, or Solution Statement promises that no Task implements and no test exercises; hedges that quietly remove a promised capability.
   3. **References to things the plan doesn't define or verify**: field names, signatures (a function's name and the values it takes), functions, external API fields, CLI flags, line numbers, task numbers, values from a fixed list of names asserted but not shown or tied to a cited source.
   4. **Tests that would pass when the feature is broken**: assertions (a test's checks that something is true) that don't exercise the failure mode; `assert in (X, Y)`, which passes if the value is either of two things, or patterns whose result can change from one run to the next; negative assertions (checks that something is not so) whose target values don't match what the rule under test would compute; settings that decide whether a test runs at all (`RUN_INTEGRATION`, `pytest.mark.slow`, project-specific equivalents) named but absent from Validation Commands; stubs (stand-ins for real code) that bypass the code under test; fixtures (pieces of test setup) whose setup can't distinguish a broken feature from a clean starting state.
   5. **Security documented but not enforced**: controls whose enforcing check (hook, validator, guard, allow-list; a hook is a script Claude Code runs by itself at set moments) doesn't cover what the narrative claims to protect (e.g. a rule in prompt text that a hook judging writes only by their file path can't see, or a step that turns input into one standard form, called input canonicalisation, that runs after the guard); tools granted to a model where the harm they could do is not limited by any check; asymmetric security tests (testing only what should be allowed, or only one direction of an attack that works both ways, such as symlinks followed in one direction only or redirects tested on one side only; a symlink is a file that points to another file, and a redirect sends a request on to another address); code handling badly formed input that does not refuse when it cannot read that input.
   6. **Silent gaps on failure paths**: places where the code stops early (early returns) and so skips the logging or reporting the plan claims; code that catches an error (an exception handler) but doesn't mark every affected item as failed before passing the error on; counters incremented but never logged; changes to saved state that don't show up anywhere.
   7. **Coverage claims that don't match the plan's own tests**: `covered by tests: X, Y, Z` bullets where no `def test_X` (the line of code that defines a test named `test_X`) exists in the plan; test totals (Feature Metadata, Phase summaries, Acceptance Criteria) that don't match the actual count of test functions in the plan's test code.
   8. **Edge cases not addressed**: hostile inputs, race windows (moments when two things running at once can get in each other's way), deletion or change partway through a run, corrupt or partial state, external API failure, two things using the same resource at once, resource conflicts (two things given the same name, or what to do when the file to be written already exists), redirects and symlinks in both directions, a file or reply whose stated kind of content differs from what it actually holds, and any unusual conditions specific to this plan that the Feature Description or User Story implies but the tests don't exercise.
   9. **Code snippets that wouldn't pass lint or type-check** (lint is the automatic check for errors and poor style; type-check is the tool that checks, before the code runs, that each value is used as the kind it is declared to be): a value declared as one kind and then changed in a way that kind does not allow; values kept inside a function that are never used; a changeable value, such as a list, given as the default for a function's input (a mutable default argument); imports (loading and using code from elsewhere) of things not shown to exist in the plan's stated dependencies.
   10. **Over-strict validators**: rejecting legitimate real-world variance the plan's own examples imply must be accepted.
   11. **Requirements traceability**: Acceptance Criteria not satisfied by any Task or Test; Tasks with no mapped Acceptance Criterion (work beyond what the plan set out to deliver); Tests that don't tie to an Acceptance Criterion or a Task; Confidence Score inflated relative to the coverage the plan actually shows.
   12. **Task DAG and prerequisites** (the DAG, short for directed acyclic graph, is the order in which the tasks depend on one another, which must never loop back on itself): tasks that reference a symbol, file, or state a later task creates; tasks that depend on each other in a loop; prerequisites the plan uses (environment variable, database table, migration (a step that changes the shape of stored data), external service, saved copy of something built earlier) but does not verify exist before use; `atomic and independently testable` claims (that a task is complete in itself and can be tested on its own) that don't hold under the DAG.
   13. **Design fit**: Solution Statement doesn't clearly resolve the Problem Statement; approach conflicts with a convention or pattern in a file the plan itself cites; alternative approaches implied by the problem shape neither acknowledged nor rejected with rationale.
   14. **Assumption disclosure and hedge audit**: essential assumptions the plan relies on but does not state; hedged verbs (`might`, `could`, `consider`, `if applicable`) that leave the agent carrying out the plan without direction on essential points.
   15. **Operational readiness (when applicable)**: for plans affecting running systems, a missing rollback path (a way to undo the change); no way to see a failure in the live system; migration of existing state omitted; work the change creates for whoever has to respond when it breaks, with no written steps for doing it. Refactors (changes that rearrange code without changing what it does) of code that is only called by other code and changes nothing outside itself are exempt; say so explicitly if exempted.
   16. **Unjustified inclusions and framings**: elements the plan carries as essential without stating what fails if they are removed (values passed from one function to another, settings passed down through several layers of code, defensive rules and guards, supporting code copied from neighbouring code, and confident claims phrased as fact). Distinct from Category 14 (hedge audit): 14 hunts hedging words; 16 hunts confident-but-unjustified claims, where the plan reads definitive but nothing names the failure mode averted by keeping the element in.
   17. **Cross-plan consistency**. Defects visible only across plan elements: (a) data or state a preceding step already worked out being re-passed or re-derived by a later step; (b) structurally identical decisions handled differently in different parts of the plan with no rationale. Per-element categories cannot catch these because the defect lives in the relationship between elements, not any single element.
   18. **Runtime environment unverified**: steps in the plan that reach outside the running program (starting a separate program, calling a web address, file locations outside the repository, environment variables, credentials, background services) whose setup on the machine they will run on isn't traced to something already in place (a task in the plan, an entry in a runbook (the written step-by-step instructions for operating the system), an existing setting, or another plan that must be finished first); summary tags like `no new dependencies` or `standard toolchain` that aren't broken down into the setup each of those steps needs.

6. **Run the meta-check.**
   - Before producing the Findings Summary, name any observation you were tempted to record but couldn't place in a category.
   - New classes of defect are the reviewer's most useful output; do not silently drop them.
   - Add each uncategorised class to the summary counts as a separate line.

7. **Produce the Findings Summary block.**
   - **Per-category counts**: list every category with a finding count (use `no findings` where zero); append any uncategorised classes surfaced by the meta-check.
   - **Material findings**: total count.
   - **Cosmetic findings**: total count.
   - **Recommended action**, exactly one of:
     - **PASS**: 0 material findings; plan is ready to implement.
     - **ITERATE**: 1+ material findings; list them, each filed under its category and index.
     - **RE-SCOPE**: plan has structural problems (undefined Problem Statement, multiple value-prop-amputating conflicts with no in-scope cures) that further rounds of fixing cannot resolve; author must re-scope (redraw what the plan covers) before another round.

8. **Write the review file.**
   - Write the review to the target path computed in Step 4.
   - Use the file structure defined in the Review File Structure section below.
   - Do not write partial reviews; every category must be present.

9. **Have the review's wording checked.**
   - Start the `document-reviewer` sub-agent once, using the agent spawning tool with `subagent_type|agent_type: "document-reviewer"`, and pass it two paths and nothing else: the communication standard at `.agents/reference/communication-standard.md` and the review file written in Step 8.
   - Follow the instruction that closes its response, using Edit on the review file only.
   - Correct wording only. Do not change a finding, its tag, a count or the Recommended action, and ignore any finding against a heading or field name the Review File Structure fixes, because `/plan:plan-review-fix` reads the review by those names.
   - If the sub-agent cannot be started, or reports that it is blocked, leave the review as written in Step 8 and say so in the handoff.

10. **Return the handoff report.**
    - Use the Human-Readable Report format below.
    - Do not include the review body in the handoff; point to the file.

**Decision discipline**

- If a claim cannot be verified from the codebase, mark the finding with `verification not possible in scope` rather than asserting the plan is wrong.
- If two findings collapse into the same underlying defect, record them once in the most specific category.
- Do not silently drop an observation because it feels out of scope. Surface it in the meta-check.

**Quality/Safety constraints**

- Do not modify the plan file under review.
- Do not decide the author's product trade-offs when a cure is value-prop-amputating; name the trade-off and stop.
- Do not compress the category list or skip a `no findings` line: the record of what was checked is what this command delivers.

## Review File Structure

Write the review to the target path computed in Step 4 using this structure:

```markdown
# Plan Review: <plan-name>

**Plan reviewed**: `<plan-filepath>`
**Verification scope**: <what was verified against the codebase; what could not be>

## Category 1: Implementation contradicts the plan's own claims

<findings, or `No findings.`>

## Category 2: Promised in narrative, missing from tasks/tests

<findings, or `No findings.`>

<... continue for every category ...>

## Meta-check: uncategorised observations

<any observations that did not fit a category, or `None.`>

## Findings Summary

**Per-category counts**:

- Category 1: <count | no findings>
- Category 2: <count | no findings>
- ... (one line per category)
- Uncategorised: <count | none>

**Material findings**: <N>
**Cosmetic findings**: <N>

**Recommended action**: <PASS | ITERATE | RE-SCOPE>
<if ITERATE: list material findings, each filed under its category and index>
<if RE-SCOPE: name the structural problems>
```

**Per-finding format:**

```markdown
### Finding <category>.<index>: <one-line title> [material|cosmetic]

**Affected claim**: <the specific narrative claim, task, test, or code snippet at issue>
**Evidence**: <plan location and, where applicable, codebase evidence from Grep/Read>
**Prior rejection?**: <none | rejected cycle N, what has changed: ... | rejected cycle N, nothing has changed, re-surfaced because: ...>
**Removal considered?**: <resolves finding via removal: cure below is the removal | removal considered but rejected because: ... | removal not applicable because the finding is about a missing item, not an unjustified inclusion>
**Cure**: <the proposed change>
**Cure audit against Problem Statement / User Story**: <does the cure preserve the promise?>
**Value-prop-amputating?**: <no | yes, alternative preserving cure: ... | yes, no preserving cure in scope, operator decision needed: <trade-off>>
```

## Output (OUTPUT)

### Human-Readable Report

Return a concise, easy-to-scan summary in plain language at a 16-year-old reading level:

- **Status**: `Success` | `Blocked`
- **Plan reviewed**: `<plan-filepath>`
- **Review file**: the target path computed in Step 4
- **Verification**: one short sentence on what was checked against the codebase and what could not be.
- **Recommended action**: `PASS` | `ITERATE` | `RE-SCOPE`
- **Material findings**: `<N>`
- **Cosmetic findings**: `<N>`
- **Uncategorised observations**: `<N | none>`
- **Findings raised again despite a prior rejection**: `<N | none>`. If any, list which categories and prior cycles.
- **Value-prop-amputating cures flagged**: `<N | none>`. If any, list which categories.
- **Document review**: what the document-reviewer's closing instruction says to tell the user, or that the review did not run.
- **Questions (only if blocked)**: numbered list.

Do not paste the review body into the handoff; point to the file.

## Notes

- Use this command after `/plan:plan-feature`, the command that writes the feature plan, and before implementation.
- The review file is the lasting record; the handoff only says where the file is and gives the verdict.
- A `PASS` verdict means zero material findings, not zero findings: cosmetic findings are acceptable.
- Re-review cycles overwrite the review file in place; the record carried from one cycle to the next (rejection log, decisions) lives in the plan's NOTES section, not here.
- The `document-reviewer` sub-agent must be present in `.claude/agents/`, or the wording check in Step 9 cannot run.
