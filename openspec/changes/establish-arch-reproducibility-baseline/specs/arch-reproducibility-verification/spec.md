## Purpose

Define evidencia y verificaciones estratificadas que distingan estructura,
convergencia, hardware real y gates humanos antes de afirmar que Arch puede
restaurarse de forma segura y predecible.

## ADDED Requirements

### Requirement: Read-only deterministic planning
El sistema SHALL ofrecer un comando de planning que no requiera root, no modifique
el host y produzca una vista humana más una proyección JSON determinista y
redactada del estado deseado y observado.

#### Scenario: Repeat the same plan
- **WHEN** dos ejecuciones usan el mismo commit, host manifest, facts normalizados
  y estado observado
- **THEN** sus proyecciones deterministas son byte-identical
- **AND** timestamps y datos volátiles permanecen solo en evidencia raw separada

#### Scenario: Refuse mutation in baseline mode
- **WHEN** el operador ejecuta el entrypoint de este baseline
- **THEN** no solicita `sudo`, no instala paquetes, no habilita servicios y no
  crea, repara ni elimina targets

### Requirement: Strict convergence status
La verificación SHALL distinguir `converged`, `incomplete`, `drifted`, `blocked`,
`manual-gate` y `unsupported`. Un target deseado ausente MUST producir exit no-cero
en strict mode aunque el modo diagnóstico normal pueda tratarlo como warning.

#### Scenario: Missing profile links fail strict verification
- **WHEN** uno o más symlinks deseados están ausentes
- **THEN** strict verification informa cada target como `incomplete`
- **AND** finaliza con exit no-cero

#### Scenario: Healthy links do not overclaim workstation health
- **WHEN** todos los symlinks están correctos pero faltan paquetes, servicios o
  gates requeridos
- **THEN** el resultado general no es `converged`
- **AND** conserva resultados separados por clase de estado

### Requirement: Complete drift classification
El sistema SHALL comparar paquetes oficiales y externos, services, root-owned
files, perfiles, dependencias runtime, hardware contract, backups y gates
manuales. Drift observado MUST ser reportado antes de cualquier corrección.

#### Scenario: Detect live host declaration drift
- **WHEN** los perfiles o componentes activos del host difieren de su manifest
- **THEN** el reporte muestra `declared`, `observed` y la acción de reconciliación
- **AND** no actualiza automáticamente el manifest ni desactiva el runtime

#### Scenario: Detect root-owned file drift
- **WHEN** contenido, owner, group o mode de un archivo privilegiado difiere
- **THEN** la verificación identifica el campo exacto sin exponer contenido
  sensible

### Requirement: Typed verification ladder
Cada check SHALL declarar un nivel y un tipo de evidencia. Un test estructural en
Ubuntu o contenedor MUST NOT presentarse como prueba native Arch, boot, hardware o
interacción humana.

#### Scenario: Classify CI evidence honestly
- **WHEN** CI reconstruye perfiles dentro de un HOME temporal no-Arch
- **THEN** la evidencia se etiqueta `rootless-structural`
- **AND** no satisface requisitos de Pacman, systemd, boot o hardware real

#### Scenario: Reserve human gates for real interaction
- **WHEN** audio, suspend, screen sharing, login gráfico o autenticación requieren
  observación humana
- **THEN** traceability los clasifica `human-review-gate`
- **AND** nunca los denomina automated test

### Requirement: Idempotence and failure evidence
Todo apply futuro SHALL demostrar plan previo, segunda ejecución sin cambios y
restauración del baseline después de fallos inyectados. Evidencia de componente
MUST NOT presentarse como rollback de workstation completa.

#### Scenario: Verify second-run convergence
- **WHEN** una fase aplicada con éxito se ejecuta por segunda vez con los mismos
  inputs
- **THEN** no cambia archivos, paquetes, services ni estado administrado
- **AND** el plan informa cero operaciones pendientes

#### Scenario: Verify interrupted apply rollback
- **WHEN** se inyecta un fallo después de la primera mutación de una fase
- **THEN** el rollback restaura bytes, symlink targets, metadata y service state
  previos
- **AND** una verificación fresh coincide con el baseline anterior

### Requirement: Restore evidence and timing
El proyecto SHALL medir por separado `ISO-to-SSH`, `SSH-to-daily-ready` y
`dotfiles-only`, indicando cold/warm cache, bytes descargados, retries, pasos
manuales y revisión Git. Ninguna meta de minutos MUST declararse cumplida sin un
drill reproducible.

#### Scenario: Record a restore drill
- **WHEN** se completa un restore en VM o canary
- **THEN** la evidencia registra duración y resultado de cada fase, inputs,
  commit, hardware class y condiciones de cache/red
- **AND** identifica explícitamente todo gate manual o check no ejecutado

#### Scenario: Publish an incomplete checkpoint
- **WHEN** una sesión termina antes de completar todos los niveles
- **THEN** el repositorio conserva resultados ejecutados, blockers y next steps
- **AND** deja unchecked toda validación no realizada

### Requirement: Current documentation remains distinguishable from history
La documentación SHALL separar contratos normativos, estado actual generado y
auditorías históricas. Conteos, versiones y fechas derivables MUST validarse o
generarse para evitar contradicciones silenciosas.

#### Scenario: Detect stale machine facts
- **WHEN** un documento actual afirma un perfil o conteo distinto del grafo
  resuelto y evidencia live revisada
- **THEN** la validación documental falla con ambos valores y sus fuentes

### Requirement: Secret-safe evidence
Raw y deterministic evidence MUST excluir valores de secrets, tokens, private
keys, cookies, credential stores y variables secret-like. Los checks SHALL
registrar únicamente presencia, permisos o un identificador no reversible cuando
sea necesario.

#### Scenario: Inspect an authentication prerequisite
- **WHEN** el verificador comprueba una credencial local
- **THEN** el reporte contiene solo estado, path redactado si corresponde y mode
- **AND** ningún stdout, JSON o log contiene el valor secreto
