"""Comando 'wikictl promote' para consolidar evidencia analizada en conocimiento persistente."""

from __future__ import annotations
import argparse
from datetime import date
from pathlib import Path
import sys

from wikictl.core.vault import Vault
from wikictl.core.links import slugify
from wikictl.core.frontmatter import parse_yaml_subset, dump_yaml_subset, join_document, parse_frontmatter
from wikictl.core.git_ops import generate_diff, stage_and_commit, format_knowledge_commit_message


def execute_promote(args: argparse.Namespace) -> int:
    vault = Vault(args.vault_dir).scan()
    raw_target = args.target.strip()

    # Normalizar slug: puede ser nombre directo, ruta en raw o ruta de archivo en .work/ingest
    slug = slugify(Path(raw_target).stem)
    ingest_file = vault.root / ".work" / "ingest" / f"{slug}.yaml"

    if not ingest_file.exists():
        print(
            f"❌ Error: No se encontró artefacto de ingesta para '{slug}'.\n"
            f"   Se esperaba: {ingest_file.relative_to(vault.root)}\n"
            f"   Ejecuta primero: wikictl ingest <fuente>",
            file=sys.stderr,
        )
        return 1

    try:
        ingest_content = ingest_file.read_text(encoding="utf-8")
        data = parse_yaml_subset(ingest_content)
    except Exception as e:
        print(f"❌ Error al leer el artefacto de ingesta: {e}", file=sys.stderr)
        return 1

    source_file = data.get("source_file", f"raw/{slug}.md")
    source_title = data.get("title", slug.replace("-", " ").title())
    concepts = data.get("concepts", [])
    claims = data.get("key_claims", [])

    today_str = date.today().isoformat()

    # Preparar plan de cambios: path -> (action, old_content, new_content, description)
    changes: dict[str, tuple[str, str, str, str]] = {}
    created_files: list[str] = []
    updated_files: list[str] = []

    # 1. Procesar conceptos propuestos
    for c in concepts:
        if not isinstance(c, dict):
            continue
        c_name = c.get("name") or source_title
        c_slug = slugify(c_name)
        c_type = c.get("type", "concept")
        c_def = c.get("definition", "")
        c_aliases = c.get("aliases", [])
        c_tags = c.get("tags", [])

        target_rel = f"wiki/concepts/{c_slug}.md"
        if c_type == "technology":
            target_rel = f"wiki/technologies/{c_slug}.md"
        elif c_type == "person":
            target_rel = f"wiki/people/{c_slug}.md"
        elif c_type == "topic":
            target_rel = f"wiki/topics/{c_slug}.md"
        elif c_type == "synthesis":
            target_rel = f"wiki/synthesis/{c_slug}.md"

        # existing_note solo debe resolverse si pertenece a wiki/ (nunca alterar archivos en raw/)
        resolved = vault.resolve_link(c_name)
        existing_note = None
        if resolved and resolved.rel_path.startswith("wiki/"):
            existing_note = resolved
        elif target_rel in vault.notes and target_rel.startswith("wiki/"):
            existing_note = vault.notes[target_rel]

        if not existing_note:
            # CREATE
            new_fm = {
                "type": c_type,
                "title": c_name,
                "status": "active",
                "created": today_str,
                "updated": today_str,
                "aliases": c_aliases,
                "tags": c_tags,
                "sources": [f"[[{source_title}]]" if source_title else f"[[{slug}]]"],
                "confidence": data.get("confidence", "high"),
                "volatile": False,
            }

            # Estructurar cuerpo distinguiendo epistemológicamente Hecho / Interpretación / Inferencia
            facts = [cl for cl in claims if isinstance(cl, dict) and cl.get("type") == "fact"]
            interpretations = [
                cl for cl in claims if isinstance(cl, dict) and cl.get("type") == "interpretation"
            ]
            inferences = [
                cl for cl in claims if isinstance(cl, dict) and cl.get("type") == "inference"
            ]

            body_lines = [f"# {c_name}\n", f"{c_def}\n"]

            if facts:
                body_lines.append("## Hechos y Evidencias Respaldadas\n")
                for f in facts:
                    claim_text = f.get("claim", "")
                    quote = f.get("evidence_quote")
                    if quote:
                        body_lines.append(f"- **Afirmación**: {claim_text}\n  > \"{quote}\"")
                    else:
                        body_lines.append(f"- {claim_text}")
                body_lines.append("")

            if interpretations:
                body_lines.append("## Interpretaciones y Síntesis\n")
                for inter in interpretations:
                    body_lines.append(f"- {inter.get('claim', '')}")
                body_lines.append("")

            if inferences:
                body_lines.append("## Inferencias e Hipótesis Derivadas\n")
                for inf in inferences:
                    conf = inf.get("confidence", "medium")
                    body_lines.append(f"- ({conf}) {inf.get('claim', '')}")
                body_lines.append("")

            body_lines.append("## Referencias y Fuentes\n")
            body_lines.append(f"- [[{source_title}]] (archivo original: `{source_file}`)")

            new_body = "\n".join(body_lines)
            new_content = join_document(new_fm, new_body)

            changes[target_rel] = ("CREATE", "", new_content, f"Creación de {c_type} '{c_name}'")
            created_files.append(target_rel)
        else:
            # UPDATE
            rel_existing = existing_note.rel_path
            old_fm = dict(existing_note.frontmatter)
            old_body = existing_note.body

            # Actualizar fecha y añadir fuente si no está
            old_fm["updated"] = today_str
            current_sources = list(old_fm.get("sources", []))
            new_source_ref = f"[[{source_title}]]"
            if new_source_ref not in current_sources:
                current_sources.append(new_source_ref)
                old_fm["sources"] = current_sources

            # Añadir nueva referencia al final del cuerpo si no existe
            new_body = old_body.rstrip()
            if source_title not in new_body:
                new_body += (
                    f"\n\n### Actualización ({today_str})\n"
                    f"- Nueva evidencia incorporada desde [[{source_title}]]."
                )

            updated_content = join_document(old_fm, new_body)
            changes[rel_existing] = (
                "UPDATE",
                existing_note.raw_content,
                updated_content,
                f"Actualización de '{existing_note.title}' con nueva fuente",
            )
            updated_files.append(rel_existing)

    # Evaluación y presentación
    is_apply = getattr(args, "apply", False)
    dry_run = not is_apply or getattr(args, "dry_run", False)

    print(f"\n📋 Plan de Promoción para '{slug}':")
    print("-" * 60)

    for path, (action, old_c, new_c, desc) in changes.items():
        icon = "✨ [CREATE]" if action == "CREATE" else "📝 [UPDATE]"
        print(f"{icon} {path} — {desc}")

    print("-" * 60)

    # Mostrar Diffs
    print("\n🔍 Diffs Detallados:")
    for path, (action, old_c, new_c, desc) in changes.items():
        diff = generate_diff(old_c, new_c, path)
        print(f"\n--- {path} ---")
        print(diff if diff else "(Sin cambios textuales)")

    if dry_run:
        print("\n🔒 Modo Dry-Run activo: No se modificó ningún archivo en el disco.")
        print("   Para aplicar los cambios, ejecuta:")
        print(f"   wikictl promote {slug} --apply")
        print("   Para aplicar y hacer commit directo en Git:")
        print(f"   wikictl promote {slug} --apply --commit\n")
        return 0

    # Aplicar cambios al filesystem
    print("\n💾 Aplicando cambios en el disco...")
    for path, (action, old_c, new_c, desc) in changes.items():
        abs_target = vault.root / path
        abs_target.parent.mkdir(parents=True, exist_ok=True)
        abs_target.write_text(new_c, encoding="utf-8")
        print(f"   ✓ {action}: {path}")

    # Actualizar estado del artefacto de ingesta a 'promoted'
    data["status"] = "promoted"
    data["promoted_at"] = today_str
    ingest_file.write_text(dump_yaml_subset(data), encoding="utf-8")
    print(f"   ✓ Estado actualizado en: {ingest_file.relative_to(vault.root)}")

    if getattr(args, "commit", False):
        commit_details = [f"created {f}" for f in created_files] + [
            f"updated {f}" for f in updated_files
        ]
        msg = format_knowledge_commit_message("promote", slug, commit_details)
        success, git_log = stage_and_commit(vault.root, msg)
        if success:
            print(f"\n📦 Git Commit realizado con éxito:\n   {msg.splitlines()[0]}")
        else:
            print(f"\n⚠️  No se pudo realizar el commit en Git: {git_log}")

    print("\n✅ Promoción completada con éxito.\n")
    return 0
