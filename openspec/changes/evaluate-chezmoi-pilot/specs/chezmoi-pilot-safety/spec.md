## Purpose

Define la contención fail-closed, ownership, preview, rollback, drift, secretos,
ambiente y permisos del piloto Chezmoi sin modificar configuración real.

## ADDED Requirements

### Requirement: Every writable host-backed path is temporary and marked

El piloto MUST capturar el home real antes de alterar el ambiente, crear una raíz
temporal `0700` nueva con marker/nonce y alojar dentro de ella HOME, destination,
source, config, cache, persistent state, logs, backup, rollback, TMP y todos los
XDG. MUST rechazar `/`, home real, checkout, parents, targets activos, marker
ausente, root reutilizado y escapes symlink.

#### Scenario: Safe temporary root is accepted
- **WHEN** todos los paths canonicalizados son descendants sin symlink del root marcado y no intersectan paths protegidos
- **THEN** el harness permite preview y registra root-contained

#### Scenario: Real home is rejected
- **WHEN** source, HOME, destination, cache, state, logs, backup, rollback o temp resuelve al home real o lo contiene
- **THEN** falla antes de invocar Chezmoi

#### Scenario: Symlink escape is rejected
- **WHEN** un componente symlink conduce fuera del root marcado
- **THEN** falla aunque el path textual parezca temporal

### Requirement: Child processes receive a minimal environment

El ambiente MUST construirse con allowlist, no mediante `os.environ.copy()`.
POSIX heredará únicamente `PATH`; Windows futuro podrá heredar solo `PATH`,
`SystemRoot`, `WINDIR`, `ComSpec` y `PATHEXT`. HOME/XDG/TMP y equivalentes
Windows MUST fijarse dentro del root. Tokens, proxies, agent sockets, credentials
y estado no declarado MUST quedar fuera.

#### Scenario: Host has tokens and an SSH agent
- **WHEN** el proceso padre contiene variables secret-like, proxy credentials o `SSH_AUTH_SOCK`
- **THEN** ninguna aparece en el ambiente hijo y los temporales explícitos sí

#### Scenario: Future Windows runtime needs host variables
- **WHEN** el adapter Windows se ejecute nativamente
- **THEN** solo usa la allowlist Windows documentada y fija `USERPROFILE`, `LOCALAPPDATA` y temporales dentro del marker

### Requirement: Linux sandbox exposes no writable host path except the marker root

En Linux, Bubblewrap MUST montar `/` read-only, bindear únicamente el root marcado
como host-backed writable y crear private `/dev` más `/proc`. MUST NOT usar
`--dev-bind /dev /dev`. Debido al kernel auditado, no SHALL afirmar network
isolation; pseudo-filesystems privados pueden ser escribibles.

#### Scenario: Bubblewrap prefix is inspected
- **WHEN** se construye el prefix Linux
- **THEN** contiene `--ro-bind / /`, un solo `--bind <run> <run>`, `--proc /proc`, `--dev /dev`, y no contiene `--dev-bind` ni `--unshare-net`

#### Scenario: Network namespace is unavailable
- **WHEN** el host rechaza el namespace de red
- **THEN** evidencia/docs declaran `networkIsolated: false` y mantienen externals/hooks prohibidos sin prometer aislamiento

### Requirement: Effective Chezmoi paths are explicit

Cada command MUST declarar source, destination, config, cache, persistent state,
working tree, no pager/TTY, no external refresh, skip secrets y error on conflict.
La config temporal repite paths críticos y fake data. `dump-config` MUST coincidir
con el manifest; `.chezmoi.homeDir` queda prohibido.

#### Scenario: Host defaults disagree with explicit isolation
- **WHEN** un default Chezmoi apunta fuera del root
- **THEN** effective-config validation falla antes de managed/diff/apply

#### Scenario: Template references real-home semantics
- **WHEN** un template usa `.chezmoi.homeDir` o ambiente host
- **THEN** static validation lo rechaza

### Requirement: Canonical inputs are read-only comparison sources

Starship, Kitty, profiles y scripts productivos MUST ser inputs read-only. Toda
adaptación SHALL ocurrir en staging temporal y conservar provenance/hashes. El
piloto MUST NOT ejecutar `configure-git` ni leer identidad real.

#### Scenario: Representative input is staged
- **WHEN** se prepara un fixture
- **THEN** source state se copia dentro del root con mapping y hash canónico

#### Scenario: Production mutation is requested
- **WHEN** una operación intenta escribir un source canónico, perfil o config activa
- **THEN** containment/Bubblewrap bloquea la escritura y validation falla

### Requirement: Chezmoi and the linker never own the same real target

El overlap lógico puede documentar casos equivalentes, pero paths reales MUST ser
disjuntos. Los symlinks actuales permanecen authoritative hasta un cutover futuro
reviewed target-by-target que quite un owner antes de agregar el otro.

