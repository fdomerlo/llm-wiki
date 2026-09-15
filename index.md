# 🌐 Meta-Indice General del Baul

> [!SUMMARY]
> Tablero de orquestacion y vision panoramica de todos los proyectos y sintesis transversales.
> - **Guia y Proposito:** [[README|README.md]]
> - **Protocolo del Orquestador:** [[AGENTS|AGENTS.md]]
> - **Bitacora Global:** [[log|log.md]]
> - **Sintesis Transversales:** `wiki/sintesis/`

---

## 📦 Estado de Proyectos Activos
```dataview
TABLE
  length(rows.file.link) AS "Total Notas Wiki",
  max(rows.ultima_actualizacion) AS "Ultima Actividad"
FROM "projects"
WHERE file.folder != "projects" AND contains(file.path, "/wiki/")
GROUP BY regexreplace(file.folder, "^projects/([^/]+).*$", "$1") AS "Proyecto"
SORT "Ultima Actividad" DESC
```

---

## 🔗 Accesos Directos a Indices de Proyectos
* [[projects/Cache-Strategy-Lab/index|🧭 Indice: Cache-Strategy-Lab]]

---

## 🌐 Sintesis Globales y Comparativas Transversales
```dataview
TABLE
  ultima_actualizacion AS "Fecha",
  proyectos_relacionados AS "Proyectos Comparados",
  tags AS "Temas"
FROM "wiki/sintesis"
WHERE tipo = "sintesis" OR tipo = "sintesis_global"
SORT ultima_actualizacion DESC
```

---

## ⏱️ Registro de Actividad Reciente en Todo el Baul
```dataview
TABLE
  tipo AS "Tipo",
  file.folder AS "Directorio",
  ultima_actualizacion AS "Fecha"
FROM "projects" OR "wiki/sintesis"
WHERE ultima_actualizacion
SORT ultima_actualizacion DESC
LIMIT 15
```