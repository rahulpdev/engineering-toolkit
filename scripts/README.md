# Scripts — Reference

## Badges

![Docs](https://img.shields.io/badge/docs-reference-informational)
![Format](https://img.shields.io/badge/format-python-blue)
![Focus](https://img.shields.io/badge/focus-tooling-5b3cc4)

## Overview

This folder holds the script that keeps the Codex sub-agents in `.codex/agents/` in step with the Claude sub-agents in `.claude/agents/`, and its tests. The converter reads a Claude sub-agent (a Markdown file with YAML frontmatter), copies the name and description, turns the body into `developer_instructions`, translates the model tier and effort through two mapping tables at the top of the script, drops the fields Codex has no equivalent for (tools and colour), and writes a TOML file. It needs Python 3.9 or later and PyYAML, declared in the script's PEP 723 header so `uv run` can install it on the fly. The tests use the standard library runner, so nothing else needs installing.

## Key Features

- One command regenerates a Codex sub-agent from its Claude source
- Model and effort mappings in one place, with an error when a value is unmapped
- A test that fails if any committed Codex file differs from the converter's output
- An overwrite guard, so an existing output file is never replaced without `--overwrite`

## Documents

Each item below is a file in this folder.

- [`claude_to_codex_subagent_converter.py`](claude_to_codex_subagent_converter.py): **Claude-to-Codex sub-agent converter** — `python scripts/claude_to_codex_subagent_converter.py <agent.md> [-o <agent.toml>] [--overwrite]`. Without `-o` the output is written beside the input with a `.toml` extension. Maps `opus` to `gpt-5.4`, `sonnet` to `gpt-5.3-codex`, `haiku` to `gpt-5.1-codex-mini`, and efforts `low`, `medium`, `high` and `xhigh` unchanged.
- [`tests/test_claude_to_codex_subagent_converter.py`](tests/test_claude_to_codex_subagent_converter.py): **Converter tests** — `python -m unittest discover -s scripts/tests`. Covers frontmatter parsing, the mapping tables, TOML string escaping, the overwrite guard, and the regeneration check over every file in `.codex/agents/`.

## Maintenance

When adding or changing files in this folder:

- Keep this README list in sync with the files present.
- When Codex model names change, update the mapping tables, regenerate all files in `.codex/agents/`, run the tests, and update the mapping listed here and in `.codex/README.md`.
- Add a test for every behaviour change to the converter.
