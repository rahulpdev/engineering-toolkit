---
description: Compare the document you authored in this conversation against another LLM's version, rate both overall and section-by-section, and propose numbered surgical edits to consolidate the best content into your document.
argument-hint: <other-llm-file> (required - relative path to the document created by the other LLM)
allowed-tools: Read, Edit
---

# /compare-docs: Cross-LLM Document Comparison & Consolidation

## Philosophy

When two LLMs draft the same document from the same instructions, the delta between their outputs reveals blind spots that neither would surface alone. The goal is not to declare a winner — it is to harvest the strongest material from both versions and forge a single document that neither LLM could have produced independently. All editing converges on the document you authored; the other file is a read-only reference that gets deleted once consolidation is complete.

## Invocation & Arguments (INPUT)

**Usage examples**

- `/compare-docs @path/to/other-llm-output.md`
- `/compare-docs @../codex-workspace/design-doc.md`

**Arguments received**

- All args as a single string: `$ARGUMENTS`

**Arguments policy**

- **Mandatory**: The relative path to the other LLM's document is required. If missing or invalid, stop and ask.

**Argument contract**

- Required args: `$ARGUMENTS` = relative path to the document produced by the other LLM
- Optional args: None
- Defaults: None
- Validation rules: The path must resolve to an existing, readable file. If it does not, stop and report the error — do not guess an alternative path.

**If arguments are missing/invalid**

- Stop and ask: "Please provide the relative path to the other LLM's document."

## Process

Follow these steps in order:

### 1. Identify the Two Documents

- **Ours**: The document you authored earlier in this conversation. You already have context on its content, structure, and the instructions that produced it. Identify its file path from the conversation history.
- **Theirs**: The file at `$ARGUMENTS`. Read it in full.

If you cannot determine which file you authored or what instructions guided its creation, stop and ask before proceeding.

### 2. Read Both Documents in Full

Read both files end-to-end. Do not skim. Build a complete mental model of each document's:

- Overall structure (headings, sections, ordering)
- Key arguments, claims, and content per section
- Voice, tone, and style
- Depth and specificity of coverage

### 3. Reconstruct the Evaluation Baseline

From your conversation context, identify the original instructions or specification that guided the document's creation. These instructions are the measuring stick for all ratings. If the instructions are ambiguous or incomplete, note this explicitly — it affects how confidently you can rate.

### 4. Map Sections Across Both Documents

Build a unified section list that covers both documents. If either document has no clear headings, create section labels based on their natural content blocks and use those labels consistently in the report. Where one document has a section the other lacks, note the gap.

### 5. Rate Overall Quality

Assign an overall quality rating (whole integer, 1–10) to each document based on how well its content fulfills the original instructions. Record both ratings.

**Rating criteria** (apply consistently to both documents):

- **Completeness**: Does the document address all requirements in the instructions?
- **Accuracy**: Is the content correct and well-reasoned?
- **Clarity**: Is the writing clear, well-organized, and easy to follow?
- **Depth**: Does the document go beyond surface-level treatment where the instructions demand it?
- **Cohesion**: Does the document flow logically as a unified piece?

### 6. Rate Each Section

For every section in the unified section list, assign a quality rating (whole integer, 1–10) to each document's version of that section. If a document lacks a corresponding section entirely, rate it 0 for that section.

### 7. Build the Summary Table

Present all ratings in a single table with the following structure:

| Section        | Ours | Theirs | Delta | Action         |
| -------------- | ---- | ------ | ----- | -------------- |
| _Overall_      | N    | N      | ±N    | —              |
| Section Name 1 | N    | N      | ±N    | Diff / RCA / — |
| Section Name 2 | N    | N      | ±N    | Diff / RCA / — |
| ...            | ...  | ...    | ...   | ...            |

**Action column logic**:

