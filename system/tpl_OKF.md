<%*
let projectName = await tp.system.prompt("Nombre del Bundle/Proyecto (OKF):");

if (projectName) {
    let basePath = "projects/" + projectName; 
    let timestamp = tp.date.now("YYYY-MM-DDTHH:mm:ssZ");

    try {
        // 1. Helper para crear carpetas de forma segura
        const createFolderSafely = async (path) => {
            if (!app.vault.getAbstractFileByPath(path)) {
                await app.vault.createFolder(path);
            }
        };

        // 2. Helper para crear archivos secundarios sin pisar los existentes
        const createFileSafely = async (path, content) => {
            if (!app.vault.getAbstractFileByPath(path)) {
                await app.vault.create(path, content);
            }
        };

        // --- CREACIÓN DEL ÁRBOL ---
        await createFolderSafely(basePath);
        await createFolderSafely(basePath + "/refs");
        await createFolderSafely(basePath + "/docs");
        await createFolderSafely(basePath + "/specs");
        await createFolderSafely(basePath + "/planning");

        // --- INYECCIÓN DE ARCHIVOS OKF (Datos) ---
        await createFileSafely(basePath + "/refs/index.md", "---\ntype: Directory Index\ntitle: References\ndescription: Elementos de referencia del dominio.\ntimestamp: " + timestamp + "\n---\n# References\n\n*No hay elementos catalogados en esta sección de forma activa.*\n");

        await createFileSafely(basePath + "/docs/index.md", "---\ntype: Directory Index\ntitle: Docs\ndescription: Documentación técnica y guías de uso.\ntimestamp: " + timestamp + "\n---\n# Documents\n\n*No hay elementos catalogados en esta sección de forma activa.*\n");
        
        await createFileSafely(basePath + "/specs/index.md", "---\ntype: Directory Index\ntitle: Specifications\ndescription: Especificaciones técnicas y documentación de diseño.\ntimestamp: " + timestamp + "\n---\n# Specifications\n\n*No hay elementos catalogados en esta sección de forma activa.*\n");

        // --- INYECCIÓN DE ARCHIVOS PLANNING (Gestión) ---
        await createFileSafely(basePath + "/planning/index.md", "---\ntype: Directory Index\ntitle: Planning & Tracking\ndescription: Gestión operativa del proyecto.\ntimestamp: " + timestamp + "\n---\n# Planning & Tracking\n\nCentro de control para la ejecución del proyecto.\n");

        await createFileSafely(basePath + "/planning/tasks.md", "---\ntype: tracking\ntitle: Tasks\nproject: " + projectName + "\n---\n# Tareas de " + projectName + "\n\n- [ ] Tarea técnica inicial\n");
        
        await createFileSafely(basePath + "/planning/epics.md", "---\ntype: tracking\ntitle: Epics\nproject: " + projectName + "\n---\n# Epics de " + projectName + "\n\n- [ ] Configuración inicial del entorno\n");
        
        await createFileSafely(basePath + "/planning/roadmap.md", "---\ntype: tracking\ntitle: Roadmap\nproject: " + projectName + "\n---\n# Roadmap de " + projectName + "\n\n- **Fase 1:** Discovery y Setup\n- **Fase 2:** Desarrollo Core\n");
        
        await createFileSafely(basePath + "/planning/milestones.md", "---\ntype: tracking\ntitle: Milestones\nproject: " + projectName + "\n---\n# Hitos de " + projectName + "\n\n- [ ] MVP Entregado\n");

        // --- INYECCIÓN DEL LOG ---
        //let logContent = "# Directory Update Log\n\n## " + tp.date.now("YYYY-MM-DD") + "\n* **Initialization**: Scaffold estructural OKF inicializado para el dominio " + projectName + ".\n";
        //await createFileSafely(basePath + "/log.md", logContent);

        // --- MOVIMIENTO DEL ARCHIVO PRINCIPAL ---
        // Se ejecuta inmediatamente sin retrasos artificiales
        await tp.file.move(basePath + "/index");

    } catch (error) {
        // Si hay un error (ej. la carpeta projects no existe), Obsidian te mostrará un cartelito nativo
        new Notice("Error al crear la estructura OKF: " + error.message);
        console.error("Detalle del error Templater:", error);
    }
}
_%>
---
type: Bundle Index
title: <% projectName %>
description: Directorio raíz estructurado bajo el estándar Open Knowledge Format (OKF).
tags: [gestion, proyectos, okf]
timestamp: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
---
# **<% projectName %>**

Este directorio funciona como el **Knowledge Bundle** principal para el dominio. 
*La estructura está optimizada tanto para lectura humana como para ingesta directa en contextos de agentes de IA.*

### Documentación y Referencias

* [Referencias](./refs/index.md) - Elementos de referencia del dominio.
* [Documentation](./docs/index.md) - Documentación técnica, Wikis y guías de uso.
* [Especificaciones](./specs/index.md) - Especificaciones y documentación de diseño.

### Gestión y Ejecución

* [Índice de Planning](./planning/index.md)
* [Roadmap](./planning/roadmap.md) - Visión general y fases.
* [Epics](./planning/epics.md) - Grandes bloques de trabajo.
* [Milestones](./planning/milestones.md) - Hitos de entrega.
* [Tasks](./planning/tasks.md) - Tareas accionables de bajo nivel.

## Backlog

*Todas las tareas pendientes de la carpeta planning.*

```dataview
TASK  
FROM "projects/<% projectName %>/planning"
WHERE !completed  
GROUP BY file.link
```

