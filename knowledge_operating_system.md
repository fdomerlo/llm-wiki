# LLM Wiki / Knowledge Operating System

## 1. Objetivo

Construir sobre un Baúl de conocimiento existente en **Obsidian + Markdown + YAML + enlaces internos**, incorporando una arquitectura tipo **LLM Wiki** inspirada en la propuesta de Andrej Karpathy.

La idea central:

> El LLM no solamente consulta el conocimiento: ayuda a construirlo, relacionarlo, mantenerlo, investigarlo y convertirlo en productos derivados.

El sistema debe ser **agnóstico del proveedor de LLM** y mantener el conocimiento en archivos Markdown versionables con Git.

No se pretende reemplazar Obsidian ni adoptar literalmente la estructura propuesta por Karpathy.

---

# 2. Arquitectura conceptual

El conocimiento sigue este flujo:

```text
RAW
 ↓
WIKI
 ↓
PROJECT
 ↓
PUBLISHED
```

Pero no es un pipeline irreversible. Existe retroalimentación:

```text
RAW → WIKI → PROJECT → PUBLISHED
       ↑                    │
       └── feedback/errors ─┘
```

### RAW

Material original o adquirido:

- papers
- libros
- artículos
- documentación
- transcripciones
- datasets
- repositorios
- notas sin procesar

**RAW = evidencia.**

Nunca modificar fuentes originales salvo autorización explícita.

### WIKI

Conocimiento consolidado y reutilizable:

- conceptos
- personas
- tecnologías
- teorías
- metodologías
- relaciones
- comparaciones
- síntesis

**WIKI = conocimiento.**

Debe conservar trazabilidad hacia las fuentes.

### PROJECT

Aplicación del conocimiento a un objetivo concreto:

- software
- investigación
- infraestructura
- artículos
- cursos
- productos
- experimentos

**PROJECT = aplicación.**

Debe reutilizar conocimiento global mediante enlaces en lugar de duplicarlo.

### PUBLISHED

Material preparado para terceros:

- artículos
- newsletters
- documentación
- cursos
- presentaciones
- publicaciones

**PUBLISHED = distribución.**

Nunca es la fuente primaria de verdad.

---

# 3. Principio epistemológico

El sistema debe distinguir:

```text
HECHO
  ↓
información respaldada directamente por una fuente

INTERPRETACIÓN
  ↓
síntesis derivada de fuentes

INFERENCIA
  ↓
conclusión obtenida mediante razonamiento
```

Nunca presentar una inferencia como hecho.

Las contradicciones entre fuentes se conservan y documentan; no se eliminan artificialmente.

---

# 4. Estructura recomendada

El Baúl global mantiene la estructura existente del usuario y agrega explícitamente `raw/` y `wiki/`.

Ejemplo:

```text
llm.wiki/
├── AGENTS.md
│
├── raw/
│   ├── papers/
│   ├── books/
│   ├── articles/
│   ├── transcripts/
│   └── ...
│
├── wiki/
│   ├── concepts/
│   ├── people/
│   ├── technologies/
│   ├── topics/
│   ├── debates/
│   ├── decisions/
│   └── synthesis/
│
├── projects/
│   └── proyecto/
│       ├── AGENTS.md
│       ├── raw/
│       ├── wiki/
│       ├── research/
│       ├── work/
│       └── published/ (optional)
│
├── published/
│   ├── articles/
│   ├── newsletters/
│   ├── documentations/
│   ├── courses/
│   ├── presentations/
│   └── publications/
│
└── ...
```

No todas las carpetas son obligatorias.

La estructura debe seguir siendo compatible con la organización OKF existente.

---

# 5. AGENTS.md

Hay dos niveles.

## Baúl global

`llm.wiki/AGENTS.md`

Define las reglas epistemológicas y operativas globales:

- preservar RAW;
- trazabilidad;
- separación hecho/interpretación/inferencia;
- evitar duplicados;
- usar enlaces Obsidian;
- gestionar contradicciones;
- controlar obsolescencia;
- privacidad;
- mínima intervención;
- reglas de promoción;
- jerarquía de instrucciones;
- criterios de lint.

## Proyecto

`projects/<project>/AGENTS.md`

Define:

- identidad;
- objetivo;
- contexto;
- límites;
- estructura;
- fuentes autorizadas;
- terminología;
- stack;
- reglas específicas;
- decisiones;
- workflow;
- criterios de publicación.

El AGENTS específico puede complementar al global, pero no contradecirlo salvo instrucción explícita del propietario.

---

# 6. Frontmatter

Debe existir un esquema pequeño, estable y semántico.

Ejemplo básico:

```yaml
---
type: concept
title: Cognitive Offloading
status: active
created: 2026-08-16
updated: 2026-08-16

aliases:
  - Descarga cognitiva

tags:
  - cognition
  - technology

sources:
  - "[[Cognitive Offloading Paper]]"

confidence: high

volatile: false
---
```

Tipos principales:

