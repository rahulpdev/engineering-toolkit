# Draft project document: TAD

This file holds what is specific to drafting a TAD. A TAD (technical architecture document) sets out how the application will be built. It is written from the PRD (product requirements document), which sets out what the application must do. The PRD is in turn written from the blueprint, the brief that starts a project. The `draft-project-document` skill, a saved set of instructions that the user starts by name, reads this file and refers to its sections by name.

## Arguments

- When the user starts the skill, they type the document type, here `tad`, and may then type file paths. Every path typed after the document type is a reference document, a file that informs the TAD. There may be any number of them, or none.

## Task

You are the principal software engineer for the user's software agency. Read these documents in full:

1. `docs/blueprint.md`
2. `docs/PRD.md`

Follow the instructions in Section 7 of the blueprint, its guidance for the Engineering team, to draft a TAD for the application the blueprint describes. Write it to the same folder as the blueprint, as `docs/TAD.md`.

## Context

The blueprint was drafted by the user, who is not technical. Do not turn its phrases into bespoke mechanisms, meaning custom designs built around its exact wording. For every requirement, reach for the standard construct, the ordinary and widely used solution, that a senior software engineer or product manager would use. When a simpler, more conventional approach meets a requirement, use it.

The application will be built and operated by the user using AI coding agents.

Before drafting, read in full each reference document given as an argument.

Use the reference documents to inform design decisions and requirements for features the PRD already puts in scope.

The PRD is what you are designing for. The blueprint is background. Use it to understand context, never cite it in the TAD, and where it disagrees with the PRD, the PRD wins.

Where the PRD is silent and the blueprint conflicts with a reference document, record the conflict in the TAD as an open question, a point still to be decided.

## Protected structure

The protected structure is what the skill's document review may not change. Here it is any heading or structure that Section 7 of the blueprint requires.
