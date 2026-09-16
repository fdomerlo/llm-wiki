---
tipo: concepto
titulo: Conocimiento Acumulativo
estado: activo
ultima_actualizacion: 2026-09-16
fuentes:
  - "[[projects/mi-baul-obsidian/raw/01-principios-karpathy-llm-wiki|raw/01-principios-karpathy-llm-wiki.md]]"
tags:
  - mi-baul-obsidian
  - epistemologia
  - aprendizaje
alias:
  - Cumulative Knowledge
  - Memoria Compuesta
certeza: alta
---

# Conocimiento Acumulativo

El **Conocimiento Acumulativo** es un paradigma de gestion documental donde cada nueva porcion de informacion no se almacena como un silo aislado, sino que se destila e integra activamente en un grafo de notas preexistente.

## Fundamentos
1. **Evitar la duplicacion:** Si un concepto ya esta definido, la nueva fuente aporta matices, ejemplos o contradicciones a la nota existente.
2. **Refactorizacion continua:** El repositorio funciona como una base de codigo viva sujeta a mejoras y simplificaciones periodicas.
3. **Atomicidad:** Cada nota aborda una unica idea o definicion, permitiendo composicion modular con otras notas mediante [[Obsidian|wikilinks]].

## Relacion con otros componentes
- Es soportado por el [[Patron-Arquitectura-LLM-Wiki]].
- Depende criticamente de la [[Inmutabilidad-Raw]] para mantener trazabilidad hacia la fuente primaria original.
- Se contrasta directamente frente a la recuperacion efimera en [[Comparativa-LLM-Wiki-vs-RAG]].
