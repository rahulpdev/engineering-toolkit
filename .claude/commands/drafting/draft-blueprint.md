---
description: Copy the software blueprint template into `.agents/blueprint.md`, populate the header, Introduction, and Sections 1-5 from the conversation plus an optional reference document, write them in the voice and vocabulary of a required sample blueprint, and report every judgement call for the user to confirm before handover to Product Management.
argument-hint: <sample-blueprint-path> [reference-doc-path] (required - a completed blueprint whose voice and vocabulary the new blueprint must match; optional - a document holding the factual project context)
allowed-tools: Read, Edit, Write, Glob, Agent, AskUserQuestion, Bash(mkdir:*), Bash(cp:*), Bash(diff:*)
---

# /draft-blueprint: Draft a Software Blueprint Through Section 5

## Philosophy (Why this exists)

A blueprint is read by Product Managers and Engineers who never see the material it was built from. It must be accurate to that material yet show no trace of it, and it must read as one author's work in one plain voice. The template owns structure, the sample owns voice, and every judgement the agent makes is surfaced for the user to confirm rather than buried in the text.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/draft-blueprint ../<another-project>/.agents/blueprint.md`
- `/draft-blueprint ../<another-project>/.agents/blueprint.md .agents/reference/<project-context>.md`

**Arguments received**

- In the order typed after the command name: `$1` (sample blueprint), `$2` (reference document, optional)

**Arguments policy**

- **Mandatory**: `$1` is required. `$2` is optional. If `$1` is missing or invalid, stop and ask.

**Argument rules**

- Required arguments:
  - `$1` = path to a completed blueprint. It is the reference for writing style, structure within answers, level of detail, tone, punctuation, and word choice. It is never a source of project facts.
- Optional arguments:
  - `$2` = path to a document holding factual context about the project (a client brief, a handoff, a research or reverse-engineering report, meeting notes). When present, it is the primary source of project facts.
- Defaults (if any):
  - If `$2` is omitted, the current conversation (including any files the user attached or pasted) is the only source of project facts.
- Validation rules:
  - Each supplied path must lead, once links are followed, to an existing, readable Markdown file, given as an absolute path (written out in full from the top of the disk) or a path relative to the current working directory (the folder the command is run from).
  - `$1` must be a populated blueprint: its Sections 1-5 must contain answers rather than the template's bracketed placeholders.
  - `$1` and `$2` must be different files, and neither may be the template itself.

**If arguments are missing/invalid**

- If `$1` is missing, stop and ask for the path to the sample blueprint.
- If any supplied path fails validation, print a one-line error naming the path and the failed check, and stop. Do not create files.

## Context to Load (INPUT)

**Read these files in full**

- `.agents/templates/template_software_blueprint.md`
- `.agents/reference/writing-standard.md`. If this file is not found, stop and ask for it. Do not continue on a remembered version of the standard.

## Process (PROCESS)

Follow these steps in order:

1. **Validate the arguments** against the Argument rules.
   - If `$1` is missing, stop and ask for the sample blueprint path.
   - Confirm each supplied path leads to an existing file (use Glob, the tool that finds files by name, or Read, the tool that opens a file). If not, stop and name the failing path.
   - Read `$1` and confirm its Sections 1-5 hold answers, not placeholders such as `[Your Answer Here]`. If it is unpopulated, stop and ask for a completed blueprint.
   - Confirm `$1`, `$2` (if given), and the template are three distinct files. If not, stop and report.
   - Confirm `.agents/reference/writing-standard.md` exists. If not, stop and ask for it.
2. **Check the output target.**
   - The target is `.agents/blueprint.md` under the current working directory.
   - If that file already exists, stop and ask before overwriting. Do not continue until the user answers.
