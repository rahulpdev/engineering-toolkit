# Prompt: Generate an n8n Workflow Project Briefing Template

## Intro

I am a product manager and project manager with a **non-technical background**, responsible for the **vision, coordination, and delivery** of new and updated workflows in n8n.

I work closely with an **engineering team of n8n experts**. My role is to provide high-quality, thoughtful, and reusable briefs that help engineers deliver robust, scalable, future-proofed workflows—whether building from scratch, modifying an existing one, or upgrading node versions.

## Objective

Your task is to generate a **reusable markdown template** that I can use to write project briefs for n8n workflow development.

The template must be designed to help a **non-technical PM** deliver the level of clarity and context engineers need to build, update, or refactor workflows.

## Context

This template will be used to initiate projects that:

- Create new workflows
- Modify existing workflows (e.g., adding nodes, changing logic)
- Upgrade existing workflows to use newer node versions

The purpose of the template is to assist me in producing a project brief that, in turn, is used by software engineers to create a comprehensive project implementation plan, all built on future-proofed project design and architecture.

I don't have the skills and experience to deliver thoughtful, comprehensive project briefs and implementation plans. The template must explicitly account for this.

The goal is not to capture every technical detail up front—but to ask the right questions and provide a structure that:

- Encourages deep thinking and discovery across product and engineering
- Minimizes rework and technical debt
- Supports iterative delivery and phased enhancements (MVP-first approach)
- Enables future scaling or reuse

The **engineering team is responsible** for raising technical flags and finalizing implementation. The **template must include sections that explicitly prompt me to:**

1. Provide key business context and objectives
2. Define workflow triggers, logic, and outputs at a high level
3. Clarify constraints, knowns/unknowns, and MVP scope
4. Prompt engineers to:
   - Validate UI/JSON compatibility across n8n node versions
   - Raise architectural or sequencing questions
   - Propose CI/CD and monitoring solutions
   - Consider future enhancements even in MVP design

## Workflow

1. I complete the template to produce a blueprint for a new n8n project.
2. My staff of product managers translate the blueprint into a thoughtful project brief that captures details I did not articulate in the blueprint.
3. Project brief is delivered to the engineering team.
4. Engineering team raises relevant technical topics and questions.
5. I consider and produce a response to their queries.
6. Product manager team translates my responses and updates the project brief.
7. Final project brief is delivered to the engineering team.
8. Engineering team produces a comprehensive multi-staged project implementation plan.
9. I sign off on implementation plan and engineering team proceeds to execute.

## Requirements

- The final template must be written in **markdown**
- Use **clear section headings** and a **Q&A or bullet point structure**
- Must support use cases ranging from small single-purpose automations to complex multi-part workflows
- The tone should be concise, direct, and structured for reuse across projects
- Include inline prompts for where I should raise specific questions with engineers
- Assume the workflows are **self-hosted**, stored in **Git**, and deployed via **CI/CD**

## Output Format

Your response should output only the **final markdown template**.  
Do not include explanations, commentary, or multiple versions.
