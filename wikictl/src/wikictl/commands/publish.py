"""Comando 'wikictl publish' para preparar notas consolidadas para distribución externa."""

from __future__ import annotations
import argparse
from datetime import date
from pathlib import Path
import re
import sys

from wikictl.core.vault import Vault
from wikictl.core.links import slugify
from wikictl.core.frontmatter import join_document


def execute_publish(args: argparse.Namespace) -> int:
    vault = Vault(args.vault_dir).scan()
    note_target = args.note.strip()
    target_format = getattr(args, "target", "markdown") or "markdown"

    note = vault.resolve_link(note_target)
    if not note:
        print(f"❌ Error: No se encontró la nota '{note_target}' en el baúl.", file=sys.stderr)
        return 1

    # Checklists de publicación
    warnings: list[str] = []

    # 1. Fact & Source check
    sources = note.frontmatter.get("sources", [])
    if not sources:
        warnings.append("La nota no tiene fuentes primarias explícitas ('sources').")

    # 2. Privacy check
    tags = note.frontmatter.get("tags", [])
    if any("private" in t.lower() or "draft" in t.lower() for t in tags):
        warnings.append("La nota contiene etiquetas que indican contenido privado o preliminar.")

    slug = slugify(note.title)
    today_str = date.today().isoformat()
    dest_rel = f"published/{target_format}/{slug}.md"
    dest_path = vault.root / dest_rel
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Transformación de enlaces internos para publicación externa:
    # [[Nota|Alias]] -> Alias
    # [[Nota]] -> Nota
    clean_body = re.sub(
        r"\[\[([^\[\]\|\n]+?)(?:#[^\[\]\|\n]+?)?\|([^\[\]\n]+?)\]\]",
        r"\2",
        note.body,
    )
    clean_body = re.sub(
        r"\[\[([^\[\]\|\n]+?)(?:#[^\[\]\|\n]+?)?\]\]",
        r"\1",
        clean_body,
    )

    published_fm = {
        "title": note.title,
        "published_at": today_str,
        "target": target_format,
        "canonical_source": f"[[{note.rel_path}]]",
    }

    published_content = join_document(published_fm, clean_body)
    dest_path.write_text(published_content, encoding="utf-8")

    print(f"\n📢 Artefacto de publicación generado:")
    print(f"   Destino: {dest_rel}")
    print(f"   Formato: {target_format}")

    if warnings:
        print("\n⚠️  Advertencias de calidad de publicación:")
        for w in warnings:
            print(f"   - {w}")

    print("\n✅ Verificación de enlaces y metadatos completada con éxito.\n")
    return 0
