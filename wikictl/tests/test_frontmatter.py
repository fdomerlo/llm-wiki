"""Tests para el módulo core/frontmatter.py."""

import unittest
from wikictl.core.frontmatter import parse_frontmatter, dump_yaml_subset, join_document


class TestFrontmatter(unittest.TestCase):
    def test_parse_standard_frontmatter(self):
        doc = """---
type: concept
title: Cognitive Offloading
status: active
created: 2026-08-16
updated: 2026-08-16
aliases:
  - Descarga cognitiva
  - Offloading
tags:
  - cognition
  - technology
sources:
  - "[[Cognitive Offloading Paper]]"
confidence: high
volatile: false
---

# Cognitive Offloading

Este es el cuerpo de la nota.
"""
        fm, body = parse_frontmatter(doc)
        self.assertEqual(fm["type"], "concept")
        self.assertEqual(fm["title"], "Cognitive Offloading")
        self.assertEqual(fm["status"], "active")
        self.assertEqual(fm["created"], "2026-08-16")
        self.assertEqual(fm["aliases"], ["Descarga cognitiva", "Offloading"])
        self.assertEqual(fm["tags"], ["cognition", "technology"])
        self.assertEqual(fm["sources"], ["[[Cognitive Offloading Paper]]"])
        self.assertEqual(fm["confidence"], "high")
        self.assertFalse(fm["volatile"])
        self.assertIn("# Cognitive Offloading", body)

    def test_parse_no_frontmatter(self):
        doc = "# Nota sin frontmatter\n\nTexto simple."
        fm, body = parse_frontmatter(doc)
        self.assertEqual(fm, {})
        self.assertEqual(body, doc)

    def test_parse_inline_lists(self):
        doc = """---
type: topic
tags: [tag1, tag2, tag3]
volatile: true
review_after: 2026-12-01
---

Cuerpo
"""
        fm, body = parse_frontmatter(doc)
        self.assertEqual(fm["type"], "topic")
        self.assertEqual(fm["tags"], ["tag1", "tag2", "tag3"])
        self.assertTrue(fm["volatile"])
        self.assertEqual(fm["review_after"], "2026-12-01")

    def test_dump_and_join_roundtrip(self):
        data = {
            "type": "technology",
            "title": "Obsidian",
            "status": "active",
            "sources": ["[[PKM Paper]]"],
            "aliases": ["Obsidian App"],
            "volatile": False,
        }
        body = "Contenido sobre Obsidian."
        full_doc = join_document(data, body)

        fm_parsed, body_parsed = parse_frontmatter(full_doc)
        self.assertEqual(fm_parsed["type"], "technology")
        self.assertEqual(fm_parsed["title"], "Obsidian")
        self.assertEqual(fm_parsed["status"], "active")
        self.assertEqual(fm_parsed["sources"], ["[[PKM Paper]]"])
        self.assertEqual(fm_parsed["aliases"], ["Obsidian App"])
        self.assertFalse(fm_parsed["volatile"])
        self.assertEqual(body_parsed.strip(), body)


if __name__ == "__main__":
    unittest.main()
