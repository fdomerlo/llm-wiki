"""Validador determinístico de salud e integridad para el Knowledge Operating System."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

from wikictl.core.vault import Vault, Note

ALLOWED_TYPES = {
    "source",
    "concept",
    "person",
    "organization",
    "technology",
    "topic",
    "idea",
    "question",
    "decision",
    "project",
    "article",
    "note",
    "synthesis",
    "comparison",
    "research",
    "debate",
}

ALLOWED_STATUSES = {
    "draft",
    "active",
    "deprecated",
    "superseded",
    "archived",
}

ALLOWED_CONFIDENCE = {
    "high",
    "medium",
    "low",
    "unknown",
}


@dataclass(frozen=True)
class LintIssue:
    level: Literal["ERROR", "WARNING", "INFO"]
    category: str
    file: str
    message: str
    line: int | None = None

    def __str__(self) -> str:
        loc = f"{self.file}:{self.line}" if self.line else self.file
        return f"[{self.level}] ({self.category}) {loc}: {self.message}"


def lint_note(note: Note, vault: Vault) -> list[LintIssue]:
    """Ejecuta todas las reglas determinísticas sobre una única nota."""
    issues: list[LintIssue] = []

    # Archivos raíz (AGENTS.md, README.md, etc.), documentación en docs/ y evidencias en raw/ están exentos
    is_root_file = "/" not in note.rel_path
    if is_root_file or note.rel_path.startswith("raw/") or note.rel_path.startswith("docs/"):
        return issues

    fm = note.frontmatter

    # 1. Validación de Frontmatter obligatorio
    if not fm:
        issues.append(
            LintIssue(
                level="ERROR",
                category="schema",
                file=note.rel_path,
                message="Falta el bloque frontmatter YAML al inicio de la nota.",
            )
        )
        return issues

    # 2. Campos obligatorios: type, title, status
    if "type" not in fm or not fm["type"]:
        issues.append(
            LintIssue(
                level="ERROR",
                category="schema",
                file=note.rel_path,
                message="Campo 'type' obligatorio ausente o vacío en frontmatter.",
            )
        )
    elif str(fm["type"]).lower() not in ALLOWED_TYPES:
        issues.append(
            LintIssue(
                level="ERROR",
                category="schema",
                file=note.rel_path,
                message=f"Tipo '{fm['type']}' no reconocido. Tipos válidos: {', '.join(sorted(ALLOWED_TYPES))}.",
            )
        )

    if "title" not in fm or not fm["title"]:
        issues.append(
            LintIssue(
                level="ERROR",
                category="schema",
                file=note.rel_path,
                message="Campo 'title' obligatorio ausente o vacío en frontmatter.",
            )
        )

    if "status" not in fm or not fm["status"]:
        issues.append(
            LintIssue(
                level="ERROR",
                category="schema",
                file=note.rel_path,
                message="Campo 'status' obligatorio ausente o vacío en frontmatter.",
            )
        )
    elif str(fm["status"]).lower() not in ALLOWED_STATUSES:
        issues.append(
            LintIssue(
                level="ERROR",
                category="schema",
                file=note.rel_path,
                message=f"Estado '{fm['status']}' inválido. Estados permitidos: {', '.join(sorted(ALLOWED_STATUSES))}.",
            )
        )

    # 3. Confianza (opcional pero si existe debe ser válida)
    if "confidence" in fm and fm["confidence"]:
        if str(fm["confidence"]).lower() not in ALLOWED_CONFIDENCE:
            issues.append(
                LintIssue(
                    level="WARNING",
                    category="schema",
                    file=note.rel_path,
                    message=f"Nivel de confianza '{fm['confidence']}' no válido. Permitidos: {', '.join(sorted(ALLOWED_CONFIDENCE))}.",
                )
            )

    # 4. Volatilidad y obsolescencia
    if fm.get("volatile") is True:
        review_after = fm.get("review_after")
        if not review_after:
            issues.append(
                LintIssue(
                    level="WARNING",
                    category="obsolescence",
                    file=note.rel_path,
                    message="Nota marcada como 'volatile: true' pero sin fecha 'review_after'.",
                )
            )
        else:
            try:
                target_date = date.fromisoformat(str(review_after).strip())
                if date.today() > target_date:
                    issues.append(
                        LintIssue(
                            level="WARNING",
                            category="obsolescence",
                            file=note.rel_path,
                            message=f"Fecha de revisión expirada ({target_date}). Requiere revisión de vigencia.",
                        )
                    )
            except ValueError:
                issues.append(
                    LintIssue(
                        level="ERROR",
                        category="schema",
                        file=note.rel_path,
                        message=f"Formato de fecha inválido en 'review_after': '{review_after}'. Use YYYY-MM-DD.",
                    )
                )

    # 5. Enlaces rotos (broken links)
    for link in note.outgoing_links:
        # Si es un archivo de imagen o adjunto existente en el repo, omitir
        clean = link.clean_target
        if any(clean.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".pdf", ".svg"]):
            # Comprobar si el archivo físico existe
            if (vault.root / clean).exists():
                continue

        resolved = vault.resolve_link(clean)
        if not resolved:
            # Comprobar si existe en raw/ como archivo crudo
            raw_target = vault.root / "raw" / clean
            raw_target_md = vault.root / "raw" / f"{clean}.md"
            if raw_target.exists() or raw_target_md.exists():
                continue

            issues.append(
                LintIssue(
                    level="ERROR",
                    category="broken_link",
                    file=note.rel_path,
                    message=f"Enlace roto: [[{link.target}]] no resuelve a ninguna nota existente.",
                )
            )

    # 6. Notas huérfanas en wiki/
    if note.rel_path.startswith("wiki/"):
        backlinks = vault.get_backlinks(note.rel_path)
        valid_outgoing = [l for l in note.outgoing_links if not l.is_embed]
        if not backlinks and not valid_outgoing:
            issues.append(
                LintIssue(
                    level="WARNING",
                    category="orphan",
                    file=note.rel_path,
                    message="Nota huérfana en wiki: no tiene enlaces entrantes ni salientes.",
                )
            )

    # 7. Trazabilidad de fuentes para conceptos consolidados
    if note.note_type in ("concept", "synthesis", "debate"):
        sources = fm.get("sources")
        derived_from = fm.get("derived_from")
        has_sources = bool(sources and isinstance(sources, list) and len(sources) > 0)
        has_derived = bool(
            derived_from and isinstance(derived_from, list) and len(derived_from) > 0
        )
        if not has_sources and not has_derived:
            issues.append(
                LintIssue(
                    level="INFO",
                    category="sources",
                    file=note.rel_path,
                    message="Nota de conocimiento sin 'sources' ni 'derived_from' declarados.",
                )
            )

    return issues


def lint_vault(vault: Vault, path_filter: str | None = None) -> list[LintIssue]:
    """Audita todas las notas del Vault de forma determinística."""
    all_issues: list[LintIssue] = []

    for rel_path, note in sorted(vault.notes.items()):
        if path_filter and not rel_path.startswith(path_filter):
            continue
        issues = lint_note(note, vault)
        all_issues.extend(issues)

    return all_issues
