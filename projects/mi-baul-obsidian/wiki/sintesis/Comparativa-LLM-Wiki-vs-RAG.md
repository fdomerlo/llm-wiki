---
tipo: sintesis
titulo: Comparativa Tecnica LLM-Wiki vs RAG Tradicional
estado: activo
ultima_actualizacion: 2026-09-16
fuentes:
  - "[[projects/mi-baul-obsidian/raw/01-principios-karpathy-llm-wiki|raw/01-principios-karpathy-llm-wiki.md]]"
tags:
  - mi-baul-obsidian
  - sintesis
  - comparativa
proyectos_relacionados:
  - "[[projects/mi-baul-obsidian/index|mi-baul-obsidian]]"
certeza: alta
---

# Comparativa Tecnica: LLM-Wiki vs. RAG Tradicional

## Contexto y Pregunta Guia
¿Cuales son las ventajas, desventajas y trade-offs operativos entre el enfoque clasico de RAG (fragmentacion vectorial de documentos en tiempo de consulta) y la arquitectura LLM-Wiki (curaduria continua y compilacion de notas en Obsidian)?

## Matriz Comparativa

| Criterio | RAG Tradicional (Vectorial) | LLM-Wiki (Curaduria Documental) |
| :--- | :--- | :--- |
| **Representacion del Conocimiento** | Chunks de texto plano indexados como embeddings vectoriales. | Grafo estructurado de archivos Markdown atomicos con [[Obsidian|wikilinks]]. |
| **Costo en Tiempo de Consulta** | Alto (busqueda vectorial + inyeccion de ventanas extensas de contexto). | Bajo (recuperacion directa de notas de sintesis y conceptos atomicos pertinentes). |
| **Manejo de Contradicciones** | Deficiente (el modelo promedia estadisticamente chunks contradictorios). | Riguroso (se documenta explicitamente el conflicto y el contexto de cada decision). |
| **Intervencion y Legibilidad Humana** | Opaca (caja negra en la base vectorial, dificil de auditar manualmente). | Transparente (archivos legibles en Obsidian, versionables con Git). |
| **Costo de Ingesta** | Rapido y automatizado (solo calcular embeddings). | Requiere razonamiento del LLM para clasificar, resumir y vincular notas. |
| **Persistencia del Aprendizaje** | Ninguna (las respuestas del chat desaparecen tras la sesion). | Alta ([[Conocimiento-Acumulativo]], las respuestas complejas se transforman en sintesis). |

## Conclusiones e Inferencias
- **Convergencia:** Ambos sistemas se benefician de la [[Inmutabilidad-Raw]] para mantener evidencia fidedigna.
- *Inferencia:* Para bases de conocimiento personales, tecnicas o de arquitectura de software, el enfoque LLM-Wiki supera sustancialmente al RAG ingenuo gracias a la trazabilidad y la eliminacion de alucinaciones por promediacion contextual.
