# Curated Quattro Daily Workstation

Esta capa convierte Quattro Lab en una estacion diaria deliberada. No instala
`omarchy-base.packages`, preinstalls ni repositorios de Omarchy. `mydotfiles`
conserva la lista y los overrides; pacman usa solo los repositorios oficiales
ya habilitados.

## Auditoria del 2026-08-15

`pacman -Si` confirmo estos nombres en `extra`. Las versiones son evidencia de
la auditoria, no pins: Arch se actualiza como sistema completo.

| Necesidad | Paquete oficial | Version auditada | Estado inicial |
|---|---|---:|---|
| Captura | `grim`, `slurp`, `wl-clipboard` | `1.5.0-2`, `1.5.0-2`, `1:2.3.0-1` | instalados |
| Anotacion | `satty` | `0.21.1-1` | pendiente |
| Grabacion rapida | `gpu-screen-recorder` | `6.0.0-1` | pendiente |
| Preview/webcam del comando fijado | `mpv` | `1:0.41.0-4` | pendiente |
| Grabacion completa | `obs-studio` | `32.2.1-6` | pendiente |
| Edicion de video | `kdenlive` | `26.04.3-2` | pendiente |
| Notas | `obsidian` | `1.13.6-1` | pendiente |
| Chat | `discord`, `telegram-desktop` | `1:1.0.153-1`, `7.0.9-2` | pendientes |
| Terminal principal/alternativo | `kitty`, `ghostty` | `0.48.2-1`, `1.3.1-2` | instalados |
| Password manager | `bitwarden` | `2026.3.1-2` | pendiente |
| Video | `vlc` | `3.0.23_2-10` | pendiente |
| Oficina estable en espanol | `libreoffice-still`, `libreoffice-still-es` | `25.8.7-5`, `25.8.7-1` | pendientes |

El manifiesto es
[`40-quattro-daily-workstation.txt`](../../packages/lists/40-quattro-daily-workstation.txt).
`LibreOffice Still` se elige por su rama de mantenimiento; `Fresh` no agrega
una necesidad concreta a este workstation.

## Instalacion, update y verificacion

```bash
# Metadata y plan, sin privilegios
os/linux/packages/scripts/install-official-list \
  os/linux/packages/lists/40-quattro-daily-workstation.txt
os/linux/hyprland/quattro-lab/scripts/check-daily-workstation --metadata-only

# Aplicacion supervisada
os/linux/packages/scripts/install-official-list --execute \
  os/linux/packages/lists/40-quattro-daily-workstation.txt
scripts/link --repair arch-hyprland-quattro-lab
os/linux/hyprland/quattro-lab/scripts/check-daily-workstation
os/linux/hyprland/quattro-lab/scripts/check-runtime

# Updates posteriores (leer primero las noticias de Arch)
sudo pacman -Syu
os/linux/hyprland/quattro-lab/scripts/check-daily-workstation
```

El installer usa `pacman -Syu --needed`; repetirlo es idempotente. El check no
abre aplicaciones: revisa paquetes, ownership de binarios, desktop entries,
sintaxis y resolucion de comandos. No captura, no graba y no abre un vault.

## Shortcuts, menu y backends

| Accion | Comando fijado v4.0.0 | Backend/resultado |
|---|---|---|
| `Print` | `omarchy-capture-screenshot` | `grim` + `slurp` + `wl-copy`; guarda y copia |
| Click en notificacion | `omarchy-screenshot-edit <png>` | Satty anota el archivo capturado |
| `Super+Ctrl+C` | `omarchy-menu toggle capture` | menu screenshot/OCR/QR/recording |
| `Alt+Print` | stop actual o `trigger.capture.screenrecord` | toggle/menu de GSR |
| Capture -> Screenrecord | `omarchy-capture-screenrecording` | GSR KMS; portal solo opt-in |
| Apps -> OBS Studio | desktop entry oficial | OBS + portal PipeWire |
| `Super+Return` | `omarchy-launch-terminal` | `xdg-terminal-exec` -> Kitty |
| Apps -> Ghostty | desktop entry oficial | terminal alternativo explicito |
| `Super+Shift+/` | `setsid uwsm-app -- bitwarden-desktop` | Bitwarden desktop |
| `Super+Shift+O` | binding upstream | Obsidian |

Durante la seleccion de screenshot, `Return` toma la ventana resaltada,
`Ctrl+Return` la pantalla completa, `Tab`/`Ctrl+Tab` recorren ventanas y las
flechas cambian la seleccion.

