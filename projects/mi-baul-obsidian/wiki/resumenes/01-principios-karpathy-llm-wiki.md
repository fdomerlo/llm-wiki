---
tipo: resumen_fuente
titulo: Resumen - Principios de LLM-Wiki segun Andrej Karpathy
estado: activo
ultima_actualizacion: 2026-09-16
fuentes:
  - "[[projects/mi-baul-obsidian/raw/01-principios-karpathy-llm-wiki|raw/01-principios-karpathy-llm-wiki.md]]"
tags:
  - mi-baul-obsidian
  - resumen
  - arquitectura
certeza: alta
---

# Resumen: Principios de LLM-Wiki segun Andrej Karpathy

## Resumen Ejecutivo
Propuesta de Andrej Karpathy para transformar el uso de modelos de lenguaje desde chats efimeros o RAG ingenuo hacia sistemas de conocimiento acumulativo organizados como Wikis de notas Markdown interconectadas. El LLM opera como curador, bibliotecario y sintetizador continuo del grafo.

## Puntos Clave Extraidos
- **Falla del RAG tradicional:** La busqueda vectorial fragmentada pierde relaciones jerarquicas y promedia contradicciones en lugar de documentarlas.
- **Doble capa de conocimiento:** Separacion tajante entre fuentes crudas inmutables y notas destiladas conectadas.
- **Grafo vivo:** Los nuevos documentos actualizan notas atomicas existentes en vez de amontonar archivos duplicados.
- **Jardineria documental:** Labor constante de auditoria, deteccion de vacios y eliminacion de enlaces rotos.

## Evidencia y Citas de Soporte
> *"Transformar al LLM en el bibliotecario y curador de un repositorio persistente de notas Markdown... Si un nuevo paper introduce un termino conocido, la nota correspondiente se amplia en lugar de duplicarse."*

## Conceptos y Entidades Derivadas
- [[Conocimiento-Acumulativo]]: Modelo mental de persistencia y sintesis iterativa.
- [[Inmutabilidad-Raw]]: Principio de preservacion absoluta de fuentes externas.
- [[Patron-Arquitectura-LLM-Wiki]]: Arquitectura de 3 capas (raw, wiki, proyectos).
- [[Obsidian]]: Entorno local basado en archivos Markdown y enlaces bidireccionales.
- [[Comparativa-LLM-Wiki-vs-RAG]]: Analisis de trade-offs tecnicos entre ambos paradigmas.