```text
source
concept
person
organization
technology
topic
idea
question
decision
project
article
note
synthesis
comparison
research
```

Estados posibles:

```text
draft
active
deprecated
archived
superseded
```

Confianza:

```text
high
medium
low
unknown
```

Para conocimiento temporalmente sensible:

```yaml
volatile: true
review_after: 2026-12-01
```

Las fuentes pueden tener metadata adicional como:

```yaml
source_type:
authors:
published:
url:
doi:
accessed:
```

---

# 7. CLI central

No implementar seis scripts independientes.

Crear una única herramienta:

```text
wikictl
```

con comandos:

```text
wikictl ingest
wikictl promote
wikictl research
wikictl lint
wikictl synthesize
wikictl publish
```

Arquitectura aproximada:

```text
wikictl/
├── src/
│   └── wikictl/
│       ├── cli.py
│       ├── commands/
│       │   ├── ingest.py
│       │   ├── promote.py
│       │   ├── research.py
│       │   ├── lint.py
│       │   ├── synthesize.py
│       │   └── publish.py
│       │
│       ├── core/
│       │   ├── vault.py
│       │   ├── frontmatter.py
│       │   ├── markdown.py
│       │   ├── links.py
│       │   ├── graph.py
│       │   ├── provenance.py
│       │   └── validation.py
│       │
│       ├── agents/
│       ├── providers/
│       └── schemas/
└── tests/
```

El almacenamiento continúa siendo:

```text
Markdown + YAML + Obsidian links + Git
```

No introducir una base de datos inicialmente.

---

# 8. Comando `ingest`

Propósito:

> Incorporar y analizar una fuente sin convertirla todavía en conocimiento consolidado.

Ejemplos:

```bash
wikictl ingest paper.pdf
wikictl ingest article.md
wikictl ingest "https://arxiv.org/..."
```

Proceso:

```text
fuente
 ↓
identificación
 ↓
extracción
 ↓
metadata
 ↓
análisis LLM
 ↓
conceptos
 ↓
entidades
 ↓
relaciones
 ↓
claims
 ↓
resultado de ingest
```

Debe producir un artefacto intermedio, por ejemplo:

```text
.work/ingest/<source>.yaml
```

`ingest` NO modifica automáticamente la Wiki.

---

# 9. Comando `promote`

Propósito:

> Convertir evidencia procesada en conocimiento persistente.

Ejemplo:

```bash
wikictl promote cognitive-offloading --dry-run
```

Debe analizar:

```text
fuente
+
resultado de ingest
+
wiki existente
+
AGENTS.md
```

y proponer:

```text
CREATE
UPDATE
LINK
CONFLICT
```

Ejemplo:

```text
CREATE
  wiki/concepts/cognitive-offloading.md

UPDATE
  wiki/concepts/cognitive-scaffolding.md

LINK
  cognitive-offloading → cognitive-scaffolding

CONFLICT
  claim X conflicts with existing knowledge
```

`--dry-run` debe ser el modo seguro por defecto.

La ejecución efectiva requiere aprobación.

---

# 10. Comando `research`

Propósito:

> Investigar una pregunta, no simplemente pedirle una respuesta al LLM.

Ejemplo:

```bash
wikictl research \
  "¿Cómo afecta la IA al cognitive offloading?"
```

Debe generar primero un **Research Plan**:

```text
pregunta
 ↓
subpreguntas
 ↓
estrategia de fuentes
 ↓
búsqueda
 ↓
evidencia
 ↓
análisis
 ↓
contradicciones
 ↓
conclusiones
```

Resultado:

```text
research/
└── 2026-08-16-ai-cognitive-offloading.md
```

La investigación debe mantener referencias y niveles de confianza.

`research` no modifica automáticamente la Wiki.

Posteriormente:

```bash
wikictl promote research/<research-note>.md
```

permite convertir sus resultados en conocimiento persistente.

---

# 11. Comando `synthesize`

Propósito:

> Construir conocimiento nuevo a partir de múltiples piezas existentes.

Ejemplo:

```bash
wikictl synthesize \
  "¿Qué patrón común existe entre MCP, function calling y tool use?"
```

o:

```bash
wikictl synthesize \
  --from "AI Agents" \
  --from "MCP" \
  --from "Tool Use"
```

Proceso:

```text
notas relevantes
 ↓
fuentes
 ↓
relaciones
 ↓
contradicciones
 ↓
síntesis
 ↓
nuevo conocimiento
```

Puede producir:

```text
wiki/synthesis/agent-tooling-architecture.md
```

La síntesis debe conservar provenance.

---

# 12. Comando `lint`

Debe tener dos niveles.

## Determinístico

```bash
wikictl lint
```

Detecta:

```text
broken links
invalid frontmatter
duplicate IDs
missing titles
invalid types
orphan notes
missing sources
expired review_after
```

No necesita LLM.

## Semántico

```bash
wikictl lint --semantic
```

