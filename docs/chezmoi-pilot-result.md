# Chezmoi Pilot Result

## Outcome

`keep-and-continue-evaluation`

El outcome se deriva del selector executable. Todos los controles críticos del
piloto aislado pasan, pero `nativeEvidence.windows` permanece falso y la policy
comparativa no encuentra un beneficio claro: Chezmoi usa más commands internos y
agrega persistent state. Por eso no puede recomendar selective migration.

Este resultado no autoriza cutover. `scripts/link`, `scripts/profile-resolve`,
perfiles y `configure-git` continúan como owners productivos.

El piloto original se publicó mediante el PR `#14`. El audit Arch posterior
detectó que un SSH no interactivo podía omitir `~/.local/bin` de `PATH`; este
follow-up corrige discovery sin cambiar el outcome, aportar evidencia Windows
nativa ni autorizar migration o modificación de configuración activa.

## Strategic Fit

Chezmoi se evaluó solamente para la futura fase `user configuration`:

```text
prerequisites -> source acquisition -> user configuration
              -> OS packages/services -> verification -> manual/auth gates
```

Paquetes, servicios privilegiados, autenticación, secretos, permisos del
sistema, reinicios, hardware, caches y estado mutable siguen fuera.

## Deterministic Evidence

`validate` ejecuta una evaluación fresh completa y compara toda la proyección de
evidencia con `evidence/review.json`. `generate-docs --check` repite ese gate
antes de comprobar Markdown. Si difiere, el error enumera paths y valores de la
proyección ya normalizada para diagnosticar drift sin ocultarlo ni saltear el
gate.
La proyección elimina timestamps y el contexto Git
dinámico de publicación completo (`branch`, `reviewedBase`, `headRevision`,
`dirty`). Conserva el runtime Python exacto en raw evidence, pero lo proyecta al
contrato compatible `>=3.11`. Conserva el banner Chezmoi completo en raw, pero
proyecta los builds Arch/upstream a la versión exacta `2.72.0`; OpenSpec permanece
exactamente `1.9.0`. Commands, exits, paths, hashes, manifests, modes, métricas,
blockers, native state y outcome continúan siendo sensibles.
Para `dump-config`, raw evidence conserva hash, line count y preview de los
defaults emitidos por cada host; la proyección usa el hash canónico de los paths
y datos efectivos que el harness valida. Así Ubuntu/Arch pueden diferir en
defaults irrelevantes sin ocultar un cambio behavioral.

Final projection digest:
`7e2243d2e3577f6a5772497c45dc1f546bec7b27793007e22deed8840bd822c7`.

Focused tests prueban que timestamps, un rebase merge sintético a `main` y otro
patch Python compatible no alteran la proyección. Un cambio de command, hash,
manifest, metric, Chezmoi/OpenSpec exactos o Python incompatible sí la altera.
Un banner de distribuidor distinto para el mismo Chezmoi `2.72.0` no altera la
proyección ni `previewDigest`; una versión Chezmoi distinta sí.

## OpenSpec Discovery

El harness resuelve OpenSpec en orden mediante `OPENSPEC_BIN`,
`shutil.which("openspec")` y el candidato POSIX derivado
`Path.home() / ".local/bin/openspec"`. Un override inválido falla de forma
explícita. Si todos los métodos faltan, el diagnóstico enumera cómo resolverlo
sin volcar el ambiente ni valores secret-like.

No se incorporó un candidato npm user-local Windows: su ubicación depende de la
configuración npm y todavía no existe un runner nativo revisado. Windows usa
`OPENSPEC_BIN` o `PATH` por ahora.

## Semantic Corrections

- Kitty `new_window` se modela como `terminal.new-pane`; Windows Terminal
  `newWindow` como `terminal.new-os-window`.
- Kitty `previous_window` se modela como previous-in-order; no equivale a
  Windows Terminal `moveFocus:left`.
- Kitty `ctrl+h` queda documentado como navegación contextual: pass-through a
  Neovim o `neighboring_window(left)` mediante `pass_keys.py`.
- Cada mapping valida una línea canónica Kitty o un objeto `command` exacto del
  fixture Windows Terminal.
- Los tests negativos rechazan false native mappings y chord collisions.
- AeroSpace Hyper/Meh permanece exacto y Windows key sigue reservado.

## Measured Comparison

| Measure | Current model | Chezmoi pilot |
| --- | ---: | ---: |
| Operator entry commands | 3 | 1 |
| Measured internal commands | 6 | 10 por fixture |
| Comparison/automation files | 3 | 10 automation/test files |
| Raw automation/test LOC | 381 | 2,887 |
| Main harness LOC | N/A | `pilot.py`: 1,701 |
| Templates | 0 | 1 |
| Persistent state | 0 | 1 DB temporal por run |
| Native Windows | No soportado | Bloqueado; structural-only en Arch |

