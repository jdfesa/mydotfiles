# Curated Quattro Daily Workstation

Esta capa convierte Quattro Lab en una estación diaria deliberada. No instala
`omarchy-base.packages`, preinstalls ni repositorios de Omarchy. `mydotfiles`
conserva la lista y los overrides de usuario; pacman usa solo los repositorios
oficiales ya habilitados.

## Package audit on 2026-08-16

`pacman -Si` confirmó estos nombres en `extra`. Las versiones son evidencia de
la auditoría, no pins: Arch se actualiza como sistema completo.

| Need | Official package | Audited version | State before this correction |
|---|---|---:|---|
| Screenshot selection | `grim`, `slurp`, `wl-clipboard` | `1.5.0-2`, `1.5.0-2`, `1:2.3.0-1` | installed |
| Annotation | `satty` | `0.22.0-1` | installed |
| Fast recording | `gpu-screen-recorder` | `6.0.0-1` | installed |
| English OCR | `tesseract`, `tesseract-data-eng` | `5.5.3-1`, `2:4.1.0-5` | missing |
| QR decoding | `zbar` | `0.23.93-7` | missing |
| Pinned preview/webcam command | `mpv` | `1:0.41.0-4` | installed |
| Full recording | `obs-studio` | `32.2.1-7` | installed |
| Video editing | `kdenlive` | `26.04.3-2` | installed |
| Notes | `obsidian` | `1.13.7-1` | installed |
| Chat | `discord`, `telegram-desktop` | `1:1.0.154-1`, `7.0.9-2` | installed |
| Primary/alternate terminal | `kitty`, `ghostty` | `0.48.2-1`, `1.3.1-2` | installed |
| Password manager | `bitwarden` | `2026.3.1-2` | installed |
| Video player | `vlc` | `3.0.23_2-10` | installed |
| Stable English office suite | `libreoffice-still` | `25.8.7-5` | installed |
| Optional Spanish spelling only | `hunspell-es_any` | `1:2.9-1` | missing |

El manifiesto es
[`40-quattro-daily-workstation.txt`](../../packages/lists/40-quattro-daily-workstation.txt).
`LibreOffice Still` se elige por su rama de mantenimiento; `Fresh` no resuelve
una necesidad concreta de esta workstation.

Los comandos de OCR y QR ya estaban expuestos por el runtime fijado de Omarchy,
pero el trasplante curado había omitido `tesseract`, `tesseract-data-eng` y
`zbar`. El checker ahora considera esos comandos no disponibles hasta que estén
presentes sus paquetes oficiales exactos y sus payloads con ownership válido.
No se agrega OCR en español; el idioma OCR predeterminado de Omarchy sigue
siendo `eng`.

## English locale, UI, and US keyboard audit

La auditoría del host del 2026-08-16 encontró:

- `LANG=en_US.UTF-8`, `LC_ALL=C.UTF-8` y ningún override `LANGUAGE`;
- `/etc/locale.conf` selecciona `en_US.UTF-8`, y el único locale no neutral
  generado es `en_US.UTF-8`;
- `/etc/vconsole.conf` selecciona `KEYMAP=us`;
- `/etc/X11/xorg.conf.d/00-keyboard.conf` selecciona `XkbLayout "us"` y no
  declara una variante especializada;
- el input default del Omarchy fijado usa `vconsole.XKBLAYOUT` con `us` como
  fallback, mientras Quattro no tiene un override local de layout;
- una consulta read-only al socket Quattro existente informó `kb_layout=us`,
  `kb_variant` vacío y `English (US)` para todos los dispositivos de teclado;
- `hyprctl binds` live informó `Screenshot` en `Print`, `Screenrecording` en
  `Alt+Print`, `Color picker` en `Super+Print`, OCR en `Super+Ctrl+Print`, el
  menú de captura en `Super+Ctrl+C` e invocación de notificación en
  `Super+Alt+comma`. Los IDs de dispatch Lua son internos del runtime, por lo
  que los comandos exactos de abajo se obtienen de los archivos Lua fijados.

