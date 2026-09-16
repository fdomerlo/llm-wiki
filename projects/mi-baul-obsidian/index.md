---
tipo: wiki_index
proyecto: mi-baul-obsidian
descripcion: Indice dinamico de conocimiento y base documental del proyecto.
tags: [llm-wiki, mi-baul-obsidian]
ultima_actualizacion: 2026-09-16
---
# 🧭 Wiki: mi-baul-obsidian

> [!TIP]
> **📖 Manual de Usuario y Guia Operativa del Baul:**
> Este proyecto funciona como un **manual vivo de referencia**. Consulta sus notas nucleares:
> - **Arranque en 3 pasos:** [[Guia-Inicio-Rapido]]
> - **Reglas de oro y catalogo de prompts:** [[Buenas-Practicas-Curaduria]]
> - **Ciclo de vida de 5 fases:** [[Flujo-Operativo-Diario]]
> - **Protocolo de ejecucion del agente:** [[projects/mi-baul-obsidian/AGENTS|AGENTS.md]]
> - **Bitacora de Operaciones:** [[projects/mi-baul-obsidian/log|log.md]]

---

## 🏗️ Decisiones de Arquitectura y Diseno
```dataview
TABLE
  ultima_actualizacion AS "Actualizado",
  fuentes AS "Fuentes",
  tags AS "Etiquetas"
FROM "projects/mi-baul-obsidian/wiki"
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
FROM "projects/mi-baul-obsidian/wiki"
WHERE tipo = "concepto" OR tipo = "entidad"
SORT file.name ASC
```

---

## 📊 Sintesis Tecnicas y Comparativas
```dataview
TABLE
  ultima_actualizacion AS "Fecha",
  fuentes AS "Basado en"
FROM "projects/mi-baul-obsidian/wiki/sintesis"
WHERE tipo = "sintesis"
SORT ultima_actualizacion DESC
```

---

## ⚔️ Debates y Discrepancias Tecnicas (Conflictos Epistemologicos)
```dataview
TABLE
  conflicto_con AS "En conflicto con",
  motivo_conflicto AS "Motivo / Trade-off"
FROM "projects/mi-baul-obsidian/wiki"
WHERE length(conflicto_con) > 0
SORT ultima_actualizacion DESC
```

---

## 📥 Fuentes Ingestadas (Resumenes de Raw)
```dataview
TABLE
  ultima_actualizacion AS "Procesado el",
  fuentes AS "Fuente Original"
FROM "projects/mi-baul-obsidian/wiki/resumenes"
WHERE tipo = "resumen_fuente"
SORT ultima_actualizacion DESC
LIMIT 10
```

---

## 🔍 Auditoria y Control de Calidad (Linting)
### Notas huerfanas (sin enlaces entrantes)
```dataview
LIST
FROM "projects/mi-baul-obsidian/wiki"
WHERE length(file.inlinks) = 0 AND file.name != "index"
```
