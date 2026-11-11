"""
Tests for scripts/claude_to_codex_subagent_converter.py.

Run from the repository root with the standard library runner, so no test
framework needs installing:

    python -m unittest discover -s scripts/tests

PyYAML must be importable, because the converter needs it.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "claude_to_codex_subagent_converter.py"


def _load_converter():
    """
    Import the converter as a module from its file path.

    Returns:
        module: The loaded converter module.
    """
    spec = importlib.util.spec_from_file_location("converter", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


conv = _load_converter()

MINIMAL_MD = """---
name: sample
description: Does one thing.
model: opus
effort: xhigh
tools: Read, Grep
color: cyan
---

# Sample

Body line with "quotes" and a \\ backslash.
"""


class ParseFrontmatterTests(unittest.TestCase):
    """The frontmatter parser accepts valid input and rejects malformed input."""

    def test_valid_frontmatter_splits_fields_and_body(self):
        frontmatter, body = conv.parse_frontmatter_and_body(MINIMAL_MD)
        self.assertEqual(frontmatter["name"], "sample")
        self.assertEqual(frontmatter["effort"], "xhigh")
        self.assertTrue(body.startswith("\n# Sample"))

    def test_missing_opening_delimiter_raises(self):
        with self.assertRaises(ValueError):
            conv.parse_frontmatter_and_body("name: x\n---\nbody\n")

    def test_missing_closing_delimiter_raises(self):
        with self.assertRaises(ValueError):
            conv.parse_frontmatter_and_body("---\nname: x\nbody\n")

    def test_non_mapping_frontmatter_raises(self):
        with self.assertRaises(ValueError):
            conv.parse_frontmatter_and_body("---\n- a\n- b\n---\nbody\n")

    def test_byte_order_mark_is_tolerated(self):
        frontmatter, _ = conv.parse_frontmatter_and_body("﻿" + MINIMAL_MD)
        self.assertEqual(frontmatter["name"], "sample")


class BuildTomlTests(unittest.TestCase):
    """TOML generation maps fields, escapes strings and enforces required fields."""

    def test_maps_model_and_effort(self):
        frontmatter, body = conv.parse_frontmatter_and_body(MINIMAL_MD)
        toml = conv.build_toml(frontmatter, body)
        self.assertIn('model = "gpt-5.4"', toml)
        self.assertIn('model_reasoning_effort = "xhigh"', toml)

    def test_every_claude_tier_and_effort_is_mapped(self):
        for tier in ("haiku", "sonnet", "opus"):
            self.assertIn(tier, conv.MODEL_MAPPING)
        for effort in ("low", "medium", "high", "xhigh"):
            self.assertIn(effort, conv.EFFORT_MAPPING)

    def test_unmapped_model_raises(self):
        frontmatter = {"name": "n", "description": "d", "model": "gpt-9"}
        with self.assertRaises(ValueError):
            conv.build_toml(frontmatter, "body")

    def test_missing_name_or_description_raises(self):
        with self.assertRaises(ValueError):
            conv.build_toml({"description": "d"}, "body")
        with self.assertRaises(ValueError):
            conv.build_toml({"name": "n", "description": "  "}, "body")

    def test_optional_model_and_effort_are_omitted_when_absent(self):
        toml = conv.build_toml({"name": "n", "description": "d"}, "body")
        self.assertNotIn("model", toml)

    def test_basic_string_escaping(self):
        self.assertEqual(conv.toml_basic_string('a"b\\c\n'), '"a\\"b\\\\c\\n"')

    def test_multiline_string_escapes_triple_quotes_and_backslashes(self):
        out = conv.toml_multiline_basic_string('x """ y \\ z\r\nw')
        self.assertTrue(out.startswith('"""\n'))
        self.assertIn('""\\"', out)
        self.assertIn("\\\\", out)
        self.assertNotIn("\r", out)


class MainTests(unittest.TestCase):
    """The command-line entry point writes a file and refuses to overwrite."""

    def test_writes_toml_and_refuses_overwrite_without_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "agent.md"
            src.write_text(MINIMAL_MD, encoding="utf-8")
            self.assertEqual(conv.main([str(src)]), 0)
            out = src.with_suffix(".toml")
            self.assertTrue(out.exists())
            self.assertEqual(conv.main([str(src)]), 1)
            self.assertEqual(conv.main([str(src), "--overwrite"]), 0)

    def test_rejects_non_markdown_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "agent.txt"
            src.write_text(MINIMAL_MD, encoding="utf-8")
            self.assertEqual(conv.main([str(src)]), 1)


class ShippedAgentsTests(unittest.TestCase):
    """Every committed Codex agent is exactly what the converter produces."""

    def test_codex_agents_match_regeneration(self):
        claude_dir = REPO_ROOT / ".claude" / "agents"
        codex_dir = REPO_ROOT / ".codex" / "agents"
        sources = sorted(p for p in claude_dir.glob("*.md") if p.name != "README.md")
        self.assertTrue(sources, "no Claude agents found")
        for src in sources:
            with self.subTest(agent=src.stem):
                frontmatter, body = conv.parse_frontmatter_and_body(
                    src.read_text(encoding="utf-8")
                )
                expected = conv.build_toml(frontmatter, body)
                target = codex_dir / f"{src.stem}.toml"
                self.assertTrue(target.exists(), f"{target} missing")
                self.assertEqual(target.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    sys.exit(unittest.main())
