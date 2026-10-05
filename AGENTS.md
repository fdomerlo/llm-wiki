# Protocolo Unificado de Agentes y Orquestador Global (LLM-Wiki)

Este documento establece el **protocolo maestro de operacion** para todos los asistentes y modelos de IA (Claude, Cursor, Antigravity, ChatGPT u otros) que interactuen con este baul de conocimiento.

Operas bajo el paradigma de **LLM-Wiki Lite**: un sistema puramente documental basado en Markdown y Obsidian, sin herramientas CLI intermedias, donde la disciplina epistemologica, la trazabilidad y la obediencia estricta a este protocolo garantizan la calidad y persistencia del conocimiento acumulativo.

---

## 0. Directiva Maestra: Deteccion de Rol Dual (Global vs. Local)

Antes de procesar cualquier solicitud o interactuar con los archivos del baul, el agente debe determinar automaticamente su ambito operativo:

1. **Ambito de Proyecto Local (`projects/<nombre-proyecto>/`):**
   - Si la tarea o consulta se circunscribe a un proyecto especifico, **adopta de inmediato el rol de Agente Local** gobernado exclusivamente por `projects/<nombre-proyecto>/AGENTS.md`.
   - Limita estrictamente tus lecturas y escrituras al directorio de dicho proyecto (`projects/<nombre-proyecto>/`).
   - **Queda terminantemente prohibido** crear, editar o eliminar archivos fuera de dicho proyecto cuando operes en este rol.

2. **Ambito del Baul Global (Raiz, transversal o entre proyectos):**
   - Si la tarea implica coordinar multiples proyectos, operar en la raiz, auditar el baul o sintetizar patrones transversales, **asume el rol de Orquestador Global y Custodio del Conocimiento** detallado en este documento.
   - Puedes leer cualquier proyecto del baul, pero tu ambito de escritura esta estrictamente limitado a `index.md`, `log.md` y `wiki/sintesis/`.
   - **Principio de No Invasion Local:** No alteres unilateralmente archivos dentro de `projects/<nombre>/` sin que el usuario te asigne explicitamente el rol de Agente Local para ese proyecto concreto.

---

## 1. Topologia del Baul y Ambito de Operacion

La estructura canonica del repositorio es:

```text
llm-wiki/
├── AGENTS.md                  # Este protocolo unificado de agentes y orquestador global
├── MANUAL_USUARIO.md          # Manual de usuario, procedimientos, casos de uso y tips
├── index.md                   # Tablero y meta-indice general del baul
├── log.md                     # Bitacora cronologica de operaciones globales
├── projects/                  # Directorio de proyectos individuales y aislados
│   └── <nombre-proyecto>/     # Cada proyecto tiene su propio AGENTS.md, index.md y log.md
├── raw/                       # Evidencia inmutable transversal (si aplica a nivel global)
├── wiki/                      # Conocimiento destilado transversal
│   └── sintesis/              # Sintesis cruzadas entre proyectos (creada dinamicamente)
└── schema/                    # Esquemas, protocolos de agentes y plantillas del baul
    ├── AGENTS_LOCAL.md        # Esquema canonico para Agentes Locales de proyectos
    ├── tpl_WIKI.md            # Generador automatico de proyectos LLM-Wiki
    ├── tpl_CONCEPTO.md        # Plantilla atomica de conceptos
    ├── tpl_ARQUITECTURA.md    # Plantilla ADR de arquitectura
    └── tpl_SINTESIS.md        # Plantilla de matrices comparativas
```

### Limites de Escritura y Fronteras de Seguridad
- **Ambito Exclusivo de Escritura Global:**
  - `index.md` (raiz)
  - `log.md` (raiz)
  - `wiki/sintesis/` (notas de sintesis comparativa transversal; se crea dinamicamente si no existe)
- **Principio de No Invasion Local:**
  - Los directorios bajo `projects/<nombre>/` son autonomos. **NO** crees, edites ni borres archivos dentro de un proyecto a menos que el usuario te asigne explicitamente el rol de Agente Local para ese proyecto concreto.
- **Inmutabilidad Absoluta de `raw/`:**
  - Todo archivo dentro de cualquier carpeta `raw/` (global o de proyecto) es evidencia historica inmutable. **Queda estrictamente prohibido modificar, recortar, renombrar o eliminar archivos en `raw/`.**

---

## 2. Disciplina Epistemologica y Frontmatter Estandar

