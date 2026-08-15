# Hyprland Quattro Lab

Sesion canary paralela que adapta el comportamiento de Omarchy Quattro a este
Arch sin instalar Omarchy ni reemplazar la configuracion Hyprland estable.

## Boundaries

- `~/.config/hypr` continua siendo la sesion estable.
- `~/.config/hypr-quattro` contiene solamente el laboratorio Lua.
- Waybar, Mako, Wofi, Hyprlock, Hypridle y el agente PolicyKit actuales se
  conservan durante esta primera fase.
- XFCE/XRDP permanece como recuperacion.
- El runtime nunca carga archivos desde `references/`.
- No se importan repositorios Pacman, instalador, bootloader ni politica de
  actualizaciones de Omarchy.

La configuracion Lua deriva de Omarchy `v4.0.0`, revision
`f0020448ca87329199de7cb12f2015ebc4a3e5e7`, bajo licencia MIT. Las adaptaciones
eliminan comandos `omarchy-*`, conservan Bitwarden en lugar de 1Password y usan
las aplicaciones ya elegidas en este repositorio.

## Install

Primero crear los enlaces del perfil sin modificar archivos reales:

```sh
scripts/link --dry-run --repair arch-hyprland-quattro-lab
scripts/link --repair arch-hyprland-quattro-lab
```

Luego instalar exclusivamente la entrada adicional de SDDM/UWSM:

```sh
os/linux/hyprland/quattro-lab/scripts/install-session --dry-run
os/linux/hyprland/quattro-lab/scripts/install-session
```

La instalacion agrega:

```text
/usr/local/libexec/dotfiles-hyprland-quattro-lab
/usr/local/share/wayland-sessions/hyprland-quattro-lab.desktop
```

No cambia la sesion predeterminada ni modifica SDDM. En el siguiente login se
puede elegir `Hyprland Quattro Lab` manualmente.

## Validation

Validar el config exacto antes de iniciar la sesion:

```sh
HYPRLAND_QUATTRO_ROOT="$HOME/.config/hypr-quattro" \
  Hyprland --verify-config \
  --config "$HOME/.config/hypr-quattro/hyprland.lua"
```

Smoke test minimo:

1. abrir Kitty, Wofi, Thunar y Helium;
2. probar foco, movimiento, resize, grupos, scratchpad y workspaces;
3. verificar copy/paste normal y dentro de Kitty;
4. probar Waybar, Mako, bloqueo, DPMS y capturas;
5. cerrar mediante `Super+Escape` y `Logout` para confirmar `uwsm stop`;
6. volver a `Hyprland (uwsm-managed)` y verificar que sigue intacto.

`Super+K` abre el mapa resumido de atajos de esta sesion.

## Rollback

La sesion estable no se reemplaza. Para retirar la entrada del laboratorio:

```sh
os/linux/hyprland/quattro-lab/scripts/rollback-session \
  "$HOME/.local/state/mydotfiles/backups/hyprland-quattro-lab/<timestamp>"
```

El perfil puede permanecer enlazado sin afectar ninguna otra sesion. No se
promueve codigo a `os/linux/hyprland/config/` hasta completar el smoke test.
