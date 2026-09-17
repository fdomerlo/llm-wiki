# LLM-Wiki — Sistema Operativo de Conocimiento Documental

Una **Wiki personal y tecnica** basado en **Obsidian + Markdown**, inspirado en la visión de Andrej Karpathy sobre el uso de Modelos de Lenguaje como curadores, bibliotecarios y analistas críticos de una base de conocimiento viva y acumulativa.

---

## 🧭 Proposito y Filosofia

El objetivo de este repositorio es transformar a cualquier Modelo de Lenguaje (LLM) en un **bibliotecario, analista y custodio activo** de tu base de conocimiento, en lugar de un mero generador pasivo de texto.

### Los fundamentos del Sistema
- **`raw/` contiene lo que otros dijeron:** Evidencia historica inmutable (articulos, transcripciones, especificaciones).
- **`wiki/` contiene lo que sabemos:** Conocimiento destilado, atomico y conectado mediante enlaces bidireccionales. En la raiz aloja `wiki/sintesis/` generada dinamicamente para comparativas globales.
- **`projects/` contiene lo que construimos:** Espacios aislados donde el conocimiento se aplica a dominios y proyectos tecnicos especificos.

---

## 🛡️ Principios Operativos y Epistemologicos

### 1. Inmutabilidad Absoluta de Evidencias (`raw/`)
Queda estrictamente prohibido que un LLM o usuario modifique, recorte o elimine archivos dentro de cualquier carpeta `raw/`. Todo documento crudo permanece como testigo historico de la informacion original.

### 2. Clasificacion de Certeza
Todo contenido generado o sintetizado por un LLM en este baul debe distinguirse con precision:
- **HECHO (Fact):** Afirmacion demostrada de forma directa por una fuente en `raw/` o nota tecnica previa. Debe citarse con `[[wikilink]]`.
- **INTERPRETACION (Interpretation):** Sintesis analitica o estructuracion conceptual derivada de los hechos observados.
- **INFERENCIA (Inference):** Conjetura, hipotesis o recomendacion externa del modelo. Debe marcarse explicitamente (`*Inferencia:* ...` o `certeza: media/baja`).

### 3. Preservacion de Conflictos (Sin Consenso Artificial)
Si dos fuentes o proyectos discrepan tecnicamente (por ejemplo, invalidacion de cache por TTL vs. invalidacion reactiva con CDC), el LLM **no debe ocultar ni reconciliar forzosamente la diferencia**. Se documentan formalmente en los metadatos YAML:
```yaml
conflicto_con:
  - "[[Nota-Discrepante]]"
motivo_conflicto: "Divergencia entre consistencia eventual y latencia ultra-baja"
```

### 4. Convencion Linguistica y Nomenclatura Segura (Safe-Spanish)
- El baul opera íntegramente en **espanol**.
- Para garantizar portabilidad en cualquier sistema operativo y terminal, los nombres de archivos, rutas de carpetas, slugs, etiquetas (`tags`) y claves YAML no contienen `ñ` ni tildes (ej. `sintesis`, `resumenes`, `arquitectura`, `diseno`, `ano`/`fecha`).

---

## 📂 Topologia del Repositorio

```text
llm-wiki/
├── AGENTS.md                  # Protocolo global del Orquestador del baul
├── README.md                  # Esta guia de uso y arquitectura
├── CLAUDE.md / .cursorrules   # Instrucciones contextuales para asistentes de IA
├── index.md                   # Tablero general con consultas Dataview
├── log.md                     # Bitacora cronologica de operaciones globales
├── raw/                       # Evidencia transversal global (inmutable)
├── wiki/                      # Conocimiento destilado transversal
│   └── sintesis/              # Matrices comparativas entre proyectos (dinamica)
├── schema/                    # Esquemas, protocolos de agentes y plantillas (Templater)
│   ├── AGENTS_GLOBAL.md       # Esquema canonico del Orquestador Global
│   ├── AGENTS_LOCAL.md        # Esquema canonico para Agentes Locales de proyectos
│   ├── tpl_WIKI.md            # Generador automatico de proyectos LLM-Wiki
│   ├── tpl_CONCEPTO.md        # Plantilla atomica de conceptos
│   ├── tpl_ARQUITECTURA.md    # Plantilla ADR de arquitectura
│   └── tpl_SINTESIS.md        # Plantilla de matrices comparativas
└── projects/                  # Directorio de proyectos autonomos
    └── mi-baul-obsidian/      # Proyecto modelo y manual de usuario integrado
        ├── AGENTS.md          # Protocolo del Agente Local de proyecto
        ├── index.md           # Tablero, enlaces de arranque y metricas
        ├── log.md             # Bitacora de ingestas y cambios locales
        ├── raw/               # Evidencias inmutables del proyecto
        └── wiki/              # Grafo de conocimiento local
            ├── arquitectura/  # Patrones, decisiones y flujo diario
            ├── conceptos/     # Modelos mentales, guia de inicio y buenas practicas
            ├── entidades/     # Herramientas, bases de datos y servicios
            ├── resumenes/     # Resumenes estructurados de cada fuente
            └── sintesis/      # Comparativas tecnicas locales
```