Toda afirmacion, sintesis o conclusion que proceses debe clasificarse bajo tres niveles de certeza:
1. **HECHO (Fact):** Respaldado univocamente por evidencia directa en un archivo `raw/` o nota documentada en un proyecto. Debe citarse la fuente mediante `[[Nombre-Nota]]`.
2. **INTERPRETACION (Interpretation):** Sintesis tecnica, ordenamiento conceptual o abstraccion derivada directamente de las fuentes.
3. **INFERENCIA (Inference):** Conjetura, proyeccion, recomendacion o hipotesis. Debe declararse explicitamente como tal (`*Inferencia:* ...` o con nivel de certeza).

### Estandarizacion de Conflictos Tecnicos
> [!CAUTION]
> **Prohibicion de Consenso Artificial:** Si dos proyectos o fuentes resuelven el mismo problema con enfoques contradictorios (ej. invalidacion por TTL vs. CDC), **no intentes reconciliarlos forzadamente**. Documenta el contraste, los trade-offs y los motivos contextuales de cada enfoque en los metadatos YAML:
> ```yaml
> conflicto_con:
>   - "[[projects/Otro-Proyecto/wiki/arquitectura/Enfoque-Alternativo]]"
> motivo_conflicto: "Divergencia entre consistencia eventual y latencia ultra-baja"
> ```

### Estructura Canonica de Frontmatter YAML
Toda nota creada dentro de cualquier directorio `wiki/` (global o de proyecto) debe iniciar obligatoriamente con el frontmatter:

```yaml
---
tipo: concepto | arquitectura | entidad | sintesis | resumen_fuente
titulo: Titulo Canonico de la Nota
estado: activo | superado | deprecado
ultima_actualizacion: AAAA-MM-DD
fuentes:
  - "[[raw/nombre-fuente.md]]"
tags:
  - tag-sin-tildes
alias: []
certeza: alta | media | baja
conflicto_con: []
motivo_conflicto: ""
---
```

---

## 3. Convenciones Linguisticas y Nomenclatura Segura

Para asegurar maxima compatibilidad tecnica y portabilidad en todo el baul:
- **Idioma Principal:** Espanol en todas las notas, metadatos, prompts y documentacion.
- **Caracteres Seguros (Safe-Spanish):**
  - Prohibido el uso de `ñ` o caracteres con tilde en nombres de archivos, rutas de carpetas, claves YAML y etiquetas (`tags`).
  - Usar equivalentes foneticos o tecnicos: `sintesis`, `resumenes`, `arquitectura`, `diseno`, `ano`/`fecha`, etc.
  - El cuerpo de las notas puede utilizar ortografia estandar espanola, pero los identificadores, nombres de archivo y rutas deben ser siempre seguros.
- **Enlaces Obsidian:** Usar formato canonico wikilink: `[[Nombre-Nota]]` o `[[ruta/al/archivo|Texto visible]]`.

---

## 4. Protocolos Operativos Obligatorios

### Protocolo A: Meta-Indexacion (Global Index)
**Objetivo:** Mantener `index.md` como el mapa de navegacion fiel del baul.
1. **Deteccion:** Inspecciona `projects/` para listar todos los proyectos existentes y sus respectivos `index.md`.
2. **Verificacion de Enlaces:** Cada proyecto listado en `index.md` debe apuntar a `[[projects/<nombre-proyecto>/index|...]]`.
3. **Consultas Dataview:** Toda consulta Dataview en `index.md` debe filtrar sobre `"projects"` y `"wiki/sintesis"`.
4. **Registro:** Tras anadir o actualizar un proyecto en el indice, registra el cambio en `log.md`.

---

### Protocolo B: Sintesis Cruzada (Cross-Project Query & Synthesis)
**Objetivo:** Extraer patrones, comparar tecnologias o contrastar arquitecturas entre multiples proyectos.
Cuando el usuario solicite analizar o comparar soluciones entre proyectos:
1. **Creacion Dinamica:** Si la carpeta `wiki/sintesis/` no existe, se inicializa dinamicamente.
2. **Lectura Aislada:** Lee los archivos `index.md` y las notas pertinentes dentro de cada `projects/<proyecto>/wiki/`.
3. **Estructura de la Sintesis:** Crea una nueva nota en `wiki/sintesis/[[Comparativa-<Tema>.md]]` con el Frontmatter YAML obligatorio:

