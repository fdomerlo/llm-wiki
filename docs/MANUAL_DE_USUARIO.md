# Manual de Usuario y Guía Avanzada: Knowledge Operating System (LLM Wiki)

Bienvenido al manual operativo y guía técnica del **Knowledge Operating System**. Este documento está especialmente diseñado para **usuarios avanzados, desarrolladores e ingenieros de conocimiento** que desean dominar el sistema a través de su interfaz de línea de comandos (`wikictl`), automatizar flujos con Git, auditar la integridad del grafo y ejecutar investigaciones y síntesis profundas.

> [!NOTE]
> Si buscas una introducción rápida y conversacional para comenzar en 3 pasos con tu asistente de IA habitual (sin usar comandos de consola), consulta el [README.md](../README.md).

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

## 4. Referencia Exhaustiva de Comandos `wikictl` (CLI)

`wikictl` es el kernel determinístico del sistema. Está diseñado para ejecutarse de forma segura tanto por humanos en la terminal como por agentes autónomos y pipelines de CI/CD.

### Resumen de Comandos

| Comando | Función Principal | Flags Clave | Modifica Disco |
| :--- | :--- | :--- | :---: |
| `init` | Restaura la estructura canónica de directorios y `.gitkeep`. | *(ninguno)* | Solo crea carpetas faltantes |
| `lint` | Audita salud del baúl (links rotos, frontmatter, huérfanos). | `--strict`, `--json` | No |
| `ingest` | Registra evidencia inmutable en `raw/` y genera plantilla YAML. | `<fuente>` | Solo en `.work/` |
| `promote` | Valida, previsualiza y aplica cambios a `wiki/`. | `--dry-run`, `--apply`, `--commit` | **Sí (con `--apply`)** |
| `research` | Inicializa un andamiaje de investigación en `research/`. | `<pregunta>` | Solo en `research/` |
| `synthesize` | Genera una nota de síntesis transversal en `wiki/synthesis/`. | `--sources <nota1> <nota2>` | Solo en `wiki/` |
| `impact` | Muestra el grafo de dependencias y blast radius de una nota. | `<nota>` | No |
| `publish` | Limpia wikilinks y compila un borrador para distribución externa. | `--target <formato>` | Solo en `published/` |

---

### Detalle de Comandos y Ejemplos de Terminal

#### 1. `wikictl init`
Recrea la estructura completa de carpetas canónicas (`raw/notes`, `raw/clippings`, `wiki/concepts`, etc.) en caso de que hayan sido eliminadas o no clonadas por Git:
```bash
./wikictl/wikictl init
```

#### 2. `wikictl lint`
Valida la integridad estructural del baúl. Detecta:
- Enlaces internos rotos (`[[Nota Inexistente]]`).
- Frontmatter YAML malformado o con campos obligatorios faltantes (`type`, `title`, `status`, `created`, `updated`, `confidence`).
- Notas huérfanas (sin enlaces entrantes ni salientes).
- Revisiones de conocimiento volátil vencidas (`review_after`).

```bash
# Modo estándar con reporte visual en consola
./wikictl/wikictl lint

# Modo estricto: retorna código de salida != 0 ante cualquier advertencia (ideal para pre-commit o CI)
./wikictl/wikictl lint --strict

# Modo JSON estructurado: ideal para scripts bash o ingestión por agentes
./wikictl/wikictl lint --json
```

#### 3. `wikictl ingest <fuente>`
Registra un documento ubicado en `raw/` como evidencia histórica inmutable. Calcula su checksum SHA-256 y crea el artefacto intermedio en `.work/ingest/<slug>.yaml`:
```bash
./wikictl/wikictl ingest raw/articles/karpathy-llm-os.md
```

#### 4. `wikictl promote <slug>`
Aplica el principio de aislamiento del filesystem. Compara el archivo estructurado en `.work/ingest/<slug>.yaml` con el estado actual de `wiki/`.
- **`--dry-run` (por defecto)**: Genera un diff unificado y coloreado en terminal mostrando exactamente qué notas se crearían o modificarían sin alterar ningún archivo:
  ```bash
  ./wikictl/wikictl promote karpathy-llm-os --dry-run
  ```
- **`--apply`**: Escribe de manera atómica las notas en `wiki/` tras validar esquemas y links:
  ```bash
  ./wikictl/wikictl promote karpathy-llm-os --apply
  ```
- **`--apply --commit`**: Escribe los cambios y genera de inmediato un commit descriptivo y semántico en Git:
  ```bash
  ./wikictl/wikictl promote karpathy-llm-os --apply --commit
  ```

#### 5. `wikictl research "<pregunta>"`
Crea una investigación guiada en `research/` para responder preguntas complejas o estructurar exploraciones temáticas:
```bash
./wikictl/wikictl research "¿Cómo optimizar la memoria extendida con IA?"
```

#### 6. `wikictl synthesize "<tema>" --sources <notas...>`
Genera una nota transversal en `wiki/synthesis/` que contrasta e integra múltiples notas existentes:
```bash
./wikictl/wikictl synthesize "Patrones de Agentes Autónomos" --sources "Model Context Protocol" "Tool Use" "ReAct Framework"
```

#### 7. `wikictl impact "<nota>"`
Evalúa el "blast radius" o impacto antes de modificar, renombrar o deprecicar una nota. Lista todas las notas, proyectos, síntesis o publicaciones que dependen de ella:
```bash
./wikictl/wikictl impact "Cognitive Offloading"
```

