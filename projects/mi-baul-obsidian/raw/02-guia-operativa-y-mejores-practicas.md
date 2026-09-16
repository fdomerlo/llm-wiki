# Guia Operativa de Campo y Buenas Practicas para LLM-Wiki

**Version:** 1.0.0  
**Fecha:** Septiembre 2026  
**Ambito:** Manual de usuario, patrones de interaccion LLM y recomendaciones practicas para baules de conocimiento personales en Obsidian.

---

## 1. El Ciclo de Vida del Conocimiento en LLM-Wiki

Un baul basado en la filosofia de Karpathy no es un vertedero pasivo de archivos, sino un sistema metabolico de informacion. Toda nueva pieza de conocimiento atraviesa cinco fases:

1. **Captura (Raw):** El usuario deposita la fuente original (articulo, video transcrito, paper, notas de reunion) en `raw/` sin editar ni resumir.
2. **Destilacion (Summarize & Atomize):** El LLM procesa la fuente, genera un resumen ejecutivo y extrae notas atomicas conceptuales de no mas de 1-2 conceptos nucleares por archivo.
3. **Interconexion (Weaving):** Se crean enlaces bidireccionales (`[[wikilinks]]`) conectando los nuevos conceptos con los existentes.
4. **Consulta Activa (Querying):** El usuario interroga a la base sobre desafios tecnicos; el modelo responde citando notas atomicas consolidadas.
5. **Jardineria (Gardening):** Refactorizacion periodica, eliminacion de enlaces rotos, resolucion de notas provisionales (stubs) y deteccion de contradicciones.

---

## 2. Puesta en Marcha en 3 Pasos (Zero to Hero)

### Paso 1: Apertura del Baul en Obsidian
1. Descarga e instala Obsidian (https://obsidian.md).
2. Selecciona **"Open folder as vault"** (Abrir carpeta como baul) y elige la raiz `llm-wiki/`.
3. Instala desde *Community Plugins* dos plugins indispensables:
   - **Dataview**: para renderizar todas las tablas dinamicas e indices. Habilita en sus opciones *Enable JavaScript Queries* y *Enable Inline Queries*.
   - **Templater**: para automatizar la creacion de proyectos y notas con metadatos. En sus opciones, fija *Template folder location* apuntando a `system/`.

### Paso 2: Creacion de tu Primer Proyecto
- Opcion A (Visual): Presiona `Alt + E` (o el atajo de Templater), selecciona `system/tpl_WIKI.md` e ingresa el nombre de tu proyecto (ej: `Motor-Recomendaciones`).
- Opcion B (Vía LLM): Pide a tu asistente: *"Crea un nuevo proyecto en projects/ llamado Motor-Recomendaciones usando la plantilla system/tpl_WIKI.md"*.

### Paso 3: Tu Primera Ingesta
1. Deja caer un archivo Markdown en `projects/<tu-proyecto>/raw/mi-fuente.md`.
2. Ejecuta el prompt de ingesta:
   > *"Actua como Agente Local de <tu-proyecto> segun su AGENTS.md. Procesa la fuente raw/mi-fuente.md ejecutando el Protocolo de Ingesta."*
3. Observa como se genera el resumen y las notas atomicas en `wiki/` con sus wikilinks y se registra en `log.md`.

---

## 3. Catalogo de Prompts Efectivos (Cheat-Sheet de Comandos)

Para comunicarse fluidamente con los agentes LLM:

| Intencion | Prompt Recomendado |
| :--- | :--- |
| **Ingestar fuente** | *"Actua como Agente Local de [proyecto]. Procesa la fuente raw/[archivo.md] siguiendo el Protocolo A. Destila conceptos atomicos y actualiza el log."* |
| **Pregunta tecnica con anclaje** | *"Como Agente Local de [proyecto], responde a: ¿Cual es la estrategia acordada para [tema]? Basa tu respuesta exclusivamente en wiki/ y cita con [[wikilinks]]."* |
| **Comparativa transversal** | *"Actua como Orquestador Global segun AGENTS.md. Compara el enfoque de [Tema] entre [Proyecto-A] y [Proyecto-B]. Crea la sintesis comparativa."* |
| **Jardineria y mantenimiento** | *"Actua como Agente Local de [proyecto]. Ejecuta una sesion de Jardineria Semantica (Protocolo D). Detecta stubs, terminos sinonimos para unificar y enlaces huerfanos."* |
| **Auditoria de consistencia** | *"Ejecuta una auditoria de calidad segun Protocolo C. Reporta errores criticos, rutas obsoletas y wikilinks rotos."* |

---

## 4. Reglas de Oro y Buenas Practicas de Curaduria

1. **Principio de Atomicidad Estricta:**
   - Una nota wiki debe explicar **un unico concepto o decision**.
   - Si una nota supera 300-400 palabras o abarca dos temas distintos, pidale al LLM que la divida en dos notas atomicas interconectadas.

2. **No reinventar la rueda (Evolucion sobre Duplicacion):**
   - Antes de crear una nota, el LLM debe comprobar si el termino ya existe.
   - Si existe, se añade la nueva evidencia y perspectiva a la nota existente, enriqueciendo su seccion de evolucion.

3. **Inmutabilidad Sagrada de `raw/`:**
   - Nunca permitas que el LLM modifique un archivo en `raw/`. `raw/` es la unica verdad historica que protege contra alucinaciones progresivas.

4. **Nombres de Archivo Sustantivos y Canonicos (Safe-Spanish):**
   - Titula las notas con nombres conceptuales en singular: `[[Cache-Distribuido]]` en lugar de `[[Sobre-el-uso-de-caches-y-sus-variantes]]`.
   - Sin acentos ni eñes en las rutas para total portabilidad en scripts, CI/CD y terminales.

5. **Alineacion de Certeza y Registro de Conflictos:**
   - Si un diseno introduce desventajas o discrepa con otro proyecto, jamas fuerces un falso consenso. Utiliza los campos `conflicto_con` y `motivo_conflicto`.
