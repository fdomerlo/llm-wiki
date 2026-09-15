# LLM Wiki — Knowledge Operating System

<p align="center">
  <img src="docs/assets/social-preview.png" alt="LLM Wiki — Knowledge Operating System" width="100%">
</p>

Un **Sistema Operativo del Conocimiento personal** basado en **Obsidian + Markdown + Git**, operado bajo el paradigma **"LLM-as-Operator"** y protegido por un kernel determinístico con **cero dependencias externas** (`wikictl`).

Inspirado en la visión de Andrej Karpathy sobre el uso de Modelos de Lenguaje como curadores, bibliotecarios y analistas críticos de una base de conocimiento viva y acumulativa.

---

## 🧭 La Filosofía del Sistema

> **RAW** contiene lo que otros dijeron.  
> **WIKI** contiene lo que sabemos.  
> **PROJECT** contiene lo que estamos haciendo con ese conocimiento.  
> **PUBLISHED** contiene lo que decidimos decirle a otros.

A diferencia de las herramientas convencionales de RAG o chatbots que solo consultan pasivamente archivos, este sistema convierte al LLM en un **asistente activo** que ayuda a estructurar, relacionar, mantener, investigar y convertir el conocimiento en productos derivados, manteniendo la verdad inmutable y versionada con Git.

---

## 🛡️ Principio Arquitectónico Crítico (Aislamiento)

> **EL LLM NUNCA ESCRIBE DIRECTAMENTE SOBRE LAS NOTAS DE LA WIKI.**

Para evitar alucinaciones, enlaces rotos y corrupción silenciosa del grafo, el flujo de incorporación siempre es:

```text
EVIDENCIA (raw/) o PROMPT
       ↓
ANÁLISIS COGNITIVO DEL LLM
       ↓
ARTEFACTO ESTRUCTURADO (.work/ingest/<fuente>.yaml)
       ↓
PLAN DE PROMOCIÓN & DIFF (wikictl promote --dry-run)
       ↓
APROBACIÓN DEL USUARIO
       ↓
ESCRITURA EN DISCO + COMMIT GIT ATÓMICO (wikictl promote --apply --commit)
```

---

## ⚡ Requisitos y Portabilidad: Cero Dependencias

- **Funciona en cualquier plataforma**: Linux, macOS y Windows.
- **Sin `pip install` ni librerías externas**: Utiliza exclusivamente la **biblioteca estándar de Python 3** (`pathlib`, `argparse`, `json`, `difflib`, `re`, `subprocess`, `dataclasses`).
- Clonas el repositorio y lo comienzas a usar de inmediato:
  ```bash
  ./wikictl/wikictl --help
  ```

---

## 📂 Estructura Canónica del Baúl

```text
llm.wiki/
├── AGENTS.md                                   # Protocolo operativo y epistemológico para LLMs
├── README.md                                   # Esta guía
├── docs/                                       # Documentación y especificación fundacional
│   ├── MANUAL_DE_USUARIO.md                    # Manual detallado paso a paso
│   └── PROJECT_FOUNDATION.md                   # Especificación arquitectónica original
├── raw/                                        # Evidencia inmutable (notes, clippings, papers, books)
│   ├── notes/                                  # Notas rápidas y notas nuevas por defecto
│   ├── clippings/                              # Recortes del plugin Obsidian Web Clipper
│   ├── articles/                               # Artículos y lecturas web
│   ├── papers/                                 # Papers académicos
│   ├── books/                                  # Resúmenes y notas de libros
│   ├── transcripts/                            # Transcripciones de audio o video
│   └── attachments/                            # Adjuntos (imágenes, audios, PDFs)
├── wiki/                                       # Conocimiento consolidado y atómico (reutilizable)
│   ├── concepts/                               # Conceptos y modelos mentales
│   ├── people/                                 # Autores y figuras clave
│   ├── technologies/                           # Herramientas, software y protocolos
│   ├── topics/                                 # Disciplinas y áreas temáticas
│   ├── debates/                                # Controversias y contrastes entre fuentes
│   ├── decisions/                              # Registros de decisiones arquitectónicas (ADRs)
│   └── synthesis/                              # Síntesis transversales de múltiples notas
├── projects/                                   # Proyectos concretos (aplicación del conocimiento)
├── published/                                  # Material final para terceros (newsletters, artículos)
├── research/                                   # Investigaciones temáticas en curso
├── .work/                                      # Espacio de trabajo intermedio (ingesta, reportes lint)
└── wikictl/                                    # Kernel determinístico y CLI (wikictl/wikictl)
```

