---
name: draft-project-document
description: Draft one of three project documents in the project's `docs/` folder, a software blueprint, a PRD (product requirements document) or a TAD (technical architecture document), then check the draft, have the document-reviewer sub-agent read it, and report every judgement call for the user to confirm.
argument-hint: "<blueprint|prd|tad> [paths] (required - the document to draft, in any letter case; then, for a blueprint - a required sample blueprint and an optional reference document; for a PRD or a TAD - any number of reference documents, or none)"
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Glob, Agent, AskUserQuestion, Bash(mkdir:*), Bash(cp:*), Bash(diff:*)
---

# /draft-project-document: Draft a Blueprint, a PRD or a TAD

## Philosophy (Why this exists)

This skill drafts three project documents: the blueprint (the brief that starts a project), the PRD (the product requirements document, written from the blueprint) and the TAD (the technical architecture document, written from the PRD). Each is read by people and AI agents who never see the material it was built from, so all three are drafted the same way: read every input in full, write only what the inputs support, review the draft, and surface every judgement for the user to confirm rather than bury it in the text. What is true for one document only is kept in that document's own file.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/draft-project-document blueprint ../<another-project>/docs/blueprint.md`
- `/draft-project-document blueprint ../<another-project>/docs/blueprint.md .agents/reference/<project-context>.md`
- `/draft-project-document PRD`
- `/draft-project-document prd .agents/reference/<platform-guide>.md`
- `/draft-project-document Tad .agents/reference/<platform-guide>.md .agents/reference/<architecture-guide>.md`

**Arguments received**

- All args as a single string: `$ARGUMENTS`

**Arguments policy**

- **Mandatory**: `$ARGUMENTS` must begin with the document type. If it is missing or invalid, stop and ask.

**Argument contract**

- Required args: the document type, first. It is `blueprint`, `prd` or `tad`, typed in any letter case, so `PRD`, `prd` and `Prd` are the same.
- Optional args: any paths after the document type, separated by spaces. What each path is, and whether the document requires it, depends on the document. The variant file, the file in this skill's folder that holds what is specific to one document, says so under its _Arguments_ section.
- Defaults (if any): the variant file states them.
- Validation rules:
  - The first word, compared without regard to letter case, must be one of the three document types.
  - A path that contains a space must be wrapped in double quotes.
  - Each path must lead to an existing, readable Markdown file, given as an absolute path (written out in full from the top of the disk) or a path relative to the current working directory (the folder the skill is run from). Where a path is a symbolic link, a file that points to another file, the file it points to must meet this rule.
  - The variant file adds the rules for its own paths.

**If arguments are missing/invalid**

- If the document type is missing, or is not one of the three, stop and ask which document to draft, and list the three.
- If any path fails validation, print a one-line error naming the path and the failed check, and stop. Do not create files.

## Context to Load (INPUT)

**Read these files in full**

- The variant file for the document type, from this skill's folder: [blueprint.md](blueprint.md), [prd.md](prd.md) or [tad.md](tad.md).
- `.agents/reference/communication-standard.md`, the project's rules for messages and documents. If this file is not found, stop and ask for it.

## Process (PROCESS)

Follow these steps in order:

1. **Read the document type.** The first word of `$ARGUMENTS` is the document type, in any letter case. If it is missing or is not `blueprint`, `prd` or `tad`, stop and ask which document to draft. Any words after it are the paths, in the order typed.
2. **Read the variant file.**
   - For a blueprint it is [blueprint.md](blueprint.md), for a PRD [prd.md](prd.md), and for a TAD [tad.md](tad.md). Read it in full from this skill's folder.
   - The steps below refer to sections of the variant file by name. Where the variant file has no section of that name, the step adds nothing for this document.
3. **Check the inputs.**
   - Check the paths against the Validation rules above and against _Arguments_ in the variant file. If a path fails, print a one-line error naming the path and the failed check, and stop. Do not create files.
   - Confirm that every document that _Task_ in the variant file tells you to read exists (use Glob, the tool that finds files by name, or Read, the tool that opens a file). If one does not, stop and name the missing file.
