"""Comando 'wikictl research' para andamiaje de investigaciones temáticas."""

from __future__ import annotations
import argparse
from datetime import date
from pathlib import Path

from wikictl.core.vault import Vault
from wikictl.core.links import slugify
from wikictl.core.frontmatter import join_document


def execute_research(args: argparse.Namespace) -> int:
    vault = Vault(args.vault_dir)
    topic = args.topic.strip()
    slug = slugify(topic)
    today_str = date.today().isoformat()

    dest_rel = f"research/{today_str}-{slug}.md"
    dest_path = vault.root / dest_rel

    if dest_path.exists() and not getattr(args, "force", False):
        print(f"⚠️  La investigación ya existe en: {dest_rel}")
        return 0

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    fm = {
        "type": "research",
        "title": topic,
        "status": "active",
        "created": today_str,
        "updated": today_str,
        "tags": ["research"],
        "confidence": "medium",
        "sources": [],
    }

    body = f"""# Investigación: {topic}

## 1. Pregunta Principal y Alcance
> {topic}

### Subpreguntas Derivadas
- ¿Cuáles son los fundamentos teóricos respaldados por fuentes primarias?
- ¿Qué contradicciones o desacuerdos existen en la literatura o práctica?
- ¿Qué implicaciones directas tiene para nuestros proyectos?

## 2. Estrategia de Fuentes y Evidencia
- Fuentes analizadas en `raw/`:
  - 

## 3. Hechos y Hallazgos Principales (Facts)
- 

## 4. Contradicciones y Debates Abiertos
- 

## 5. Conclusiones e Inferencias (Inferences)
- (high/medium/low) Síntesis de los hallazgos.

## 6. Siguientes Pasos
- [ ] Promover conceptos consolidados con `wikictl promote`.
"""

    content = join_document(fm, body)
    dest_path.write_text(content, encoding="utf-8")

    print(f"\n🔬 Investigación inicializada:")
    print(f"   Archivo: {dest_rel}")
    print("\n💡 Próximo paso:")
    print("   Trabaja con tu LLM para completar la evidencia y subpreguntas.")
    print(f"   Al finalizar, puedes promover conceptos usando: wikictl promote {dest_rel} --dry-run\n")
    return 0
