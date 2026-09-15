# Manual de Usuario: Knowledge Operating System (LLM Wiki)

Bienvenido al manual operativo del **Knowledge Operating System**. Esta guía te enseñará cómo utilizar tu baúl de Obsidian potenciado por modelos de lenguaje (LLM) y gobernado por el kernel determinístico `wikictl`.

---

## 1. Conceptos Fundamentales

El sistema organiza el conocimiento en cuatro capas funcionales:

```text
RAW → WIKI → PROJECT → PUBLISHED
 ↑                         │
 └────── feedback ─────────┘
```

1. **RAW (`raw/`) = Evidencia**:
   - Papers, libros, transcripciones, artículos, datasets y notas crudas.
   - **Regla inmutable**: Los archivos en `raw/` nunca se modifican ni se corrigen. Son la evidencia histórica de lo que otros dijeron.
2. **WIKI (`wiki/`) = Conocimiento Consolidado**:
   - Conceptos (`concepts/`), personas (`people/`), tecnologías (`technologies/`), áreas temáticas (`topics/`), controversias (`debates/`), decisiones de arquitectura (`decisions/`) y síntesis cruzadas (`synthesis/`).
   - Todo lo que reside en `wiki/` es conocimiento destilado, atómico, reutilizable y enlazado mediante wikilinks.
3. **PROJECT (`projects/`) = Aplicación del Conocimiento**:
   - Proyectos específicos (ej. desarrollo de software, un curso, una investigación aplicada).
   - Reutilizan las notas de `wiki/` mediante enlaces (`[[Nombre del Concepto]]`) en lugar de duplicar información.
4. **PUBLISHED (`published/`) = Distribución Externa**:
   - Artículos para blogs, newsletters, cursos o presentaciones destinados a audiencias públicas. Nunca es la fuente de verdad del baúl.

---

## 2. Principio Epistemológico: La Verdad en tu Baúl

Todo contenido procesado debe respetar esta distinción:

* **HECHO (Fact)**: Información verificable con cita textual o referencia directa a un documento en `raw/`.
* **INTERPRETACIÓN (Interpretation)**: Explicación o estructuración conceptual derivada directamente de las fuentes.
* **INFERENCIA (Inference)**: Conclusión, conjetura o hipótesis obtenida mediante razonamiento deductivo o inductivo. Siempre debe ir acompañada de un nivel de certeza: `high`, `medium`, `low` o `unknown`.

> [!IMPORTANT]
> **Preservación de contradicciones**: Si dos fuentes autorizadas discrepan, **no fuerces un consenso artificial**. El sistema documenta ambas posturas en una nota de debate (`wiki/debates/`).

---

## 3. Guía Paso a Paso: Flujo de Ingesta y Promoción

### ¿Cómo incorporar un nuevo paper, artículo o libro?

#### Paso 1: Guardar la fuente en `raw/`
Coloca el archivo original en la subcarpeta correspondiente:
- `raw/articles/mi-articulo.md`
- `raw/papers/paper-investigacion.pdf` (o versión en texto/markdown)

#### Paso 2: Registrar la ingesta
Ejecuta en tu terminal:
```bash
./wikictl/wikictl ingest raw/articles/mi-articulo.md
```
Esto calcula el checksum SHA-256 de la fuente y genera un archivo de análisis intermedio en `.work/ingest/mi-articulo.yaml`.

#### Paso 3: Análisis Cognitivo del LLM
Si estás conversando con un LLM (o un agente como Antigravity, Claude Code, Cursor, Aider):
- El agente lee el material de `raw/` y completa en `.work/ingest/mi-articulo.yaml`:
  - Afirmaciones clave distinguiendo **hechos** (con citas textuales) de **interpretaciones**.
  - Conceptos nuevos o tecnologías identificadas.
  - Relaciones con notas existentes.

#### Paso 4: Verificación segura (Dry-Run)
Antes de modificar cualquier archivo de la wiki, ejecuta:
```bash
./wikictl/wikictl promote mi-articulo --dry-run
```
El kernel comparará el análisis con las notas existentes en `wiki/` y te mostrará el plan con diffs exactos:
- ✨ `[CREATE] wiki/concepts/cognitive-offloading.md`
- 📝 `[UPDATE] wiki/technologies/obsidian.md`

#### Paso 5: Aplicar y registrar en Git
Una vez que revisaste el diff y estás conforme, aplica los cambios:
```bash
./wikictl/wikictl promote mi-articulo --apply --commit
```
`wikictl` creará y actualizará las notas en `wiki/` y generará automáticamente un commit descriptivo en Git:
```text
knowledge: promote mi-articulo

- created wiki/concepts/cognitive-offloading.md
- updated wiki/technologies/obsidian.md
```

