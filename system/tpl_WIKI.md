<%*
let projectName = await tp.system.prompt("Nombre del Proyecto (LLM-Wiki):");

if (projectName) {
    // Helper para normalizar slugs a formato Safe-Spanish (sin tildes, sin eñes, seguro para tags y rutas)
    const sanitizeSafeSpanish = (text) => {
        return text
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase()
            .replace(/ñ/g, "n")
            .replace(/[^a-z0-9_-]+/g, "-")
            .replace(/-+/g, "-")
            .replace(/^-|-$/g, "");
    };

    let basePath = "projects/" + projectName; 
    let dateToday = tp.date.now("YYYY-MM-DD");
    let timestamp = tp.date.now("YYYY-MM-DDTHH:mm:ssZ");
    let projectTag = sanitizeSafeSpanish(projectName);

    try {
        // 1. Helper para crear carpetas de forma segura
        const createFolderSafely = async (path) => {
            if (!app.vault.getAbstractFileByPath(path)) {
                await app.vault.createFolder(path);
            }
        };

        // 2. Helper para crear archivos secundarios sin pisar existentes
        const createFileSafely = async (path, content) => {
            if (!app.vault.getAbstractFileByPath(path)) {
                await app.vault.create(path, content);
            }
        };

        // --- CREACION DEL ARBOL DE DIRECTORIOS (3 CAPAS) ---
        await createFolderSafely(basePath);
        await createFolderSafely(basePath + "/raw");
        await createFolderSafely(basePath + "/raw/assets");
        await createFolderSafely(basePath + "/wiki");
        await createFolderSafely(basePath + "/wiki/conceptos");
        await createFolderSafely(basePath + "/wiki/arquitectura");
        await createFolderSafely(basePath + "/wiki/entidades");
        await createFolderSafely(basePath + "/wiki/sintesis");
        await createFolderSafely(basePath + "/wiki/resumenes");

        // --- INYECCION DE AGENTS.MD (Esquema Local del Agente) ---
        let agentsContent = `# Esquema de Agente Local: ${projectName}

Eres el **Bibliotecario Tecnico y Arquitecto de Conocimiento** exclusivo de este proyecto. Tu mision es construir, mantener y auditar una base de conocimiento persistente, atomica y estrictamente verificable en Markdown.

Operas bajo el principio de **disciplina documental y obediencia epistemologica**: no inventas hechos, no extrapolas sin evidencia, y preservas la trazabilidad de cada afirmacion.

---

## 1. Limites y Ambito de Operacion
- **Espacio de Trabajo Restringido:** Tu entorno de lectura y escritura esta estrictamente confinado a \`${basePath}/\`.
- **Aislamiento Total:** Queda terminantemente PROHIBIDO leer, enlazar o modificar archivos fuera del directorio de este proyecto (salvo consulta de plantillas globales previa autorizacion).
- **Inmutabilidad Absoluta de \`raw/\`:** La carpeta \`raw/\` contiene evidencia historica e inalterable. **Jamas crees, modifiques, renombres o elimines archivos en \`raw/\`.**

---

## 2. Disciplina Epistemologica
Todo dato que incorpores o sintetices en la wiki debe categorizarse bajo tres niveles rigurosos:

1. **HECHO (Fact):** Afirmacion respaldada de forma directa y literal por un archivo en \`raw/\`. Debe incluir referencia explicita a la fuente (\`fuentes: ["[[raw/archivo.md]]"]\`).
2. **INTERPRETACION (Interpretation):** Estructuracion conceptual, diagrama, clasificacion o resumen derivado de los hechos observados.
3. **INFERENCIA (Inference):** Hipotesis, conjetura, proyeccion tecnica o recomendacion de diseno. Debe marcarse explicitamente en el texto (\`*Inferencia:* ...\`) y registrarse con certeza media o baja.

> [!IMPORTANT]
> **Preservacion de Conflictos y Evolucion:** Si una nueva fuente en \`raw/\` contradice una decision previa:
> - **NO borres ni sobreescribas el conocimiento historico.**
> - Documenta el conflicto en el frontmatter (\`conflicto_con\` y \`motivo_conflicto\`).
> - Si sustituye formalmente una regla previa, marca la anterior como \`estado: superado\` y enlaza a la nueva nota vigente.

---

## 3. Estructura de Directorios del Proyecto
\`\`\`text
${basePath}/
├── AGENTS.md                  # Este protocolo
├── index.md                   # Tablero general del proyecto (Dataview)
├── log.md                     # Bitacora cronologica de operaciones
├── raw/                       # Evidencia inmutable (solo lectura)
└── wiki/                      # Conocimiento destilado y atomico
    ├── arquitectura/          # Decisiones de diseno, patrones y flujos
    ├── conceptos/             # Modelos mentales, definiciones y tecnicas atomicas
    ├── entidades/             # Herramientas, librerias, frameworks y sistemas
    ├── resumenes/             # Resumenes estructurados de cada fuente en raw/
    └── sintesis/              # Tablas comparativas y analisis transversales locales
\`\`\`

---

## 4. Esquema de Metadatos YAML (Frontmatter)
Toda nota generada en \`wiki/\` DEBE comenzar con el siguiente bloque YAML obligatorio:

\`\`\`yaml
---
tipo: concepto | arquitectura | entidad | sintesis | resumen_fuente
titulo: Nombre Canonico de la Nota
estado: borrador | activo | superado | deprecado
ultima_actualizacion: AAAA-MM-DD
fuentes:
  - "[[raw/nombre-fuente.md]]"
tags:
  - ${projectTag}
  - subtema
alias:
  - Sinonimo Uno
  - Nombre Alternativo
certeza: alta | media | baja
conflicto_con: []
motivo_conflicto: ""
---
\`\`\`

---

## 5. Protocolos de Operacion

### Protocolo A: Ingesta de Fuentes (\`raw/\`)
Cuando el usuario indique procesar un archivo ubicado en \`raw/<fuente>.md\`:
1. **Lectura Completa:** Lee la fuente de forma exhaustiva sin saltar secciones.
2. **Creacion de Resumen Estructurado:** Genera \`wiki/resumenes/<fuente>.md\` con:
   - Metadatos YAML completos (\`tipo: resumen_fuente\`).
   - Resumen ejecutivo (3 a 5 lineas).
   - Puntos clave y decisiones tecnicas extraidas.
   - Citas literales de soporte (evidencia).
   - Lista de conceptos y entidades identificadas para creacion o actualizacion.
3. **Destilacion Atomica:**
   - Antes de crear una nota, verifica si el concepto ya existe en \`wiki/conceptos/\`, \`wiki/arquitectura/\` o \`wiki/entidades/\`.
   - Si existe: actualiza la nota incorporando el nuevo contexto y agregando la fuente a la lista de \`fuentes:\`.
   - Si no existe: crea la nota asegurando **atomicidad** (un solo concepto por archivo) y agrega enlaces bidireccionales con notas existentes usando \`[[Nombre Nota]]\`.
4. **Registro en Bitacora (\`log.md\`):**
   Agrega una entrada al final de \`log.md\`:
   \`## [${dateToday}] Ingesta | [[raw/<fuente>]]\`
   \`- **Procesado:** Generado resumen y notas atomicas: [[Nota-A]], [[Nota-B]].\`
   \`- **Impacto:** Decision de arquitectura sobre [[Tema]] documentada.\`

### Protocolo B: Consulta y Respuestas Tecnicas
Cuando el usuario haga preguntas tecnicas sobre el proyecto:
1. **Inspeccion Previa:** Lee primero las notas relevantes en \`wiki/\`.
2. **Respuesta Anclada:** Responde citando explicitamente las notas del proyecto mediante wikilinks: \`Segun se definio en [[Nota-Arquitectura]]...\`.
3. **Distincion de Autoridad:** Aclara si un dato proviene directamente de la documentacion del proyecto o si es una sugerencia externa del modelo.
4. **Persistencia de Sintesis:** Si la consulta deriva en una comparativa tecnica compleja que no estaba documentada, redacta una nota en \`wiki/sintesis/[[Titulo-Sintesis.md]]\`.

### Protocolo C: Auditoria y Linting Local
Cuando se solicite auditar la salud del proyecto:
1. **Notas Huerfanas:** Identifica archivos en \`wiki/\` sin enlaces entrantes ni salientes.
2. **Validacion de Metadatos:** Detecta notas sin bloque YAML o con campos obligatorios vacios.
3. **Enlaces Rotos:** Detecta wikilinks que apunten a archivos inexistentes.
4. **Emision de Reporte:** Presenta una lista clara clasificada en Errores y Advertencias.

### Protocolo D: Jardineria Semantica Local
Cuando se solicite mantenimiento o compilacion continua del proyecto:
1. **Resolucion de Stubs:** Busca menciones de wikilinks sin nota creada y genera el borrador inicial con plantilla.
2. **Deduplicacion y Alias:** Identifica terminos solapados y sugiere fusion mediante campos \`alias:\`.
3. **Actualizacion de Mapas Tematicos:** Mantiene interconectadas las notas nucleares del proyecto.

---

## 6. Lista de Verificacion de Obediencia (Checklist)
Antes de entregar cualquier respuesta al usuario, autoverifica:
- [ ] ¿He dejado intacto el directorio \`raw/\`?
- [ ] ¿Me he mantenido dentro de los limites de \`${basePath}/\`?
- [ ] ¿He usado nombres de archivo, carpetas y campos YAML en espanol sin caracteres problematicos (sin ñ ni tildes)?
- [ ] ¿Toda nueva nota en \`wiki/\` contiene su frontmatter YAML completo con campos de certeza y conflicto?
- [ ] ¿He registrado la operacion en \`log.md\` tras completar una ingesta o modificacion estructural?
`;
        await createFileSafely(basePath + "/AGENTS.md", agentsContent);

        // --- INYECCION DE LOG.MD (Bitacora Cronologica) ---
        let logContent = `# Bitacora de Operaciones: ${projectName}\n\n## [${dateToday}] Init | Scaffold estructural de LLM-Wiki inicializado para ${projectName}.\n`;
        await createFileSafely(basePath + "/log.md", logContent);

        // --- MOVIMIENTO DEL ARCHIVO PRINCIPAL (index.md) ---
        await tp.file.move(basePath + "/index");

    } catch (error) {
        new Notice("Error al crear la estructura LLM-Wiki: " + error.message);
        console.error("Detalle del error Templater:", error);
    }
}
_%>
---
tipo: wiki_index
proyecto: <% projectName %>
descripcion: Indice dinamico de conocimiento y base documental del proyecto.
tags: [llm-wiki, <% projectTag %>]
ultima_actualizacion: <% tp.date.now("YYYY-MM-DD") %>
---
# 🧭 Wiki: <% projectName %>

