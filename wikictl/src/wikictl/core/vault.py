"""Abstracción y gestión del Baúl de Obsidian (Vault), indexación y resolución de enlaces."""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from wikictl.core.frontmatter import parse_frontmatter, join_document
from wikictl.core.links import WikiLink, extract_links, slugify


IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    ".work",
    "wikictl",
    "__pycache__",
    ".pytest_cache",
    ".obsidian",
    "node_modules",
}


@dataclass
class Note:
    rel_path: str
    abs_path: Path
    frontmatter: dict[str, Any]
    body: str
    raw_content: str
    outgoing_links: list[WikiLink] = field(default_factory=list)

    @property
    def title(self) -> str:
        fm_title = self.frontmatter.get("title")
        if fm_title:
            return str(fm_title).strip()
        return self.abs_path.stem

    @property
    def note_type(self) -> str | None:
        val = self.frontmatter.get("type")
        return str(val).strip() if val else None

    @property
    def status(self) -> str | None:
        val = self.frontmatter.get("status")
        return str(val).strip() if val else None

    @property
    def confidence(self) -> str | None:
        val = self.frontmatter.get("confidence")
        return str(val).strip() if val else None

    @property
    def is_volatile(self) -> bool:
        return bool(self.frontmatter.get("volatile", False))

    @property
    def review_after(self) -> str | None:
        val = self.frontmatter.get("review_after")
        return str(val).strip() if val else None

    @property
    def aliases(self) -> list[str]:
        raw_aliases = self.frontmatter.get("aliases")
        if isinstance(raw_aliases, list):
            return [str(a).strip() for a in raw_aliases if a]
        return []

    @property
    def tags(self) -> list[str]:
        raw_tags = self.frontmatter.get("tags")
        if isinstance(raw_tags, list):
            return [str(t).strip() for t in raw_tags if t]
        return []

    @property
    def sources(self) -> list[str]:
        raw_sources = self.frontmatter.get("sources")
        if isinstance(raw_sources, list):
            return [str(s).strip() for s in raw_sources if s]
        return []


class Vault:
    """Representa el baúl de Obsidian en disco, manteniendo un índice en memoria."""

    def __init__(self, root_dir: Path | str | None = None):
        self.root = self._find_root(root_dir)
        self.notes: dict[str, Note] = {}  # rel_path -> Note
        self.title_index: dict[str, str] = {}  # lower_title -> rel_path
        self.stem_index: dict[str, str] = {}  # lower_stem -> rel_path
        self.slug_index: dict[str, str] = {}  # slug -> rel_path
        self.alias_index: dict[str, str] = {}  # lower_alias -> rel_path
        self.backlinks: dict[str, set[str]] = {}  # target_rel_path -> set of source_rel_paths

    @staticmethod
    def _find_root(start_dir: Path | str | None) -> Path:
        start = Path(start_dir).resolve() if start_dir else Path.cwd().resolve()
        current = start
        while current != current.parent:
            if (current / "AGENTS.md").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return start

    def scan(self) -> Vault:
        """Escanea recursivamente el baúl e indexa todas las notas Markdown."""
        self.notes.clear()
        self.title_index.clear()
        self.stem_index.clear()
        self.slug_index.clear()
        self.alias_index.clear()
        self.backlinks.clear()

        for path in self.root.rglob("*.md"):
            # Filtrar carpetas ignoradas
            parts = path.relative_to(self.root).parts
            if any(part in IGNORE_DIRS for part in parts):
                continue

            rel_path = str(path.relative_to(self.root))
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            fm, body = parse_frontmatter(content)
            # Extraer links del cuerpo
            links = extract_links(body)
            # Extraer también links que estén en el frontmatter (sources, derived_from)
            for src in fm.get("sources", []) if isinstance(fm.get("sources"), list) else []:
                links.extend(extract_links(str(src)))
            for der in (
                fm.get("derived_from", []) if isinstance(fm.get("derived_from"), list) else []
            ):
                links.extend(extract_links(str(der)))

            note = Note(
                rel_path=rel_path,
                abs_path=path,
                frontmatter=fm,
                body=body,
                raw_content=content,
                outgoing_links=links,
            )
            self.notes[rel_path] = note

            # Índices
            title_lower = note.title.lower()
            self.title_index[title_lower] = rel_path
            self.stem_index[path.stem.lower()] = rel_path
            self.slug_index[slugify(note.title)] = rel_path
            self.slug_index[slugify(path.stem)] = rel_path

            for alias in note.aliases:
                self.alias_index[alias.lower()] = rel_path

        # Construir backlinks
        for src_path, note in self.notes.items():
            for link in note.outgoing_links:
                resolved = self.resolve_link(link.clean_target)
                if resolved:
                    self.backlinks.setdefault(resolved.rel_path, set()).add(src_path)

        return self

    def resolve_link(self, target: str) -> Note | None:
        """Resuelve el nombre de un wikilink a su objeto Note correspondiente."""
        clean = target.strip()
        if clean.lower().endswith(".md"):
            clean = clean[:-3]

        clean_lower = clean.lower()
        clean_slug = slugify(clean)

        # 1. Búsqueda por ruta exacta relativa
        target_path = clean if clean.endswith(".md") else f"{clean}.md"
        if target_path in self.notes:
            return self.notes[target_path]

        # 2. Búsqueda por nombre de archivo (stem)
        if clean_lower in self.stem_index:
            return self.notes[self.stem_index[clean_lower]]

        # 3. Búsqueda por título canónico
        if clean_lower in self.title_index:
            return self.notes[self.title_index[clean_lower]]

        # 4. Búsqueda por slug
        if clean_slug in self.slug_index:
            return self.notes[self.slug_index[clean_slug]]

        # 5. Búsqueda por alias
        if clean_lower in self.alias_index:
            return self.notes[self.alias_index[clean_lower]]

        return None

    def get_backlinks(self, rel_path: str) -> set[str]:
        """Devuelve el conjunto de rutas de notas que enlazan a la nota dada."""
        return self.backlinks.get(rel_path, set())

    def find_by_type(self, note_type: str) -> list[Note]:
        """Devuelve todas las notas de un tipo específico (concept, technology, etc.)."""
        return [n for n in self.notes.values() if n.note_type == note_type]

    def write_note(self, rel_path: str, frontmatter: dict[str, Any], body: str) -> Path:
        """Guarda o actualiza una nota de forma atómica en el baúl."""
        abs_path = self.root / rel_path
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        content = join_document(frontmatter, body)
        abs_path.write_text(content, encoding="utf-8")
        return abs_path
