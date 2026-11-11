#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["PyYAML>=6.0"]
# ///
"""
Convert a Claude subagent Markdown file to a Codex-compatible TOML file.

The Claude file carries YAML frontmatter (name, description, model, effort,
tools, color) above a Markdown body. The Codex file carries the same name
and description, the body as developer_instructions, and the model and
effort translated through the two mapping tables below. Tools and color have
no Codex equivalent and are dropped.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:
    yaml = None

# Claude model tier -> Codex model. Kept in step with the hand-maintained
# values in .codex/agents/*.toml; update here first, then regenerate.
MODEL_MAPPING = {
    "haiku": "gpt-5.1-codex-mini",
    "sonnet": "gpt-5.3-codex",
    "opus": "gpt-5.4",
}

# Claude effort -> Codex model_reasoning_effort. Codex accepts xhigh.
EFFORT_MAPPING = {
    "low": "low",
    "medium": "medium",
    "high": "high",
    "xhigh": "xhigh",
}


def fail(message: str) -> int:
    print(f"Error: {message}", file=sys.stderr)
    return 1


def parse_frontmatter_and_body(raw: str) -> tuple[dict[str, Any], str]:
    if yaml is None:
        raise ValueError("PyYAML is required. Install it with: pip install PyYAML")

    text = raw.lstrip("\ufeff")
    lines = text.splitlines(keepends=True)

    if not lines or lines[0].strip() != "---":
        raise ValueError("YAML frontmatter not found (expected '---' block at top of file)")

    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index is None:
        raise ValueError("YAML frontmatter not found (expected '---' block at top of file)")

    frontmatter_text = "".join(lines[1:end_index])
    body = "".join(lines[end_index + 1 :])

    try:
        parsed = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        raise ValueError(f"Failed to parse YAML frontmatter: {exc}") from exc

    if parsed is None:
        parsed = {}
    if not isinstance(parsed, dict):
        raise ValueError("Failed to parse YAML frontmatter: top-level YAML must be a mapping")

    return parsed, body


def require_field(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if value is None:
        raise ValueError(f"Missing required field: {key}")
    text = str(value).strip()
    if not text:
        raise ValueError(f"Missing required field: {key}")
    return text


def map_optional_value(
    data: dict[str, Any], source_key: str, mapping: dict[str, str], error_label: str
) -> str | None:
    if source_key not in data or data[source_key] is None:
        return None

    source_value = str(data[source_key]).strip()
    if source_value not in mapping:
        raise ValueError(
            f"Unmapped {error_label} value: {source_value}. Add it to "
            f"{'MODEL_MAPPING' if error_label == 'model' else 'EFFORT_MAPPING'}"
        )

    return mapping[source_value]


def toml_basic_string(value: str) -> str:
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\b", "\\b")
        .replace("\t", "\\t")
        .replace("\n", "\\n")
        .replace("\f", "\\f")
        .replace("\r", "\\r")
    )
    return f'"{escaped}"'


def toml_multiline_basic_string(value: str) -> str:
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    escaped = normalized.replace("\\", "\\\\").replace('"""', '""\\"')
    return f'"""\n{escaped}"""'


def build_toml(frontmatter: dict[str, Any], body: str) -> str:
    name = require_field(frontmatter, "name")
    description = require_field(frontmatter, "description")
    model = map_optional_value(frontmatter, "model", MODEL_MAPPING, "model")
    effort = map_optional_value(frontmatter, "effort", EFFORT_MAPPING, "effort")

    if body.strip() == "":
        print("Warning: developer_instructions is empty", file=sys.stderr)

    lines = [
        f"name = {toml_basic_string(name)}",
        f"description = {toml_basic_string(description)}",
        f"developer_instructions = {toml_multiline_basic_string(body)}",
    ]

    if model is not None:
        lines.append(f"model = {toml_basic_string(model)}")
    if effort is not None:
        lines.append(f"model_reasoning_effort = {toml_basic_string(effort)}")

    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Claude subagent Markdown with YAML frontmatter to Codex TOML."
    )
    parser.add_argument("input", help="Path to input .md file")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output .toml file (default: input name with .toml extension)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output file if it already exists",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    input_path = Path(args.input)

    if input_path.suffix.lower() != ".md":
        return fail("Input file must be a .md file")

    if not input_path.is_file():
        return fail(f"Input file not found: {input_path}")

    output_path = Path(args.output) if args.output else input_path.with_suffix(".toml")
    if output_path.exists() and not args.overwrite:
        return fail(f"Output file already exists: {output_path}")

    try:
        raw = input_path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter_and_body(raw)
        toml_output = build_toml(frontmatter, body)
    except ValueError as exc:
        return fail(str(exc))

    output_path.write_text(toml_output, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
