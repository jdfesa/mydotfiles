## Context

Ver [proposal.md](proposal.md) para la motivación. El deployment productivo actual
resuelve perfiles y crea symlinks de usuario; en el canary ese contrato está sano
para `arch-hyprland`, pero no describe la workstation completa. La auditoría
encontró cuatro límites relevantes para el diseño:

- los hosts son inventarios informativos y no seleccionan paquetes, services ni
  archivos privilegiados;
- los manifests oficiales cubren capas de aplicaciones, mientras que boot,
  recovery, networking, audio, GPU y desktop fallback permanecen en el host;
- `scripts/doctor` valida symlinks y puede salir cero ante targets ausentes;
- CI reconstruye HOME en Ubuntu y no constituye evidencia de Pacman, systemd,
  boot, hardware o restore Arch.

El change no debe convertir una auditoría en un instalador destructivo. Primero
se necesita un modelo suficientemente completo para que un plan read-only revele
la diferencia entre “dotfiles enlazados” y “workstation convergida”.

## Goals / Non-Goals

**Goals:**

- representar el estado Arch como un grafo pequeño de roles y componentes
  revisables;
- producir un plan determinista sin root ni side effects;
- hacer visibles ownership, drift, dependencias, gates manuales y evidencia
  faltante;
- agregar strict verification y una escalera de pruebas con labels honestos;
- dejar contratos estables que un futuro script explícito o piloto Ansible pueda
  consumir sin redefinir la fuente de verdad.

**Non-Goals:**

- diseñar un instalador de discos, cifrado o boot dentro de este change;
- hacer converger automáticamente `/etc`, systemd o paquetes;
- convertir logs o snapshots del canary en desired state sin clasificación;
- fijar Arch indefinidamente a versiones históricas;
- transferir ownership desde los perfiles/symlinks actuales;
- mezclar el rollout del multiplexor con esta base arquitectónica.

## Decisions

### 1. Model components separately from composition

La composición vivirá bajo un namespace Arch explícito:

```text
os/linux/workstation/
  README.md
  schema/
    component.schema.json
    role.schema.json
  components/
    foundation.toml
    boot-recovery.toml
    networking.toml
    audio.toml
    graphics-common.toml
    graphics-intel.toml
    graphics-amd.toml
    display-recovery.toml
    wayland-desktop.toml
    daily-workstation.toml
  roles/
    arch-workstation.toml
    arch-hyprland.toml
  scripts/
    plan
    verify
  lib/
    arch_state.py
```

Un componente referencia fuentes existentes en vez de copiarlas: package lists,
profiles, service units, root-owned templates y checks continúan junto a su owner.
Un rol solo compone componentes. `hosts/<id>/host.toml` selecciona roles y conserva
facts/policy de la máquina; `profiles/*.links` sigue limitado a configuración de
usuario.

Alternativas rechazadas:

- **Agregar paquetes y services a `profiles/*.links`:** confunde user deployment
  con privilegios y rompe el formato simple actual.
- **Un único manifest gigante por host:** duplica estado reusable y convierte un
  cambio de hardware en copia completa.
- **Inferir desired state desde `pacman -Qqe`:** captura accidentes, dependencias
  temporales y deuda como política permanente.

### 2. Use typed TOML plus JSON Schema and Python standard library

Los manifests de composición usarán TOML legible, `schema_version = 1` y enums
cerrados. JSON Schema documentará forma, constraints y generación; el parser
autoritativo usará Python 3.11+ standard library (`tomllib`) con validación
semántica adicional. Python se declarará como dependencia de la foundation Arch.

El parser no ejecutará contenido ni expandirá shell. Paths serán relativos al
repositorio o expresiones permitidas como `$HOME/...`; identifiers usarán
kebab-case. Toda referencia se resolverá antes de consultar el host.

Se prefiere Python pequeño frente a AWK creciente porque arrays/tables TOML,
errores tipados, JSON determinista y tests de fixtures ya exceden lo que un parser
ad-hoc puede manejar con seguridad. No se incorpora framework ni package Python de
terceros.

### 3. Make ownership a first-class key

Cada recurso normalizado tendrá una key estable:

```text
package:official:<name>
package:reviewed:<name>
user-target:<expanded-target>
root-target:<absolute-target>
service:system:<unit>
service:user:<unit>
manual-gate:<id>
check:<id>
```

El resolver permite deduplicar solo declaraciones byte-identical con el mismo
owner efectivo. Dos definiciones distintas para la misma key fallan e informan la
cadena de composición completa. Un recurso observado pero no declarado es drift,
no un owner implícito.

Esta decisión permite evaluar Ansible después sin entregarle la definición del
estado: cualquier provisioner futuro consume el grafo y solo obtiene ownership
mediante otro change explícito.