---

## 🤖 Jerarquia de Agentes (Global vs. Local)

El sistema define dos roles de agente claramente delimitados:

| Rol | Ubicacion de su Protocolo | Ambito de Escritura | Responsabilidad Principal |
| :--- | :--- | :--- | :--- |
| **Orquestador Global** | `AGENTS.md` (sincronizado con `schema/AGENTS_GLOBAL.md`) | `index.md`, `log.md`, `wiki/sintesis/` | Mantener el mapa de navegacion general, conectar patrones entre proyectos y auditar la salud del baul. |
| **Agente Local** | `projects/<nombre>/AGENTS.md` (derivado de `schema/AGENTS_LOCAL.md`) | Exclusivamente `projects/<nombre>/` | Ingestar fuentes en `raw/`, crear notas atomicas, responder consultas de dominio y auditar el proyecto. |

> [!IMPORTANT]
> **Barrera de Aislamiento:** El Orquestador Global tiene prohibido modificar unilateralmente archivos internos de un proyecto para evitar corrupcion o contaminacion cruzada.

---

## 🚀 Guia de Uso y Flujos Operativos

### Flujo A: Crear un Nuevo Proyecto
Existen dos formas de iniciar un proyecto en `projects/`:

1. **Desde Obsidian con Templater:**
   - Ejecuta el comando *Templater: Open Insert Template Modal*.
   - Selecciona `schema/tpl_WIKI.md`.
   - Ingresa el nombre del proyecto (ej. `Auth-Service`).
   - La plantilla creara la estructura de carpetas, inyectara `AGENTS.md` (leyendolo desde `schema/AGENTS_LOCAL.md`), inicializara `log.md` y creara `index.md`.

2. **Mediante Instruccion al LLM:**
   - Pide al asistente:
     > *"Crea un nuevo proyecto en projects/ llamado API-Gateway siguiendo la plantilla schema/tpl_WIKI.md y registralo en el index.md global."*

---

### Flujo B: Ingesta de Documentos en un Proyecto
Cuando agregues un nuevo articulo, paper o nota en la carpeta `raw/` de un proyecto:

1. Coloca el archivo en `projects/<proyecto>/raw/<fuente>.md`.
2. Asigna la instruccion al LLM en modo Agente Local:
   > *"Actua como Agente Local de mi-baul-obsidian segun su AGENTS.md. Procesa la fuente raw/01-principios-karpathy-llm-wiki.md ejecutando el Protocolo de Ingesta."*
3. El LLM realizara:
   - Resumen estructurado en `wiki/resumenes/`.
   - Creacion o actualizacion de notas atomicas en `wiki/conceptos/`, `wiki/arquitectura/` o `wiki/entidades/` con enlaces bidireccionales.
   - Registro de la operacion en `projects/<proyecto>/log.md`.

---

### Flujo C: Sintesis Transversal entre Proyectos
Cuando desees comparar enfoques o contrastar como diferentes proyectos resuelven un mismo desafio:

1. Invoca al LLM en rol de Orquestador Global:
   > *"Actua como Orquestador Global del baul segun AGENTS.md. Compara las estrategias de gestion de estado entre mi-baul-obsidian y Auth-Service. Crea la sintesis comparativa correspondiente."*
2. El LLM:
   - Lee los indices y notas pertinentes de ambos proyectos.
   - Crea `wiki/sintesis/` dinamicamente si no existe y genera la nota `[[Comparativa-<Tema>.md]]` con tabla comparativa y analisis de trade-offs.
   - Actualiza el meta-indice [[index|index.md]] y registra el evento en [[log|log.md]].

---

### Flujo D: Auditoria de Calidad (Linting Documental)
Para verificar la salud y consistencia del baul:

1. Solicita al LLM:
   > *"Ejecuta una auditoria global del baul segun el Protocolo C de AGENTS.md."*
