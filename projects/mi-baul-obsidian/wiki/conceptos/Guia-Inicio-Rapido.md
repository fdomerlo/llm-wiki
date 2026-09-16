---
tipo: concepto
titulo: Guia de Inicio Rapido
estado: activo
ultima_actualizacion: 2026-09-16
fuentes:
  - "[[projects/mi-baul-obsidian/raw/02-guia-operativa-y-mejores-practicas|raw/02-guia-operativa-y-mejores-practicas.md]]"
tags:
  - mi-baul-obsidian
  - onboarding
  - tutorial
  - guia-rapida
alias:
  - Quickstart Guide
  - Arranque Rapido
certeza: alta
conflicto_con: []
motivo_conflicto: ""
---

# Guia de Inicio Rapido (Quickstart)

Instrucciones practicas para poner en funcionamiento tu baul **LLM-Wiki** en menos de 5 minutos.

---

## Paso 1: Configurar Obsidian

1. Abre **Obsidian** y haz clic en **"Open folder as vault"** (Abrir carpeta como baul).
2. Selecciona la carpeta raiz del repositorio (`llm-wiki/`).
3. Ve a **Settings > Community plugins** y desactiva el *Restricted mode*.
4. Instala y activa los dos plugins indispensables:
   - **Dataview**:
     - Entra en los ajustes de Dataview.
     - Activa las casillas `Enable JavaScript Queries` y `Enable Inline Queries`.
   - **Templater**:
     - Entra en los ajustes de Templater.
     - En `Template folder location`, escribe: `system`.

> [!TIP]
> **Plugins Opcionales Recomendados:**
> - **Omnisearch:** Búsqueda difusa instantánea con soporte OCR.
> - **Smart Connections:** Detección de notas semánticamente afines en Obsidian mediante embeddings locales.

---

## Paso 2: Crear tu Primer Proyecto

El baul organiza el conocimiento por proyectos aislados dentro de `projects/`:

### Metodo A: Desde la interfaz de Obsidian
1. Crea una nota vacía en la raíz.
2. Abre la paleta de comandos (`Ctrl + P` o `Cmd + P`) y escribe `Templater: Open Insert Template Modal`.
3. Selecciona `system/tpl_WIKI.md`.
4. Escribe el nombre del proyecto (ej: `Mi-Servicio-Web`).  
   *La plantilla creará automáticamente la estructura completa de carpetas, su propio `AGENTS.md`, su `log.md` y moverá la nota como `index.md`.*

### Metodo B: Mediante tu Asistente de IA (CLI / IDE)
Simplemente dile al modelo:
> *"Crea un nuevo proyecto en projects/ llamado Mi-Servicio-Web usando la plantilla system/tpl_WIKI.md y enlazalo en el index.md global."*

---

## Paso 3: Tu Primera Ingesta Documental

1. Coloca cualquier artículo, especificación, notas o transcripción en la carpeta `raw/` de tu proyecto:
   `projects/Mi-Servicio-Web/raw/01-introduccion.md`
2. Pide a tu asistente de IA:
   > *"Actua como Agente Local de Mi-Servicio-Web segun su AGENTS.md. Procesa la fuente raw/01-introduccion.md ejecutando el Protocolo de Ingesta."*
3. **¡Listo!** El LLM creará:
   - El resumen en `wiki/resumenes/`.
   - Las notas atómicas en `wiki/conceptos/` o `wiki/arquitectura/` con sus respectivos `[[wikilinks]]`.
   - Registrará la operación en `log.md`.

---

## Relacion con el Sistema
- Sigue el [[Flujo-Operativo-Diario]].
- Aplica las [[Buenas-Practicas-Curaduria]].
- Se apoya en el [[Patron-Arquitectura-LLM-Wiki]] y el entorno [[Obsidian]].
