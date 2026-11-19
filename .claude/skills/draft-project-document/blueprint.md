# Draft project document: blueprint

This file holds what is specific to drafting a software blueprint, the brief that starts a project. Product Management and Engineering work from it. The `draft-project-document` skill, a saved set of instructions that the user starts by name, reads this file and refers to its sections by name.

A blueprint is read by Product Managers and Engineers who never see the material it was built from. It must be accurate to that material yet show no trace of it, and it must read as one author's work in one plain voice. The template, the blank blueprint that the skill copies, sets the structure. The sample blueprint, a completed blueprint that the user supplies, sets the voice.

The skill copies the template into `.agents/blueprint.md` and populates the header, the Introduction, and Sections 1-5. Sections 1-4 hold the project's context, requirements, scope and exclusions. Section 5 holds the questions, quality requirements and risks raised by the agency, the firm that writes the blueprint for its client. Sections 6-10 are guidance for Product Management and Engineering, and the skill leaves them as the template gives them.

## Arguments

- When the user starts the skill, they type the document type, here `blueprint`, and then file paths. In the order typed after the document type, the paths are the sample blueprint, then the reference document (optional).
- The sample blueprint is required. The reference document is optional. If the sample blueprint is missing or invalid, stop and ask for the path to the sample blueprint.
- Required arguments:
  - The sample blueprint = path to a completed blueprint. It is the reference for writing style, structure within answers, level of detail, tone, punctuation, and word choice. It is never a source of project facts.
- Optional arguments:
  - The reference document = path to a document holding factual context about the project (a client brief, a handoff, a research or reverse-engineering report, meeting notes). When present, it is the primary source of project facts.
- Defaults:
  - If the reference document is omitted, the current conversation (including any files the user attached or pasted) is the only source of project facts.
- Validation rules:
  - The sample blueprint must be a populated blueprint: its Sections 1-5 must contain answers rather than the template's bracketed placeholders, such as `[Your Answer Here]`. Read the sample blueprint to confirm this. If it is unpopulated, stop and ask for a completed blueprint.
  - The sample blueprint, the reference document (if given), and the template must be three distinct files. If not, stop and report.

## Task

- Read the template at `.agents/templates/template_software_blueprint.md`.
- Read the sample blueprint, and the reference document if one was given.
- Re-read the conversation from the first turn.
- Write the blueprint to `.agents/blueprint.md` under the current working directory.

## What to take from each input

- **Template**: note the header block (title, Project Name, Prepared By, Date, Version), the Introduction, the exact headings, question text, and table columns of Sections 1-5, and the exact text of Sections 6-10.
- **Sample blueprint**: build three lists.
  - _Voice profile_: punctuation habits, when the author uses bullets, numbered lists, tables, or prose, how questions in 5.3 and 5.4 are phrased, how assumptions are phrased, and how specific the answers are.
  - _Vocabulary_: the everyday words and phrases the author uses for common ideas (for example how they say "the system", "the client", "must", "out of scope").
  - _Sample project facts_: every product name, client, technology, figure, feature, and term specific to the sample's project. None of these may appear in the new blueprint unless the factual source independently supports them.
- **Reference document (if given)**: extract every fact relevant to the header and Sections 1-5, and build a _jargon list_ of technical, academic, or research terms that will need rewriting into the sample's vocabulary.
- **Conversation**: re-read it from the first turn. Extract project facts, framing decisions, and any instructions about this blueprint. If the reference document was omitted and the conversation does not hold enough facts to populate Sections 1-4 without invention, stop and ask for the missing facts or a reference document.

## Points to settle before writing

Determine each of the following from the conversation and the reference document:

- The project name.
- Who "the client" is.
- Whether the source's recommendations, findings, or proposals count as client priorities (Section 2.1) and client constraints (Section 2.2), or as agency judgement to be placed in Section 5.
- What "this delivery" includes (which phases, releases, or priority levels), so Sections 3 and 4 can be drawn.
- The Prepared By name. Default to the sample's Prepared By value.
- Any conflict between the template and the sample on structure: headings, numbering, question text, table columns, or Q/A markers where the sample departs from the template.

A point is not settled if any of the first four is not stated, or if any such conflict exists. The skill then has you ask the user before writing.

## Drafting

1. **Create the file from the template.**
   - Run `mkdir -p .agents`.
   - Run `cp .agents/templates/template_software_blueprint.md .agents/blueprint.md`.
   - Run `diff` between the template and the new file and confirm no differences. If the copy failed or differs, stop and report.