#### 8. `wikictl publish "<nota>" --target <plataforma>`
Toma una nota consolidada o síntesis de `wiki/`, sustituye o expande los wikilinks internos por texto legible, verifica advertencias de privacidad y crea un borrador listo para exportar en `published/`:
```bash
# Para Substack o newsletters
./wikictl/wikictl publish "Cognitive Offloading" --target substack

# Para blogs técnicos o documentación en Markdown plano
./wikictl/wikictl publish "Cognitive Offloading" --target blog
```

---

## 5. Modalidades de Uso según el Perfil

### Modalidad Avanzada: Flujo de Consola y Automatización (CLI)

Los usuarios avanzados y desarrolladores pueden utilizar `wikictl` directamente en su terminal para mantener el baúl con máxima precisión:

```bash
# Secuencia completa de incorporación de nuevo conocimiento:
# 1. Guardar la evidencia
cp ~/Downloads/paper.pdf raw/papers/paper.pdf
pdftotext raw/papers/paper.pdf raw/papers/paper.txt

# 2. Iniciar el registro de ingesta
./wikictl/wikictl ingest raw/papers/paper.txt

# 3. Tras completar .work/ingest/paper.yaml (manualmente o con tu agente):
# Previsualizar el diff
./wikictl/wikictl promote paper --dry-run

# 4. Aplicar y commitear
./wikictl/wikictl promote paper --apply --commit

# 5. Auditar integridad del baúl tras la incorporación
./wikictl/wikictl lint --strict
```

#### Integración en Pre-Commit Hooks de Git
Puedes asegurar que nunca se comitee una nota con frontmatter inválido o enlaces rotos agregando lo siguiente a `.git/hooks/pre-commit`:
```bash
#!/usr/bin/env bash
./wikictl/wikictl lint --strict
```

---

### Modalidad Asistida: Chat Conversacional (Principiantes o IDEs)

Para flujos dentro de IDEs o chats con LLMs (Cursor, Antigravity, Claude Code, Aider, ChatGPT):
1. Comparte un archivo o texto de `raw/` y di: *"Quiero incorporar este documento a la wiki"*.
2. El LLM consulta `AGENTS.md`, extrae afirmaciones clave distinguiendo hechos de inferencias, prepara `.work/ingest/` y te muestra la propuesta:
   > *"Propongo crear el concepto `wiki/concepts/mi-concepto.md` y actualizar `wiki/technologies/otra.md`. ¿Estás de acuerdo?"*
3. Con tu visto bueno (*"Aplica los cambios"*), el agente ejecuta `./wikictl/wikictl promote <slug> --apply --commit` de manera transparente.

---

### Modalidad C: Entornos sin Terminal ni Python (Agent-Native Fallback)
Si estás utilizando Obsidian en un móvil, tablet o interfaz web sin acceso a consola ni Python:
- `AGENTS.md` le instruye al modelo para que **emule mentalmente las validaciones de `wikictl`** (esquemas frontmatter, separación hechos/inferencias y enlaces canónicos).
- El modelo genera el código Markdown completo y te da las instrucciones directas de guardado:
  > *"Guarda este contenido en el archivo: `wiki/concepts/mi-concepto.md`"*

---

## 6. Configuración Recomendada de Obsidian (Vault Setup)

Para garantizar que el flujo de conocimiento sea 100% fluido y que cualquier nota o captura web caiga en el lugar correcto sin contaminar la wiki consolidada, configura Obsidian con estos parámetros en **Ajustes (`Settings`)**:

### A. Ubicación de Notas Nuevas (`Archivos y enlaces` / `Files and links`)
- **Ubicación por defecto para notas nuevas**: Selecciona `En la carpeta especificada a continuación` y escribe:
  `raw/notes`  
  *(Esto garantiza que cuando presiones `Ctrl/Cmd + N` o crees una nota rápida, nazca como evidencia cruda en `raw/notes/` y nunca directamente en `wiki/` sin procesar).*
- **Ubicación por defecto para nuevos archivos adjuntos**: Selecciona `En la carpeta especificada a continuación` y escribe:
  `raw/attachments`  
  *(Así, cualquier imagen que pegues, PDF o grabación quedará resguardada como evidencia inmutable).*

### B. Enlaces Internos (`Archivos y enlaces`)
- **Usar [[Wikilinks]]**: **Activado** (`ON`).
- **Formato de enlaces nuevo**: `Ruta más corta cuando sea posible` (`Shortest path when possible`).
- **Detectar todas las extensiones de archivo**: **Activado** (`ON`). Te permitirá ver archivos `.pdf`, `.yaml`, `.csv`, etc. dentro del explorador lateral de Obsidian.

### C. Obsidian Web Clipper (Extensión de Navegador)
Si utilizas el plugin oficial de Obsidian para capturar artículos o documentación desde tu navegador web:
- **Carpeta de destino**: Configura la ruta a `raw/clippings/`.
- **Plantilla de captura**: Puedes guardar el contenido completo del artículo con metadatos de URL y fecha de captura.
- **Flujo resultante**: El artículo queda guardado en `raw/clippings/<articulo>.md`, listo para que ejecutes:
  ```bash
  ./wikictl/wikictl ingest raw/clippings/<articulo>.md
  ./wikictl/wikictl promote <articulo> --dry-run
  ```

### D. Plugins Opcionales Recomendados
1. **Dataview**: Permite crear tablas dinámicas y tableros de control en notas de índice (`index.md`) de tus proyectos para consultar notas por etiquetas, tipo o fecha.
2. **Omnisearch**: Búsqueda difusa profunda de texto completo y contenido dentro de PDFs e imágenes.
3. **Graph View (Nativo)**: Activa filtros por color en el grafo de Obsidian (por ejemplo, verde para `wiki/concepts`, azul para `wiki/technologies`, rojo para `raw/`).

---

## 7. Preguntas Frecuentes (FAQ)

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