### 4. Separate facts, selectors and policy

El preflight read-only normaliza un conjunto acotado de facts:

- `uname` architecture;
- UEFI versus legacy boot;
- CPU vendor;
- PCI GPU vendor y kernel driver;
- presencia de batería para desktop/laptop;
- root filesystem y encryption visibility;
- network reachability como observación, no identidad.

Selectors de componentes comparan esos facts con enums declarados. No se usarán
model names, connector names, DHCP addresses, seriales ni UUID como identidad
portable. Un selector desconocido, multiple GPU policy ambigua o arquitectura no
soportada produce `unsupported` antes de cualquier fase privilegiada.

El baseline no elige disco, particiones, encryption ni bootloader. Esos facts se
registran para diseñar el futuro ISO-to-SSH change y para impedir que una
workstation distinta herede silenciosamente la policy del canary.

### 5. Adopt a convergent-current package contract

El estado deseado fija nombres, roles, procedencia y constraints; no promete que
un rolling release entregue para siempre los mismos bytes. Toda futura convergencia
oficial comenzará con una sola transacción `pacman -Syu --needed`. Queda prohibido
refrescar bases y luego instalar selectivamente.

Después de un run, evidencia raw registrará repositorios, package versions y source
revision; una proyección redactada permitirá comparar cobertura y outcomes. Un
drill histórico utilizará una fecha de Arch Linux Archive como input explícito y
nunca cambiará mirrors productivos de forma implícita.

Paquetes se separan por propósito, al menos:

```text
foundation -> boot-recovery -> networking -> audio
           -> graphics selector -> display-recovery
           -> wayland-desktop -> daily-workstation
```

El primer inventario clasifica cada paquete explícito live como `desired`,
`dependency/build-only`, `local-reviewed`, `candidate-remove` o `unknown`. Nada se
elimina automáticamente. Duplicados entre lists se resuelven en el grafo y se
reportan para limpieza sin convertirlos en conflicto cuando la declaración es
idéntica.

