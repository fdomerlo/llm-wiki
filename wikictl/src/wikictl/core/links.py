"""Manejo, extracción y normalización de enlaces internos tipo wikilinks de Obsidian."""

from __future__ import annotations
from dataclasses import dataclass
import re
import unicodedata

# Expresión regular para wikilinks Obsidian: !?[[target(#anchor)?(|alias)?]]
WIKILINK_REGEX = re.compile(
    r"(!)?\[\[([^\[\]\|\n]+?)(?:#([^\[\]\|\n]+?))?(?:\|([^\[\]\n]+?))?\]\]"
)


@dataclass(frozen=True)
class WikiLink:
    raw: str
    target: str
    anchor: str | None = None
    alias: str | None = None
    is_embed: bool = False

    @property
    def clean_target(self) -> str:
        """Devuelve el target sin extensión .md ni espacios extras."""
        t = self.target.strip()
        if t.lower().endswith(".md"):
            t = t[:-3]
        return t


def slugify(text: str) -> str:
    """Convierte un título a slug kebab-case para comparaciones y nombres de archivo."""
    # Normalizar caracteres unicode (ej: tildes)
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    # Reemplazar no alfanuméricos por guiones
    s = re.sub(r"[^\w\s-]", "", ascii_text).strip().lower()
    s = re.sub(r"[-\s]+", "-", s)
    return s


def extract_links(text: str) -> list[WikiLink]:
    """Extrae todos los wikilinks presentes en un texto (cuerpo o frontmatter)."""
    links: list[WikiLink] = []
    if not text:
        return links

    for match in WIKILINK_REGEX.finditer(text):
        is_embed = bool(match.group(1))
        target = match.group(2).strip()
        anchor = match.group(3).strip() if match.group(3) else None
        alias = match.group(4).strip() if match.group(4) else None
        raw = match.group(0)

        links.append(
            WikiLink(
                raw=raw,
                target=target,
                anchor=anchor,
                alias=alias,
                is_embed=is_embed,
            )
        )
    return links
