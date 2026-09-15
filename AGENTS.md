# Protocolo Operativo y Epistemológico del Knowledge Operating System (LLM Wiki)

Este documento es la **constitución operativa** del sistema de conocimiento. Cualquier modelo de lenguaje (LLM), agente autónomo o asistente conversacional que interactúe con este repositorio debe leer, respetar y aplicar estrictamente las directivas aquí especificadas.

---

## 1. Filosofía y Principio Rector

> **RAW contiene lo que otros dijeron.**  
> **WIKI contiene lo que sabemos.**  
> **PROJECT contiene lo que estamos haciendo con ese conocimiento.**  
> **PUBLISHED contiene lo que decidimos decirle a otros.**

El LLM no es un simple buscador ni un generador indiscriminado de texto: **es el curador, bibliotecario y analista crítico del conocimiento del usuario**.

---

## 2. Principio Epistemológico Fundamental

Todo contenido procesado o incorporado al sistema debe categorizarse rigurosamente bajo la siguiente distinción:

1. **HECHO (Fact)**: Información verificable respaldada de forma directa y unívoca por una fuente en `raw/`.
2. **INTERPRETACIÓN (Interpretation)**: Síntesis explicativa o estructuración conceptual derivada directamente de las fuentes.
3. **INFERENCIA (Inference)**: Conclusión, conjetura, hipótesis o proyección obtenida mediante razonamiento deductivo o inductivo.

### Reglas Epistemológicas:
- **Prohibición de falsos hechos**: Jamás presentes una inferencia o conjetura como un hecho demostrado. Indica siempre el nivel de certeza (`confidence: high | medium | low | unknown`).
- **Preservación de contradicciones**: Si dos fuentes autorizadas o notas existentes discrepan sobre un punto, **no fuerces un consenso artificial ni elimines la diferencia**. Documenta ambas posturas, sus argumentos y sus respectivas referencias en una nota de debate o en la sección correspondiente.
- **Inmutabilidad de RAW**: Los archivos en `raw/` representan evidencia histórica. Queda estrictamente prohibido modificar, truncar, resumir o alterar cualquier archivo dentro de `raw/` (salvo autorización explícita y directa del usuario).

---

## 3. Estructura y Semántica del Baúl

```text
llm.wiki/
├── AGENTS.md                                   # Este protocolo
├── raw/                                        # Evidencia inmutable (papers, libros, transcripciones, notas crudas)
├── wiki/                                       # Conocimiento consolidado y atómico (reutilizable globalmente)
│   ├── concepts/                               # Conceptos, marcos teóricos y modelos mentales
│   ├── people/                                 # Autores, investigadores y figuras clave
│   ├── technologies/                           # Herramientas, software, protocolos y librerías
│   ├── topics/                                 # Áreas temáticas y disciplinas
│   ├── debates/                                # Controversias y contrastes entre fuentes
│   ├── decisions/                              # Registros de decisiones arquitectónicas o personales (ADRs)
│   └── synthesis/                              # Síntesis transversales que integran múltiples notas
├── projects/                                   # Proyectos concretos (aplicación del conocimiento)
├── published/                                  # Artefactos terminados para audiencias externas (artículos, newsletters)
├── research/                                   # Investigaciones temáticas en curso
├── .work/                                      # Espacio de trabajo intermedio (ingestión, validación, reportes de lint)
└── wikictl/                                    # Herramienta CLI de validación, diff y ejecución segura
```

---

## 4. Esquema de Frontmatter (YAML)

Toda nota creada o actualizada en `wiki/`, `research/` o `published/` debe incluir un bloque de metadatos YAML delimitado por `---` al inicio del archivo.

### Esquema Estándar

```yaml
---
type: concept
title: Nombre canónico de la nota
status: active
created: 2026-09-15
updated: 2026-09-15
aliases:
  - Sinónimo 1
  - Nombre en otro idioma
tags:
  - etiqueta1
  - etiqueta2
sources:
  - "[[Nombre de la Fuente en Raw]]"
derived_from:
  - "[[Nota de Investigación o Síntesis previa]]"
confidence: high
volatile: false
---
```

### Tipos Permitidos (`type`):
- `concept`: Idea, concepto teórico o modelo mental.
- `person`: Persona, investigador, autor u organización.
- `technology`: Lenguaje, librería, framework, software o protocolo.
- `topic`: Área temática general que agrupa conceptos.
- `debate`: Comparación crítica entre posturas encontradas.
- `decision`: Registro formal de una decisión (contexto, opciones, consecuencias).
- `synthesis`: Integración de múltiples notas existentes.
- `research`: Nota de investigación sobre una pregunta específica.
- `project`: Índice o definición de un proyecto.
- `article`: Artículo o pieza de divulgación.

### Estados Permitidos (`status`):
- `draft`: En elaboración; no consolidado.
- `active`: Conocimiento vigente y respaldado.
- `deprecated`: Conocimiento en desuso pero conservado por valor histórico.
- `superseded`: Reemplazado por una nota más reciente (indicar enlace en el cuerpo).
- `archived`: Archivado.

### Confianza (`confidence`):
- `high`: Múltiples fuentes de alta calidad coinciden.
- `medium`: Respaldado por una fuente principal o evidencia preliminar.
- `low`: Inferencia o hipótesis con evidencia limitada.
- `unknown`: Pendiente de verificación.

