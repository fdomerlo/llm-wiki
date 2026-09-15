"""Tests para el módulo core/validator.py."""

import tempfile
import unittest
from pathlib import Path
from wikictl.core.vault import Vault
from wikictl.core.validator import lint_vault


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "wiki" / "concepts").mkdir(parents=True)
        (self.root / "wiki" / "technologies").mkdir(parents=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_broken_link_detection(self):
        note = """---
type: concept
title: Nota con link roto
status: active
---

Enlaza a [[Nota Inexistente]].
"""
        (self.root / "wiki" / "concepts" / "test.md").write_text(note, encoding="utf-8")
        vault = Vault(self.root).scan()
        issues = lint_vault(vault)

        broken_links = [i for i in issues if i.category == "broken_link"]
        self.assertEqual(len(broken_links), 1)
        self.assertIn("Nota Inexistente", broken_links[0].message)

    def test_missing_frontmatter_detection(self):
        (self.root / "wiki" / "concepts" / "plain.md").write_text(
            "# Sin frontmatter", encoding="utf-8"
        )
        vault = Vault(self.root).scan()
        issues = lint_vault(vault)

        schema_errors = [
            i for i in issues if i.category == "schema" and i.file.endswith("plain.md")
        ]
        self.assertTrue(any("Falta el bloque frontmatter" in i.message for i in schema_errors))

    def test_expired_volatility_detection(self):
        note = """---
type: technology
title: Librería Vieja
status: active
volatile: true
review_after: 2020-01-01
---

Texto
"""
        (self.root / "wiki" / "technologies" / "old.md").write_text(note, encoding="utf-8")
        vault = Vault(self.root).scan()
        issues = lint_vault(vault)

        obsolescence_warnings = [i for i in issues if i.category == "obsolescence"]
        self.assertTrue(any("Fecha de revisión expirada" in i.message for i in obsolescence_warnings))

    def test_orphan_note_detection(self):
        note = """---
type: concept
title: Nota Aislada
status: active
---

No tiene links a nadie.
"""
        (self.root / "wiki" / "concepts" / "isolated.md").write_text(note, encoding="utf-8")
        vault = Vault(self.root).scan()
        issues = lint_vault(vault)

        orphans = [i for i in issues if i.category == "orphan"]
        self.assertEqual(len(orphans), 1)


if __name__ == "__main__":
    unittest.main()
