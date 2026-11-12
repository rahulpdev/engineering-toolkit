Run comprehensive validation of the project to ensure every check the project defines is passing.

Execute the checks in the **Checks** section in sequence and report results:

- Run each command exactly as written and compare its output with the **Expected** result beneath it.
- A check passes only when every test passes with none skipped and every tool reports zero errors and zero warnings, whatever its expected result says.
- Stop anything a check starts, such as a server or a container, before the next check begins, whether or not the check passed.
- If the Checks section holds no checks, run every validation command the project defines instead: its tests, type checks, linting, formatting, build and any other check, as its `package.json` scripts, `pyproject.toml` tool configuration or Makefile define them.

## Checks

Each check is a numbered `###` heading holding its commands in fenced `bash` blocks, each block followed by its **Expected:** result. The project writes its own checks here.

## Summary Report

After all validations complete, provide a summary report with:

- The status of each check, with tests passed/failed where the check runs tests
- The commands run and where they came from, when the Checks section held none
- Any errors or warnings encountered
- Overall health assessment (PASS/FAIL)

**Format the report clearly with sections and status indicators (✅/❌)**
