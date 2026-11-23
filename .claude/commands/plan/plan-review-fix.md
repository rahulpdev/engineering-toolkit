---
description: Apply an adversarial plan review to the underlying plan, judging each finding against author context, honouring the plan's rejection log, updating the plan in place, and adding an entry to the plan's NOTES section, marked with the current round of review, for every declined finding.
argument-hint: <plan-review-filepath> (required - path to the review file)
allowed-tools: Read, Edit, Grep, Glob, Bash(test:*)
---

# /plan-review-fix: Apply Plan Review With Author Judgment

## Philosophy (Why this exists)

The reviewer surfaces possible gaps; the author decides what is actually a gap, what cure (the review's word for the fix to a gap) preserves the plan's goal, and what goes on the page. This command exists to preserve that asymmetry through the fix loop (the repeated rounds in which a review finds gaps and a fix pass answers them), accepting the reviewer's search power without delegating the author's judgment. A fix pass succeeds when the next review would find only findings this pass could not have anticipated. The plan's NOTES rejection log, the list in the plan's NOTES section of every finding a fix pass declined, is the record kept from one cycle (one round of review and fix) to the next. It lets successive fix passes recognise a finding raised again and stop degrading the plan by cutting out what it promised. `Zero findings` is a signal that something is being suppressed, not a target; a plan that delivers its value proposition (what the plan promises, shortened to value-prop) with an accepted, documented limitation can beat a plan that closes a gap by cutting the feature out. A cure that cuts out something the plan promises is what the review calls value-prop-amputating.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/plan-review-fix docs/reviews/add-user-authentication-plan-review.md`
- `/plan-review-fix docs/reviews/detect-pdf-table-plan-plan-review.md`

**Arguments received**

- Argument (the text typed after the command's name, which is put here when the command runs): `$ARGUMENTS`

**Arguments policy**

- **Mandatory**: `$ARGUMENTS` is required.

**Argument rules**

- Required arguments: `$ARGUMENTS` = path to the plan review file produced by `/plan:plan-review`.
- Optional arguments: None.
- Validation rules:
  - `$ARGUMENTS` must be a path to an existing readable file.
  - `$ARGUMENTS` must end in `.md`.

**If arguments are missing/invalid**

- If `$ARGUMENTS` is absent, stop and ask for the review file path.
- If `$ARGUMENTS` does not exist or is unreadable, stop and ask for a valid path.

## Process (PROCESS)

Follow these steps in order:

1. **Validate the review file.**
   - Capture the artifacts directory (the folder Archon, the tool that can run this command as one step of a workflow, gives that run for its files; `$ARTIFACTS_DIR` is empty when a person runs the command by hand) into a shell variable, a named value the shell keeps: `DIR="$ARTIFACTS_DIR"`.
   - If `$DIR` is non-empty, confirm the review exists with `test -f "$DIR/plan-review.md"` (Archon workflow context); the review source is `$DIR/plan-review.md`.
   - Otherwise, confirm the review exists with `test -f "$ARGUMENTS"` (a person ran the command by hand); the review source is `$ARGUMENTS`.
   - If the check fails, stop: when run by hand, ask for a valid path; under Archon, report the missing review input and halt.

2. **Read the review in full.**
   - Read the review source from top to bottom.
   - Extract the Recommended Action from the Findings Summary: one of `PASS` (the plan needs no further round of fixes), `ITERATE` (it needs another round of fixes) or `RE-SCOPE` (what the plan covers must be redrawn before another round).
   - Extract per-category findings and per-finding fields (Affected claim, Evidence, Prior rejection?, Removal considered?, Cure, Cure audit, Value-prop-amputating?), plus any uncategorised observations.
   - If `$DIR` is empty, extract the `**Plan reviewed**` header to identify the plan filepath; if the header is missing, stop and ask the User for it. Under Archon the plan filepath is fixed at `$DIR/plan.md`, so this extraction is skipped.

3. **Read the plan in full.**
   - If `$DIR` is non-empty, read the plan from `$DIR/plan.md`; otherwise read the plan filepath extracted in Step 2.
   - Capture the NOTES section, including any prior-cycle rejection log entries.

4. **Check the Recommended Action before going on.**
   - If **PASS**: the fix loop is not the normal path after a PASS verdict. Stop and confirm with the User before proceeding. If the User declines, report the status `Gated on PASS` (stopped because the review passed the plan) and stop.
   - If **RE-SCOPE**: stop. Surface the review's structural findings to the User with your assessment of what re-scope would entail (redefined Problem Statement, split into companion plans, part of the work put off to a later version). Do not apply fixes to a plan that needs restructuring.
   - If **ITERATE**: proceed.

5. **Determine cycle count and check for convergence failure (the same kinds of finding returning cycle after cycle).**
   - If the plan's NOTES rejection log has entries, the cycle count is one more than the highest cycle number recorded there (`cycle count = max(cycle number recorded) + 1`).
   - If the log is empty, `cycle count = 1` unless the User states otherwise.
   - If cycle count ≥ 3 and material findings persist across the same categories that raised findings on prior cycles, surface the pattern to the User before applying fixes: which categories keep coming back, which cures keep causing new findings elsewhere. Convergence is not guaranteed by iteration alone. Wait for explicit instruction from the User before continuing.

6. **Process each finding against author context.**
   - For every finding in the review, apply these in order:
     - **Check the rejection log first.** If the plan's NOTES rejection log records this class as rejected on a prior cycle, do not reject again by default. Re-read the prior rejection's cited evidence and name what has changed: new evidence, new context, or nothing. `Nothing changed and I'm rejecting again` is a signal to surface the pattern to the User, not to reject silently.
     - **Audit the observation** against your context, separately from the proposed cure. A correct observation can come paired with a wrong cure. Reject findings your context shows are not actually gaps, and cite specific evidence (Problem Statement clause, existing code that already handles it, prior decision, instruction from the User). Accept the rest.
     - **Audit the proposed cure** against the Problem Statement. If it removes a promised capability, the cure is wrong even when the observation is right. Either propose an alternative that preserves the goal (enforcing it in a different layer, one of the levels the code is arranged in; a companion plan; a follow-up limited to that gap) OR surface the conflict to the User with the trade-off laid out. Do not unilaterally pick a value-prop-amputating cure.
     - **Honour the removal-first discipline.** Every finding carries a `Removal considered?` field. If the review marks removal as the cure, apply it. If the review proposed an additive cure with removal rejected, verify the rejection reason against your context: if removal resolves the finding without cost to the Problem Statement, override to removal. If removal was marked not applicable, verify the finding is genuinely about a missing item and not a misapplied classification. The loop's default bias runs additive; the reviewer having considered removal does not relieve the author of the same consideration.
     - **Do not accept `out of scope` framing without evaluating it.** State what the adjacent work would take, whether it is tractable, whether it warrants its own plan. Declining is a decision; record it as one.
     - **Optimise for `preserved the goal AND closed the gap`.** Clearing the reviewer's list is not the objective.

7. **Apply accepted fixes to the plan in place.**
   - Use the `Edit` tool (Claude's tool for changing the text inside a file) on the plan file to make each change.
   - Track each applied change as either a **material fix, additive** (substantive plan change that adds a task, test, rule, guard, capability, or handling for an unusual case), a **material fix, removal** (substantive plan change that removes an input, rule, piece of supporting structure, or other unjustified element the finding attached to), or a **cosmetic fix** (narrative or precision cleanup: stale references, count mismatches, formatting).

8. **Check the plan against the original Feature Description and Problem Statement (the anchor-check).**
   - Re-read the Feature Description and Problem Statement as they stood at the start of the plan (before any fix cycle touched them), not as they read after this cycle's edits.
   - Confirm the current plan still promises every capability those original statements promised.
   - Per-finding checks catch a single fix cutting out a promise; this catches cumulative drift across cycles.
   - If a cumulative drift has removed a promise, surface the drop to the User before finalising and either restore the promise or record the removal as a value-prop-amputating conflict awaiting decision.

9. **Update the plan's own bookkeeping.**
   - Re-check Feature Metadata (complexity, systems affected).
   - Re-check the RUNTIME ENVIRONMENT section, the part of the plan that lists what the feature needs from the machine it runs on. Every fix that added or removed a subprocess call (the code starting a separate program), a web address the code calls, a file or folder outside the repository, an environment variable (a named setting the machine passes to the program), a credential, or a background service must be reflected there, with the line that installs or sets it up given a fixed version, or removed, to match.
   - Re-check the Confidence Score.
   - Re-check the Quality Criteria checklists (Context Completeness, Implementation Ready, Pattern Consistency, Information Density).
   - Update every item that material fixes have changed. Stale bookkeeping after a fix pass erodes trust in later reviews.

10. **Append rejection log entries to the plan's NOTES section.**
    - If the plan has no NOTES section, add one at the end of the plan before appending.
    - For every finding you declined or every cure you refused, append one structured entry:
      - `Cycle`: `<N>`
      - `Category`: `<finding category>`
      - `Finding class`: one-line description
      - `Evidence cited`: what supported the rejection
      - `Decision`: rejected / cure refused / deferred / out-of-scope
    - Append only; do not rewrite or delete prior entries. Future fix cycles read this log to detect a finding raised again.

11. **Prepare the report for the User.**
    - Use the Human-Readable Report format below.
    - Distinguish applied vs considered-and-rejected; within applied, distinguish material vs cosmetic.
    - Do not silently drop findings.

**Decision discipline**

- Neither side of the loop is generically deficient: the reviewer sees ways the plan can fail that you may have blind spots on; you carry constraints they cannot see. The asymmetry is what makes the loop useful. Use the reviewer to expand your search, not to replace your judgment.
- If a cure is value-prop-amputating, stop and ask the User with the trade-off laid out; do not decide.
- If assumptions are unavoidable, list them explicitly and keep them minimal.

**Quality/Safety constraints**

- Do not modify files other than the plan referenced by the review.
- Do not rewrite, reorder, or delete prior NOTES rejection log entries; append only.
- Do not accept a value-prop-amputating cure without the User's confirmation.
- Do not report a fix as applied if the corresponding edit was not written to the plan.

## Output (OUTPUT)

### Human-Readable Report

Return a concise, easy-to-scan summary in plain language at a 16-year-old reading level:

- **Status**: `Success` | `Blocked` | `Gated on PASS` | `Gated on RE-SCOPE` | `Gated on convergence failure`
- **Review file**: `<path>`
- **Plan file updated**: `<path>` (or `<path>: not modified` if the command stopped at one of its checks)
- **Recommended Action from review**: `PASS` | `ITERATE` | `RE-SCOPE`
- **Cycle number**: `<N>`
- **Convergence signal**: `none` | `cycle N+ with persistent categories: <list>`
- **Applied material fixes (additive)**: bulleted list, each filed under the finding's category and index; one short line per fix.
- **Applied material fixes (removal)**: bulleted list, each filed under category and index; one short line naming what was removed.
- **Applied cosmetic fixes**: bulleted list, each filed under category and index.
- **Considered and rejected**: bulleted list; for each, category, index, one-line finding class, evidence cited, decision.
- **Value-prop-amputating conflicts surfaced**: bulleted list of trade-offs awaiting the User's decision, or `none`.
- **Anchor-check**: `Preserved` | `Drift detected: <list of dropped promises>`
- **Bookkeeping updated**: bullets for any of Feature Metadata / Confidence Score / Quality Criteria checklists that changed, or `no changes needed`.
- **Questions (only if the command stopped at one of its checks or was blocked)**: numbered list.

## Notes

- Run after `/plan:plan-review`. The next `/plan:plan-review` will read the appended rejection log entries and honour them.
- The plan is the file that lasts from one cycle to the next; the review file is regenerated each cycle. All memory the loop needs lives in the plan's NOTES section.
- `Gated on PASS` is normal: a PASS verdict means the fix loop is skipped unless the User explicitly wants to iterate on cosmetic drift.