2. **Populate the header, Introduction, and Sections 1-5** of the new file with Edit. Do not touch Sections 6-10.
   - Header: keep the title as the template gives it, put the project name on the Project Name line, the Prepared By name settled under _Points to settle before writing_, today's date as `YYYY-MM-DD`, and keep the Version value unchanged. In the Introduction, replace only the project name.
   - Wherever a ❓ Q line appears, keep its question text exactly as the template gives it, removing only the square brackets. Replace each ✅ A placeholder with the answer.
   - Section 5: fill the 5.1 NFR table (non-functional requirements, the qualities the system must have, such as speed and security, rather than what it does), the 5.2 Dependency-Risk Register (dependencies drawn from Section 2.2), the 5.3 Product Management questions, the 5.4 Engineering questions, and the 5.5 assumptions list. Give every table row an Owner (`PM` for Product Management or `ENG` for Engineering) and a Status of `Open`.
   - Apply these writing rules to every line you write:
     - **Facts**: every project fact comes from the reference document or the conversation. Do not infer facts to make the blueprint look complete.
     - **No trace of the sources**: never mention, cite, or refer to the reference document, the sample, or the conversation. No section references, evidence labels, source notes, or commentary about them. Write directly as the agency.
     - **Voice and vocabulary**: match the sample's voice profile. Rewrite every term on the jargon list into the sample's plain vocabulary, reusing the sample's own words for the same ideas. Reuse the sample's everyday wording freely; only its project facts are banned.
     - **Several ideas**: where a template answer needs several ideas, use several bullets under it.
     - **Gaps**: show missing information only through the template's own tools: `TBD` (to be determined) in a table cell or target, a question in 5.3 or 5.4, or an assumption in 2.3 or 5.5. No hedging inside sentences (such as "possibly", "appears to", "it is unclear whether"), no invented markers, no caveat notes. A qualification the source itself states, such as a threshold not expected to be met or a rule that applies only in one region, is a fact and stays in the sentence.
     - **Required content the source lacks**: where the template needs content the source does not supply (for example error handling in 3.2, unusual situations the system must still handle in 3.1, success metrics in 1.3), propose agency-standard content rather than leaving the field empty, and record the proposal in the judgement log.
     - **Judgement log**: the skill has you keep a judgement log, a running record of each judgement you make while drafting. Also record in it every L/M/H rating (Low, Medium or High) you give in the 5.2 Dependency-Risk Register and every Owner assignment, with where it landed.

## Checks

Run the checks below on the finished draft and fix failures with minimal edits until every check is clean.

- _Template check_: the title is unchanged and the Project Name line holds the project name. Sections 1-5 headings present, in order, and unchanged. Question text unchanged. Table columns unchanged. No bracketed placeholders or template example text left in the header, Introduction, or Sections 1-5. Sections 6-10 identical to the template (copy Sections 6-10 of each file into a temporary file and `diff` the two files, or read both).
- _Sample check, direction one_: scan the draft for every term on the sample project facts list, matching whole words only. Remove any that the factual source does not independently support.
- _Sample check, direction two_: scan the draft for every term on the jargon list. Rewrite any that remain.
- _Voice check_: punctuation, list and table usage, and question phrasing match the voice profile.
- _Qualification check_: confirm no fact-bearing qualification was removed by the gap check.
- _Source-trace check_: no mention of the reference document, the sample, or the conversation, and no citation-like wording (such as "according to", "the report", "the handoff", "see section", "source:").
- _Gap check_: no hedging phrases inside sentences; every gap sits in a permitted place.
- If a failure cannot be fixed without inventing a fact, move the gap to a permitted place instead.

## Protected structure

The protected structure is what the skill's document review may not change. Here it is Sections 6-10 of the blueprint, which are the template's text. Ignore any finding the document review makes there, and do not report it.

## Additions to the judgement list

The skill compiles a numbered judgement list for the user from the judgement log. Add one item for each point settled under _Points to settle before writing_, including the Prepared By name, one for each L/M/H rating and one for each Owner assignment.

## Additions to the report

The skill's report to the user has fields named What you did, Check results and Could not be determined. Add to them as follows.

- Under **What you did**, add the parts populated (header, Introduction, Sections 1-5) and confirmation that Sections 6-10 are untouched.
- Under **Check results**, add one plain sentence per check under _Checks_ (template, sample direction one, sample direction two, voice, qualification, source-trace, gap), stating that it passed or what was fixed. No scores.
- Under **Could not be determined**, say where each item landed: a `TBD`, a 5.3 or 5.4 question, or a 2.3 or 5.5 assumption.

## Limits

- Make assumptions visible in the judgement list, never inside the blueprint's sentences.
- Where the template and the sample conflict, the template controls structure and the sample controls wording. If a conflict does not fall cleanly into one of those, ask.
- Do not alter Sections 6-10 of the new blueprint in any way.
- Do not do implementation work, code changes, architecture design, or product redesign; populate the blueprint only.
- Do not carry project facts from the sample into the new blueprint.

## Notes

- The template is read from the target folder: `.agents/templates`. Place a copy there before running the skill.
- Blueprint drafting stops at Section 5 by design. Sections 6-10 are the Product Management and Engineering teams' guidance and remain template text until those teams act on them.
- The optional reference document adds facts; it does not replace relevant factual context already supplied in the conversation.