2. El LLM verificara:
   - Integridad de rutas y ausencia de nomenclaturas obsoletas.
   - Presencia de `index.md`, `AGENTS.md` y `log.md` en cada proyecto.
   - Identificacion de wikilinks rotos o notas desvinculadas.
   - Emision de un reporte estructurado con semaforo de estado.

---

### Flujo E: Jardineria Semantica y Compilacion Continua
Para evolucionar la base de conocimiento sin dejar notas desvinculadas o redundantes:

1. Solicita al LLM:
   > *"Ejecuta una sesion de jardineria semantica segun el Protocolo E de AGENTS.md."*
2. El LLM realizara:
   - **Deteccion de Stubs:** Identifica enlaces `[[...]]` citados que aun no tienen archivo fisico y propone borradores iniciales usando `schema/tpl_CONCEPTO.md`.
   - **Deduplicacion y Alias:** Localiza notas solapadas y propone unificarlas bajo la nota canonica agregando alias YAML.
   - **Mapeo Tematico (MOC):** Agrupa clusters conceptuales para enriquecer los indices de navegacion.

---

## 🧪 Proyecto de Demostracion y Manual de Usuario: `mi-baul-obsidian`

El repositorio incluye una implementacion de referencia completamente operativa en `projects/mi-baul-obsidian/` que funciona simultaneamente como **modelo vivo** (*few-shot example*) y como **manual de usuario interactivo** para comenzar de inmediato:

- **📖 Manual Operativo y Quickstart Integrado:**
  - `[[projects/mi-baul-obsidian/wiki/conceptos/Guia-Inicio-Rapido|Guia de Inicio Rapido]]`: Puesta en marcha en 3 pasos simples (configurar Obsidian, crear proyecto, primera ingesta con LLM).
  - `[[projects/mi-baul-obsidian/wiki/conceptos/Buenas-Practicas-Curaduria|Buenas Practicas y Tips]]`: Las 5 reglas de oro (atomicidad, enriquecer antes de duplicar, inmutabilidad de raw, safe-spanish y preservación de conflictos) junto a un **Cheat-Sheet de prompts listos para usar**.
  - `[[projects/mi-baul-obsidian/wiki/arquitectura/Flujo-Operativo-Diario|Flujo Operativo Diario]]`: Diagrama visual y explicacion detallada del ciclo metabolico de 5 fases (Captura -> Destilacion -> Interconexion -> Consulta -> Jardineria).
- **Evidencia inmutable original:** Fuentes en `raw/01-principios-karpathy-llm-wiki.md` y `raw/02-guia-operativa-y-mejores-practicas.md`.
- **Resumenes estructurados:** En `wiki/resumenes/`, sintetizando los puntos clave y citas literales de cada documento.
- **Notas atomicas interconectadas:** Modeladas en `wiki/conceptos/` (`Conocimiento-Acumulativo`, `Inmutabilidad-Raw`), `wiki/entidades/` (`Obsidian`) y `wiki/arquitectura/` (`Patron-Arquitectura-LLM-Wiki`).
- **Sintesis comparativa:** En `wiki/sintesis/Comparativa-LLM-Wiki-vs-RAG.md`, con matriz de trade-offs tecnicos entre curaduria documental y recuperacion vectorial tradicional.
- **Operacion local:** Incluye su propio `AGENTS.md`, bitacora cronologica en `log.md` y un tablero dinamico en `index.md` con consultas Dataview listas para explorar en Obsidian.

---

## ⚙️ Configuracion Recomendada de Obsidian

Para aprovechar al maximo este baul documental:

1. **Plugin Dataview:**
   - Activar *Enable JavaScript Queries* y *Enable Inline Queries*.
   - Permite que los tableros de `index.md` (global y locales) muestren automaticamente las notas clasificadas, debates abiertos y su fecha de actividad.
2. **Plugin Templater:**
   - Configurar la carpeta de plantillas apuntando a `schema/`.
3. **Plugins Semanticos Complementarios (Opcionales):**
   - **Omnisearch:** Busqueda difusa profunda, indexacion instantanea y OCR de diagramas.
   - **Smart Connections:** Calculo de embeddings locales sobre `wiki/` sin tocar `raw/`, facilitando recomendaciones de notas relacionadas durante la redaccion.
4. **Ajustes Nativos de Archivos y Enlaces:**
   - **Formato de enlaces nuevo:** Usar enlaces tipo Wikilink (`[[...]]`).
   - **Ruta de creacion de notas nuevas:** Apuntando a la carpeta `raw/`.
