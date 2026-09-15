"""Tests para el módulo core/vault.py."""

import tempfile
import unittest
from pathlib import Path
from wikictl.core.vault import Vault


class TestVault(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        # Crear estructura de carpetas simulada
        (self.root / "wiki" / "concepts").mkdir(parents=True)
        (self.root / "wiki" / "technologies").mkdir(parents=True)

        # Nota 1: Concepto
        note1 = """---
type: concept
title: Cognitive Offloading
status: active
aliases:
  - Descarga cognitiva
---

# Cognitive Offloading

Refiere a la transferencia de memoria a [[Obsidian]].
"""
        (self.root / "wiki" / "concepts" / "cognitive-offloading.md").write_text(
            note1, encoding="utf-8"
        )

        # Nota 2: Tecnología
        note2 = """---
type: technology
title: Obsidian
status: active
---

# Obsidian

Herramienta de notas vinculadas que asiste en la [[Descarga cognitiva]].
"""
        (self.root / "wiki" / "technologies" / "obsidian.md").write_text(note2, encoding="utf-8")

        self.vault = Vault(self.root).scan()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scan_notes(self):
        self.assertEqual(len(self.vault.notes), 2)
        concepts = self.vault.find_by_type("concept")
        self.assertEqual(len(concepts), 1)
        self.assertEqual(concepts[0].title, "Cognitive Offloading")

    def test_resolve_link_by_title_and_alias(self):
        # Resolver por título directo
        resolved = self.vault.resolve_link("Obsidian")
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.title, "Obsidian")

        # Resolver por alias
        resolved_alias = self.vault.resolve_link("Descarga cognitiva")
        self.assertIsNotNone(resolved_alias)
        self.assertEqual(resolved_alias.title, "Cognitive Offloading")

        # Resolver por slug de archivo
        resolved_slug = self.vault.resolve_link("cognitive-offloading")
        self.assertIsNotNone(resolved_slug)
        self.assertEqual(resolved_slug.title, "Cognitive Offloading")

    def test_backlinks_calculation(self):
        obsidian_path = "wiki/technologies/obsidian.md"
        concept_path = "wiki/concepts/cognitive-offloading.md"

        # Note 1 links to Obsidian -> Obsidian should have note 1 in backlinks
        backlinks_obsidian = self.vault.get_backlinks(obsidian_path)
        self.assertIn(concept_path, backlinks_obsidian)

        # Note 2 links to alias "Descarga cognitiva" -> Note 1 should have note 2 in backlinks
        backlinks_concept = self.vault.get_backlinks(concept_path)
        self.assertIn(obsidian_path, backlinks_concept)


if __name__ == "__main__":
    unittest.main()