#### Scenario: Pilot target overlaps a profile target
- **WHEN** un destination real intersecta un target resuelto por perfiles
- **THEN** el piloto falla antes de preview

#### Scenario: Duplicate target appears inside one model
- **WHEN** dos sources Chezmoi administran el mismo target temporal
- **THEN** inventory validation falla

#### Scenario: Future cutover is proposed
- **WHEN** una propuesta posterior transfiere un target
- **THEN** debe declarar owner anterior/nuevo y probar que nunca coexisten

### Requirement: Preview tokens prevent stale apply

El flujo MUST ejecutar status, diff y dry-run antes de apply. Un preview token
liga platform, nonce y digest de inputs. Cambios posteriores invalidan apply.

#### Scenario: Preview is clean and current
- **WHEN** token, marker e input digest coinciden
- **THEN** el state machine permite apply únicamente al destination temporal

#### Scenario: Source changes after preview
- **WHEN** source/config/data cambia antes de apply
- **THEN** el digest difiere y apply se rechaza

### Requirement: Idempotence drift and rollback are measured

Cada plataforma MUST ejecutar dos runs limpios; dentro de cada run, segundo
apply/dry-run/diff MUST ser no-op. El harness MUST introducir drift temporal,
detectarlo, restaurar contenido y recuperar destination más state al baseline.

#### Scenario: Clean runs match
- **WHEN** dos roots nuevos renderizan el mismo fixture
- **THEN** manifests y projection-relevant evidence son idénticos

#### Scenario: Second apply changes state
- **WHEN** segundo apply, dry-run o diff produce cambio
- **THEN** idempotencia crítica falla y outcome selector rechaza

#### Scenario: Temporary rollback succeeds
- **WHEN** termina la prueba de drift
- **THEN** destination y persistent state coinciden exactamente con baseline

#### Scenario: No-adoption outcome is selected
- **WHEN** se cierra/rechaza el piloto
- **THEN** no existe rollback productivo porque nunca obtuvo owner real

### Requirement: Drift and provenance remain visible

La evidencia MUST incluir manifests paths/types/modes/hashes, source provenance,
command outputs normalizados y detección de drift. Normalización de texto MUST
ocurrir después de containment y no puede ocultar escapes.

#### Scenario: Canonical input changes
- **WHEN** cambia un Starship/Kitty canónico sin revisar expected hashes
- **THEN** validation falla antes del render

#### Scenario: Temporary destination changes out of band
- **WHEN** se modifica un archivo aplicado
- **THEN** Chezmoi status detecta drift y lo registra

### Requirement: Secrets and authentication remain outside the pilot

Fixtures MUST ser públicos/falsos. Static y rendered/log scans MUST rechazar
private keys, tokens, credentials y funciones que ejecuten commands o consulten
secret stores. La evaluación no lee sesiones GitHub/Git/SSH/password-manager.

#### Scenario: Secret-like fixture is introduced
- **WHEN** aparece material secret-like o lookup prohibido
- **THEN** validation falla sin imprimir el valor

#### Scenario: Host authentication exists
- **WHEN** el host tiene sesiones autenticadas
- **THEN** allowlist y fake data impiden leerlas o exportarlas

### Requirement: Permissions are explicit and unprivileged

El piloto MUST declarar modes de files/directories, rechazar setuid/setgid,
world-writable o executables inesperados y registrar ACL Windows por separado.
Nunca invoca sudo ni escribe paths root-owned.

#### Scenario: POSIX modes match
- **WHEN** un fixture Linux o macOS simulado se aplica temporalmente
- **THEN** todos los paths cumplen modes declarados

#### Scenario: Privilege would be required
- **WHEN** un target requiere root o system path
- **THEN** queda fuera de scope y el piloto falla sin elevar

#### Scenario: Windows permissions are reviewed
- **WHEN** exista validación Windows nativa
- **THEN** evidencia registra ACL inheritance/explicit y falla ante acceso más amplio

### Requirement: Chezmoi remains user-configuration-only

Packages, servicios privilegiados, mutable state, caches, auth sessions, hardware
y provisioning general SHALL permanecer fuera salvo otro cambio independiente.

#### Scenario: Provisioning item enters the pilot
- **WHEN** un source/script intenta administrar uno de esos elementos
- **THEN** scope validation falla e identifica ownership externo

### Requirement: Executable Chezmoi automation remains prohibited

Source state MUST NOT contener run scripts, hooks, externals, removals o encrypted
payloads. Commands MUST desactivar refresh/secret evaluation y fallar conflicts.

#### Scenario: Executable source attribute appears
- **WHEN** inventory detecta una feature ejecutable/prohibida
- **THEN** validation falla antes de que Chezmoi la evalúe

#### Scenario: Conflict requires a choice
- **WHEN** Chezmoi detecta un conflict no interactivo
- **THEN** command termina non-zero y la evidencia no aplica una resolución implícita
