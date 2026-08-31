## Why

El repositorio reconstruye correctamente los 19 symlinks del perfil Arch activo,
pero todavía no puede explicar ni verificar una workstation nueva: gran parte de
los paquetes, servicios, archivos privilegiados, decisiones de hardware, gates
manuales y rutas de recuperación existen solo en el host o en prosa histórica.
Antes de incorporar un provisioner o prometer una restauración de pocos minutos,
se necesita un contrato Arch completo, medible y seguro que convierta ese estado
implícito en un plan revisable.

## What Changes

- Definir un grafo de estado deseado exclusivo de Arch que relacione roles de
  workstation con paquetes oficiales y revisados, perfiles de usuario, servicios,
  archivos privilegiados, facts de hardware, gates manuales y verificadores, sin
  duplicar ownership.
- Agregar un entrypoint read-only que seleccione un host y roles, detecte hardware,
  produzca un plan determinista y compare estado deseado con estado observado sin
  solicitar privilegios ni modificar el sistema.
- Establecer una política `convergent-current`: cada apply futuro comenzará con una
  actualización Arch completa y sincronizada; la evidencia registrará versiones y
  hashes efectivos, mientras que los restores históricos se ensayarán por separado
  con Arch Linux Archive.
- Hacer estricta y componible la verificación: package coverage, dependencias de
  runtime, servicios, root-owned files, symlinks, hardware, manual gates, backups y
  evidencia de recuperación deberán informar estados distintos y accionables.
- Incorporar pruebas rootless de plan, segunda ejecución sin cambios, drift,
  interrupción y rollback; reservar contenedores Arch, VMs UEFI y host canary para
  niveles posteriores claramente etiquetados.
- Crear documentación Arch específica para arquitectura, restore, operación,
  evidencia y tiempos por fase, y corregir afirmaciones obsoletas que hoy mezclan
  inventario histórico con estado normativo.
- Publicar una matriz de deuda priorizada y cambios posteriores pequeños; este
  baseline no convierte toda la workstation ni activa un provisioner opaco.

### Scope

- Arch Linux x86_64, comenzando en `lab-desktop-01` como canary.
- Declaración, planning read-only, validación, documentación y evidencia.
- El tramo desde una instalación Arch mínima con red, usuario sudo y Git hasta un
  plan completo de workstation; el diseño registra el lifecycle previo sin
  automatizar todavía operaciones destructivas de disco o boot.

### Non-goals

- Modificar macOS, Windows, NixOS o sus perfiles y manifests.
- Particionar discos, configurar cifrado, instalar el bootloader o mutar el host
  activo durante este change.
- Adoptar Ansible, Chezmoi u otro owner productivo.
- Versionar secretos, datos personales, caches, builds o session state.
- Activar tmux o Zellij; esa decisión y rollout viven en un change independiente.
- Prometer un tiempo absoluto antes de ejecutar y medir restores cold-cache y
  warm-cache.

### Rollback / No-adoption

El baseline agrega contratos, validadores read-only y documentación; no obtiene
ownership privilegiado. Rechazarlo consiste en retirar esos artefactos y conservar
los perfiles/symlinks actuales. Cualquier follow-up con apply deberá definir su
propio backup, rollback y gate de autorización.

## Capabilities

### New Capabilities

- `arch-workstation-contract`: modelo declarativo y componible del estado Arch,
  sus owners, roles, hardware, dependencias y gates manuales.
- `arch-reproducibility-verification`: planning, drift detection, validación por
  niveles, evidencia reproducible y medición honesta del restore.

### Modified Capabilities

Ninguna. Todavía no existen specs principales para estos contratos y el deployment
productivo de symlinks conserva su ownership.

## Impact

- Afecta `os/linux/packages/`, `profiles/`, `hosts/`, `scripts/`, documentación
  Arch y CI, exclusivamente mediante declaración y verificación en esta fase.
- Requiere definir schemas versionados y parsers explícitos; no incorpora una
  dependencia de provisioning hasta que un piloto separado demuestre menor
  complejidad total.
- Expone deuda actualmente silenciosa —paquetes sin owner, services sin política,
  paths hard-coded y gates manuales— como resultados fallidos o incompletos, por lo
  que algunos checks existentes dejarán de considerarse evidencia suficiente.
- Los perfiles de macOS/Windows, Chezmoi y la configuración activa del host no se
  modifican.
