# Chezmoi Pilot

## Purpose

Este directorio contiene una evaluación no productiva de Chezmoi. Mide si puede
simplificar la futura fase `user configuration` de un bootstrap personal
cross-platform sin ocultar complejidad ni tomar ownership de paquetes,
servicios, autenticación, permisos, reinicios o secretos.

`scripts/link`, `scripts/profile-resolve`, perfiles y `configure-git` siguen
siendo autoridad productiva. Ningún perfil referencia este experimento y ningún
archivo canónico se mueve, edita o reemplaza.

## Safety Model

Cada ejecución crea una raíz `0700` nueva con marker/nonce. HOME, destination,
source, config, cache, persistent state, logs, backup, rollback, TMP y XDG viven
debajo de ella. Los paths se canonicalizan y se rechazan home real, checkout,
parents, targets activos, root reutilizado y escapes symlink.

Los child processes reciben un ambiente allowlisted: POSIX hereda únicamente
`PATH`; HOME/XDG/TMP/locale/timezone se fijan explícitamente. Tokens, proxy
credentials y `SSH_AUTH_SOCK` no se heredan. La allowlist Windows futura está
documentada en el design OpenSpec y no cuenta como evidencia nativa.

En Linux, Bubblewrap monta `/` read-only, bind-mount únicamente la raíz marcada
y crea private `/dev` y `/proc`. La raíz marcada es el único path host-backed
escribible; esos pseudo-filesystems privados pueden ser escribibles. El host no
pudo crear un network namespace, por lo que **no se afirma aislamiento de red**.
Externals, hooks y refresh siguen prohibidos, pero esa limitación permanece
explícita.

## Representative Cases

- **Starship:** literal byte-identical de `shared/starship/starship.toml`.
- **Git:** small template con identidad pública falsa `example.invalid`; no se
  ejecuta ni copia `configure-git`.
- **Kitty:** `shared/kitty/common.conf` conserva bindings, helpers y sesiones;
  Linux/macOS mantienen entrypoints, `kitty_mod`, clipboard y chords separados.
- **Windows Terminal:** fixture separado contra versión `1.24.11321.0`; nunca se
  presenta como Kitty.

## Semantic Actions

`semantics.json` distingue OS window, pane/Kitty window, spatial focus y
previous-in-order. Cada mapping apunta a una línea canónica Kitty o a un command
exacto del fixture Windows Terminal. `new_window` no equivale a `newWindow`, y
`previous_window` no equivale a `moveFocus:left`. Statuses unsupported,
contextual o application-specific son resultados válidos.

## Commands

```sh
# Unit tests y comparación fresh de la proyección completa.
experiments/chezmoi-pilot/scripts/validate

# Regenerar evidencia reviewable después de estabilizar behavior.
experiments/chezmoi-pilot/scripts/run

# Regenerar o comprobar documentos derivados.
experiments/chezmoi-pilot/scripts/generate-docs
experiments/chezmoi-pilot/scripts/generate-docs --check

# Doctor read-only.
experiments/chezmoi-pilot/scripts/doctor
```

`generate-docs --check` también ejecuta una evaluación fresh y compara toda la
proyección determinista antes de aceptar los documentos. No basta con que el
outcome coincida.

`scripts/run-windows.ps1` queda preparado para una revisión futura; no debe
ejecutarse sin runner nativo aprobado. macOS permanece audit-only.

## Failure Modes

El harness falla ante containment inválido, ambiente heredado no permitido,
source features peligrosas, secreto, missing fixture data, ownership duplicado,
canonical drift, semantic false mapping/collision, preview obsoleto, mode
inesperado, evidencia fresh distinta o documentación generada stale.

## Rollback

Antes del apply temporal se respaldan destination y persistent state dentro del
root. El run introduce drift, lo detecta, restaura contenido y finalmente vuelve
al baseline exacto. No existe rollback productivo porque no se tocó producción.

## Evidence and Traceability

`evidence/review.json` conserva commands, exits, hashes, manifests, modes,
métricas, blockers, native state, runtime Python exacto y provenance Git raw. Su
proyección determinista elimina timestamps y los cuatro campos Git dinámicos de
publicación (`branch`, `reviewedBase`, `headRevision`, `dirty`), y proyecta cada
patch Python compatible al contrato `>=3.11`. Chezmoi y OpenSpec permanecen
exactos. `traceability.json` declara una entrada tipada por escenario OpenSpec;
`TRACEABILITY.md` es generated.

## Ownership

Las copias staged son snapshots no autoritativos. `mappings.json` registra su
source y `expected/canonical-hashes.json` detecta drift. Toda migration requiere
otra change OpenSpec y transferencia target-by-target con un solo owner.
