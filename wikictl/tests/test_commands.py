"""Tests de integración para los comandos CLI de wikictl."""

import tempfile
import unittest
from pathlib import Path

from wikictl.cli import main


class TestCLICommands(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        # Crear estructura básica
        (self.root / "raw" / "articles").mkdir(parents=True)
        (self.root / "wiki" / "concepts").mkdir(parents=True)
        (self.root / "wiki" / "technologies").mkdir(parents=True)
        (self.root / "wiki" / "synthesis").mkdir(parents=True)
        (self.root / "projects").mkdir(parents=True)
        (self.root / "published" / "markdown").mkdir(parents=True)
        (self.root / ".work" / "ingest").mkdir(parents=True)
        (self.root / "research").mkdir(parents=True)

        # Crear archivo AGENTS.md en raíz del baúl
        (self.root / "AGENTS.md").write_text("# Protocolo", encoding="utf-8")

        # Crear un archivo de prueba en raw
        self.sample_raw = self.root / "raw" / "articles" / "test-paper.md"
        self.sample_raw.write_text(
            "# Test Paper\n\nEste paper describe la memoria extendida y el concepto de descarga cognitiva.\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ingest_and_promote_cycle(self):
        # 1. wikictl ingest
        code = main(["--vault-dir", str(self.root), "ingest", str(self.sample_raw)])
        self.assertEqual(code, 0)

        ingest_yaml = self.root / ".work" / "ingest" / "test-paper.yaml"
        self.assertTrue(ingest_yaml.exists())
        content = ingest_yaml.read_text(encoding="utf-8")
        self.assertIn("source_slug: test-paper", content)

        # 2. wikictl promote --dry-run
        code_dry = main(
            ["--vault-dir", str(self.root), "promote", "test-paper", "--dry-run"]
        )
        self.assertEqual(code_dry, 0)
        # En dry-run no se debe haber creado la nota en wiki/concepts
        concept_file = self.root / "wiki" / "concepts" / "test-paper.md"
        self.assertFalse(concept_file.exists())

        # 3. wikictl promote --apply
        code_apply = main(
            ["--vault-dir", str(self.root), "promote", "test-paper", "--apply"]
        )
        self.assertEqual(code_apply, 0)
        self.assertTrue(concept_file.exists())

        concept_text = concept_file.read_text(encoding="utf-8")
        self.assertIn("type: concept", concept_text)
        self.assertIn("title: Test Paper", concept_text)
        self.assertIn("status: active", concept_text)
        self.assertIn("[[Test Paper]]", concept_text)

    def test_research_command(self):
        code = main(
            [
                "--vault-dir",
                str(self.root),
                "research",
                "Impacto de la IA en la memoria",
            ]
        )
        self.assertEqual(code, 0)
        research_files = list((self.root / "research").glob("*.md"))
        self.assertEqual(len(research_files), 1)
        content = research_files[0].read_text(encoding="utf-8")
        self.assertIn("type: research", content)
        self.assertIn("Impacto de la IA en la memoria", content)

    def test_synthesize_command(self):
        code = main(
            [
                "--vault-dir",
                str(self.root),
                "synthesize",
                "Arquitectura de Agentes",
                "--sources",
                "MCP",
                "Tool Use",
            ]
        )
        self.assertEqual(code, 0)
        synth_file = self.root / "wiki" / "synthesis" / "arquitectura-de-agentes.md"
        self.assertTrue(synth_file.exists())
        content = synth_file.read_text(encoding="utf-8")
        self.assertIn("type: synthesis", content)
        self.assertIn("[[MCP]]", content)
        self.assertIn("[[Tool Use]]", content)

    def test_publish_and_impact_commands(self):
        # Crear una nota consolidada
        concept = """---
type: concept
title: Descarga Cognitiva
status: active
sources:
  - "[[Paper 2026]]"
---

# Descarga Cognitiva

Consiste en usar [[Obsidian|herramientas externas]] para almacenar información.
"""
        note_path = self.root / "wiki" / "concepts" / "descarga-cognitiva.md"
        note_path.write_text(concept, encoding="utf-8")

        # Otra nota que dependa de ella
        other = """---
type: concept
title: Memoria Externa
status: active
sources:
  - "[[Paper 2026]]"
---

Se relaciona con [[Descarga Cognitiva]].
"""
        (self.root / "wiki" / "concepts" / "memoria-externa.md").write_text(
            other, encoding="utf-8"
        )

        # 1. wikictl impact
        code_impact = main(
            ["--vault-dir", str(self.root), "impact", "Descarga Cognitiva"]
        )
        self.assertEqual(code_impact, 0)

        # 2. wikictl publish
        code_pub = main(
            [
                "--vault-dir",
                str(self.root),
                "publish",
                "Descarga Cognitiva",
                "--target",
                "markdown",
            ]
        )
        self.assertEqual(code_pub, 0)
        pub_file = self.root / "published" / "markdown" / "descarga-cognitiva.md"
        self.assertTrue(pub_file.exists())
        pub_content = pub_file.read_text(encoding="utf-8")
        # Verificar que transformó el wikilink con alias: [[Obsidian|herramientas externas]] -> herramientas externas
        self.assertIn("herramientas externas", pub_content)
        self.assertNotIn("[[Obsidian|", pub_content)

    def test_init_command(self):
        # Borrar una carpeta canónica
        import shutil
        target_dir = self.root / "raw" / "transcripts"
        if target_dir.exists():
            shutil.rmtree(target_dir)
        self.assertFalse(target_dir.exists())

        code = main(["--vault-dir", str(self.root), "init"])
        self.assertEqual(code, 0)
        self.assertTrue(target_dir.exists())
        self.assertTrue((target_dir / ".gitkeep").exists())


if __name__ == "__main__":
    unittest.main()