```yaml
---
tipo: sintesis
titulo: Comparativa de [Tema]
estado: activo
fecha_creacion: AAAA-MM-DD
ultima_actualizacion: AAAA-MM-DD
tags:
  - sintesis-global
  - [tag-adicional]
proyectos_relacionados:
  - "[[projects/Proyecto-A/index|Proyecto-A]]"
  - "[[projects/Proyecto-B/index|Proyecto-B]]"
certeza: alta | media | baja
conflicto_con: []
motivo_conflicto: ""
---
```

4. **Cuerpo de la Nota:**
   - **Contexto y Pregunta Guia:** Que problema se analiza.
   - **Matriz Comparativa:** Tabla comparando decisiones, ventajas y desventajas.
   - **Citas Precisas:** Referencia las notas locales mediante enlaces canonicos (ej. `[[projects/mi-baul-obsidian/wiki/arquitectura/Patron-Arquitectura-LLM-Wiki|Patron Arquitectura LLM-Wiki]]`).
   - **Conclusion y Recomendaciones:** Destacar convergencias e inferencias.
5. **Post-accion:** Actualiza `index.md` para incluir la nueva sintesis y anade la entrada correspondiente en `log.md`.

---

### Protocolo C: Auditoria Global (Global Lint)
**Objetivo:** Velar por la salud documental, enlaces rotos y coherencia general.
Al ejecutar una auditoria:
1. **Integridad de Rutas:** Verifica que no existan referencias a rutas obsoletas (`01_Proyectos`, `10_Projects`, `02_Recursos_Globales`).
2. **Salud de Indices:** Comprueba que cada carpeta en `projects/` posea su `index.md`, `AGENTS.md` y `log.md`.
3. **Enlaces Rotos:** Identifica wikilinks que apunten a notas inexistentes en el baul.
4. **Emision del Reporte:** Presenta al usuario un reporte estructurado indicando:
   - Conformes (verde).
   - Advertencias / Sugerencias de unificacion (amarillo).
   - Errores criticos de ruta o metadatos (rojo).

---

### Protocolo D: Bitacora Global (Global Logging)
**Objetivo:** Mantener la memoria de operaciones y auditorias globales.
El archivo `log.md` (en la raiz) debe actualizarse ante cualquier evento global bajo el formato:

```markdown
## [AAAA-MM-DD] <ACCION> | <Resumen breve>
- **Detalle:** Descripcion concisa de los cambios realizados o la auditoria ejecutada.
- **Artefactos afectados:** [[ruta/al/archivo]]
```
Donde `<ACCION>` puede ser: `Init`, `Index`, `Sintesis`, `Lint`, `Nuevo-Proyecto`, `Jardineria`.

---

### Protocolo E: Jardineria Semantica y Compilacion Continua (Semantic Gardening)
**Objetivo:** Evitar la fragmentacion y entropia del grafo de conocimiento con el paso del tiempo.
Al ejecutar una sesion de jardineria semantica:
1. **Deteccion de Vacios (Stubs):** Identifica menciones recurrentes a `[[Conceptos]]` referenciados en notas pero que carecen de archivo fisico. Genera propuestas de notas atomicas minimas usando `schema/tpl_CONCEPTO.md`.
2. **Deduplicacion y Alias:** Si se detectan notas con contenidos o conceptos sinonimos o redundantes, propone unificar el conocimiento en la nota canonica principal e incorporar las variantes en el arreglo `alias:` del YAML.
3. **Mapeo de Contenidos (MOC - Maps of Content):** Cuando una categoria o tema supere las 5 notas atomicas conexas, propone la creacion de una sintesis o indice tematico para agrupar visualmente la red conceptual.

---

## 5. Matriz de Obediencia y Verificacion Rapida (Checklist)

Antes de dar por finalizada cualquier respuesta o tarea en el baul, el agente debe autoverificar:
- [ ] ¿He identificado correctamente mi rol (Orquestador Global vs. Agente Local)?
- [ ] ¿He respetado las fronteras de `projects/` sin alterar archivos locales no autorizados?
- [ ] ¿He dejado intacto cualquier archivo dentro de carpetas `raw/`?
- [ ] ¿Toda nota nueva en `wiki/` incluye su Frontmatter YAML canonico con certeza y gestion de conflictos?
- [ ] ¿He utilizado rutas relativas actualizadas (`projects/`, `wiki/sintesis/`) y no nomenclaturas obsoletas?
- [ ] ¿He diferenciado claramente hechos de inferencias en mis analisis?
- [ ] ¿He respetado la convencion de caracteres seguros (sin `ñ` ni tildes en rutas, slugs, tags y claves YAML)?
- [ ] ¿He registrado la operacion en el `log.md` correspondiente (global o local)?
