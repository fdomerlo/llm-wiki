# Principios de LLM-Wiki segun Andrej Karpathy

**Fecha original:** Septiembre 2024  
**Fuente:** Reflexiones sobre memoria acumulativa en modelos de lenguaje y sistemas de segundo cerebro.  
**Autor:** Andrej Karpathy (sintesis de declaraciones publicas)  

---

## 1. El problema del chat efimero y RAG ingenuo

Los modelos de lenguaje actuales son extremadamente capaces en tareas de razonamiento local, pero sufren de un defecto fundamental: no acumulan conocimiento estructurado de forma autonoma. Cada sesion de chat comienza desde cero o depende de tecnicas de RAG (Retrieval-Augmented Generation) superficiales, donde fragmentos de texto crudo se recuperan mediante busqueda de similitud vectorial y se inyectan en el prompt.

Este enfoque presenta limitaciones claras:
- Fragmentacion del contexto: los chunks vectoriales pierden relaciones semanticas complejas y jerarquias.
- Ambiguedad y contradicciones: cuando dos fuentes se contradicen, el RAG suele promediar o confundir las respuestas sin un arbitraje critico.
- Falta de destilacion: el conocimiento crudo nunca se depura ni se transforma en sintesis legibles.

## 2. La propuesta de la Wiki Asistida por LLM

La solucion planteada propone un modelo alternativo: transformar al LLM en el bibliotecario y curador de un repositorio persistente de notas Markdown (idealmente en herramientas como Obsidian).

En lugar de consultar documentos crudos directamente:
1. **Fase de Ingesta:** Cada documento entrante se preserva intacto como evidencia historica. El LLM extrae conceptos atomicos, crea resúmenes y actualiza las notas existentes de la wiki.
2. **Grafo de Conocimiento Vivo:** Las notas se interconectan mediante enlaces bidireccionales (wikilinks). Si un nuevo paper introduce un termino conocido, la nota correspondiente se amplía en lugar de duplicarse.
3. **Mantenimiento y Jardineria:** Periodicamente el LLM revisa la wiki para encontrar contradicciones, enlaces rotos y sintetizar mapas tematicos de contenido.
4. **Respuestas Basadas en la Wiki:** Ante preguntas del usuario, el LLM consulta la wiki ya sintetizada, permitiendo respuestas mucho mas coherentes, verificables y libres de alucinaciones.