> [!TIP]
> Si borras carpetas vacías o clonas el repositorio en limpio, puedes restaurar toda la estructura canónica en cualquier momento ejecutando:
> ```bash
> ./wikictl/wikictl init
> ```

---

## ⚙️ Configuración Recomendada de Obsidian

Para que Obsidian trabaje en perfecta armonía con el sistema, aplica estas configuraciones en **Ajustes (`Settings`)**:

1. **Ubicación de nuevas notas (`Archivos y enlaces` / `Files and links`)**:
   - *Ubicación de notas nuevas por defecto*: `En la carpeta especificada a continuación` → `raw/notes` (para que cualquier nota creada manualmente o con atajo quede en `raw/` como evidencia preliminar sin procesar).
   - *Ubicación de archivos adjuntos*: `En la carpeta especificada a continuación` → `raw/attachments`.
2. **Enlaces (`Files and links`)**:
   - *Usar [[Wikilinks]]*: **Activado** (`ON`).
   - *Formato de enlaces nuevo*: `Ruta más corta cuando sea posible` (`Shortest path when possible`).
   - *Detectar todas las extensiones de archivo*: **Activado** (`ON`) para ver PDFs, audios y datasets en el explorador.
3. **Obsidian Web Clipper (Extensión de Navegador)**:
   - Configura la ruta de guardado a: `raw/clippings/`
   - Así, cualquier artículo o captura web cae automáticamente como evidencia pura en `raw/` lista para ser analizada e ingesta.

---

## 🚀 Inicio Rápido

### Modalidad A: Para Principiantes (Modo Chat / Conversacional)

Si usas un asistente como **Antigravity, Claude Code, Cursor, Aider o ChatGPT**:
1. Coloca un documento o texto en `raw/articles/mi-nota.md` (o simplemente compártelo en el chat).
2. Dile al LLM en lenguaje natural:
   > *"Quiero incorporar este documento a la wiki"*.
3. El LLM (guiado por `AGENTS.md`) analizará la fuente, distinguirá Hechos de Inferencias, creará el artefacto en `.work/ingest/` y te mostrará el plan con un diff seguro:
   > *"Propongo crear el concepto `wiki/concepts/mi-concepto.md` y actualizar `wiki/technologies/otra.md`. ¿Estás de acuerdo?"*
4. Al darle tu visto bueno, el agente ejecuta la promoción y registra el commit en Git.

### Modalidad B: Para Usuarios Avanzados (Modo CLI)

```bash
# 1. Verificar la integridad de la estructura de carpetas
./wikictl/wikictl init

# 2. Auditar la salud del Baúl (enlaces rotos, esquemas, notas huérfanas)
./wikictl/wikictl lint

# 3. Registrar una fuente en raw/ para análisis
./wikictl/wikictl ingest raw/articles/paper.md

# 4. Ver el diff propuesto sin tocar disco (Modo seguro por defecto)
./wikictl/wikictl promote paper --dry-run

# 5. Aplicar los cambios y registrar un commit descriptivo en Git
./wikictl/wikictl promote paper --apply --commit

# 6. Investigar una pregunta temática
./wikictl/wikictl research "¿Cómo optimizar la memoria extendida con IA?"

# 7. Crear una síntesis comparativa entre notas
./wikictl/wikictl synthesize "Patrones de Agentes" --sources "MCP" "Tool Use"

# 8. Analizar qué notas se verían afectadas si modificas un concepto
./wikictl/wikictl impact "Cognitive Offloading"

# 9. Preparar un borrador para publicación externa
./wikictl/wikictl publish "Cognitive Offloading" --target substack
```

---

## 🧪 Pruebas Automatizadas

El sistema incluye una suite completa de 24 tests unitarios e integrales que validan el parsing de YAML, la resolución multidimensional de enlaces Obsidian, la detección de links rotos, diffs, git commits y todos los subcomandos:

```bash
PYTHONPATH=wikictl/src python3 -m unittest discover -s wikictl/tests
```

---

## 📚 Documentación Adicional

- [Manual Completo de Usuario](file:///home/fdomerlo/Proyectos/github.com/fdomerlo/llm.wiki/docs/MANUAL_DE_USUARIO.md): Flujos detallados, convenciones y guía para Obsidian.
- [Protocolo AGENTS.md](file:///home/fdomerlo/Proyectos/github.com/fdomerlo/llm.wiki/AGENTS.md): Reglas epistemológicas y directivas operativas para agentes.
- [Especificación Fundacional](file:///home/fdomerlo/Proyectos/github.com/fdomerlo/llm.wiki/docs/PROJECT_FOUNDATION.md): Fundamentos teóricos y diseño conceptual original.
