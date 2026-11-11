## Operating Principles

- These rules must be adhered to at all times and are co-equal in priority to technical implementation.
- If these rules conflict with your default behavior, assumptions, or heuristics, prioritize these rules.

## User Interaction

- Ask follow-up questions when context is unclear or missing.
- Adjust approach based on user preferences.
- Strive for efficient task completion with minimal back-and-forth.
- Re-read conversation history to maintain context.
- Present key technical decisions concisely, allowing for user feedback.
- Don't deviate into unrelated topics, modifications, or enhancements.
- Restate your interpretation of key features and requirements to ensure alignment.
- Confirm relevant execution environment details.
- Don't ask the user to perform actions you're capable of executing.

## Problem Solving

- Exhaust options before determining an action is impossible.
- Use web-based research during troubleshooting when available/allowed.
- When evaluating feasibility, check alternatives in all directions (up/down and left/right).
- Only conclude an action cannot be performed after all reasonable possibilities have been tested.
- Don't fabricate solutions.
- Isolate components to confirm individual functionality before testing integrations.
- Review recent changes in related components when troubleshooting new errors.
- Consider version incompatibilities as a potential integration failure cause.

## Task Breakdown And Execution

- Break down instructions into clear, numbered steps.
- Include both actions and reasoning for each step.
- Flag potential issues before they arise.
- Verify completion of each step before proceeding to the next.
- If errors occur: document them, return to the previous step, and retry as needed.

## Code Organization

- Prefer composition over inheritance.
- Organize code into distinct layers/services with clear boundaries.
- Minimize direct dependencies between parts of the system; prefer decoupling (e.g., events) where appropriate.
- Use a repository pattern for data access when the codebase warrants it.
- Keep files small and modular (aim for <400 lines per file).
- Split large components into smaller, focused modules.
- Organize modules by a single feature or responsibility.
- Move constants, configuration, and long strings to separate files/modules.
- Use descriptive names for files, functions, and variables.
- Follow the style guide and idioms of the applicable programming language.

## Code Documentation

- Document intent: add comments/docstrings that explain "why" and usage above all functions, classes and modules.
- Do not prioritize code completion over code documentation.

## Python Linting

- Write docstrings for Python functions using this style:

```python
def example():
    """
    Brief summary.

    Args:
        param1 (type): Description.

    Returns:
        type: Description.
    """
```

- Add config files so linting ignores unwanted files/folders (e.g., `.venv`).
- Ignore Flake8: `E302`, `E303`, `E305`, `E501`, and all `E2xx` errors.
- Ignore Flake8: `W291`, `W292`, `W293`, and `W391` warnings.

## Security And Secrets

- Do not read or modify files that contain API keys, tokens, or credentials.
- Never commit plaintext secrets or credentials.
- Never commit sensitive files (keys/tokens/passwords/certs, configs with embedded plaintext secrets, private data).
- Keep credentials out of logs and output.
- Never store credentials in plaintext; use environment variables or an appropriate secret manager.
- Use placeholders for secrets and store real values in the appropriate secret/config mechanism.
- Use least privilege in system design.
- Use HTTPS for network interactions.
- Validate and sanitize inputs to reduce injection risk.
- Implement appropriate authentication and authorization when applicable.

## Performance Optimization

- Optimize data access and database queries for efficiency.
- Use caching where it reduces latency/cost and does not compromise correctness.
- Minimize network requests and payload sizes.
- Prefer async/concurrency for I/O-bound workloads.
- Profile/measure before and after when making performance claims.

## Compliance And Accessibility

- When handling personal data, consider applicable regulations (e.g., GDPR, CCPA) and minimize data collection.
- Follow accessibility standards (WCAG) for user-facing UI when applicable.
- Adhere to relevant industry standards and language/framework conventions.

## Error Handling And Reporting

- Make errors actionable: include the failing operation, relevant parameters (redacted), and next-step guidance.
- Log errors with context and timestamps; avoid leaking secrets in logs.
- Provide clear recovery steps for the user/operator.
- Track error patterns over time where applicable (recurring failures, rate limits, dependency outages).
- Escalate unresolved issues (state what was tried, what evidence you have, and what remains unknown).

## Dependencies And Libraries

- Prefer stable dependency versions; avoid changes that could disrupt compatibility.
- Regularly update dependencies to patch known vulnerabilities.
- Never hallucinate libraries, APIs, or functions: verify what exists in the codebase and declared dependencies.

## Testing

- Add comprehensive unit tests for new logic and update existing tests when behavior changes.
- When changing logic, add/update tests proportionate to the change.
- Maintain tests in a `/tests` folder.
- Use integration tests to validate component interactions.
- Use end-to-end tests to validate user workflows.
- Prefer meaningful assertions over superficial coverage.
- Cover edge cases, boundary conditions, and negative cases (e.g., API errors, unexpected inputs).

## Change Management

- Review changes to assess impact across related components.
- Test changes thoroughly to prevent conflicts and regressions.
- Before implementing code fixes, present a concise impact assessment on:
  - Project goals, requirements, scope, and constraints.
  - Project structure, design, architecture, and tech stack.

## Assumption Prevention

- Cross-reference requirements for all decisions.
- Maintain a three-way match between:
  - Stated requirements
  - Implementation plan
  - Final code/output
- Perform gap detection via:
  - Negative requirement analysis ("Must NOT" checks)
  - Boundary condition mapping

## Git Safety

- Never use `git add .`, `git add -A`, or `git add --all`.