---

## 4. Guía de Comandos de `wikictl`

| Comando | Función | Modifica Disco |
| :--- | :--- | :---: |
| `./wikictl/wikictl init` | Recrea y verifica toda la estructura de carpetas canónicas si alguna fue borrada. | Solo carpetas vacías |
| `./wikictl/wikictl lint` | Audita enlaces rotos, esquemas YAML inválidos, notas huérfanas y revisiones vencidas. | No |
| `./wikictl/wikictl ingest <fuente>` | Registra evidencia cruda y prepara la plantilla en `.work/ingest/<slug>.yaml`. | Solo en `.work/` |
| `./wikictl/wikictl promote <slug> --dry-run` | Muestra el diff de cambios propuestos sin tocar el baúl. | No |
| `./wikictl/wikictl promote <slug> --apply` | Aplica la creación y actualización de notas en `wiki/`. | **Sí (validado)** |
| `./wikictl/wikictl promote <slug> --apply --commit` | Aplica los cambios y genera un commit semántico en Git. | **Sí** |
| `./wikictl/wikictl research "<pregunta>"` | Genera un andamiaje de investigación estructurada en `research/`. | Solo en `research/` |
| `./wikictl/wikictl synthesize "<tema>"` | Genera un andamiaje de síntesis transversal en `wiki/synthesis/`. | Solo en `wiki/` |
| `./wikictl/wikictl impact "<nota>"` | Muestra el árbol de impacto de dependencias si vas a modificar una nota. | No |
| `./wikictl/wikictl publish "<nota>" --target substack` | Limpia wikilinks y genera un borrador para publicación en `published/`. | Solo en `published/` |

---

## 5. Modalidades de Uso según el Perfil

### Modo A: Principiante (Chat Conversacional)
No necesitas memorizar comandos. En tu chat con el LLM:
1. Pega el texto o di: *"Quiero incorporar el paper que puse en `raw/articles/ia-memoria.md`"*.
2. El LLM te explicará en lenguaje natural:
   > *"He analizado el documento. Propongo crear 2 conceptos nuevos (`Descarga Cognitiva` y `Andamiaje Cognitivo`) y actualizar la nota de `Obsidian` para enlazarla. Este es el diff que aplicaría..."*
3. Le respondes: *"Adelante, aplícalo"*.
4. El LLM ejecutará internamente `./wikictl/wikictl promote ia-memoria --apply --commit` y te confirmará la acción.

### Modo B: Avanzado (CLI y Automatización)
Puedes ejecutar directamente los comandos desde tu consola habitual:
```bash
# Auditar salud del baúl
./wikictl/wikictl lint --strict

# Ver salida estructurada en JSON para scripts o CI
./wikictl/wikictl lint --json
```

### Modo C: Entornos sin Terminal ni Python (Agent-Native Fallback)
Si estás utilizando Obsidian en un móvil o una tablet, o interactuando en la web de Claude.ai/ChatGPT sin acceso a consola:
- `AGENTS.md` le instruye al modelo para que **emule mentalmente las validaciones de `wikictl`**.
- El modelo te entregará el código Markdown completo listo para copiar, indicándote la ruta exacta:
  > *"Copia este contenido en: `wiki/concepts/mi-concepto.md`"*

---

## 6. Preguntas Frecuentes (FAQ)

### ¿Qué pasa si borro carpetas vacías o clono el repositorio sin ellas?
Git no rastrea carpetas vacías por defecto. Si borraste carpetas o clonaste el repo, simplemente corre:
```bash
./wikictl/wikictl init
```
El motor recreará automáticamente todas las carpetas canónicas (`raw/`, `wiki/`, `published/`, etc.) con sus correspondientes archivos `.gitkeep`. Además, comandos como `promote` o `research` crean automáticamente las carpetas intermedias que necesitan (`mkdir -p`).

### ¿Requiere instalar dependencias con `pip` o entornos virtuales?
**No, absolutamente ninguna.** El kernel `wikictl` fue construido deliberadamente utilizando el 100% de la biblioteca estándar de Python 3. No hay `pip install`, ni dependencias de compilación en C, ni dependencias de Node.js. Clonas y funciona.

### ¿Cómo navego el conocimiento en Obsidian?
1. Abre la carpeta `llm.wiki` como un baúl (Vault) en Obsidian.
2. Abre la **Vista de Grafo** (`Graph View`): verás cómo los conceptos se agrupan en clústeres naturales.
3. Haz clic en cualquier `[[enlace]]` para navegar entre conceptos, fuentes y proyectos.
4. Consulta el panel de **Enlaces Entrantes** (`Backlinks`) para descubrir qué otras notas mencionan el concepto actual.
