# wikictl — Kernel y CLI para Knowledge Operating System (LLM Wiki)

`wikictl` es una herramienta ligera, determinística y con **cero dependencias externas** (usa exclusivamente la biblioteca estándar de Python 3) diseñada para orquestar y proteger un Baúl de Conocimiento personal en **Obsidian + Markdown + Git**.

---

## 🎯 Filosofía: Arquitectura LLM-as-Operator

A diferencia de herramientas que integran claves de API propietarias y cobran por llamadas, `wikictl` separa tajantemente la inteligencia del almacenamiento:

```text
EVIDENCIA (raw/)
       ↓
LLM EXTERNO (Antigravity, Claude Code, Cursor, Aider, ChatGPT)
       ↓ (análisis epistemológico)
ARTEFACTO (.work/ingest/<slug>.yaml)
       ↓
wikictl promote --dry-run (validación de esquema + diffs)
       ↓
APROBACIÓN DEL USUARIO
       ↓
wikictl promote --apply --commit (escritura en wiki/ + git commit)
```

**Regla de Oro**: El LLM propone cambios estructurados; `wikictl` valida, calcula el diff y escribe atómicamente en el disco.

---

## 🚀 Requisitos y Portabilidad

- **Python 3.9+** (Linux, macOS, Windows).
- **Cero dependencias**: No requiere `pip install`, ni `virtualenv`, ni librerías pesadas. Solo clona y ejecuta:
  ```bash
  ./wikictl/wikictl --help
  ```

---

## 📖 Comandos Disponibles

### 1. `wikictl lint`
Audita la salud e integridad de todo el baúl sin necesidad de conexión ni modelos:
```bash
./wikictl/wikictl lint
./wikictl/wikictl lint --strict
./wikictl/wikictl lint --json
```
- Detecta wikilinks rotos (`[[Nota Inexistente]]`).
- Valida esquemas YAML obligatorios (`type`, `title`, `status`).
- Alerta sobre notas huérfanas en `wiki/` (sin enlaces entrantes ni salientes).
- Alerta sobre notas volátiles con fecha de revisión expirada (`review_after`).

### 2. `wikictl ingest <fuente>`
Registra un archivo de evidencia ubicado en `raw/` y genera la plantilla de análisis estructurado:
```bash
./wikictl/wikictl ingest raw/articles/mi-paper.md
```
- Calcula el checksum SHA-256.
- Genera el artefacto en `.work/ingest/mi-paper.yaml` para que el LLM complete afirmaciones (claims) y conceptos.

### 3. `wikictl promote <slug>`
Compara el análisis estructurado con el conocimiento existente en `wiki/`:
```bash
# Modo seguro (por defecto): muestra el plan y diffs sin tocar disco
./wikictl/wikictl promote mi-paper --dry-run

# Aplicar cambios validados
./wikictl/wikictl promote mi-paper --apply

# Aplicar cambios y registrar commit semántico en Git
./wikictl/wikictl promote mi-paper --apply --commit
```

### 4. `wikictl research <pregunta>`
Genera el andamiaje epistemológico para investigar una pregunta temática:
```bash
./wikictl/wikictl research "¿Cómo impacta la IA en la memoria humana?"
```
Crea `research/YYYY-MM-DD-<slug>.md` con desglose en subpreguntas, evidencias, debates y conclusiones.

### 5. `wikictl synthesize <tema> [--sources s1 s2...]`
Crea una nota de síntesis transversal que vincula notas existentes:
```bash
./wikictl/wikictl synthesize "Arquitectura de Agentes" --sources "MCP" "Tool Use"
```
Crea `wiki/synthesis/<slug>.md` con estructura para matrices comparativas y patrones comunes.

### 6. `wikictl publish <nota> [--target <formato>]`
Adapta una nota consolidada para audiencias externas:
```bash
./wikictl/wikictl publish "Cognitive Offloading" --target substack
```
- Transforma wikilinks internos en texto limpio para publicación web.
- Ejecuta checklists de privacidad y trazabilidad de fuentes.
- Genera el borrador en `published/<target>/<slug>.md`.

### 7. `wikictl impact <nota>`
Muestra el árbol de dependencias del grafo de Obsidian:
```bash
./wikictl/wikictl impact "Cognitive Offloading"
```
Muestra qué conceptos, síntesis, proyectos o publicaciones se verían afectados si la nota cambia.

---

## 🧪 Ejecutar Tests

La suite completa utiliza `unittest` nativo de Python:
```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