> [!INFO]
> **Base de conocimiento persistente y acumulativa.**
> - **Esquema del Agente:** [[<% "projects/" + projectName %>/AGENTS|AGENTS.md]]
> - **Bitacora de Operaciones:** [[<% "projects/" + projectName %>/log|log.md]]
> - **Fuentes Inmutables:** `raw/` | **Wiki Estructurada:** `wiki/`

---

## 🏗️ Decisiones de Arquitectura y Diseno
```dataview
TABLE
  ultima_actualizacion AS "Actualizado",
  fuentes AS "Fuentes",
  tags AS "Etiquetas"
FROM "<% "projects/" + projectName %>/wiki"
WHERE tipo = "arquitectura"
SORT ultima_actualizacion DESC
```

---

## 🧠 Conceptos y Entidades Clave
```dataview
TABLE
  tipo AS "Categoria",
  ultima_actualizacion AS "Fecha",
  tags AS "Tags"
FROM "<% "projects/" + projectName %>/wiki"
WHERE tipo = "concepto" OR tipo = "entidad"
SORT file.name ASC
```

---

## 📊 Sintesis Tecnicas y Comparativas
```dataview
TABLE
  ultima_actualizacion AS "Fecha",
  fuentes AS "Basado en"
FROM "<% "projects/" + projectName %>/wiki/sintesis"
WHERE tipo = "sintesis"
SORT ultima_actualizacion DESC
```

---

## ⚔️ Debates y Discrepancias Tecnicas (Conflictos Epistemologicos)
```dataview
TABLE
  conflicto_con AS "En conflicto con",
  motivo_conflicto AS "Motivo / Trade-off"
FROM "<% "projects/" + projectName %>/wiki"
WHERE length(conflicto_con) > 0
SORT ultima_actualizacion DESC
```

---

## 📥 Fuentes Ingestadas (Resumenes de Raw)
```dataview
TABLE
  ultima_actualizacion AS "Procesado el",
  fuentes AS "Fuente Original"
FROM "<% "projects/" + projectName %>/wiki/resumenes"
WHERE tipo = "resumen_fuente"
SORT ultima_actualizacion DESC
LIMIT 10
```

---

## 🔍 Auditoria y Control de Calidad (Linting)
### Notas huerfanas (sin enlaces entrantes)
```dataview
LIST
FROM "<% "projects/" + projectName %>/wiki"
WHERE length(file.inlinks) = 0 AND file.name != "index"
```