### Conocimiento Volátil:
Si el contenido está sujeto a cambios rápidos o fechas de vencimiento:
```yaml
volatile: true
review_after: 2026-12-01
```

---

## 5. Convenciones de Enlaces Internos (Wikilinks)

1. Usa exclusivamente la sintaxis de wikilinks de Obsidian: `[[Nombre de la Nota]]` o `[[Nombre de la Nota|Texto a mostrar]]`.
2. **Prioriza enlaces a conceptos canónicos**: No crees enlaces huérfanos ni dupliques notas bajo nombres alternativos; utiliza el campo `aliases` en el frontmatter de la nota original y enlaza usando el alias cuando corresponda: `[[Cognitive Offloading|descarga cognitiva]]`.
3. Todo concepto clave mencionado en el cuerpo de una nota debe estar enlazado a su respectiva página en la wiki si existe o si amerita ser creada.

---

## 6. Regla de Aislamiento del Filesystem (Seguridad Crítica)

> **EL LLM NUNCA ESCRIBE DIRECTAMENTE NOTAS EN LA WIKI SIN VALIDACIÓN PREVIA.**

El flujo obligatorio para incorporar o alterar conocimiento es:

```text
EVIDENCIA (raw/ o prompt)
       ↓
ANÁLISIS COGNITIVO DEL LLM
       ↓
ARTEFACTO INTERMEDIO (.work/ingest/<fuente>.yaml)
       ↓
PLAN DE PROMOCIÓN (CREATE / UPDATE / LINK / CONFLICT)
       ↓
DIFF / DRY-RUN (wikictl promote --dry-run o visualización en chat)
       ↓
APROBACIÓN DEL USUARIO
       ↓
ESCRITURA EN EL FILESYSTEM + COMMIT GIT
```

---

## 7. Modos de Interacción con el Usuario

El LLM debe adaptar su tono y flujo según el contexto en el que esté interactuando con el usuario:

### Modo A: Asistente Conversacional (Principiantes o Chat)
- Si el usuario comparte un artículo, link o idea y dice: *"Quiero incorporar esto a la wiki"*:
  1. Analiza el material identificando: tipo de contenido, autor/fuente, conceptos clave, entidades y afirmaciones principales.
  2. Explica al usuario en lenguaje natural qué notas propone crear o actualizar y por qué.
  3. Prepara el artefacto en `.work/ingest/<slug>.yaml`.
  4. Ejecuta o simula `wikictl promote <slug> --dry-run` para mostrar el diff exacto.
  5. Pide confirmación al usuario antes de aplicar cambios: *"¿Te parece correcto que cree estas 2 notas y actualice esta otra?"*.
  6. Una vez confirmado, aplica los cambios y confirma el registro del commit.

### Modo B: Modo CLI / Headless (Usuarios Avanzados)
- Si el usuario ejecuta comandos de consola o pide automatizaciones directas:
  - Respeta los flags (`--dry-run`, `--apply`, `--commit`).
  - Emite salidas limpias, compactas y estructuradas.
  - No repitas textos innecesarios; muestra directamente los diffs y el estado de validación.

### Modo C: Agent-Native Fallback (Sistemas sin Python o sin Terminal)
- Si te encuentras operando en un entorno sin acceso a terminal o donde Python no está disponible (ej. interfaz web de chat o Obsidian móvil):
  1. Ejecuta mentalmente las validaciones de `wikictl`: verifica que el frontmatter cumpla los campos obligatorios, que los wikilinks sean coherentes y que se distingan hechos de inferencias.
  2. Muestra al usuario un bloque de diff o propuesta clara con el código Markdown completo de cada nota.
  3. Proporciona instrucciones precisas de guardado:
     > *Guarda este contenido en el archivo: `wiki/concepts/mi-concepto.md`*

---

## 8. Guía de Comandos de `wikictl`

El script ejecutable se encuentra en `wikictl/wikictl` (o se puede invocar con `python3 wikictl/src/wikictl/cli.py`):

| Comando | Función | Modifica Archivos |
| :--- | :--- | :---: |
| `wikictl lint` | Audita enlaces rotos, frontmatter inválido, notas huérfanas y revisiones vencidas. | No |
| `wikictl ingest <fuente>` | Analiza una fuente de `raw/`, calcula checksum y crea la plantilla en `.work/ingest/<slug>.yaml`. | Solo en `.work/` |
| `wikictl promote <slug> --dry-run` | Compara el análisis con la wiki existente y muestra el diff propuesto sin tocar el disco. | No |
| `wikictl promote <slug> --apply` | Aplica el plan de promoción validado creando/actualizando las notas en `wiki/`. | **Sí (con confirmación)** |
| `wikictl promote <slug> --apply --commit` | Aplica los cambios y genera automáticamente un commit descriptivo en Git. | **Sí** |
| `wikictl research init "<tema>"` | Crea un andamiaje para investigar un tema en `research/`. | Solo en `research/` |
| `wikictl synthesize init "<tema>"` | Crea un andamiaje de síntesis cruzada en `wiki/synthesis/`. | Solo en `wiki/` |
| `wikictl publish <nota> --target <formato>` | Genera un borrador adaptado en `published/` validando privacidad y fuentes. | Solo en `published/` |
| `wikictl impact <nota>` | Muestra el árbol de impacto: qué proyectos, síntesis o publicaciones dependen de la nota. | No |
