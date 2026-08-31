## Why

Arch ya instala tmux y conserva una configuración candidata, pero ningún perfil la
despliega, el host no la usa y la documentación mezcla estados “activo”, “pendiente”
y macOS/Homebrew. Una comparación actual de tmux y Zellij permite elegir un único
owner de sesiones terminales antes de sumar más integración implícita.

## What Changes

- Adoptar tmux como único multiplexor productivo del perfil Arch, comenzando con
  funcionalidad core y package oficial de Arch.
- Corregir la configuración candidata para usar XDG, `tmux-256color` verificado,
  terminal features acotadas y paths portables; eliminar defaults inseguros o no
  demostrados.
- Crear una capa Arch explícita y canary-first, separada de shell, Kitty, Ghostty y
  otras plataformas; no autoarrancar tmux desde startup genérico.
- Validar detach/reattach, SSH local-remoto, clipboard, true color, undercurl,
  resize, aplicaciones TUI, layouts y rollback en Kitty y Ghostty.
- Reconstruir workspaces mediante scripts declarativos e idempotentes; documentar
  que los procesos sobreviven desconexiones, no reboot ni crash del servidor.
- Mantener TPM, Sesh, tmux-resurrect y cualquier plugin/download fuera del baseline.
- Registrar Zellij como alternativa rechazada para producción inmediata y como
  challenger opcional mediante un perfil canary mutuamente exclusivo de máximo 14
  días, solo si tmux no supera gates de ergonomía o recuperación.
- Publicar ADR, runbook, keybindings y criterios medibles de promoción/rollback.

### Scope

- Arch Linux canary `lab-desktop-01`, tmux desde Arch Extra, Kitty y Ghostty.
- Configuración de usuario, profile layer, tests rootless y validación manual
  read-only/interactive explícita.

### Non-goals

- Activar tmux en macOS, Windows u otro host.
- Mantener tmux y Zellij autoarrancados, anidados o activos simultáneamente.
- Instalar Zellij, Sesh o plugins en el baseline productivo.
- Prometer persistencia de procesos después de reboot o restaurar comandos con
  efectos laterales.
- Cambiar Zsh, el login shell o el inicio de terminal global para forzar attach.
- Publicar benchmarks de RAM/CPU inferidos desde el tamaño del package.

### Rollback / No-adoption

Antes de retirar la capa se enumeran sesiones y se pide al operador guardar o
cerrar trabajo. El rollback elimina únicamente el symlink/profile Arch y vuelve al
shell normal; no mata sesiones silenciosamente. El package puede conservarse o
retirarse en un cambio de paquetes separado. Zellij permanece sin instalar y no
requiere rollback.

## Capabilities

### New Capabilities

- `arch-terminal-multiplexing`: deployment, comportamiento, compatibilidad,
  operación SSH, workspace reconstruction, evidencia canary y rollback de tmux.

### Modified Capabilities

Ninguna. No existe un contrato productivo previo de multiplexing.

## Impact

- Afecta `shared/tmux/`, una nueva capa bajo `profiles/layers/`, el perfil Arch
  seleccionado, package/runtime validation, documentación y tests.
- `tmux` ya está en `10-workstation-base.txt` y en el host; no se agrega AUR ni
  descarga runtime.
- Sesh y la configuración Ghostty macOS-centric permanecen fuera de ownership; la
  documentación dejará de llamarlos activos en Arch.
- El rollout requiere interacción canary y SSH, pero no root ni cambios de service.
