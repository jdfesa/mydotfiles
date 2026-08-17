## Context

El deployment actual ya aporta propiedades de seguridad valiosas:

- `scripts/profile-resolve` expande layers revisados, rechaza sources inválidos
  o escapados, detecta ciclos y conflictos de ownership.
- `scripts/link` ofrece dry-run, rechaza archivos/directorios reales y solo
  reemplaza un symlink incorrecto cuando se solicita `--repair`.
- Starship y Kitty ya separan contenido shared de entrypoints por plataforma;
  X11, Wayland y desktop sessions permanecen explícitos.

El modelo es intencionalmente simple, pero solo despliega symlinks. Los datos Git
por host pertenecen a otro script y Windows no tiene perfil productivo. Chezmoi
agrega archivos materializados, templates, diff/status y soporte Windows, pero
también source names codificados, estado persistente, defaults implícitos y un
destino peligroso por defecto: el home real.

OpenSpec `1.9.0` y Chezmoi `2.72.0` son tooling de evaluación. Su presencia no
altera ownership productivo.

## Goals / Non-Goals

**Goals:**

- Construir un piloto cuya única escritura host-backed sea una raíz temporal
  marcada.
- Comparar workflows equivalentes del linker actual y Chezmoi con evidencia raw.
- Modelar casos literales, data-driven, entrypoints Kitty y Windows Terminal sin
  modificar archivos canónicos.
- Producir una proyección determinista completa y un outcome derivado de gates.
- Hacer posible un canary posterior sin autorizarlo.

**Non-Goals:**

- Diseñar todo el workstation provisioner o un archivo universal.
- Ejercitar hooks, externals, removals, encryption, password managers o package
  installation de Chezmoi.
- Ejecutar un piloto nativo macOS o modificar el controller.
- Seleccionar storage productivo para identidad Git o packages Windows.
- Realizar cutover, transferencia de ownership o lifecycle Git/PR.

## Decisions

### 0. Evaluate one bootstrap phase, not the whole provisioner

La arquitectura futura debe ser descomponible:

```text
prerequisites -> source acquisition -> user configuration
              -> OS packages/services -> verification -> manual/auth gates
```

Este piloto mide Chezmoi únicamente dentro de `user configuration`. Un script
pequeño es válido cuando reduce repetición o previene errores. Python standard
library se usa para lógica realmente compartida; shell para POSIX y PowerShell
para adaptación nativa. Todo adapter declara su support matrix y falla rápido
fuera de ella. No se fuerza portabilidad si aumenta la complejidad total.

### 1. Keep the experiment outside production trees

```text
experiments/chezmoi-pilot/
  README.md
  SUPPORT.md
  mappings.json
  semantics.json
  traceability.json
  data/{linux,macos,windows}.json
  fixtures/
  expected/{canonical-hashes,targets}.json
  scripts/{pilot.py,pilot_policy.py,run,validate,doctor,generate-docs,run-windows.ps1}
  tests/test_pilot.py
  evidence/review.json
  TRACEABILITY.md
docs/generated/
  chezmoi-pilot-matrix.md
  chezmoi-pilot-scorecard.md
```

Ningún perfil puede referenciar `experiments/chezmoi-pilot`. El source state se
staging nuevamente dentro de cada raíz temporal antes de invocar Chezmoi. Los
archivos `.json` contienen JSON real y se parsean con `json.loads`; no se usa una
extensión YAML engañosa ni se introduce una dependencia YAML.

Usar la raíz del repositorio como source Chezmoi fue rechazado porque invadiría
el layout actual y difuminaría ownership antes de una decisión de adoption.

### 2. Use redundant containment controls

El runner captura el home real antes de construir el ambiente, crea una raíz
`0700` nueva, escribe un marker con nonce y canonicaliza todos los paths. Rechaza
`/`, el home real, la raíz del checkout, sus parents, targets de perfiles, roots
reutilizados, markers inválidos y componentes symlink.