`libreoffice-still` ya aporta la ayuda base inglesa y la configuración inglesa
de fuentes, incluidos:

```text
/usr/lib/libreoffice/help/en-US/contents.js
/usr/lib/libreoffice/share/registry/res/fcfg_langpack_en-US.xcd
```

El paquete instalado `libreoffice-still-es` fue un error. Pacman lo describe
como un Spanish language pack y sus archivos incluyen catálogos de UI en
español y datos de registry como:

```text
/usr/lib/libreoffice/program/resource/es/LC_MESSAGES/vcl.mo
/usr/lib/libreoffice/share/registry/Langpack-es.xcd
/usr/lib/libreoffice/share/registry/res/registry_es.xcd
```

El gate privilegiado debe retirarlo. No forma parte del manifiesto y el check
live falla mientras un paquete instalado se describa como Spanish language
pack, localization o translation.

La corrección ortográfica en español sigue disponible sin localizar la UI de
LibreOffice ni del sistema. Pacman identifica `hunspell-es_any` como el
diccionario Hunspell genérico oficial de español. El manifiesto de archivos de
Arch contiene solo documentación y payloads de spelling; los archivos
compatibles con LibreOffice son:

```text
/usr/share/hunspell/es.aff
/usr/share/hunspell/es.dic
```

El paquete también publica los mismos datos ortográficos en formatos MySpell y
Qt WebEngine. No contiene message catalogs, un registry language pack de
LibreOffice, menús ni recursos de UI. Es el único paquete de diccionario en
español permitido por este baseline; no se instalan language packs adicionales
para otras aplicaciones.

## Installation, upgrades, and verification

```bash
# Metadata and plan, without privileges
os/linux/packages/scripts/install-official-list \
  os/linux/packages/lists/40-quattro-daily-workstation.txt
os/linux/hyprland/quattro-lab/scripts/check-daily-workstation --metadata-only

# Operator-supervised application
os/linux/packages/scripts/install-official-list --execute \
  os/linux/packages/lists/40-quattro-daily-workstation.txt
scripts/link --repair arch-hyprland-quattro-lab
os/linux/hyprland/quattro-lab/scripts/check-daily-workstation
os/linux/hyprland/quattro-lab/scripts/check-runtime

# Later upgrades (read Arch news first)
sudo pacman -Syu
os/linux/hyprland/quattro-lab/scripts/check-daily-workstation
```

El installer usa `pacman -Syu --needed`; repetirlo es idempotente. El checker no
abre aplicaciones: revisa paquetes, ownership de binarios/archivos, desktop
entries, sintaxis, bindings y comandos fijados exactos, declaraciones de locale
y resolución de comandos. Nunca toma screenshots, graba la pantalla, abre un
vault ni cambia un teclado.

## Source-backed capture shortcut matrix

La fuente de verdad es el checkout limpio de Omarchy `v4.0.0` en el commit
`f0020448ca87329199de7cb12f2015ebc4a3e5e7`, no la memoria. Todas las filas de
abajo se validan sin ejecutar captura ni grabación.

