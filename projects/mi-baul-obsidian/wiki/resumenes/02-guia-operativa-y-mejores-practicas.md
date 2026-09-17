---
tipo: resumen_fuente
titulo: Resumen - Guia Operativa de Campo y Buenas Practicas para LLM-Wiki
estado: activo
ultima_actualizacion: 2026-09-17
fuentes:
  - "[[projects/mi-baul-obsidian/raw/02-guia-operativa-y-mejores-practicas|raw/02-guia-operativa-y-mejores-practicas.md]]"
tags:
  - mi-baul-obsidian
  - resumen
  - manual-usuario
  - buenas-practicas
certeza: alta
conflicto_con: []
motivo_conflicto: ""
---

# Resumen: Guia Operativa de Campo y Buenas Practicas

## Resumen Ejecutivo
Manual operacional que establece el protocolo paso a paso para inicializar y operar un baul LLM-Wiki en Obsidian. Proporciona instrucciones de arranque en 3 pasos, catalogo de prompts para agentes locales y globales, y cinco reglas de oro para la curaduria del grafo de conocimiento.

## Puntos Clave Extraidos
- **Metabolismo en 5 fases:** Captura (`raw/`) -> Destilacion (`resumenes/` y notas atomicas) -> Interconexion (`[[wikilinks]]`) -> Consulta anclada -> Jardineria periodica.
- **Configuracion Minima Requerida:** Obsidian + Plugins Dataview (con JS y consultas inline) + Templater (apuntando a `schema/`).
- **Prompts Estandarizados:** Formulas explicitas para invocar roles sin ambiguedad (Ingesta, Consultas, Sintesis, Jardineria, Auditoria).
- **Criterio de Atomicidad:** 1 idea por nota, maximo 300-400 palabras; evolucionar notas existentes en vez de duplicar.

## Conceptos y Arquitectura Derivados
- [[Guia-Inicio-Rapido]]: Procedimiento de arranque en 3 pasos para nuevos usuarios.
- [[Buenas-Practicas-Curaduria]]: Reglas operativas, atomicidad y catalogo de prompts.
- [[Flujo-Operativo-Diario]]: El ciclo metabolico diario de documentacion asistida por IA.
