"""Parser y serializador de Frontmatter YAML para Obsidian usando biblioteca estándar de Python."""

from __future__ import annotations
import re
from typing import Any


def _parse_scalar(val: str) -> Any:
    val = val.strip()
    if not val:
        return ""
    # Quoted string
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    # Boolean
    lower = val.lower()
    if lower in ("true", "yes"):
        return True
    if lower in ("false", "no"):
        return False
    if lower in ("null", "none", "~"):
        return None
    # Integer
    if re.fullmatch(r"[-+]?\d+", val):
        try:
            return int(val)
        except ValueError:
            pass
    # Float
    if re.fullmatch(r"[-+]?\d+\.\d+", val):
        try:
            return float(val)
        except ValueError:
            pass
    # Inline list: [a, b, c]
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        items = [s.strip() for s in re.split(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", inner)]
        return [_parse_scalar(it) for it in items if it]
    return val


def parse_yaml_subset(yaml_str: str) -> dict[str, Any]:
    """Parsea un subconjunto estándar de YAML comúnmente usado en frontmatter de Obsidian y artefactos de ingesta."""
    result: dict[str, Any] = {}
    lines = yaml_str.splitlines()
    current_key: str | None = None
    current_list: list[Any] | None = None
    current_dict_in_list: dict[str, Any] | None = None

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        # Comentario o línea vacía
        if not stripped or stripped.startswith("#"):
            continue

        # Elemento de lista con par clave-valor: '  - clave: valor'
        list_kv_match = re.match(r"^\s*-\s+([a-zA-Z0-9_\-]+)\s*:\s*(.*)$", line)
        if list_kv_match and current_key:
            subk = list_kv_match.group(1).strip()
            subv = list_kv_match.group(2).strip()
            current_dict_in_list = {subk: _parse_scalar(subv)}
            if current_list is None:
                current_list = []
                result[current_key] = current_list
            current_list.append(current_dict_in_list)
            continue

        # Continuación de pares dentro de un diccionario de lista: '    clave: valor'
        sub_kv_match = re.match(r"^\s{3,}([a-zA-Z0-9_\-]+)\s*:\s*(.*)$", line)
        if sub_kv_match and current_dict_in_list is not None:
            subk = sub_kv_match.group(1).strip()
            subv = sub_kv_match.group(2).strip()
            current_dict_in_list[subk] = _parse_scalar(subv)
            continue

        # Elemento de lista escalar: '  - valor' o '- valor'
        list_match = re.match(r"^\s*-\s+(.*)$", line)
        if list_match and current_key:
            item_val = list_match.group(1).strip()
            parsed_item = _parse_scalar(item_val)
            if current_list is None:
                current_list = []
                result[current_key] = current_list
            current_list.append(parsed_item)
            current_dict_in_list = None
            continue

        # Par clave-valor de nivel superior: 'clave: valor' o 'clave:'
        kv_match = re.match(r"^([a-zA-Z0-9_\-]+)\s*:\s*(.*)$", line)
        if kv_match:
            key = kv_match.group(1).strip()
            rest = kv_match.group(2).strip()

            current_key = key
            current_list = None
            current_dict_in_list = None

            if not rest:
                result[key] = []
                current_list = result[key]
            else:
                parsed_val = _parse_scalar(rest)
                result[key] = parsed_val
            continue

    return result


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Separa el frontmatter YAML del cuerpo de una nota Markdown.

    Devuelve (frontmatter_dict, body_markdown).
    Si no tiene frontmatter, devuelve ({}, content).
    """
    if not content.startswith("---"):
        return {}, content

    # Buscar el segundo '---' al inicio de una línea
    match = re.search(r"^---\s*$", content[3:], re.MULTILINE)
    if not match:
        return {}, content

    end_pos = match.start() + 3
    yaml_text = content[3:end_pos].strip()
    body = content[match.end() + 3 :]
    if body.startswith("\r\n"):
        body = body[2:]
    elif body.startswith("\n"):
        body = body[1:]

    parsed_data = parse_yaml_subset(yaml_text)
    return parsed_data, body


def dump_yaml_subset(data: dict[str, Any]) -> str:
    """Serializa un diccionario en formato YAML limpio compatible con Obsidian."""
    lines: list[str] = []

    # Orden preferido canónico para legibilidad en Obsidian
    priority_keys = [
        "type",
        "title",
        "status",
        "created",
        "updated",
        "aliases",
        "tags",
        "sources",
        "derived_from",
        "confidence",
        "volatile",
        "review_after",
    ]

    all_keys = list(data.keys())
    ordered_keys = [k for k in priority_keys if k in all_keys] + [
        k for k in all_keys if k not in priority_keys
    ]

    for key in ordered_keys:
        val = data[key]
        if isinstance(val, list):
            if not val:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in val:
                    if isinstance(item, dict):
                        first = True
                        for subk, subv in item.items():
                            if isinstance(subv, list):
                                subv_str = "[" + ", ".join(f'"{x}"' if ":" in str(x) else str(x) for x in subv) + "]"
                            elif isinstance(subv, bool):
                                subv_str = "true" if subv else "false"
                            elif subv is None:
                                subv_str = "~"
                            else:
                                subv_str = str(subv).strip()
                                if ":" in subv_str or "[" in subv_str or '"' in subv_str or "\n" in subv_str:
                                    clean_subv = subv_str.replace('"', '\\"')
                                    subv_str = f'"{clean_subv}"'
                            if first:
                                lines.append(f"  - {subk}: {subv_str}")
                                first = False
                            else:
                                lines.append(f"    {subk}: {subv_str}")
                    else:
                        item_str = str(item)
                        if "[[" in item_str or ":" in item_str or "#" in item_str:
                            lines.append(f'  - "{item_str}"')
                        else:
                            lines.append(f"  - {item_str}")
        elif isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        elif val is None:
            lines.append(f"{key}: ~")
        elif isinstance(val, (int, float)):
            lines.append(f"{key}: {val}")
        else:
            val_str = str(val).strip()
            if ":" in val_str or "[" in val_str or '"' in val_str:
                clean_val = val_str.replace('"', '\\"')
                lines.append(f'{key}: "{clean_val}"')
            else:
                lines.append(f"{key}: {val_str}")

    return "\n".join(lines)


def join_document(frontmatter: dict[str, Any], body: str) -> str:
    """Une el frontmatter YAML y el cuerpo en un documento Markdown."""
    if not frontmatter:
        return body
    yaml_str = dump_yaml_subset(frontmatter)
    body_clean = body.lstrip("\r\n")
    return f"---\n{yaml_str}\n---\n\n{body_clean}"