| Action | Exact keyboard path | Exact command/action | Source |
|---|---|---|---|
| Open capture menu | `Super+Ctrl+C` | `omarchy-menu toggle capture` | Upstream `default/hypr/bindings/utilities.lua` |
| Screenshot | `Print` | `omarchy-capture-screenshot` | Upstream |
| Annotate the screenshot just taken | `Super+Alt+,` después de la notificación | `omarchy-shell notifications invokeLast`; la notificación ejecuta `omarchy-screenshot-edit <png>` mediante `OMARCHY_SCREENSHOT_EDITOR` | Upstream notification binding and screenshot action; local editor compatibility command only |
| OCR directly | `Super+Ctrl+Print` | `omarchy-capture-text` | Upstream |
| OCR from the menu | `Super+Ctrl+C`, luego `Text` | `omarchy-capture-text` | Upstream menu |
| Decode QR | `Super+Ctrl+C`, luego `QR Code` | `omarchy-capture-qr` | Upstream menu; no direct upstream chord |
| Pick a color | `Super+Print` | `pkill hyprpicker \|\| hyprpicker -a` | Upstream |
| Start/stop screen recording | `Alt+Print` | `omarchy-capture-screenrecording --stop-recording \|\| omarchy-menu toggle trigger.capture.screenrecord` | Upstream |
| Record without audio | `Alt+Print`, luego `With no audio` | `omarchy-capture-screenrecording` | Upstream menu |
| Record desktop audio | `Alt+Print`, luego `With desktop audio` | `omarchy-capture-screenrecording --with-desktop-audio` | Upstream menu |
| Record desktop and microphone | `Alt+Print`, luego `With desktop + microphone audio` | `omarchy-capture-screenrecording --with-desktop-audio --with-microphone-audio` | Upstream menu |
| Record with webcam | `Alt+Print`, luego la entrada de webcam cuando se detecte una | `omarchy-capture-screenrecording-with-webcam` | Upstream menu |
| Open the recording just saved | `Super+Alt+,` después de la notificación | `omarchy-shell notifications invokeLast`; la notificación ejecuta `mpv <mp4>` | Upstream |

Durante la selección de screenshot o de grabación sin portal, `Return` toma la
ventana resaltada, `Ctrl+Return` toma la pantalla enfocada completa, `Tab` y
`Ctrl+Tab` recorren ventanas, y las flechas cambian la ventana resaltada. Estos
bindings temporales upstream existen solo mientras la layer `selection` está
abierta.

No se agrega ningún chord local de captura. Screenshot, anotación, OCR, QR,
color picker y grabación ya tienen rutas upstream keyboard-first, por lo que
inventar un shortcut nuevo solo agregaría riesgo de colisión. La única
adaptación local de captura es el comando aislado `omarchy-screenshot-edit`,
que envía el PNG seleccionado a Satty porque el binario upstream
`tensaku-edit` no forma parte de este baseline Arch.

### Layer 2 + P

El sistema operativo solo ve el keycode/keysym emitido por el teclado; no ve el
nombre de la layer física ni la `P` impresa. El binding de screenshot auditado
de Omarchy es exactamente `Print`. Por lo tanto, Layer 2 + P invocará
directamente el flujo de screenshot de Omarchy solo si esa tecla emite el evento
`Print`/Print Screen. Si emite `P`, un shortcut exclusivo de macOS o cualquier
otro evento, no coincidirá con este binding. Este repositorio no adivina el
output del firmware y no modifica Vial, QMK, ZMK ni firmware del teclado.

## Recording backends

La RX 550 usa `amdgpu`; `mesa`, `libva` y `vulkan-radeon` ya estaban
instalados. El paquete oficial GSR declara Mesa/libva como la ruta AMD. El script
`v4.0.0` usa KMS, `-k auto` y fallback de CPU.
`OMARCHY_SCREENRECORD_USE_PORTAL=true` permanece como opt-in porque upstream
advierte que EGL DMA-BUF puede fallar. OBS sigue siendo el recorder principal
si el toggle rápido no supera la aceptación interactiva.

`mpv` se conserva como backend exacto de preview y webcam usado por el script
fijado. VLC sigue siendo el player diario solicitado.

## Kitty ownership and compatibility

Antes de esta capa, `xdg-terminal-exec --print-id` devolvía `foot.desktop`.
Quattro había ejecutado GNU `sed -i` sobre `~/.config/kitty/kitty.conf`, lo que
reemplazó el symlink por un archivo regular aunque backup y source tenían
SHA-256 idéntico. Kitty seguía incluyendo `shared/kitty/active-theme.conf`; el
`kitty.conf` Tokyo Night de Quattro nunca fue incluido. La diferencia visual
probada fue el terminal lanzado (Foot), no un theme aplicado a Kitty.