4. **Check the output target.**
   - _Task_ in the variant file names the file to write.
   - If that file already exists, stop and ask before overwriting. Do not continue until the user answers.
5. **Read every input in full**, start to finish. Do not search, sample, or skim.
   - The inputs are the documents that _Task_ in the variant file tells you to read, the documents at the paths, and the communication standard.
   - Follow _What to take from each input_ in the variant file.
6. **Settle what must be settled before writing.**
   - Follow _Points to settle before writing_ in the variant file.
   - If any point it lists is not settled, ask the user with AskUserQuestion, the tool that puts a question to the user, and wait. Do not choose silently, and do not create files yet.
7. **Draft the document.**
   - Follow _Task_, _Context_ and _Drafting_ in the variant file.
   - As you write, keep a judgement log, a running record of each judgement you make. Record each of these, with where it landed in the document:
     - every inference, assumption and interpretation
     - every piece of content you proposed that the inputs do not supply
     - every place where you used a standard construct in place of a mechanism that the wording of an input implies
     - anything else the variant file says to log
   - Step 10 depends on this log.
8. **Run the accuracy review.**
   - Check material claims in the document against the available evidence. The evidence is the inputs you read in Step 5. Correct any claim the evidence does not support.
   - Then run the checks under _Checks_ in the variant file.
9. **Run the document review.**
   - Start the `document-reviewer` sub-agent once. It is a separate agent that reads the document without having seen the conversation. Pass it two paths and nothing else: the communication standard at `.agents/reference/communication-standard.md` and the document.
   - Follow the instruction that closes its response. Fix wording only: do not let a finding change a requirement, a priority or a scope decision.
   - Ignore any finding against what the variant file names under _Protected structure_.
   - After the edits, run the checks under _Checks_ in the variant file once more.
10. **Compile the judgement list** from the Step 7 log: a numbered list in plain English, with one item for each logged judgement, plus one item for each entry that _Additions to the judgement list_ in the variant file asks for. Each item states what was decided, why, and where it sits in the document. This list goes in the report, never in the document.
11. **Report** using the Output section below, then stop and wait for the user to confirm or reject each judgement by number. When the user responds, apply their answers with minimal edits. Then run only the checks under _Checks_ in the variant file again, not the document review, and report again with the judgement list updated.

**Decision discipline**

- If you must make assumptions, make them visible in the judgement list.
- If blocked by a missing input, or by a point in Step 6 that is not settled, stop and ask targeted questions. Do not proceed on guesses.
- Where the variant file is more specific than this file, follow the variant file.

**Quality/Safety constraints**

- Do not modify any input document.
- Do not report the document as finished until the accuracy review in Step 8 and the document review in Step 9 are both complete.
- Follow _Limits_ in the variant file.
- Do not include self-assessment scores or ratings of your own work in the report.

## Output (OUTPUT)

### Human-Readable Report (for humans)

Return a concise, easy-to-scan summary:

- **Status**: Success | Blocked
- **File**: the full path to the document, or the intended path if blocked
- **What you did**: the document drafted (path) and the inputs read, plus what _Additions to the report_ in the variant file adds
- **Judgement list**: the numbered list from Step 10, for the user to confirm or reject by number
- **Check results**: one plain sentence on the accuracy review, stating that it passed or what was corrected, then what _Additions to the report_ in the variant file adds
- **Document review**: what the document-reviewer's closing instruction says to tell the user
- **Could not be determined**: each item the inputs did not settle and that you left open, and where it landed in the document
- **Questions (only if blocked)**: numbered list

## Notes (Optional)

- The documents are drafted in order. A PRD needs the blueprint at `docs/blueprint.md`, and a TAD needs both the blueprint and the PRD at `docs/PRD.md`.
- This skill runs only when the user invokes it by name. Claude does not start it on its own.
- A skill works only in the project whose folder holds it, so copy this skill's folder into the target project's `.claude/skills/` and run it from that project's root (its top folder); the document lands in that project's `docs/` folder.
- The document-reviewer sub-agent must be present in the target project's `.claude/agents/` folder, or the document review in Step 9 cannot run.
