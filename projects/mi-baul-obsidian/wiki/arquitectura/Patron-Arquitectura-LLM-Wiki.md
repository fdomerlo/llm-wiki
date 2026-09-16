---
tipo: arquitectura
titulo: Patron de Arquitectura LLM-Wiki
estado: activo
ultima_actualizacion: 2026-09-16
fuentes:
  - "[[projects/mi-baul-obsidian/raw/01-principios-karpathy-llm-wiki|raw/01-principios-karpathy-llm-wiki.md]]"
tags:
  - mi-baul-obsidian
  - arquitectura
  - diseno-sistemas
alias:
  - Arquitectura LLM-Wiki
  - Patron Tripartito
certeza: alta
---

# Patron de Arquitectura LLM-Wiki

Patron estructural que organiza el conocimiento asistido por IA en tres capas con fronteras de seguridad y aislamiento claramente delimitadas.

## Estructura de Capas
1. **Capa Raw (`raw/`):** Almacen de evidencias externas. Solo lectura, inmutable.
2. **Capa Wiki (`wiki/`):** Grafo semantico procesado. Contiene notas atomicas categorizadas (`conceptos/`, `arquitectura/`, `entidades/`, `resumenes/`, `sintesis/`).
3. **Capa Proyectos (`projects/`):** Espacios aislados donde el conocimiento se especializa en contextos operativos independientes.

```mermaid
graph TD
    A["raw/ (Evidencias Crudas Inmutables)"] -->|"Ingesta y Destilacion"| B["wiki/resumenes/"]
    B -->|"Extraccion Atomica"| C["wiki/conceptos/"]
    B -->|"Decisiones de Diseno"| D["wiki/arquitectura/"]
    B -->|"Sistemas y Herramientas"| E["wiki/entidades/"]
    C <-->|"Wikilinks Bidireccionales"| D
    D <-->|"Wikilinks Bidireccionales"| E
    C <-->|"Wikilinks Bidireccionales"| E
    C & D & E -->|"Analisis Transversal"| F["wiki/sintesis/"]
```

## Beneficios
- Garantiza la [[Inmutabilidad-Raw]].
- Posibilita el [[Conocimiento-Acumulativo]].
- Se integra de forma natural en [[Obsidian]].
