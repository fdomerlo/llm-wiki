"""Comando 'wikictl synthesize' para andamiaje de síntesis transversales."""

from __future__ import annotations
import argparse
from datetime import date
from pathlib import Path

from wikictl.core.vault import Vault
from wikictl.core.links import slugify
from wikictl.core.frontmatter import join_document


def execute_synthesize(args: argparse.Namespace) -> int:
    vault = Vault(args.vault_dir).scan()
    topic = args.topic.strip()
    slug = slugify(topic)
    today_str = date.today().isoformat()

    dest_rel = f"wiki/synthesis/{slug}.md"
    dest_path = vault.root / dest_rel

    if dest_path.exists() and not getattr(args, "force", False):
        print(f"⚠️  La síntesis ya existe en: {dest_rel}")
        return 0

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    sources_linked = []
    if getattr(args, "sources", None):
        for s in args.sources:
            sources_linked.append(f"[[{s.strip()}]]")

    fm = {
        "type": "synthesis",
        "title": topic,
        "status": "active",
        "created": today_str,
        "updated": today_str,
        "tags": ["synthesis"],
        "confidence": "high",
        "sources": sources_linked,
        "derived_from": [],
    }

    body = f"""# Síntesis: {topic}

## 1. Patrón o Núcleo Conceptual
> Descripción concisa del principio o patrón unificador.

## 2. Notas y Fuentes Convergentes
"""
    if sources_linked:
        for sl in sources_linked:
            body += f"- {sl}\n"
    else:
        body += "- [[Nota Relacionada 1]]\n- [[Nota Relacionada 2]]\n"

    body += """
## 3. Comparativa y Matices
| Dimensión | Enfoque A | Enfoque B |
| :--- | :--- | :--- |
| Propósito | | |
| Trade-offs | | |

## 4. Implicaciones y Nuevo Conocimiento (Inferences)
- 

## 5. Referencias
"""
    content = join_document(fm, body)
    dest_path.write_text(content, encoding="utf-8")

    print(f"\n🧩 Síntesis inicializada:")
    print(f"   Archivo: {dest_rel}")
    print("\n💡 Próximo paso:")
    print(f"   El LLM debe analizar los patrones comunes entre las notas vinculadas.")
    print(f"   Ejecuta 'wikictl lint' posteriormente para verificar la integridad de los enlaces.\n")
    return 0