3. **Read every input in full**, start to finish. Do not search, sample, or skim.
   - **Template** (read it from the path in **Context to Load**): note the header block (title, Prepared By, Date, Version), the Introduction, the exact headings, question text, and table columns of Sections 1-5, and the exact text of Sections 6-10.
   - **Sample (`$1`)**: build three lists.
     - _Voice profile_: punctuation habits, when the author uses bullets, numbered lists, tables, or prose, how questions in 5.3 and 5.4 are phrased, how assumptions are phrased, and how specific the answers are. Note the sample's sentence length, but the writing standard in Step 6 sets the ceiling, not the sample.
     - _Vocabulary_: the everyday words and phrases the author uses for common ideas (for example how they say "the system", "the client", "must", "out of scope").
     - _Sample project facts_: every product name, client, technology, figure, feature, and term specific to the sample's project. None of these may appear in the new blueprint unless the factual source independently supports them.
   - **Reference document (`$2`, if given)**: extract every fact relevant to the header and Sections 1-5, and build a _jargon list_ of technical, academic, or research terms that will need rewriting into the sample's vocabulary.
   - **Conversation**: re-read it from the first turn. Extract project facts, framing decisions, and any instructions about this blueprint. If `$2` was omitted and the conversation does not hold enough facts to populate Sections 1-4 without invention, stop and ask for the missing facts or a reference document.
4. **Settle framing before writing** (stop and ask here if any of the points below is not settled; do not create files yet). Determine each of the following from the conversation and `$2`:
   - The project name.
   - Who "the client" is.
   - Whether the source's recommendations, findings, or proposals count as client priorities (Section 2.1) and client constraints (Section 2.2), or as agency judgement to be placed in Section 5.
   - What "this delivery" includes (which phases, releases, or priority levels), so Sections 3 and 4 can be drawn.
   - The Prepared By name. Default to the sample's Prepared By value.
   - Any conflict between the template and the sample on structure: headings, numbering, question text, table columns, or Q/A markers where the sample departs from the template.
   - If any of the first four is not stated, or any conflict exists, ask the user with AskUserQuestion and wait. Do not choose silently.
5. **Create the file from the template.**
   - Run `mkdir -p .agents`.
   - Run `cp .agents/templates/template_software_blueprint.md .agents/blueprint.md`.
   - Run `diff` between the template and the new file and confirm no differences. If the copy failed or differs, stop and report.
6. **Populate the header, Introduction, and Sections 1-5** of the new file with Edit. Do not touch Sections 6-10.
   - Header: put the project name in the title, the Prepared By name from Step 4, today's date as `YYYY-MM-DD`, and keep the Version value unchanged. In the Introduction, replace only the project name.
   - Wherever a ❓ Q line appears, keep its question text exactly as the template gives it, removing only the square brackets. Replace each ✅ A placeholder with the answer.
   - Section 5: fill the 5.1 NFR table (non-functional requirements, the qualities the system must have, such as speed and security, rather than what it does), the 5.2 Dependency-Risk Register (dependencies drawn from Section 2.2), the 5.3 Product Management questions, the 5.4 Engineering questions, and the 5.5 assumptions list. Give every table row an Owner (`PM` for Product Management or `ENG` for Engineering) and a Status of `Open`.
   - Apply these writing rules to every line you write:
     - **Facts**: every project fact comes from `$2` or the conversation. Do not infer facts to make the blueprint look complete.
     - **No trace of the sources**: never mention, cite, or refer to `$2`, the sample, or the conversation. No section references, evidence labels, source notes, or commentary about them. Write directly as the agency.
     - **Voice and vocabulary**: match the sample's voice profile. Rewrite every term on the jargon list into the sample's plain vocabulary, reusing the sample's own words for the same ideas. Reuse the sample's everyday wording freely; only its project facts are banned.
     - **Plain writing**: apply the **Standard** section of `.agents/reference/writing-standard.md`. Where a template answer needs several ideas, use several bullets under it. The sample's vocabulary and formality still apply; the standard caps length and density.
     - **Gaps**: show missing information only through the template's own tools: `TBD` (to be determined) in a table cell or target, a question in 5.3 or 5.4, or an assumption in 2.3 or 5.5. No hedging inside sentences (such as "possibly", "appears to", "it is unclear whether"), no invented markers, no caveat notes. A qualification the source itself states, such as a threshold not expected to be met or a rule that applies only in one region, is a fact and stays in the sentence.
     - **Required content the source lacks**: where the template needs content the source does not supply (for example error handling in 3.2, unusual situations the system must still handle in 3.1, success metrics in 1.3), propose agency-standard content rather than leaving the field empty, and record the proposal as a judgement in Step 9.
     - **Judgement log**: as you write, record every inference, assumption, interpretation, L/M/H rating (Low, Medium or High), Owner assignment, and proposed content, with where it landed. Step 9 depends on this log.
