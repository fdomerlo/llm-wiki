# LLM-Wiki Instructions for Claude & AI Agents

You are operating inside an **LLM-Wiki** knowledge vault based on Andrej Karpathy's cumulative knowledge base philosophy and Obsidian Markdown.

## Core Directives

### 1. Dual Role Detection
- **Local Project Scope:** When working on files inside `projects/<project-name>/`, adopt the **Agente Local** role defined in `projects/<project-name>/AGENTS.md`. Strictly limit reads and writes to that project's directory.
- **Global Vault Scope:** When working across projects or in root, adopt the **Orquestador Global** role defined in `AGENTS.md`. You may read any project but only write to `index.md`, `log.md`, and create cross-project comparisons dynamically in `wiki/sintesis/`.

### 2. Absolute Immutability of `raw/`
- **NEVER** edit, truncate, rename, or delete any file inside any `raw/` directory (root or project). `raw/` is immutable historical evidence.

### 3. Epistemological Discipline & Conflict Preservation
- Categorize claims as: **HECHO (Fact)**, **INTERPRETACION (Interpretation)**, or **INFERENCIA (Inference)**.
- **Do not force consensus:** If sources disagree, preserve the conflict using frontmatter fields `conflicto_con` and `motivo_conflicto`.

### 4. Safe-Spanish Naming Convention
- Vault content is in **Spanish**.
- Filenames, folder paths, YAML keys, and tags must NOT contain accents or `ñ` (use `sintesis`, `resumenes`, `arquitectura`, `diseno`, `ano`, etc.).
- Obsidian wikilinks must match file basenames: `[[Nombre-Nota]]`.

### 5. Mandatory YAML Frontmatter
All notes inside any `wiki/` directory must start with:
```yaml
---
tipo: concepto | arquitectura | entidad | sintesis | resumen_fuente
titulo: Canonical Note Title
estado: activo | superado | deprecado
ultima_actualizacion: YYYY-MM-DD
fuentes:
  - "[[raw/source-file.md]]"
tags:
  - tag-sin-tildes
alias: []
certeza: alta | media | baja
conflicto_con: []
motivo_conflicto: ""
---
```

### 6. Logging
- Record significant operations (ingestions, architecture decisions, linting, gardening) in the respective `log.md`.
