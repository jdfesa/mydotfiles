## Purpose

Define evidencia, métricas, documentación, automatización y outcome para evaluar
Chezmoi sin predisponer la decisión de adoption.

## ADDED Requirements

### Requirement: The comparison measures total complexity honestly

La evaluación SHALL comparar Chezmoi con `scripts/link` más
`scripts/profile-resolve` mediante casos equivalentes y evidencia raw. MUST
registrar commands, pasos internos, files/adapters, estado persistente, failure
safety, reruns, diff/status, drift, permisos, rollback, factibilidad Windows,
documentation burden y complejidad cognitiva. Ningún score podrá ponderarse para
forzar una victoria de Chezmoi.

#### Scenario: Chezmoi reduces visible commands through hidden orchestration
- **WHEN** un wrapper reduce commands visibles pero agrega state, staging, wrappers o recovery concepts
- **THEN** la comparación informa ambas caras y no lo presenta automáticamente como simplificación

#### Scenario: Future bootstrap phase requires native behavior
- **WHEN** una fase futura necesita comportamiento específico de un OS
- **THEN** la evaluación permite un adapter pequeño con support matrix y fail-fast, en lugar de portabilidad artificial

#### Scenario: Current linker blocks a real file
- **WHEN** el baseline temporal encuentra un archivo real en un target
- **THEN** verifica que `scripts/link` lo preserve y falle, registrando el command y exit

#### Scenario: Current model lacks rendered host data
- **WHEN** Git requiere datos por host que el linker no renderiza
- **THEN** se registra como gap actual sin ejecutar ni reemplazar `configure-git`

### Requirement: Complexity metrics are dynamically derived

Los counts de files, adapters, documentación y commands MUST derivarse de scopes
declarados o records reales, sin ajustes manuales. La comparación SHALL incluir
raw LOC dinámico para los scripts productivos comparados y automation/tests del
piloto. LOC MUST permanecer un dato no ponderado y documentar que no mide por sí
solo mantenibilidad, dificultad ni behavior.

#### Scenario: Pilot automation grows
- **WHEN** se agrega, elimina o divide un archivo dentro del scope declarado
- **THEN** file count y raw LOC cambian automáticamente y obligan a regenerar evidencia

#### Scenario: Command sequence changes
- **WHEN** cambia una invocación Chezmoi o del baseline
- **THEN** el count se deriva de command records y la proyección fresh deja de coincidir con la evidencia revisada

### Requirement: Mandatory acceptance thresholds are measurable

La evidencia MUST registrar cero writes fuera del root, cero overlaps reales,
cero secret/prohibited findings, modes esperados, manifests completos, dos runs
deterministas, segundo apply/dry-run no-op, drift detectado, rollback exacto y
metadata protegida sin cambios. Ninguna afirmación manual reemplaza un threshold.

#### Scenario: Every mandatory metric passes
- **WHEN** todos los thresholds se satisfacen
- **THEN** el piloto puede completar la evaluación, aunque native evidence y complexity policy aún pueden bloquear migration

#### Scenario: One mandatory metric fails
- **WHEN** un criterio obligatorio queda incompleto
- **THEN** el outcome máximo es `keep-and-continue-evaluation`, salvo que sea un fallo crítico que exige `reject`

### Requirement: Outcome is selected from evidence

El resultado MUST seleccionarse mediante una función explícita entre `reject`,
`keep-and-continue-evaluation` y `recommend-selective-migration`. Writes fuera de
root, overlap, secretos, features prohibidas, metadata protegida alterada,
rollback fallido o idempotencia fallida MUST seleccionar `reject`. Missing native
Windows, mandatory incompleto o ausencia de beneficio claro MUST seleccionar
continuidad. Una recomendación MUST ser imposible salvo Windows nativo verdadero,
todos los thresholds y policy comparativa permisiva.

#### Scenario: Critical safety failure occurs
- **WHEN** falla seguridad, ownership, secretos, rollback o idempotencia crítica
- **THEN** el selector produce `reject`

