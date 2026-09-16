---
tipo: entidad
titulo: Obsidian
estado: activo
ultima_actualizacion: 2026-09-16
fuentes:
  - "[[projects/mi-baul-obsidian/raw/01-principios-karpathy-llm-wiki|raw/01-principios-karpathy-llm-wiki.md]]"
tags:
  - mi-baul-obsidian
  - herramientas
  - software
alias:
  - Obsidian.md
certeza: alta
---

# Obsidian

**Obsidian** es una aplicacion de base de conocimiento y toma de notas basada en archivos de texto plano Markdown almacenados localmente en el sistema de archivos (*local-first*).

## Caracteristicas Clave en la Arquitectura LLM-Wiki
- **Archivos planos:** Almacenamiento directo en disco, sin bases de datos propietarias, permitiendo inspeccion y modificacion directa mediante agentes LLM y herramientas de control de versiones (Git).
- **Enlaces bidireccionales:** Soporte nativo para enlaces `[[wikilinks]]` y grafos de relacion.
- **Ecosistema extensible:** Complementos esenciales como **Dataview** (para tableros dinamicos e indices estructurados) y **Templater** (para inicializacion parametrica de proyectos y notas).

## Relaciones
- Herramienta host para el [[Patron-Arquitectura-LLM-Wiki]].
- Facilita la navegacion visual del [[Conocimiento-Acumulativo]].