El ambiente POSIX hijo se construye desde cero. Del host solo hereda `PATH`; el
runner fija `HOME`, todos los XDG, `TMPDIR`/`TMP`/`TEMP`, locale, timezone y
`NO_COLOR`. No hereda tokens, proxies, `SSH_AUTH_SOCK`, sesiones o variables no
declaradas. Un runner Windows futuro podrá heredar únicamente `PATH`,
`SystemRoot`, `WINDIR`, `ComSpec` y `PATHEXT`, y deberá fijar `USERPROFILE`,
`LOCALAPPDATA` y temporales dentro del root marcado.

En Linux, Bubblewrap usa:

```text
--ro-bind / /
--bind <run> <run>
--proc /proc
--dev /dev
```

`/dev` y `/proc` son pseudo-filesystems privados. La raíz marcada es el único
path de filesystem host-backed escribible; los pseudo-filesystems privados
pueden ser escribibles. El kernel del host rechazó la creación del network
namespace, por lo que **no existe aislamiento de red**. El riesgo se reduce con
`--refresh-externals=never`, ausencia de externals/hooks y lint estático, pero no
se presenta como una garantía de red.

Cada comando Chezmoi repite flags explícitos de source, destination, config,
cache, persistent state, working tree, no pager/TTY, no refresh, skip secrets,
error on conflict y builtin diff. `apply` solo es alcanzable después de preview
y únicamente dentro del state machine del harness.

### 3. Disable high-risk Chezmoi features

La validación estática rechaza scripts ejecutables, hooks, externals, removals,
encryption, funciones de command/dynamic file/secret lookup y material con forma
de secreto. El piloto no intenta demostrar toda la amplitud de Chezmoi; prueba
solo lo necesario para decidir ownership de configuración de usuario.

### 4. Use deterministic fake fixture data

Cada run selecciona `pilot.platform` desde un JSON versionado. Git usa únicamente
`Pilot User`, `pilot@example.invalid` y credential helpers públicos de fixture.
No se lee Git global ni identidad/credenciales reales. Missing keys producen
error mediante `missingkey=error`.

Cross-rendering en Arch demuestra estructura, no runtime nativo. Windows nativo
debe validar paths, schema, encoding/line endings, idempotencia, rollback y ACLs.
macOS permanece audit-only salvo aprobación futura explícita para un destino
temporal.

### 5. Model the four cases without redesigning production

| Case | Pilot model | Rationale |
| --- | --- | --- |
| Starship | Copia literal byte-identical desde `shared/starship/starship.toml` | No requiere datos ni branches. |
| Git | Small template y fixtures falsos | Separa policy compartida de identidad/helper explícitos. |
| Kitty | Base shared más entrypoints Linux/macOS separados | Preserva `kitty_mod`, bindings, sesiones, clipboard y opciones nativas. |
| Windows | Fixture Windows Terminal separado | Es otra aplicación y otro formato; no es Kitty. |

Las transformaciones Kitty solo reemplazan paths convencionales por paths dentro
del destino temporal. No cambian actions ni chords canónicos.

### 6. Put semantic boundaries before template guardrails

```text
¿cambia aplicación, formato, significado o sesión?
  sí -> archivo separado
  no -> ¿es byte-identical y sin datos?
          sí -> literal
          no -> ¿sustituciones escalares locales mejoran legibilidad?
                  sí -> small-template candidate
                  no -> archivo separado
```

Cinco scalar keys, un conditional no nested y diez líneas divergentes son
tripwires conservadores **solo del piloto**. No constituyen política productiva,
no definen mantenibilidad y nunca prevalecen sobre semántica o legibilidad.

### 7. Model actual terminal semantics, not visual chord similarity

El vocabulario distingue:

- `terminal.new-os-window`: ventana superior del OS.
- `terminal.new-pane`: Kitty `new_window` o Windows Terminal `splitPane`.
- `terminal.focus-pane-left`: navegación espacial.
- `terminal.previous-pane-in-order`: navegación según orden de aplicación.

Kitty `new_window` crea una Kitty window/pane dentro del tab actual; no equivale
a Windows Terminal `newWindow`. Kitty `previous_window` es order-based y no
equivale a `moveFocus:left`. `pass_keys.py` implementa navegación espacial
contextual: pasa `ctrl+h` a Neovim o llama `neighboring_window(left)`.