#### Scenario: Safety passes but evidence is incomplete
- **WHEN** los fallos críticos están ausentes pero falta Windows nativo, otro mandatory o beneficio de complejidad
- **THEN** el selector produce `keep-and-continue-evaluation`

#### Scenario: Selective migration is recommended
- **WHEN** Windows nativo, todo mandatory y policy comparativa pasan
- **THEN** el selector puede producir `recommend-selective-migration`, sujeto a otro cambio canary

#### Scenario: Recommendation contradicts native evidence
- **WHEN** aparece `recommend-selective-migration` mientras `nativeEvidence.windows` es falso
- **THEN** unit test, validate y doctor fallan el invariante

### Requirement: Evidence projection is deterministic and complete

La evaluación MUST definir una sola proyección determinista para comparar fresh
evidence con `review.json` y para generar todos los input digests. Puede excluir
únicamente timestamps y el contexto Git dinámico de publicación. La versión
Python exacta MUST conservarse en evidencia raw, pero la proyección MUST usar el
contrato compatible `>=3.11`. El banner Chezmoi raw MUST conservar provenance
del distribuidor, mientras la proyección MUST exigir la versión semántica exacta
`2.72.0`; OpenSpec MUST permanecer exactamente `1.9.0`. La proyección MUST
conservar commands, exits, paths normalizados, hashes, manifests, modes,
métricas, blockers, native evidence y outcome.
El `dump-config` raw MAY conservar hash, line count y preview del host como
provenance informativa, pero la proyección MUST usar un hash canónico de los
paths y datos efectivos validados.

#### Scenario: Only timestamps change
- **WHEN** cambian `recordedAt`, `startedAt` o `endedAt`
- **THEN** proyección y digest permanecen iguales

#### Scenario: Publication changes Git state
- **WHEN** rebase/merge cambia `git.branch`, `git.reviewedBase`, `git.headRevision` y `git.dirty`
- **THEN** la evidencia raw conserva provenance y la proyección omite los cuatro campos dinámicos

#### Scenario: Compatible Python patch changes
- **WHEN** cambia únicamente el patch Python exacto y ambas versiones satisfacen `>=3.11`
- **THEN** la evidencia raw conserva ambas versiones auditables y la proyección permanece en el contrato `>=3.11`

#### Scenario: Chezmoi distributor build banner changes
- **WHEN** Arch y upstream reportan distinto build/commit banner para Chezmoi `2.72.0`
- **THEN** raw evidence conserva ambos banners y la proyección permanece exactamente `2.72.0`

#### Scenario: Chezmoi distributor build banner changes preview token
- **WHEN** cambia solo el banner de build para Chezmoi semántico `2.72.0`
- **THEN** `previewDigest` permanece estable, pero cambia ante otra versión semántica

#### Scenario: Dump-config host defaults differ
- **WHEN** Arch y Ubuntu emiten defaults raw distintos fuera del contrato efectivo validado
- **THEN** raw evidence conserva esa provenance y la proyección compara el mismo hash canónico de paths/datos

#### Scenario: Deterministic behavior changes
- **WHEN** cambia un command, hash, manifest, mode, metric, blocker o native-evidence field
- **THEN** cambia la proyección y `validate`/`generate-docs --check` fallan hasta regenerar evidencia y docs

#### Scenario: Normalization hides a path escape
- **WHEN** un path real escapa antes de normalizarse
- **THEN** containment falla; la normalización nunca convierte un escape en evidencia válida

### Requirement: Documentation ownership is explicit

Rationale, HOW, limitations, failure modes y outcome interpretation SHALL vivir
en Markdown human-owned. Matrices, manifests, commands, hashes, métricas y
traceability SHALL generarse determinísticamente y marcarse `DO NOT EDIT`. Toda
prosa explicativa MUST estar en español profesional UTF-8; nombres técnicos,
paths, headings y keywords OpenSpec permanecen en inglés.

#### Scenario: Generated document is edited manually
- **WHEN** un generated document difiere del renderer y evidencia revisada
- **THEN** `generate-docs --check` falla y exige regeneración, no edición manual

