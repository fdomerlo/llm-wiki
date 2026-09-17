<%*
let projectName = await tp.system.prompt("Nombre del Proyecto (LLM-Wiki):");

if (!projectName) {
    new Notice("Creacion de proyecto cancelada.");
    return;
}

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

    // --- INYECCION DE AGENTS.MD (Cargado dinamicamente desde schema/AGENTS_LOCAL.md) ---
    let agentsContent = "";
    const localAgentSchemaFile = app.vault.getAbstractFileByPath("schema/AGENTS_LOCAL.md");
    if (localAgentSchemaFile) {
        agentsContent = await app.vault.read(localAgentSchemaFile);
        agentsContent = agentsContent
            .replace(/{{PROJECT_NAME}}/g, projectName)
            .replace(/{{PROJECT_TAG}}/g, projectTag)
            .replace(/{{BASE_PATH}}/g, basePath)
            .replace(/{{DATE_TODAY}}/g, dateToday);
    } else {
        agentsContent = `# Esquema de Agente Local: ${projectName}\nConsulte schema/AGENTS_LOCAL.md para el protocolo.\n`;
    }
    await createFileSafely(basePath + "/AGENTS.md", agentsContent);

    // --- INYECCION DE LOG.MD (Bitacora Cronologica) ---
    let logContent = `# Bitacora de Operaciones: ${projectName}\n\n## [${dateToday}] Init | Scaffold estructural de LLM-Wiki inicializado para ${projectName}.\n`;
    await createFileSafely(basePath + "/log.md", logContent);

    // --- MOVIMIENTO DEL ARCHIVO PRINCIPAL (index.md) ---
    await tp.file.move(basePath + "/index");

    // --- GENERACION DEL CONTENIDO DEL TABLERO (INDEX.MD) ---
    tR += `---
tipo: wiki_index
proyecto: ${projectName}
descripcion: Indice dinamico de conocimiento y base documental del proyecto.
tags: [llm-wiki, ${projectTag}]
ultima_actualizacion: ${dateToday}
---
# 🧭 Wiki: ${projectName}

> [!INFO]
> **Base de conocimiento persistente y acumulativa.**
> - **Esquema del Agente:** [[projects/${projectName}/AGENTS|AGENTS.md]]
> - **Bitacora de Operaciones:** [[projects/${projectName}/log|log.md]]
> - **Fuentes Inmutables:** \`raw/\` | **Wiki Estructurada:** \`wiki/\`

---

## 🏗️ Decisiones de Arquitectura y Diseno
\`\`\`dataview
TABLE
  ultima_actualizacion AS "Actualizado",
  fuentes AS "Fuentes",
  tags AS "Etiquetas"
FROM "projects/${projectName}/wiki"
WHERE tipo = "arquitectura"
SORT ultima_actualizacion DESC
\`\`\`

---

## 🧠 Conceptos y Entidades Clave
\`\`\`dataview
TABLE
  tipo AS "Categoria",
  ultima_actualizacion AS "Fecha",
  tags AS "Tags"
FROM "projects/${projectName}/wiki"
WHERE tipo = "concepto" OR tipo = "entidad"
SORT file.name ASC
\`\`\`

---

## 📊 Sintesis Tecnicas y Comparativas
\`\`\`dataview
TABLE
  ultima_actualizacion AS "Fecha",
  fuentes AS "Basado en"
FROM "projects/${projectName}/wiki/sintesis"
WHERE tipo = "sintesis"
SORT ultima_actualizacion DESC
\`\`\`

---

## ⚔️ Debates y Discrepancias Tecnicas (Conflictos Epistemologicos)
\`\`\`dataview
TABLE
  conflicto_con AS "En conflicto con",
  motivo_conflicto AS "Motivo / Trade-off"
FROM "projects/${projectName}/wiki"
WHERE length(conflicto_con) > 0
SORT ultima_actualizacion DESC
\`\`\`

---

## 📥 Fuentes Ingestadas (Resumenes de Raw)
\`\`\`dataview
TABLE
  ultima_actualizacion AS "Procesado el",
  fuentes AS "Fuente Original"
FROM "projects/${projectName}/wiki/resumenes"
WHERE tipo = "resumen_fuente"
SORT ultima_actualizacion DESC
LIMIT 10
\`\`\`

---

## 🔍 Auditoria y Control de Calidad (Linting)
### Notas huerfanas (sin enlaces entrantes)
\`\`\`dataview
LIST
FROM "projects/${projectName}/wiki"
WHERE length(file.inlinks) = 0 AND file.name != "index"
\`\`\`
`;

} catch (error) {
    new Notice("Error al crear la estructura LLM-Wiki: " + error.message);
    console.error("Detalle del error Templater:", error);
}
_%>