---
tipo: concepto
titulo: Buenas Practicas y Tips de Curaduria
estado: activo
ultima_actualizacion: 2026-09-16
fuentes:
  - "[[projects/mi-baul-obsidian/raw/02-guia-operativa-y-mejores-practicas|raw/02-guia-operativa-y-mejores-practicas.md]]"
tags:
  - mi-baul-obsidian
  - curaduria
  - buenas-practicas
  - prompts
alias:
  - Best Practices
  - Consejos de Curaduria
certeza: alta
conflicto_con: []
motivo_conflicto: ""
---

# Buenas Practicas y Tips de Curaduria

Guia de referencia con reglas de oro, recomendaciones tecnicas y catalogo de prompts para mantener tu baul de conocimiento siempre util, rapido y libre de alucinaciones.

---

## Las 5 Reglas de Oro

### 1. Atomicidad Radical (Una Idea por Nota)
- Cada nota en `wiki/conceptos/` o `wiki/arquitectura/` debe resolver una sola pregunta o concepto.
- **Regla practica:** Si una nota supera 300-400 palabras o aborda dos subtipos de arquitectura distintos, pídele al LLM que la descomponga en dos notas atómicas y las vincule con un `[[wikilink]]`.

### 2. Enriquecer antes de Duplicar
- Antes de que el LLM genere una nota nueva, debe buscar si el término ya existe.
- Si una nueva fuente aporta matices sobre un concepto previo, se agrega un subtítulo o se amplía la nota existente. Esto alimenta el [[Conocimiento-Acumulativo]].

### 3. Inmutabilidad Sagrada de `raw/`
- Jamás permitas que un script o LLM modifique un archivo en `raw/`.
- `raw/` es la evidencia forense. Si se sospecha que una nota sintetizó mal un dato, la fuente intacta permite auditarla de inmediato.

### 4. Nomenclatura Segura (Safe-Spanish)
- Nombres de notas: sustantivos en singular sin tildes ni eñes (`[[Patron-Diseno]]` en vez de `[[patrones-de-diseño]]`).
- Garantiza que los archivos se puedan clonar en Windows, Linux, macOS o servidores de CI/CD sin incompatibilidades de codificación UTF-8 / NFD.

### 5. Preservar Conflictos y Trade-offs
- No fuerces consensos artificiales. Si un autor defiende microservicios y otro monolitos modulares, documenta ambos en notas independientes y registra en el YAML:
  ```yaml
  conflicto_con: ["[[Monolito-Modular]]"]
  motivo_conflicto: "Divergencia en complejidad operacional vs. desacoplamiento de despliegue"
  ```

---

## 💬 Cheat-Sheet: Catalogo de Prompts Listos para Usar

Copia y pega estos comandos en tu cliente de IA preferido:

| Tarea | Prompt Recomendado |
| :--- | :--- |
| **Ingesta de fuente** | `Actua como Agente Local de [proyecto] segun su AGENTS.md. Procesa la fuente raw/[nombre.md] ejecutando el Protocolo de Ingesta A. Genera resumen, extrae conceptos atomicos y actualiza el log.` |
| **Consulta documentada** | `Como Agente Local de [proyecto], responde a la siguiente duda tecnica: [¿Como manejamos X?]. Responde citando estrictamente las notas de wiki/ mediante [[wikilinks]]. No inventes soluciones no documentadas.` |
| **Sintesis entre proyectos** | `Actua como Orquestador Global segun AGENTS.md. Compara la solucion arquitectonica para [Tema] entre [Proyecto-A] y [Proyecto-B]. Redacta una sintesis comparativa en wiki/sintesis/ con matriz de trade-offs.` |
| **Jardineria Semantica** | `Actua como Agente Local de [proyecto]. Ejecuta una sesion de Jardineria Semantica (Protocolo D). Revisa stubs (enlaces rotos o sin crear), busca sinonimos para unificar y propone notas atomicas faltantes.` |
| **Auditoria y Linting** | `Ejecuta una auditoria documental del baul segun el Protocolo C de AGENTS.md. Reporta con semaforo: notas huerfanas, rutas invalidas y enlaces rotos.` |

---

## Relaciones
- Complemento esencial de la [[Guia-Inicio-Rapido]].
- Define las directrices de calidad para el [[Flujo-Operativo-Diario]].
