"""Comando 'wikictl init' para verificar y recrear la estructura canónica del baúl."""

from __future__ import annotations
import argparse
from pathlib import Path

from wikictl.core.vault import Vault

CANONICAL_FOLDERS = [
    "raw/papers",
    "raw/books",
    "raw/articles",
    "raw/transcripts",
    "raw/notes",
    "raw/clippings",
    "raw/attachments",
    "wiki/concepts",
    "wiki/people",
    "wiki/technologies",
    "wiki/topics",
    "wiki/debates",
    "wiki/decisions",
    "wiki/synthesis",
    "projects",
    "published/articles",
    "published/newsletters",
    "published/documentations",
    "published/courses",
    "published/presentations",
    "published/publications",
    "research",
    ".work/ingest",
    ".work/lint",
]


def execute_init(args: argparse.Namespace) -> int:
    vault = Vault(args.vault_dir)
    created_count = 0

    print(f"\n📁 Verificando estructura canónica en: {vault.root}")

    for folder_rel in CANONICAL_FOLDERS:
        folder_path = vault.root / folder_rel
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            # Agregar .gitkeep si el directorio está vacío para que Git lo rastree
            gitkeep = folder_path / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
            created_count += 1
            print(f"   ✨ Creada carpeta: {folder_rel}/")

    if created_count == 0:
        print("   ✅ Todas las carpetas canónicas ya existen.")
    else:
        print(f"   ✅ Se recrearon {created_count} carpetas faltantes con éxito.")

    print("\nEstructura lista para operar con Obsidian, Git y LLMs.\n")
    return 0
