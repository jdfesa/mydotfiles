# Hyprland Quattro Lab

Sesion paralela que ejecuta el **runtime completo del escritorio** de Omarchy
Quattro sobre el Arch existente. No instala Omarchy como distribucion, no
reemplaza el bootloader y no cambia la sesion Hyprland estable.

## Que se trasplanta

El runtime se materializa desde el tag oficial `v4.0.0`, commit
`f0020448ca87329199de7cb12f2015ebc4a3e5e7`, y conserva:

- los 425 comandos `omarchy-*` y sus helpers;
- el shell Quickshell completo (barra, menu, notificaciones, clipboard,
  lockscreen, OSD, paneles, fondo y PolicyKit);
- los defaults Lua de Hyprland y los 22 temas oficiales;
- la configuracion de usuario Hyprland inicial sin modificaciones funcionales.

La copia completa queda fuera de Git, fijada por `runtime/source.lock`, en:

```text
~/.local/share/mydotfiles/omarchy-quattro/runtime
```

Los dotfiles pequenos y personalizables permanecen versionados en este repo.
El perfil los enlaza como `~/.config/hypr-quattro` y `~/.config/omarchy`.

## Limites deliberados

- `~/.config/hypr` continua siendo la sesion estable.
- XFCE/XRDP y la sesion Hyprland estable permanecen como recuperacion.
- No se ejecutan el instalador de la distro, migraciones, provisioning,
  configuracion de Pacman, SDDM, Limine, Snapper, firewall o servicios del host.
- No se instalan en bloque las aplicaciones opcionales de la ISO (Kdenlive,
  LibreOffice, Docker, juegos, etc.). El escritorio y su superficie de comandos
  si se copian completos; una accion que lance una app ausente se ajusta despues.
- La primera prueba conserva incluso la seleccion de apps upstream, incluido el
  binding de 1Password. Bitwarden se sustituye una vez validado el arranque base.
- La configuracion activa de macOS no participa en este perfil.

`prepare-user` marca el provisioning de distribucion como completado antes del
primer login. Esto evita que el autostart upstream reescriba navegador, Git,
agentes, audio o GTK, sin recortar el shell del escritorio.

## Por que no extraer la ISO

La ISO contiene este mismo codigo, paquetes binarios, un repositorio offline y
el instalador del sistema. Para el trasplante, el tag Git es la fuente legible y
trazable; los dos binarios especiales se descargan por nombre y SHA-256 desde el
repositorio oficial de Omarchy. Desmontar la ISO agregaria peso, no una capa de
dotfiles mas completa.

## Instalacion

Todas las etapas tienen modo de inspeccion y son reversibles:

```sh
# 1. Copiar el runtime upstream completo y fijado.
os/linux/hyprland/quattro-lab/scripts/sync-runtime --dry-run
os/linux/hyprland/quattro-lab/scripts/sync-runtime

# 2. Instalar dependencias del escritorio.
os/linux/hyprland/quattro-lab/scripts/install-dependencies --dry-run
os/linux/hyprland/quattro-lab/scripts/install-dependencies

# 3. Enlazar exclusivamente la configuracion paralela.
scripts/link --dry-run --repair arch-hyprland-quattro-lab
scripts/link --repair arch-hyprland-quattro-lab

# 4. Inicializar fuente, tema y guardas de provisioning.
os/linux/hyprland/quattro-lab/scripts/prepare-user --dry-run
os/linux/hyprland/quattro-lab/scripts/prepare-user

# 5. Verificar todo antes de tocar SDDM.
os/linux/hyprland/quattro-lab/scripts/check-runtime

# 6. Instalar la entrada adicional de SDDM/UWSM.
os/linux/hyprland/quattro-lab/scripts/install-session --dry-run
os/linux/hyprland/quattro-lab/scripts/install-session
```

`install-dependencies` no agrega el repositorio Omarchy a
`/etc/pacman.conf`. Descarga `quickshell-git` y `xdg-terminal-exec` por sus
payloads exactos, valida los SHA-256 fijados y luego usa `pacman -U`.

## Validacion interactiva

En SDDM elegir manualmente `Hyprland Quattro Lab`. La sesion estable no cambia
como predeterminada.

1. confirmar barra, fondo, notificaciones, menu y paneles;
2. probar terminal, launcher, workspaces, grupos, resize y scratchpad;
3. probar clipboard, capturas, lockscreen, DPMS y PolicyKit;
4. revisar que acciones de apps opcionales faltantes fallan de forma acotada;
5. salir mediante el menu Quattro y volver a la sesion Hyprland estable;
6. ejecutar `scripts/doctor arch-hyprland-quattro-lab`.

El launcher escribe fallos tempranos en:

```text
~/.local/state/mydotfiles/hyprland-quattro-lab.log
```

## Rollback

La entrada de SDDM se retira con el archivo de respaldo informado al instalar:

```sh
os/linux/hyprland/quattro-lab/scripts/rollback-session \
  "$HOME/.local/state/mydotfiles/backups/hyprland-quattro-lab/<timestamp>"
```

El runtime, los paquetes y el estado de usuario se conservan para diagnostico;
el rollback nunca toca `~/.config/hypr` ni macOS.

## Proveniencia

Omarchy se distribuye bajo licencia MIT. La licencia upstream se conserva en
`LICENSE.omarchy`; hashes, tag y revision viven en `runtime/`.