El RX 550 usa `amdgpu`; `mesa`, `libva` y `vulkan-radeon` ya estaban
instalados. El paquete oficial GSR declara Mesa/libva como ruta AMD. El script
v4.0.0 usa KMS, `-k auto` y fallback de CPU. Se conserva
`OMARCHY_SCREENRECORD_USE_PORTAL=true` solo como opt-in porque upstream advierte
que EGL DMA-BUF puede fallar. OBS sigue siendo el recorder principal aunque el
toggle rapido no supere la prueba interactiva.

Satty cubre el editor faltante `tensaku-edit`. `mpv` se conserva como backend
exacto de preview y webcam del script fijado; VLC sigue siendo el player diario
pedido por el usuario.

## Kitty: root cause y compatibilidad

Antes de esta capa, `xdg-terminal-exec --print-id` devolvia `foot.desktop`.
Quattro habia ejecutado GNU `sed -i` sobre `~/.config/kitty/kitty.conf`: eso
reemplazo el symlink por una copia regular, aunque backup y source tienen
SHA-256 identico. Kitty seguia incluyendo `shared/kitty/active-theme.conf`; el
`kitty.conf` Tokyo Night de Quattro nunca fue incluido. La diferencia visual
probada fue el terminal lanzado (Foot), no una paleta aplicada a Kitty.

[`xdg-terminals.list`](../../xdg/xdg-terminals.list) devuelve Kitty al default.
Ghostty permanece instalado y visible. No se modifica `shared/**` ni macOS.

La sesion antepone `~/.config/hypr-quattro/compat-bin` solo a su `PATH`. Los
wrappers de `omarchy-display-text-size` y `omarchy-font-set` delegan al runtime
fijado con un HOME temporal que enlaza Alacritty, Foot, Ghostty, fontconfig y
Omarchy, pero omite Kitty cuando su config es un symlink. Asi preservan el
comportamiento upstream restante sin reemplazar el link ni ensuciar Git.

```bash
os/linux/hyprland/quattro-lab/scripts/test-kitty-compat
```

## Bitwarden y datos privados

El override soportado hace `hl.unbind` del shortcut de 1Password y lo registra
para Bitwarden. La extension del menu reutiliza el ID upstream de 1Password
para que no ofrezca ese installer y lance Bitwarden. El runtime queda limpio.
No se versionan vaults, login state, extensiones, tokens ni credenciales.

## Vial: recomendado, no instalado

`vial` no existe en los repositorios oficiales consultados. Vial ofrece
`v0.7.5` beta como AppImage, sin checksum/firma del publisher. La descarga
autentica auditada dio SHA-256
`b0df22fcc38f85a2d9e2224d2b3fcc76944819365557f1b9a83ee8f880fc7403`;
es observacion local, no autenticacion del publisher.

Se reviso `vial-git` AUR:

- commit `6ec5590b10cf6639f81127c1f98a88cbe523064a`;
- `PKGBUILD` `bc1745db3be6a2db6eeed22d7b6d14b7e637fa71df02d5b7d709c16fbe2b9e51`;
- `.SRCINFO` `a269e3e3623a61c15115574e35f9ece967b37a6317bd0a269a0a37b121d6058c`;
- reglas udev `a6af0820ee6960dccab9ce0df0a898ccd0a50fecd992e341656dd1af78680502`
  y `f91d36792b315caf9faa380860ae093fb1ef0ee966dad46023f033ab2ba7f22e`.

El recipe usa source Git movil con `SKIP`, Python 3.6/pyenv, pip y
`pkg2appimage`. No alcanza el patron reproducible de Helium. Vial queda
diferido hasta disponer de integridad upstream o un PKGBUILD fijado. No usar
`yay -S vial-git` a ciegas.

## Radar no instalado

- `wf-recorder`: redundante con GSR y OBS.
- `gpu-screen-recorder-ui`: redundante con menu Quattro y OBS.
- `libreoffice-fresh`: Still satisface el requisito estable.
- catalogo Omarchy: contiene servicios/apps no solicitados.
- 1Password: reemplazado por Bitwarden.
- Vial: diferido por reproducibilidad.

No se retiran XFCE ni el Hyprland anterior. Solo se considera despues de la
aceptacion interactiva de Quattro.

## Rollback/remocion

Revertir configuracion requiere un revert Git y nuevo link del perfil. Para
retirar solo los paquetes agregados en la primera aplicacion (preservando los
backends y terminales que ya existian):

```bash
sudo pacman -Rns satty gpu-screen-recorder mpv obs-studio kdenlive \
  obsidian discord telegram-desktop bitwarden vlc \
  libreoffice-still libreoffice-still-es
```

Revisar la transaccion de pacman. Los datos de aplicaciones no se borran
automaticamente; no eliminarlos sin backup y autorizacion explicita.