Cada mapping de `semantics.json` apunta a una línea exacta del Kitty canónico o
a un objeto `command` exacto del fixture Windows Terminal. La validación rechaza
native actions incompatibles y collisions de chords. Los statuses
`unsupported-*`, `application-specific`, `order-based` y `contextual` son
preferibles a una equivalencia falsa.

Los modifier roles siguen separados: physical GUI/meta es descriptivo;
application-primary es Command en macOS y Ctrl en Linux/Windows; el modifier de
desktop/window-manager es definido por sesión y puede ser chord. AeroSpace
conserva Hyper (`cmd-alt-ctrl-shift`) y Meh (`alt-ctrl-shift`). Windows key queda
reservado.

Las referencias primarias son Kitty `actions`, `mapping` y `kitty.conf`, y
Microsoft Windows Terminal `actions`. El fixture mantiene Windows Terminal
estable `1.24.11321.0`, schema `https://aka.ms/terminal-profiles-schema`, path
packaged estable y formato `command` revisado.

### 8. Compare complete deterministic evidence projections

`review.json` conserva timestamps, contexto Git y runtime Python exacto para
auditoría humana, pero la comparación reproducible usa una única
`evidence_projection`. Excluye o normaliza únicamente:

- `recordedAt`;
- `startedAt`/`endedAt` de command records;
- el objeto Git dinámico de publicación completo: `branch`, `reviewedBase`,
  `headRevision` y `dirty`;
- el patch Python exacto, proyectado al contrato compatible `>=3.11` que también
  aplica `doctor`;
- el banner de build/distribuidor Chezmoi, proyectado a la versión semántica
  exacta `2.72.0`.

La evidencia raw conserva el banner Chezmoi completo. La proyección conserva
Chezmoi exactamente en `2.72.0`, OpenSpec exactamente en `1.9.0`, commands,
exits, previews, hashes, manifests, modes, paths normalizados, source provenance,
métricas, blockers, native evidence y outcome. Una versión Python incompatible o
Chezmoi distinta no se normaliza como válida. `validate` ejecuta evidencia fresca
y compara toda la proyección.
`generate-docs --check` hace la misma comparación antes de verificar contenido.
Los input digests de documentos son exactamente el digest de esa proyección.

### 9. Derive the outcome from explicit gates

El selector es puro y testeable:

1. Escritura fuera de root, overlap, secreto, feature prohibida, metadata
   protegida alterada, rollback fallido o idempotencia fallida => `reject`.
2. Otro mandatory incompleto, Windows nativo ausente o beneficio de complejidad
   no claro => `keep-and-continue-evaluation`.
3. Solo Windows nativo verdadero, todo mandatory aprobado y policy comparativa
   permisiva => `recommend-selective-migration`.

CI y doctor validan además el invariante que prohíbe una recomendación sin
Windows nativo.

### 10. Derive complexity metrics from declared scopes

Los file counts se calculan dinámicamente sobre scopes declarados. La comparación
reporta raw LOC para `scripts/link`, `scripts/profile-resolve`, `scripts/doctor`
y para automation/tests del piloto. LOC no se pondera: mezcla languages,
comments, validation y adapters, por lo que solo aproxima superficie de revisión.
No se oculta que el harness es considerablemente mayor que los scripts actuales.

Los internal command counts se derivan de command records. Eliminar la
invocación redundante de `chezmoi data` reduce la ejecución por fixture y obliga
a regenerar evidencia.

La policy de complejidad exige, como mínimo medible, no aumentar commands
internos ni persistent state para permitir una recomendación. LOC permanece
informativo y no participa del gate.

### 11. Make traceability typed and verifiable

`traceability.json` declara exactamente una entrada por escenario OpenSpec. Cada
entrada tiene uno de estos tipos:

- `automated-check`: ID estable registrado y locator concreto de test/check;
- `generated-evidence`: JSON pointer concreto dentro de `review.json`;
- `native-blocked`: evidencia nativa ausente;
- `human-review-gate`: decisión manual explícita.

El validator exige cobertura uno-a-uno, existencia de todo automated check ID y
resolución de cada JSON pointer. `TRACEABILITY.md` se genera desde esa fuente y
no denomina “test” a un integration run o gate humano.