- **Diff**: Theirs > Ours and at least one is >= 9 for this section. Surgical edits will be proposed in Step 8.
- **RCA**: Both Ours and Theirs are rated below 9 for this section. Root cause analysis will be provided in Step 9.
- **—**: Ours >= Theirs and at least one is >= 9. No action needed.

### 8. Propose Surgical Edits (Diff Sections)

For every section marked **Diff** in the summary table, propose the specific edits required to bring our document's section up to the quality of theirs. Present each edit as a numbered diff block.

**Edit format**:

```
Edit #N — [Section Name]
Rationale: [1-2 sentences explaining what the other LLM did better and why this edit closes the gap]

--- CURRENT (ours) ---
[exact text to be replaced, with enough surrounding context to locate it unambiguously]

--- PROPOSED ---
[replacement text]
```

**Edit constraints** (non-negotiable):

- Preserve the voice, rhythm, style, tone, verbosity, and grammar of the existing document.
- Preserve the structure, layout, and flow of the existing document.
- Do not bolt on phrases to the end of existing sentences. If new content is needed, weave it into the existing prose naturally or place it where it reads as if it was always there.
- Each edit must be the minimum change that closes the quality gap for that specific point. Do not bundle unrelated improvements into a single edit.
- Number edits sequentially across all sections (Edit #1, Edit #2, ... Edit #N) so the user can reference any edit by number.

After presenting all edits, pause and wait for the user to approve or reject each one by number before applying any changes.

### 9. Root Cause Analysis (RCA Sections)

For every section marked **RCA** in the summary table (both documents rated below 9), provide a diagnosis instead of edits.

**RCA format per section**:

**[Section Name]** — Ours: N/10, Theirs: N/10

- **What went wrong**: Identify the root cause of the low quality. Was it a misunderstanding of the instructions? Insufficient depth? Wrong framing? Missing context? Be specific.
- **What the instructions required**: Restate the relevant part of the original instructions that this section was supposed to address.
- **Gap analysis**: What is conceptually missing or misaligned that prevents either document from reaching a 9 or 10?
- **Path to 9+**: Describe, at a conceptual level, what would need to change in approach, framing, or content to achieve a 9 or 10. Do not provide specific text edits — the purpose is to align on the direction before drafting new content.

Do not propose edits for RCA sections. These require a separate conversation to resolve the underlying issues before editing makes sense.

### 10. Prepare the output report

Include the summary table, diffs, and RCAs and present a fully complete output report using the **Human-Readable Report** format below. Wait for the user to:

- Approve or reject individual edits by number
- Discuss RCA findings and decide on next steps
- Request additional edits or analysis

**Quality/Safety constraints**

- Do not modify any file until the user explicitly approves specific edits.
- Do not modify the other LLM's document at `$ARGUMENTS` — it is read-only for comparison.
- Do not add content that was not present in either document unless the user requests it.
- Do not reformat, restyle, or reorganize sections that are not flagged for editing.
- If you are uncertain whether a quality gap is real or a matter of stylistic preference, flag it as an observation rather than proposing an edit.

## Output

### Human-Readable Report

Return a concise, easy-to-scan summary in plain language at a 16-year-old reading level:

- **Documents compared**:
  - Ours: `[file path]`
  - Theirs: `[file path]`
- **Instructions baseline**: 1–3 sentence summary of the original instructions used to generate both documents
- **Summary table**: The ratings table from Step 7
- **Surgical edits** (if any): Numbered edit blocks from Step 8
- **Root cause analyses** (if any): RCA blocks from Step 9
- **Awaiting your input**: Prompt the user to approve/reject edits by number and discuss any RCA findings

## Notes

- This command assumes you authored one of the two documents in the current conversation. If invoked in a fresh conversation with no prior document authorship, it cannot determine which file is "ours" — stop and ask.
- The command is designed for iterative use. After approved edits are applied, the user may re-invoke it to verify the gap has closed.
- Once all edits are applied and the user is satisfied, the other LLM's file can be deleted. This command does not delete it automatically — confirm with the user first.
