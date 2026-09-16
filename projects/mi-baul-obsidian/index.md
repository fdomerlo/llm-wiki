---
tipo: wiki_index
proyecto: mi-baul-obsidian
descripcion: Indice dinamico de conocimiento y base documental del proyecto.
tags: [llm-wiki, mi-baul-obsidian]
ultima_actualizacion: 2026-09-16
---
# 🧭 Wiki: mi-baul-obsidian

> [!INFO]
> **Base de conocimiento persistente y acumulativa.**
> - **Esquema del Agente:** [[projects/mi-baul-obsidian/AGENTS|AGENTS.md]]
> - **Bitacora de Operaciones:** [[projects/mi-baul-obsidian/log|log.md]]
> - **Fuentes Inmutables:** `raw/` | **Wiki Estructurada:** `wiki/`

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
