"""Comando 'wikictl ingest' para registrar y preparar el análisis de evidencias."""

from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
from pathlib import Path
import re
import sys

from wikictl.core.vault import Vault
from wikictl.core.links import slugify
from wikictl.core.frontmatter import dump_yaml_subset, parse_yaml_subset


def calculate_sha256(path: Path) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


def execute_ingest(args: argparse.Namespace) -> int:
    vault = Vault(args.vault_dir)
    source_path = Path(args.source)

    if not source_path.is_absolute():
        source_path = (vault.root / source_path).resolve()

    if not source_path.exists():
        print(f"❌ Error: La fuente '{source_path}' no existe.", file=sys.stderr)
        return 1

    try:
        rel_source = source_path.relative_to(vault.root)
    except ValueError:
        rel_source = source_path.name

    slug = slugify(source_path.stem)
    dest_dir = vault.root / ".work" / "ingest"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / f"{slug}.yaml"

    checksum = calculate_sha256(source_path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extraer título candidato si es Markdown o texto
    candidate_title = source_path.stem.replace("-", " ").replace("_", " ").title()
    if source_path.suffix.lower() in (".md", ".txt"):
        try:
            content = source_path.read_text(encoding="utf-8", errors="replace")
            for line in content.splitlines():
                line_s = line.strip()
                if line_s.startswith("# "):
                    candidate_title = line_s[2:].strip()
                    break
        except Exception:
            pass

    # Si ya existe y no se especifica --force
    if dest_file.exists() and not args.force and not getattr(args, "validate", False):
        print(f"⚠️  El artefacto de ingesta ya existe en: {dest_file.relative_to(vault.root)}")
        print("Usa --force para sobrescribir o procede a completar el análisis con tu LLM.")
        return 0

    if getattr(args, "validate", False):
        # Modo validación de la estructura del artefacto de ingesta
        if not dest_file.exists():
            print(f"❌ Error: No existe el artefacto de ingesta {dest_file}", file=sys.stderr)
            return 1
        raw_yaml = dest_file.read_text(encoding="utf-8")
        data = parse_yaml_subset(raw_yaml)
        if not data.get("source_file") or not data.get("key_claims") or not data.get("concepts"):
            print("❌ Validación fallida: El archivo de ingesta carece de claims o conceptos.")
            return 1
        print("✅ Artefacto de ingesta validado correctamente.")
        return 0

    # Plantilla estructurada de ingesta conforme al principio epistemológico
    template_data = {
        "source_file": str(rel_source),
        "source_slug": slug,
        "checksum": checksum,
        "ingested_at": now,
        "status": "pending_llm_analysis",
        "title": candidate_title,
        "authors": [],
        "source_type": "article",  # paper, book, article, transcript, dataset
        "confidence": "high",
        "key_claims": [
            {
                "claim": "Describir aquí la primera afirmación clave extraída",
                "type": "fact",  # fact | interpretation | inference
                "confidence": "high",
                "evidence_quote": "Cita o extracto textual de la fuente original",
            }
        ],
        "concepts": [
            {
                "name": candidate_title,
                "type": "concept",  # concept, technology, person, topic, debate
                "definition": "Definición del concepto según la fuente",
                "aliases": [],
                "tags": [],
            }
        ],
        "proposed_actions": [
            {
                "action": "CREATE",
                "target": f"wiki/concepts/{slug}.md",
                "title": candidate_title,
            }
        ],
    }

    # Guardar artefacto
    yaml_output = dump_yaml_subset(template_data)
    dest_file.write_text(yaml_output, encoding="utf-8")

    print(f"\n📥 Ingesta registrada con éxito:")
    print(f"   Fuente:    {rel_source}")
    print(f"   Checksum:  {checksum[:12]}...")
    print(f"   Artefacto: {dest_file.relative_to(vault.root)}")
    print("\n💡 Próximo paso (LLM):")
    print(f"   El LLM debe analizar '{rel_source}', completar 'key_claims' y 'concepts'")
    print(f"   en '{dest_file.relative_to(vault.root)}' y luego ejecutar:")
    print(f"   wikictl promote {slug} --dry-run\n")
    return 0
