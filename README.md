# LLM-Wiki Lite — Sistema Operativo de Conocimiento Documental

Un **baul de conocimiento personal y tecnico** basado en **Obsidian + Markdown**, disenado bajo el paradigma **LLM-as-Operator** en su variante **Lite**: puramente documental, sin scripts CLI intermediarios ni dependencias de software externas, donde la **disciplina epistemologica**, la **verbosidad guiada** y la **obediencia del LLM** aseguran la coherencia del conocimiento.

---

## 🧭 Proposito y Filosofia

El objetivo de este repositorio es transformar a cualquier Modelo de Lenguaje (LLM) en un **bibliotecario, analista y custodio activo** de tu base de conocimiento, en lugar de un mero generador pasivo de texto.

### La Triada del Sistema
- **`raw/` contiene lo que otros dijeron:** Evidencia historica inmutable (articulos, transcripciones, especificaciones).
- **`wiki/` contiene lo que sabemos:** Conocimiento destilado, atomico y conectado mediante enlaces bidireccionales.
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
Si dos fuentes o proyectos discrepan tecnicamente (por ejemplo, invalidacion de cache por TTL vs. invalidacion reactiva con CDC), el LLM **no debe ocultar ni reconciliar forzosamente la diferencia**. Se documentan ambos enfoques, sus pros, sus contras y el contexto de cada decision.

### 4. Convencion Linguistica y Nomenclatura Segura (Safe-Spanish)
- El baul opera íntegramente en **espanol**.
- Para garantizar portabilidad en cualquier sistema operativo y terminal, los nombres de archivos, rutas de carpetas, slugs, etiquetas (`tags`) y claves YAML no contienen `ñ` ni tildes (ej. `sintesis`, `resumenes`, `arquitectura`, `diseno`, `ano`/`fecha`).

---

## 📂 Topologia del Repositorio

```text
llm.wiki.2/
├── AGENTS.md                  # Protocolo global del Orquestador del baul
├── README.md                  # Esta guia de uso y arquitectura
├── index.md                   # Tablero general con consultas Dataview
├── log.md                     # Bitacora cronologica de operaciones globales
├── raw/                       # Evidencia transversal global (inmutable)
├── wiki/                      # Conocimiento destilado transversal
│   └── sintesis/              # Matrices comparativas entre proyectos
├── system/                    # Plantillas del sistema (Templater)
│   ├── tpl_WIKI.md            # Generador de proyectos LLM-Wiki
│   └── tpl_OKF.md             # Generador de proyectos OKF
└── projects/                  # Directorio de proyectos autonomos
    └── Cache-Strategy-Lab/    # Ejemplo de proyecto activo
        ├── AGENTS.md          # Protocolo del Agente Local de proyecto
        ├── index.md           # Tablero y metricas del proyecto
        ├── log.md             # Bitacora de ingestas y cambios locales
        ├── raw/               # Evidencias inmutables del proyecto
        └── wiki/              # Grafo de conocimiento local
            ├── arquitectura/  # Patrones y decisiones de diseno
            ├── conceptos/     # Modelos mentales y tecnicas atomicas
            ├── entidades/     # Herramientas, bases de datos y servicios
            ├── resumenes/     # Resumenes estructurados de cada fuente
            └── sintesis/      # Comparativas tecnicas locales
```

---

## 🤖 Jerarquia de Agentes (Global vs. Local)

El sistema define dos roles de agente claramente delimitados:

| Rol | Ubicacion de su Protocolo | Ambito de Escritura | Responsabilidad Principal |
| :--- | :--- | :--- | :--- |
| **Orquestador Global** | `llm.wiki.2/AGENTS.md` | `index.md`, `log.md`, `wiki/sintesis/` | Mantener el mapa de navegacion general, conectar patrones entre proyectos y auditar la salud del baul. |
| **Agente Local** | `projects/<nombre>/AGENTS.md` | Exclusivamente `projects/<nombre>/` | Ingestar fuentes en `raw/`, crear notas atomicas, responder consultas de dominio y auditar el proyecto. |

> [!IMPORTANT]
> **Barrera de Aislamiento:** El Orquestador Global tiene prohibido modificar unilateralmente archivos internos de un proyecto para evitar corrupcion o contaminacion cruzada.

---

## 🚀 Guia de Uso y Flujos Operativos

### Flujo A: Crear un Nuevo Proyecto
Existen dos formas de iniciar un proyecto en `projects/`:

1. **Desde Obsidian con Templater:**
   - Ejecuta el comando *Templater: Open Insert Template Modal*.
   - Selecciona `system/tpl_WIKI.md`.
   - Ingresa el nombre del proyecto (ej. `Auth-Service`).
   - La plantilla creara la estructura de carpetas, inyectara `AGENTS.md`, inicializara `log.md` y creara `index.md`.

2. **Mediante Instruccion al LLM:**
   - Pide al asistente:
     > *"Crea un nuevo proyecto en projects/ llamado API-Gateway siguiendo la plantilla tpl_WIKI.md y registralo en el index.md global."*

---

### Flujo B: Ingesta de Documentos en un Proyecto
Cuando agregues un nuevo articulo, paper o nota en la carpeta `raw/` de un proyecto:

1. Coloca el archivo en `projects/<proyecto>/raw/<fuente>.md`.
2. Asigna la instruccion al LLM en modo Agente Local:
   > *"Actua como Agente Local de Cache-Strategy-Lab segun su AGENTS.md. Procesa la fuente raw/03-patron-bulkhead.md ejecutando el Protocolo de Ingesta."*
3. El LLM realizara:
   - Resumen estructurado en `wiki/resumenes/`.
   - Creacion o actualizacion de notas atomicas en `wiki/conceptos/`, `wiki/arquitectura/` o `wiki/entidades/` con enlaces bidireccionales.
   - Registro de la operacion en `projects/<proyecto>/log.md`.

---

### Flujo C: Sintesis Transversal entre Proyectos
Cuando desees comparar enfoques o contrastar como diferentes proyectos resuelven un mismo desafio:

1. Invoca al LLM en rol de Orquestador Global:
   > *"Actua como Orquestador Global del baul segun AGENTS.md. Compara las estrategias de invalidacion de cache entre Cache-Strategy-Lab y Session-Manager. Crea la sintesis comparativa correspondiente."*
2. El LLM:
   - Lee los indices y notas pertinentes de ambos proyectos.
   - Genera una nota en `wiki/sintesis/[[Comparativa-<Tema>.md]]` con tabla comparativa y analisis de trade-offs.
   - Actualiza el meta-indice [index.md](file:///home/fdomerlo/Proyectos/llm.wiki.2/index.md) y registra el evento en [log.md](file:///home/fdomerlo/Proyectos/llm.wiki.2/log.md).

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

## ⚙️ Configuracion Recomendada de Obsidian

Para aprovechar al maximo este baul documental:

1. **Plugin Dataview:**
   - Activar *Enable JavaScript Queries* y *Enable Inline Queries*.
   - Permite que los tableros de `index.md` (global y locales) muestren automaticamente las notas clasificadas y su fecha de actividad.
2. **Plugin Templater:**
   - Configurar la carpeta de plantillas apuntando a `system/`.
3. **Ajustes Nativos de Archivos y Enlaces:**
   - **Formato de enlaces nuevo:** Usar enlaces tipo Wikilink (`[[...]]`).
   - **Ruta de creacion de notas nuevas:** En la misma carpeta que el archivo actual o carpeta especificada.
