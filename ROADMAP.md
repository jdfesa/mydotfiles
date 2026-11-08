# Repository Roadmap

Este documento resume las capacidades versionadas y las prioridades de evolución
del repositorio. Las tareas concretas y sus criterios de cierre viven en
[TODO.md](TODO.md); la instalación y la verificación se documentan junto a cada
herramienta. El historial de Git conserva los estados anteriores.

La presencia de una configuración o de un paquete en un manifiesto no acredita
su instalación ni su despliegue en todas las máquinas. Los destinos se declaran
en [perfiles](profiles/README.md), y la promoción entre sistemas sigue el
[ciclo de vida de las workstations](docs/WORKSTATION_LIFECYCLE.md).

## Established Capabilities

Estas capacidades ya tienen fuentes o procedimientos versionados; no son
instalaciones pendientes del roadmap.

| Capacidad | Estado y evidencia |
|---|---|
| Shell y utilidades CLI | Zsh integra Starship, `eza`, `bat`, `ripgrep`, `fzf` y `zoxide`; véase [Zsh](shared/zsh/README.md). |
| Entorno de ventanas macOS | AeroSpace, Sketchybar y Borders tienen fuentes bajo `os/macos/` y destinos en el [perfil macOS](profiles/macos-main.links). La [distribución numérica 1–5](os/macos/aerospace/WORKSPACES.md) está en prueba y requiere aceptación de uso real; no acredita despliegue. |
| Terminales | [Ghostty](shared/ghostty/README.md) tiene configuración compartida; Kitty separa sus entrypoints de [macOS](os/macos/kitty/README.md) y [Linux](os/linux/kitty/README.md). |
| Sesiones de terminal | [Tmux](shared/tmux/README.md) tiene capas macOS/Linux, guías de uso diario, entrenamiento y recuperación de disposiciones. |
| Git y navegación | [Lazygit](shared/lazygit/README.md) y [Yazi](shared/yazi/README.md) tienen configuración y destinos en los perfiles macOS y Arch. |
| Monitorización | [Btop](shared/btop/README.md) y [Fastfetch](shared/fastfetch/README.md) tienen fuentes compartidas y destinos declarados por perfil. |
| Editores | [Neovim/LazyVim](shared/nvim/README.md) vive en `shared/nvim/`; [VS Code](shared/vscode/README.md) mantiene una configuración propia. No se presupone una migración completa entre editores. |
| Paquetes macOS | Hay [Brewfiles por capas](os/macos/packages/homebrew/README.md). Su existencia está resuelta; el curado y la comprobación de recuperación siguen siendo trabajo independiente. |
| Despliegue de dotfiles | Los [perfiles y capas](profiles/README.md) se resuelven, enlazan y diagnostican con los [scripts del repositorio](scripts/README.md), sin depender de Stow. |
| Verificación automatizada | [CI](.github/workflows/lint.yml) ejecuta ShellCheck, validadores, reconstrucción de perfiles en hogares aislados y pruebas de terminal Linux. |

## Current Focus

El foco inmediato es el mantenimiento documental, sin cambios de configuración
ni despliegues asociados:

1. Mantener explícita la sincronización desde GitHub antes de cualquier trabajo
   en cada máquina, según [AGENTS.md](AGENTS.md#cross-machine-synchronization).
2. Separar capacidades existentes, tareas pendientes e ideas todavía no
   aprobadas, con evidencia enlazada y criterios de cierre en [TODO.md](TODO.md).
3. Normalizar los README de herramientas: cuerpo en español, títulos en inglés,
   fuente canónica, perfil, dependencias y verificación reproducible.
4. Alinear la documentación de restauración y los manifiestos sin presentar un
   inventario importado como una recuperación completa ya validada.

## Future Capabilities

Estas líneas no autorizan instalaciones ni migraciones. Cada implementación
requiere un alcance propio, validación y aceptación antes de integrarse.

| Línea | Límite y criterio de avance |
|---|---|
| Recuperación reproducible | Curar dependencias y demostrar una restauración desde un entorno limpio, con secretos recuperables por separado; referencia: [Restore macOS](docs/RESTORE.md). |
| Calificación de Arch | Mantener el canary y documentar compatibilidad, uso sostenido y recuperación antes de promover cambios; referencia: [Workstation Lifecycle](docs/WORKSTATION_LIFECYCLE.md). |
| Provisioning de workstation | Ansible es candidato para paquetes, servicios y archivos privilegiados, no para duplicar el ownership de los dotfiles; requiere un piloto aislado según [ADR 0008](docs/adr/0008-separate-dotfile-deployment-from-workstation-provisioning.md). |
| Windows | Definir perfiles y automatización solo cuando exista validación nativa y una estrategia de privilegios; referencia: [Windows](os/windows/README.md). |

## Candidates And Boundaries

- **Atuin y otras utilidades opcionales:** permanecen como ideas en
  [Brew and Shell Ideas](os/macos/packages/homebrew/IDEAS.md). Antes de adoptar
  hooks de shell o sincronización de historial, definir necesidad, solapamientos
  y privacidad. No equivalen a tareas de instalación aprobadas.
- **Chezmoi:** el [resultado del piloto](docs/chezmoi-pilot-result.md) es evidencia
  histórica, no una migración autorizada. Los perfiles y symlinks siguen siendo
  el mecanismo productivo.
- **Stow, Yabai, Warp y frameworks de Zsh:** no tienen una adopción programada en
  este roadmap. Una reconsideración debe justificar una necesidad concreta y
  documentar convivencia o sustitución, verificación y recuperación.
- **Plugins y nuevas capas de Hyprland:** se ensayan en el canary; no se activan
  implícitamente en perfiles estables ni se trasladan a macOS.

## Maintenance Rules

Actualizar este documento y las tareas afectadas cuando cambie una capacidad.
Enlazar a las fuentes canónicas en lugar de duplicar comandos de instalación.
No conservar como pendientes herramientas ya incorporadas ni marcar una
capacidad como desplegada en todas las máquinas por su sola presencia en Git.
El flujo de ramas, revisión e integración se define en
[AGENTS.md](AGENTS.md#documentation-maintenance).
