# Bitacora de Operaciones Globales (Global Log)

## [2026-10-05] Protocolo | Unificacion de AGENTS.md y creacion del Manual de Usuario
- **Detalle:** Se unifico CLAUDE.md con AGENTS.md en un protocolo maestro unico en espanol con deteccion automatica de rol dual (Orquestador Global vs. Agente Local) y estandar de frontmatter YAML. Se creo el Manual de Usuario integral (MANUAL_USUARIO.md) con flujo diario de 5 fases, catalogo de prompts para casos de uso y tips operativos. Se mantuvieron sincronizados schema/AGENTS_GLOBAL.md, index.md y README.md.
- **Artefactos afectados:** [[AGENTS.md]], [[schema/AGENTS_GLOBAL.md]], [[MANUAL_USUARIO.md]], [[index.md]], [[README.md]]

## [2026-10-05] Refactor | Eliminacion de redundancia en schema/AGENTS_GLOBAL.md
- **Detalle:** Se elimino schema/AGENTS_GLOBAL.md al ser 100% redundante con AGENTS.md (fuente unica de verdad). Se actualizaron las referencias en AGENTS.md, README.md y MANUAL_USUARIO.md.
- **Artefactos afectados:** [[AGENTS.md]], [[README.md]], [[MANUAL_USUARIO.md]]

## [2026-10-05] Refactor | Eliminacion de .cursorrules
- **Detalle:** Se elimino .cursorrules consolidando a AGENTS.md como unico estandar de instrucciones tanto para Cursor como para los demas asistentes de IA.
- **Artefactos afectados:** [[.cursorrules]], [[README.md]]
