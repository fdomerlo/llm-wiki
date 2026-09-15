"""Tests para el módulo core/links.py."""

import unittest
from wikictl.core.links import extract_links, slugify, WikiLink


class TestLinks(unittest.TestCase):
    def test_extract_simple_link(self):
        text = "Mencionamos a [[Andrej Karpathy]] en la introducción."
        links = extract_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].target, "Andrej Karpathy")
        self.assertEqual(links[0].clean_target, "Andrej Karpathy")
        self.assertIsNone(links[0].alias)
        self.assertIsNone(links[0].anchor)
        self.assertFalse(links[0].is_embed)

    def test_extract_with_alias_and_anchor(self):
        text = "Ver [[Cognitive Offloading#Mecanismos|mecanismos de descarga]] para más detalle."
        links = extract_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].target, "Cognitive Offloading")
        self.assertEqual(links[0].anchor, "Mecanismos")
        self.assertEqual(links[0].alias, "mecanismos de descarga")

    def test_extract_embed(self):
        text = "![[diagrama-arquitectura.png]]"
        links = extract_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].target, "diagrama-arquitectura.png")
        self.assertTrue(links[0].is_embed)

    def test_extract_target_with_extension(self):
        text = "Revisar [[paper-2026.md]] y [[paper-2026]]."
        links = extract_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0].clean_target, "paper-2026")
        self.assertEqual(links[1].clean_target, "paper-2026")

    def test_slugify(self):
        self.assertEqual(slugify("Cognitive Offloading"), "cognitive-offloading")
        self.assertEqual(slugify("¿Qué es la IA?"), "que-es-la-ia")
        self.assertEqual(slugify("LLM / Wiki Architecture"), "llm-wiki-architecture")


if __name__ == "__main__":
    unittest.main()