Utiliza LLM para detectar:

```text
posibles duplicados
contradicciones
obsolescencia
relaciones faltantes
conocimiento sin respaldo
proyectos que duplican conocimiento global
```

Resultado:

```text
.work/lint/<date>-report.md
```

`lint` detecta y recomienda.

No realiza cambios masivos automáticamente.

---

# 13. Comando `publish`

Propósito:

> Convertir conocimiento consolidado en un artefacto para una audiencia externa.

Ejemplo:

```bash
wikictl publish \
  wiki/synthesis/agent-tooling-architecture.md \
  --target substack
```

Pipeline:

```text
WIKI
 ↓
selección de fuentes
 ↓
audiencia
 ↓
objetivo
 ↓
estructura
 ↓
draft
 ↓
fact checking
 ↓
provenance check
 ↓
privacy check
 ↓
copyright check
 ↓
PUBLICATION
```

Resultado:

```text
published/substack/<article>.md
```

Publicar y generar un draft son operaciones distintas.

La publicación real requiere aprobación explícita.

---

# 14. Provenance

Debe existir una capa explícita de trazabilidad.

Cada pieza importante de conocimiento debería poder responder:

> ¿De dónde salió esto?

Modelo conceptual:

```text
WIKI
 ↓
RESEARCH / SYNTHESIS
 ↓
SOURCES
```

Ejemplo:

```yaml
sources:
  - "[[Paper X]]"
  - "[[Paper Y]]"

derived_from:
  - "[[Research 2026-08-16]]"
```

No es necesario inicialmente rastrear cada oración.

Es suficiente comenzar con trazabilidad a nivel de nota, claim o bloque relevante.

---

# 15. Regla arquitectónica crítica

El LLM **no debe escribir directamente sobre el filesystem**.

Incorrecto:

```text
LLM → filesystem
```

Correcto:

```text
LLM
 ↓
structured result
 ↓
schema validation
 ↓
planner
 ↓
diff
 ↓
approval
 ↓
filesystem
```

El LLM propone cambios.

`wikictl` valida y ejecuta.

Esto permite:

- seguridad;
- reproducibilidad;
- dry-run;
- auditoría;
- rollback;
- independencia del modelo.

---

# 16. Git

Git forma parte del sistema.

Debe proporcionar:

- versionado;
- diff;
- historial;
- rollback;
- auditoría;
- branches.

Opcionalmente:

```bash
wikictl promote ... --commit
```

puede crear commits descriptivos.

Ejemplo:

```text
knowledge: promote cognitive offloading

- created concept
- updated cognitive scaffolding
- added references
- added relationships
```

---

# 17. Impact analysis

Una capacidad futura importante:

```bash
wikictl impact "cognitive-offloading"
```

Debe mostrar:

```text
Concept
 ├── Research
 ├── Projects
 ├── Syntheses
 └── Published
```

Esto permite saber qué artefactos podrían quedar afectados si cambia el conocimiento base.

Es especialmente útil para publicaciones.

---

# 18. Workflow cotidiano

Ejemplo completo:

```bash
# Incorporar fuente
wikictl ingest paper.pdf

# Ver qué propone
wikictl promote paper --dry-run

# Aprobar promoción
wikictl promote paper

# Investigar una cuestión
wikictl research "..."

# Consolidar conocimiento
wikictl synthesize "..."

# Revisar el Baúl
wikictl lint --semantic

# Generar publicación
wikictl publish wiki/synthesis/foo.md --target substack
```

---

# 19. Orden recomendado de implementación

No implementar los seis comandos simultáneamente.

### Fase 1 — infraestructura

```text
Markdown parser
YAML/frontmatter
Obsidian links
Vault abstraction
Git
schemas
validation
```

### Fase 2 — núcleo

```text
ingest
promote
lint
```

Estos tres construyen la infraestructura cognitiva.

### Fase 3 — inteligencia

```text
research
synthesize
```

### Fase 4 — distribución

```text
publish
```

### Fase 5 — capacidades avanzadas

```text
provenance
impact analysis
semantic lint
dependency tracking
automatic review
multi-provider LLM
```

---

# 20. Principio rector

La definición más importante del sistema es:

> **RAW contiene lo que otros dijeron. WIKI contiene lo que sabemos. PROJECT contiene lo que estamos haciendo con ese conocimiento. PUBLISHED contiene lo que decidimos decirle a otros.**

El objetivo no es acumular notas.

El objetivo es construir un sistema donde cada nueva fuente pueda:

```text
agregar conocimiento
        ↓
crear relaciones
        ↓
mejorar conocimiento existente
        ↓
alimentar proyectos
        ↓
producir publicaciones
        ↓
recibir feedback
        ↓
mejorar nuevamente la Wiki
```

Esto convierte Obsidian + Markdown + Git + LLMs en un **Knowledge Operating System personal**, manteniendo los datos bajo control del usuario y utilizando los modelos como capa de procesamiento, razonamiento y transformación.
