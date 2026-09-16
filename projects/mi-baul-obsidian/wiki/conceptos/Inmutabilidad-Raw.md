---
tipo: concepto
titulo: Inmutabilidad de Raw
estado: activo
ultima_actualizacion: 2026-09-16
fuentes:
  - "[[projects/mi-baul-obsidian/raw/01-principios-karpathy-llm-wiki|raw/01-principios-karpathy-llm-wiki.md]]"
tags:
  - mi-baul-obsidian
  - seguridad
  - gobernanza
alias:
  - Inmutabilidad de Evidencia
  - Raw Immutability
certeza: alta
---

# Inmutabilidad de Raw

La **Inmutabilidad de Raw** es la regla operacional fundamental que prohibe la modificacion, eliminacion o truncamiento de cualquier archivo dentro de las carpetas `raw/`.

## Proposito Epistemologico
- **Trazabilidad:** Cualquier afirmacion en la wiki debe poder contrastarse contra el texto literal original.
- **Auditoria historica:** Si un modelo sintetiza erroneamente un punto, la evidencia intacta permite re-evaluar la extraccion sin perdida de datos.
- **Separacion de responsabilidades:** `raw/` representa "lo que otros dijeron", mientras que `wiki/` representa "lo que nosotros sabemos y organizamos".

## Relaciones
- Permite construir un sistema de [[Conocimiento-Acumulativo]] libre de distorsiones progresivas.
- Es la base documental del [[Patron-Arquitectura-LLM-Wiki]].