#### Scenario: Policy needs explanation
- **WHEN** una decisión requiere contexto, trade-off, rollback o limitación
- **THEN** la prosa human-owned explica WHY y HOW en español

### Requirement: Traceability is one-to-one and typed

Cada escenario OpenSpec MUST tener exactamente una entrada declarada. Una entrada
MUST ser `automated-check` con ID/locator existente, `generated-evidence` con JSON
pointer resoluble, `native-blocked` o `human-review-gate`. Un integration run
genérico no SHALL presentarse como focused unit test.

#### Scenario: Scenario is only a human gate
- **WHEN** no existe check automatizado ni evidencia native/generated concreta
- **THEN** traceability lo etiqueta `human-review-gate` con rationale

#### Scenario: Automated check ID is stale
- **WHEN** un entry refiere un ID no registrado o locator inexistente
- **THEN** validation falla

#### Scenario: OpenSpec scenario has no entry
- **WHEN** aparece o desaparece un escenario sin actualizar traceability
- **THEN** validation falla por diferencia uno-a-uno

### Requirement: CI and doctor enforce the real gates

Linux CI MUST ejecutar unit tests, evidencia fresh versus reviewed, generated-doc
check, outcome/native invariant, OpenSpec strict/doctor y validators relevantes.
MUST usar directamente el host GitHub `ubuntu-22.04` fijado, sin job container,
instalar Chezmoi `2.72.0` y OpenSpec `1.9.0` exactos antes del sandbox y ejecutar
primero el smoke test Bubblewrap estricto. MUST fallar si el host no permite
private `/dev`/`proc` más un único root host-backed escribible. MUST prohibir
privileged mode, capabilities adicionales, bypass AppArmor/seccomp, cambios de
sysctl, skip silencioso y fallback fuera de Bubblewrap. El job Windows disabled
no cuenta como gate; native evidence falso en la evidencia executable sí. El
checkout MUST incluir history completa para calcular `reviewedBase` contra
`origin/main`, no depender de un PR ref shallow.

#### Scenario: Linux CI environment lacks safe Bubblewrap
- **WHEN** el host `ubuntu-22.04` no puede crear el sandbox requerido
- **THEN** CI falla sin degradar containment

#### Scenario: Portable Linux CI passes
- **WHEN** el runner directo Ubuntu completa smoke, matrix y validators
- **THEN** la evidencia se etiqueta `portable-linux`, no native Arch ni native Windows

#### Scenario: Windows CI is not configured
- **WHEN** el job Windows sigue disabled o no hay runner revisado
- **THEN** native Windows permanece bloqueado y el selector no puede recomendar migration

#### Scenario: Unrelated repository path changes
- **WHEN** un PR no modifica piloto, OpenSpec change, workflow, inputs canónicos o scripts/perfiles comparados
- **THEN** path filters pueden evitar el job Ubuntu sin omitir una dependencia relevante

### Requirement: Toolchain provenance stays reproducible

La documentación MUST registrar versiones auditadas, sources primarios y commands
de instalación/verificación. OpenSpec/Node/npm/Chezmoi permanecen tooling remoto
de evaluación, no dependencias productivas implícitas.

#### Scenario: Evaluation dependency changes
- **WHEN** una versión instalada difiere de la auditada
- **THEN** doctor falla y exige revisión de provenance antes de nueva evidencia

### Requirement: No-adoption remains a complete path

Cerrar o rechazar el piloto MUST requerir solamente remover experimento, CI y
docs asociados; nunca rollback productivo porque Chezmoi no obtuvo ownership.
La presencia o remoción de packages del host queda para otra decisión.

#### Scenario: Reviewers choose no adoption
- **WHEN** el outcome es `reject` o se cierra la evaluación
- **THEN** los artifacts pueden eliminarse sin tocar perfiles, symlinks o homes

#### Scenario: Chezmoi package remains installed
- **WHEN** se cierra el piloto pero el package permanece en el host remoto
- **THEN** se documenta como tooling inerte y no como owner productivo
