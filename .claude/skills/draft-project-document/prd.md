# Draft project document: PRD

This file holds what is specific to drafting a PRD. A PRD (product requirements document) sets out what the application must do. It is written from the blueprint, the brief that starts a project. The `draft-project-document` skill, a saved set of instructions that the user starts by name, reads this file and refers to its sections by name.

## Arguments

- When the user starts the skill, they type the document type, here `prd`, and may then type file paths. Every path typed after the document type is a reference document, a file that informs the PRD. There may be any number of them, or none.

## Task

You are the principal product manager for the user's software agency. Read this document in full:

1. `.agents/blueprint.md`

Follow the instructions in Section 6 of the blueprint, its guidance for the Product Management team, to draft a PRD for the application the blueprint describes. Write it to the same folder as the blueprint, as `.agents/PRD.md`.

## Context

The blueprint was drafted by the user, who is not technical. Do not turn its phrases into bespoke mechanisms, meaning custom designs built around its exact wording. For every requirement, reach for the standard construct, the ordinary and widely used solution, that a senior software engineer or product manager would use. When a simpler, more conventional approach meets a requirement, use it.

The application will be built and operated by the user using AI coding agents.

Before drafting, read in full each reference document given as an argument.

Use the reference documents to inform design decisions and requirements for features the blueprint already puts in scope.

Never cite the blueprint in the PRD.

Where the blueprint conflicts with a reference document, record the conflict in the PRD as an open question, a point still to be decided.

## Protected structure

The protected structure is what the skill's document review may not change. Here it is any heading or structure that Section 6 of the blueprint requires.