Referencias operativas: [Arch system maintenance](https://wiki.archlinux.org/title/System_maintenance),
[Pacman](https://wiki.archlinux.org/title/Pacman) y
[Arch Linux Archive](https://wiki.archlinux.org/title/Arch_Linux_Archive).

### 6. Keep the baseline planner incapable of apply

`os/linux/workstation/scripts/plan` aceptará un host y uno o más roles. Su proceso:

```text
load schemas -> resolve graph -> collect safe facts -> observe state
             -> classify differences -> render human plan + JSON projection
```

No tendrá `--execute`, no invocará `sudo` y no reutilizará funciones mutadoras.
Los adapters de observación usarán comandos absolutos o allowlisted, timeouts y
salida parseada. La ausencia de systemd/Pacman en fixtures se representa como
`unsupported`, no como éxito.

Raw evidence con timestamps vive bajo
`${XDG_STATE_HOME:-$HOME/.local/state}/mydotfiles/evidence/`. La proyección
determinista se escribe solo cuando se solicita y excluye hostname no estable,
seriales, IPs, user paths privados, environment y cualquier valor secret-like.
Git versiona schemas, fixtures sintéticos y, después de revisión, una muestra
redactada; no versiona snapshots live completos.

### 7. Add layered verification rather than one overloaded doctor

`scripts/doctor` conservará su modo diagnóstico compatible y agregará `--strict`
para que missing targets fallen. El planner agregará verificadores por clase y un
resultado agregado que solo sea `converged` si todas las clases obligatorias pasan.

La evidencia declara uno de estos niveles:

| Level | Environment | Claim allowed |
|---|---|---|
| L0 | Static PR checks | Schema, references, syntax, docs |
| L1 | Rootless fixtures | Plan, user links, idempotence, injected rollback |
| L2 | Digest/date-pinned Arch container | Package resolution and transaction policy |
| L3 | Disposable UEFI VM | Blank-disk lifecycle, boot and systemd |
| L4 | Disposable VM failure drill | Resume, snapshot and external restore |
| L5 | Hardware fixtures plus real canary | Selector qualification |
| L6 | Live canary | Services, graphics, audio, suspend, SSH and drift |
| L7 | Timed restore drill | Cold/warm phase SLO evidence |

Este change implementa L0/L1 y define los contratos L2-L7. No se agregará un VM
job que aparente cobertura sin boot real. CI fijará versiones o digests de tools y
actions relevantes; un runner label móvil se registrará como environment, no como
una imagen reproducible.

### 8. Preflight portable paths and runtime dependencies

La validación de perfiles se amplía en dos capas:

1. **Lexical:** targets no vacíos, sin traversal, segments ambiguos ni delimiters.
2. **Physical:** el parent existente más cercano se canonicaliza y MUST permanecer
   debajo del home canonical; symlink ancestors que escapen fallan.

Cada component declara comandos/runtime que sus sources necesitan. Verificadores
específicos inspeccionan includes transitivos y rechazan referencias runtime a
`~/mydotfiles` cuando el checkout real difiere. El path convencional seguirá
documentado para humanos, pero no será un requisito oculto de ejecución.

### 9. Treat manual gates and secrets as planned state

Un manual gate contiene id, fase, reason, instructions document path y check seguro.
Ejemplos: GitHub auth, SSH/GPG restore, Bitwarden login, VNC credential, audio,
screen sharing y reboot. El planner informa `manual-gate`; nunca ejecuta login ni
lee valores.

Checks de presencia solo pueden registrar boolean, mode y una ruta redactada.
Además de `.gitignore`, L0 incorpora scanning de private-key markers, high-entropy
candidates y nombres prohibidos, con allowlist pequeña y revisada. Un finding
secret-like bloquea la publicación de evidence.

### 10. Put Arch documentation under a dedicated lifecycle index

La documentación normativa nueva se organiza así:

```text
docs/arch/
  README.md                 # índice y estado de soporte
  REPRODUCIBILITY.md         # contrato, ownership y límites
  RESTORE.md                 # flujo honesto por fases
  VERIFICATION.md            # ladder, evidence y drills
  BACKLOG.md                 # P0/P1/P2 y changes derivados
```

`docs/machines/` conserva hechos y evidencia de hosts; secciones históricas quedan
marcadas como tales. Conteos y matrices derivables se generan bajo `docs/generated/`
y `generate --check` evita drift. `docs/RESTORE.md` de macOS no se renombra ni
edita durante este scope; README enlazará ambas guías con nombres explícitos.

### 11. Measure three recovery clocks

No existe un único “restore en minutos”. La evidencia separa:

1. `ISO-to-SSH`: instalación, boot y acceso de recuperación;
2. `SSH-to-daily-ready`: packages, system state, user config y gates;
3. `dotfiles-only`: clone/link/strict verification sobre base compatible.

Cada clock registra cold/warm cache, bytes, network, retries, human time y blocked
gates. El primer drill crea baseline; los SLO numéricos se aprueban después con
datos. El objetivo cualitativo permanece: fuera de descargas, builds y gates
humanos, la orquestación debe aportar minutos, no horas.

## Risks / Trade-offs

- **[El schema se convierte en otro sistema complejo]** → comenzar solo con
  resources observados y dos roles; medir LOC/references y rechazar campos sin un
  consumidor o verificador.
- **[El inventario live legitima paquetes accidentales]** → exigir clasificación y
  reason; `unknown` permanece blocker y nunca se promueve automáticamente.
- **[Python no existe en una base mínima]** → declarar el preflight mínimo por
  separado; este baseline comienza después de red, sudo, Git y Python disponibles.
- **[Convergent-current no reproduce bytes históricos]** → conservar evidencia de
  versiones y usar Archive solo en drills fechados; no prometer bit reproducibility.
- **[Strict mode rompe automatización existente]** → mantener modo diagnóstico
  compatible y migrar gates explícitamente a `--strict`.
- **[Evidence filtra datos del host]** → fixtures sintéticos, redacción allowlist,
  secret scanning y review antes de versionar cualquier proyección live.
- **[Un planner read-only retrasa la automatización]** → reduce el riesgo de adoptar
  Ansible o scripts sobre un modelo incompleto; follow-ups pueden aplicar recursos
  por owner una vez que el plan sea estable.

## Migration Plan

1. Crear schemas, fixtures sintéticos y resolver de components/roles sin consultar
   el host.
2. Clasificar el inventario Arch live y representar solo capas P0 necesarias para
   boot/recovery y el perfil actual; dejar `unknown` visible.
3. Agregar adapters read-only, JSON projection y tests de redacción/determinismo.
4. Implementar physical path preflight, runtime dependency checks y
   `scripts/doctor --strict` sin cambiar el modo actual.
5. Agregar L0/L1 CI, generated-doc checks y documentación `docs/arch/`.
6. Ejecutar el plan en `lab-desktop-01` sin root, revisar findings y guardar una
   proyección redactada solo con aprobación.
7. Derivar changes independientes para package/service apply, VM blank-disk,
   backups/firewall/SMART y cada deuda P0/P1.

Rollback del change: retirar el planner, schemas, docs y strict mode; los perfiles
y el modo doctor existente continúan. No existe rollback de host porque este
baseline no aplica estado.

## Open Questions

- Los SLO numéricos de los tres clocks se fijarán después del primer drill medido;
  definirlos no cambia el modelo ni la implementación del baseline.
- El piloto de provisioning (scripts explícitos versus Ansible) se decide después
  de que el grafo cubra boot/recovery, no durante este change.