LOC es raw y no ponderado: mezcla languages, comments, validation y adapters;
no equivale por sí solo a complejidad cognitiva. Sí revela una superficie de
revisión considerablemente mayor que los scripts productivos comparados.

## Safety and Environment

- POSIX hereda únicamente `PATH`; HOME/XDG/TMP/locale/timezone son temporales.
- Tokens, proxies y `SSH_AUTH_SOCK` no pasan a child processes.
- Windows futuro puede heredar únicamente `PATH`, `SystemRoot`, `WINDIR`,
  `ComSpec` y `PATHEXT`; `USERPROFILE`/`LOCALAPPDATA` serán temporales.
- Bubblewrap usa `/` read-only, un solo bind host-backed escribible para el root
  marcado, private `/dev` y private `/proc`.
- El host rechazó el network namespace: `networkIsolated` es falso. No se promete
  aislamiento de red.
- Externals, hooks, secret lookup y refresh continúan prohibidos.
- Writes fuera de root, ownership overlaps, secret findings, prohibited findings
  y protected metadata changes: cero.
- Segundo apply/dry-run: cero cambios; drift detectado; rollback exacto.

## Traceability

Los 98 escenarios OpenSpec tienen 98 entries declaradas:

- 57 `automated-check` con ID y locator concretos;
- 28 `generated-evidence` con JSON pointer;
- 3 `native-blocked`;
- 10 `human-review-gate`.

El validator rechaza IDs stale, pointers no resolubles, duplicados y diferencias
entre scenarios y entries. Un gate humano o native block no se llama test.

## CI Behavior

El workflow Linux ejecuta unit tests, comparación fresh, generated-doc check,
outcome invariant, OpenSpec strict/doctor y validators del repositorio. Path
filters cubren piloto, change OpenSpec, workflow, inputs Starship/Kitty/AeroSpace
y scripts/perfiles comparados.

El primer PR check falló porque Docker bloqueó el user namespace antes de que
Bubblewrap pudiera crear el sandbox dentro del container Arch. No se aceptó
`seccomp=unconfined` ni otra relajación. El workflow ahora usa directamente el
VM fijado `ubuntu-22.04`, sin job container, privileged mode, capabilities,
bypass seccomp/AppArmor, sysctl, skip ni fallback.

Las dependencias y herramientas fijadas se instalan antes del sandbox.
ShellCheck `0.11.0` se obtiene del release oficial con SHA-256 fijado porque el
parser empaquetado por Ubuntu 22.04 es anterior al usado por el repositorio; así
se conserva el validator completo en vez de omitirlo. El smoke test Bubblewrap
estricto ocurre antes del checkout y del harness completo; exige
`/` read-only, private `/dev`/`proc` y temp privado. El checkout conserva history
completa para calcular `reviewedBase` contra `origin/main`. Esta arquitectura elimina
una capa de namespaces sin debilitar Bubblewrap. Su resultado es evidencia
`portable-linux` en Ubuntu, no native Arch ni native Windows. Arch se cubre
separadamente con doctor, profiles y symlinks en la máquina real. El job Windows
disabled permanece visible, pero no cuenta como gate executable.

## Native Blockers

- Windows Terminal no fue ejecutado en Windows: faltan behavior, paths reales,
  encoding/line endings, idempotencia, rollback y ACLs.
- El harness macOS no fue autorizado ni ejecutado; macOS sigue audit-only.
- No se creó propuesta de selective migration.

## Task Status

La change queda en `65/67` tareas completadas. Permanecen abiertas:

- `6.6`: native Windows evidence, bloqueada sin runner revisado.
- `9.4`: no aplica con el outcome actual; requiere otra change si una revisión
  futura recomienda migration.

La tarea `9.5` queda completada en este follow-up porque merge, branch cleanup y
sincronización Arch del PR `#14` ya ocurrieron y pudieron verificarse sin
anticipar estado futuro.

## No-Adoption Path

Cerrar o rechazar la evaluación requiere eliminar experimento, workflow y docs;
no hay rollback productivo porque Chezmoi nunca obtuvo un target real. Retener o
remover Node.js/npm/Chezmoi del host, o adoptarlos en manifests, es otra decisión.

## Next Decision

La próxima decisión es habilitar o no un runner Windows nativo revisado. Sin esa
evidencia y sin ventaja clara de complejidad, el outcome máximo es continuar la
evaluación.