[`xdg-terminals.list`](../../xdg/xdg-terminals.list) devuelve Kitty al default.
Ghostty permanece instalado y visible. No se modifica `shared/**` ni macOS.

La sesión antepone `~/.config/hypr-quattro/compat-bin` solo a su propio `PATH`.
Los wrappers `omarchy-display-text-size` y `omarchy-font-set` delegan al runtime
fijado con un HOME temporal que enlaza Alacritty, Foot, Ghostty, fontconfig y
Omarchy, pero omite Kitty cuando su config es un symlink. Así se preserva el
comportamiento upstream restante sin reemplazar el link ni ensuciar Git.

```bash
os/linux/hyprland/quattro-lab/scripts/test-kitty-compat
```

## Bitwarden and private data

El override soportado hace unbind del shortcut de 1Password y registra
Bitwarden. La extensión del menú reutiliza el ID upstream de 1Password para que
no pueda ofrecer ese installer y lance Bitwarden. El runtime permanece limpio.
No se versionan vaults, login state, extensiones, tokens ni credenciales.

## Vial: recommended, not installed

`vial` no existe en los repositorios oficiales revisados. Vial ofrece `v0.7.5`
beta como AppImage sin checksum o firma del publisher. La descarga autenticada
auditada tuvo SHA-256
`b0df22fcc38f85a2d9e2224d2b3fcc76944819365557f1b9a83ee8f880fc7403`;
es una observación local, no autenticación del publisher.

La receta AUR `vial-git` se revisó en:

- commit `6ec5590b10cf6639f81127c1f98a88cbe523064a`;
- `PKGBUILD` `bc1745db3be6a2db6eeed22d7b6d14b7e637fa71df02d5b7d709c16fbe2b9e51`;
- `.SRCINFO` `a269e3e3623a61c15115574e35f9ece967b37a6317bd0a269a0a37b121d6058c`;
- reglas udev `a6af0820ee6960dccab9ce0df0a898ccd0a50fecd992e341656dd1af78680502`
  y `f91d36792b315caf9faa380860ae093fb1ef0ee966dad46023f033ab2ba7f22e`.

La receta usa un source Git móvil con `SKIP`, Python 3.6/pyenv, pip y
`pkg2appimage`. No alcanza el patrón de reproducibilidad usado para Helium. Vial
queda diferido hasta disponer de integridad del publisher o un PKGBUILD fijado.
No ejecutar `yay -S vial-git` a ciegas.

## Not installed

- `wf-recorder`: redundante con GSR y OBS.
- `gpu-screen-recorder-ui`: redundante con el menú Quattro y OBS.
- `libreoffice-fresh`: Still satisface el requisito de oficina estable.
- `libreoffice-still-es`: localización de UI de LibreOffice en español,
  prohibida en este baseline.
- datos OCR en español u otros application language packs: no requeridos.
- catálogo Omarchy: incluye servicios y aplicaciones no solicitados.
- 1Password: reemplazado por Bitwarden.
- Vial: diferido por reproducibilidad.

No se retiran XFCE ni la sesión Hyprland anterior. Solo se considera después de
la aceptación interactiva de Quattro.

## Rollback and removal

El rollback de configuración requiere un revert Git seguido de un relink del
perfil. Para retirar solo los paquetes introducidos por la workstation curada
(preservando backends de captura y terminales que ya existían), revisar primero
esta transacción pacman:

```bash
sudo pacman -Rns satty gpu-screen-recorder tesseract tesseract-data-eng zbar \
  mpv obs-studio kdenlive obsidian discord telegram-desktop bitwarden vlc \
  libreoffice-still hunspell-es_any
```

Los datos de aplicaciones no se eliminan automáticamente; nunca borrarlos sin
backup y autorización explícita.
