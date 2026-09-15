"""Entrypoint CLI principal para wikictl."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

from wikictl.commands.lint import execute_lint
from wikictl.commands.ingest import execute_ingest
from wikictl.commands.promote import execute_promote
from wikictl.commands.research import execute_research
from wikictl.commands.synthesize import execute_synthesize
from wikictl.commands.publish import execute_publish
from wikictl.commands.impact import execute_impact


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wikictl",
        description="Kernel determinístico y CLI para el Knowledge Operating System (LLM Wiki)",
    )
    parser.add_argument(
        "--vault-dir",
        type=Path,
        default=None,
        help="Ruta a la raíz del baúl de Obsidian (por defecto busca AGENTS.md hacia arriba)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # wikictl lint
    lint_p = subparsers.add_parser("lint", help="Audita enlaces, esquemas, huérfanos y fechas de revisión")
    lint_p.add_argument("--path", type=str, default=None, help="Filtrar por subdirectorio (ej. wiki/concepts)")
    lint_p.add_argument("--strict", action="store_true", help="Falla (código 1) si hay advertencias además de errores")
    lint_p.add_argument("--json", action="store_true", help="Emite salida en formato JSON estructurado")

    # wikictl ingest
    ingest_p = subparsers.add_parser("ingest", help="Registra y prepara el análisis de una fuente de raw/")
    ingest_p.add_argument("source", type=str, help="Ruta al archivo original (ej. raw/articles/paper.md)")
    ingest_p.add_argument("--force", action="store_true", help="Sobrescribe el artefacto de ingesta si ya existe")
    ingest_p.add_argument("--validate", action="store_true", help="Valida la estructura del artefacto de ingesta")

    # wikictl promote
    promote_p = subparsers.add_parser("promote", help="Convierte análisis de ingesta en notas consolidadas")
    promote_p.add_argument("target", type=str, help="Slug o nombre de la fuente analizada")
    promote_p.add_argument("--dry-run", action="store_true", help="Muestra diffs y acciones sin escribir en disco")
    promote_p.add_argument("--apply", action="store_true", help="Aplica los cambios en el baúl")
    promote_p.add_argument("--commit", action="store_true", help="Crea automáticamente el commit descriptivo en Git")

    # wikictl research
    research_p = subparsers.add_parser("research", help="Crea el andamiaje para investigar un tema")
    research_p.add_argument("topic", type=str, help="Pregunta o tema a investigar")
    research_p.add_argument("--force", action="store_true", help="Sobrescribe si ya existe")

    # wikictl synthesize
    synth_p = subparsers.add_parser("synthesize", help="Crea el andamiaje de síntesis transversal")
    synth_p.add_argument("topic", type=str, help="Tema unificador de la síntesis")
    synth_p.add_argument("--sources", nargs="*", help="Títulos o notas existentes a vincular")
    synth_p.add_argument("--force", action="store_true", help="Sobrescribe si ya existe")

    # wikictl publish
    pub_p = subparsers.add_parser("publish", help="Adapta una nota consolidada para publicación externa")
    pub_p.add_argument("note", type=str, help="Título o ruta de la nota a publicar")
    pub_p.add_argument("--target", type=str, default="markdown", help="Destino (substack, markdown, newsletter, etc.)")

    # wikictl impact
    impact_p = subparsers.add_parser("impact", help="Muestra el árbol de impacto de dependencias de una nota")
    impact_p.add_argument("note", type=str, help="Título o ruta de la nota a analizar")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    commands_map = {
        "lint": execute_lint,
        "ingest": execute_ingest,
        "promote": execute_promote,
        "research": execute_research,
        "synthesize": execute_synthesize,
        "publish": execute_publish,
        "impact": execute_impact,
    }

    handler = commands_map.get(args.command)
    if not handler:
        parser.print_help()
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