### 12. Keep CI strict and honest

Linux CI ejecuta unit tests, evaluación fresca/proyección, generated-doc check,
outcome invariant, OpenSpec strict/doctor y validators relevantes. Path filters
cubren piloto, change OpenSpec, workflow, Starship/Kitty canónicos y scripts o
perfiles comparados.

El primer PR check demostró que anidar Bubblewrap dentro de un job container
Arch agrega una barrera Docker que bloquea el user namespace antes del sandbox.
La corrección elimina esa capa y ejecuta directamente sobre `ubuntu-22.04`
fijado. Esto reduce orquestación sin debilitar el boundary primario: no existe
job container, privileged mode, capability adicional, bypass seccomp/AppArmor,
sysctl, skip silencioso ni fallback fuera de Bubblewrap.

El job instala dependencias Ubuntu y las versiones exactas Chezmoi `2.72.0`,
OpenSpec `1.9.0`, Node.js `26.7.0` y npm `12.0.2` antes del sandbox. El binario
Chezmoi se verifica contra un SHA-256 fijado. Luego ejecuta primero un smoke test
con `/` read-only, private `/dev` y `/proc`; solo después hace checkout y corre
el harness estricto. El checkout usa history completa para que la provenance
Git calcule `reviewedBase` contra `origin/main` también bajo el PR merge ref. Las
descargas ocurren antes del sandbox y dentro del piloto
siguen prohibidos externals, hooks y refresh. La evidencia común no promete un
network namespace que el host Arch auditado no soporta.

El resultado CI se clasifica `portable-linux` en Ubuntu 22.04: no es evidencia
nativa Arch ni Windows. Arch se verifica separadamente sobre la máquina real con
profiles, symlinks y doctor. El job Windows permanece visiblemente disabled y no
cuenta como evidencia; el invariante executable es el gate real.

### 13. Preserve coexistence and rollback boundaries

El overlap lógico sirve solo para comparar casos equivalentes. Las rutas reales
del destino temporal no intersectan targets productivos. Chezmoi nunca obtiene
ownership real, por lo que cerrar/rechazar el piloto consiste en eliminar
experimento, workflow y docs; no existe rollback productivo.

Un cutover futuro requiere otro cambio, canary literal, snapshot, dry-run,
aprobación target-by-target, remoción simultánea del owner anterior y rollback
que restaure un único owner.

## Risks / Trade-offs

- **False confidence from Arch cross-rendering:** mitigado con labels
  `structural-only` y blocker Windows nativo.
- **Harness complexity dominates the tool:** mitigado con LOC/file/command
  dinámicos y policy no ponderada.
- **Network is not isolated:** documentado explícitamente; externals/hooks están
  prohibidos, pero el riesgo residual permanece visible.
- **Canonical Kitty drift:** hashes y líneas/actions exactos hacen fallar el run.
- **Stale evidence:** la proyección fresh-versus-reviewed y los doc digests
  completos impiden publicar métricas viejas.
- **Template growth:** límites semánticos mandan; tripwires numéricos son locales.

## Migration Plan

1. Validar source/model/traceability antes de ejecutar Chezmoi.
2. Crear roots temporales nuevos por plataforma y run.
3. Ejecutar config, managed, status, diff y dry-run.
4. Aplicar únicamente al destino temporal, repetir, introducir drift y restaurar.
5. Comparar dos runs limpios, baseline linker y proyección completa.
6. Regenerar evidencia/docs solo después de estabilizar implementación.
7. El controller audit aprobó publicar los artifacts del piloto mediante PR;
   esa aprobación no autoriza migration ni cutover productivo.

## Open Questions

- ¿Se aprobará un runner Windows nativo para paths, behavior, encoding, rollback
  y ACLs?
- ¿El runner directo `ubuntu-22.04` seguirá ofreciendo el user namespace
  requerido por Bubblewrap durante la vida de este piloto?
- ¿Conviene cerrar la evaluación si la complejidad sigue excediendo al linker?
- Si una evidencia futura recomienda migration, ¿cuál será el canary literal
  del nuevo cambio? Starship es el candidato normal, no una autorización.