7. **Run the checks below** on the finished draft and fix failures with minimal edits until every check is clean.
   - _Template check_: Sections 1-5 headings present, in order, and unchanged. Question text unchanged. Table columns unchanged. No bracketed placeholders or template example text left in the header, Introduction, or Sections 1-5. Sections 6-10 identical to the template (copy Sections 6-10 of each file into a temporary file and `diff` the two files, or read both).
   - _Sample check, direction one_: scan the draft for every term on the sample project facts list, matching whole words only. Remove any that the factual source does not independently support.
   - _Sample check, direction two_: scan the draft for every term on the jargon list. Rewrite any that remain.
   - _Voice check_: punctuation, list and table usage, and question phrasing match the voice profile.
   - _Plain-writing check_: apply the **Verification** section of `.agents/reference/writing-standard.md` to Sections 1-5: the defined-term check, the mechanical prompt and the exceptions rule.
   - _Qualification check_: confirm no fact-bearing qualification was removed by the gap check.
   - _Source-trace check_: no mention of the reference document, the sample, or the conversation, and no citation-like wording (such as "according to", "the report", "the handoff", "see section", "source:").
   - _Gap check_: no hedging phrases inside sentences; every gap sits in a permitted place.
   - If a failure cannot be fixed without inventing a fact, move the gap to a permitted place instead.
8. **Run the writing review.** Call the document-reviewer sub-agent once, using the agent spawning tool with `subagent_type|agent_type: "document-reviewer"`, passing `standard=.agents/reference/writing-standard.md` and `document=.agents/blueprint.md`. Follow its handoff, except that a finding in Sections 6-10 is ignored, because that text is the template's. After the edits, repeat the checks in Step 7 once.
9. **Compile the judgement list** from the Step 6 log: a numbered list in plain English. One item per inference, assumption, interpretation, rating, Owner, framing decision from Step 4, Prepared By choice, and proposed content. Each item states what was decided, why, and where it sits in the blueprint. This list goes in the report, never in the blueprint.
10. **Report** using the Output section below, then stop and wait for the user to confirm or reject each judgement by number. When the user responds, apply the rulings with minimal edits and repeat Step 7 only before reporting again.

**Decision discipline**

- If you must make assumptions, make them visible in the judgement list, never inside the blueprint's sentences.
- If blocked by missing framing (Step 4) or missing facts (Step 3), stop and ask targeted questions. Do not proceed on guesses.
- Where the template and the sample conflict, the template controls structure and the sample controls wording. If a conflict does not fall cleanly into one of those, ask.

**Quality/Safety constraints**

- Do not modify `$1`, `$2`, or the template.
- Do not alter Sections 6-10 of the new blueprint in any way.
- Do not do implementation work, code changes, architecture design, or product redesign; populate the blueprint only.
- Do not carry project facts from the sample into the new blueprint.
- Do not include self-assessment scores or ratings of your own work in the report.

## Output (OUTPUT)

### Human-Readable Report (for humans)

Return a concise, easy-to-scan summary in plain language at a 16-year-old reading level:

- **Status**: Success | Blocked
- **File**: the full path to `.agents/blueprint.md`, or the intended path if blocked
- **What you did**: the file created (path), the parts populated (header, Introduction, Sections 1-5), and confirmation that Sections 6-10 are untouched
- **Judgement list**: the numbered list from Step 9, for the user to confirm or reject by number
- **Check results**: one plain sentence per check from Step 7 (template, sample direction one, sample direction two, voice, plain writing, qualification, source-trace, gap), stating that it passed or what was fixed. No scores.
- **Writing exceptions**: each reviewer finding refused and why, each sentence kept over the limit and why its length is needed, or a statement that there are none
- **Could not be determined**: each item the sources did not settle, and where it landed (a `TBD`, a 5.3 or 5.4 question, or a 2.3 or 5.5 assumption)
- **Questions (only if blocked)**: numbered list

## Notes (Optional)

- The template is read from the target folder: `.agents/templates`. Place a copy there before running the command.
- Commands work only in the project whose folder holds them, so copy this file into the target project's `.claude/commands/drafting/` and run it from that project's root (its top folder); the blueprint lands in that project's `.agents/` folder.
- The document-reviewer sub-agent must be present in the target project's `.claude/agents/` folder, or the writing review in Step 8 cannot run.
- This command stops at Section 5 by design. Sections 6-10 are the Product Management and Engineering teams' guidance and remain template text until those teams act on them.
- The optional project-context document adds facts; it does not replace relevant factual context already supplied in the conversation.
