"""Comando 'wikictl impact' para análisis de impacto en el grafo de dependencias."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

from wikictl.core.vault import Vault


def execute_impact(args: argparse.Namespace) -> int:
    vault = Vault(args.vault_dir).scan()
    note_target = args.note.strip()

    note = vault.resolve_link(note_target)
    if not note:
        print(f"❌ Error: No se encontró la nota '{note_target}' en el baúl.", file=sys.stderr)
        return 1

    backlinks = sorted(vault.get_backlinks(note.rel_path))

    print(f"\n📊 Análisis de Impacto para: {note.title}")
    print(f"   Ruta: {note.rel_path}")
    print(f"   Tipo: {note.note_type or 'desconocido'}")
    print("-" * 60)

    if not backlinks:
        print("🌱 Esta nota no tiene dependientes directos. Modificarla no impacta otros artefactos.\n")
        return 0

    # Categorizar dependientes
    groups: dict[str, list[str]] = {
        "Concepts / Wiki": [],
        "Syntheses": [],
        "Research": [],
        "Projects": [],
        "Published": [],
        "Otros": [],
    }

    for b in backlinks:
        if b.startswith("wiki/synthesis/"):
            groups["Syntheses"].append(b)
        elif b.startswith("wiki/"):
            groups["Concepts / Wiki"].append(b)
        elif b.startswith("research/"):
            groups["Research"].append(b)
        elif b.startswith("projects/"):
            groups["Projects"].append(b)
        elif b.startswith("published/"):
            groups["Published"].append(b)
        else:
            groups["Otros"].append(b)

    total_dependents = sum(len(items) for items in groups.values())
    print(f"Total de notas dependientes: {total_dependents}\n")

    for group_name, items in groups.items():
        if items:
            print(f"📁 {group_name} ({len(items)}):")
            for item in items:
                dep_note = vault.notes.get(item)
                title = dep_note.title if dep_note else item
                print(f"   └── {title} (`{item}`)")

    print("-" * 60)
    print("💡 Si vas a modificar o depreciar esta nota, revisa los artefactos listados arriba.\n")
    return 0
