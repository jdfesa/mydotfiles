# Arch Desktop

Notas operativas de la maquina Arch Linux accesible por SSH en
`jd@192.168.8.15`.

## Objetivo

Usar esta maquina para probar Arch, window managers y configuraciones Linux sin
comprometer el entorno de recuperacion. La fuente de verdad es
`~/mydotfiles`; la maquina actua como runtime con symlinks, builds en cache y
datos locales fuera de Git.

## Estado verificado el 2026-07-13

- Arch Linux usa `graphical.target` y SDDM 0.21 como display manager.
- SDDM, SSH y XRDP estan habilitados y activos.
- XFCE 4.20 permanece instalado y aparece como sesion X11 y Wayland.
- DWM y dmenu se compilan desde los snapshots versionados en
  `os/linux/{dwm,dmenu}/src`, no desde clones sueltos bajo `$HOME`.
- DWMBlocks se mantiene como snapshot independiente en
  `os/linux/dwmblocks/src`; su build regenerable vive fuera de Git.
- `xorg-server-xephyr` y `xorg-server-xvfb` estan instalados para pruebas
  visuales y headless, respectivamente.
- La sesion `DWM (dotfiles)` se instala en `/usr/local/share/xsessions/` y usa
  un launcher de `/usr/local/libexec/`.
- El autostart de DWM es independiente de XFCE: no se usa `~/.xprofile` para
  iniciar `picom`, `dwmblocks` o el rotador de wallpapers.
- Los binarios y archivos manuales anteriores quedan respaldados antes de cada
  instalacion reproducible.
- Jump Desktop desde macOS debe conectarse mediante el tunel SSH documentado en
  `os/linux/x11/README.md`.

## Display manager y sesiones disponibles

SDDM es el programa de login. DWM y XFCE son sesiones seleccionables dentro de
SDDM; no son distintas variantes de SDDM.

```text
SDDM
  -> DWM (dotfiles), X11 experimental
  -> XFCE Session, X11 de recuperacion
  -> XFCE on Wayland, alternativa empaquetada
```

No se cambia a LightDM, GDM ni otro display manager durante esta etapa. La
comparacion y los comandos de diagnostico estan en
`os/linux/display-managers/README.md`.

Para salir normalmente de DWM y volver al selector se usa
`Mod+Shift+Backspace`. Si la sesion grafica queda inutilizable, entrar por SSH o
`Ctrl+Alt+F3` y reiniciar SDDM. Ese reinicio cierra cualquier sesion grafica:

```sh
sudo systemctl restart sddm
```

## Fuente y flujo DWM/dmenu

Los arboles bajo `os/linux/dwm/src` y `os/linux/dmenu/src` son las fuentes
propias. Sus versiones, parches y modificaciones se documentan en el mismo
repositorio; no se usa la identidad ni el commit de otro usuario como referencia
operativa.

La configuracion propia se modifica en cada `src/config.def.h`. Flujo seguro:

```sh
cd ~/mydotfiles
os/linux/dwm/scripts/build
os/linux/dmenu/scripts/build

# Ejecutar desde una terminal de XFCE X11, no desde SSH sin DISPLAY:
os/linux/dwm/scripts/test-nested

# Despues de validar la prueba:
os/linux/dwm/scripts/install-session
```

El test anidado requiere `xorg-server-xephyr`. La instalacion crea primero un
archivo de rollback bajo:

```text
~/.local/state/mydotfiles/backups/dwm-session/<fecha>/
```

La primera instalacion reproducible termino correctamente y su respaldo
verificado es:

```text
~/.local/state/mydotfiles/backups/dwm-session/20260713-140717/
```

La revision que elimina las colisiones de atajos genero un segundo respaldo
verificado antes de instalar el binario final:

```text
~/.local/state/mydotfiles/backups/dwm-session/20260713-141540/
```

Las builds instaladas coinciden por SHA-256 con las compiladas en cache. DWM
6.5 y dmenu 5.4 permanecieron activos juntos sobre Xvfb durante el smoke test;
SDDM se reinicio despues y volvio a estado `active` con el greeter operativo.

El procedimiento detallado, los atajos iniciales y el rollback se documentan
en `os/linux/dwm/README.md`.

### DWMBlocks

La barra historica se recupero desde el respaldo de la maquina. Su base es
`torrinfail/dwmblocks` en el commit `8cedd22`, con ajustes menores para una
compilacion limpia y dos bloques: sensores y fecha/hora.

La configuracion anterior llamaba a la ruta obsoleta
`~/.local/scripts/status-sensors.sh`. La configuracion versionada usa ahora el
comando `status-sensors`, resuelto desde `~/.local/bin` por el launcher de la
sesion. Build, instalacion y rollback se documentan en
`os/linux/dwmblocks/README.md`.

## Perfil y scripts de usuario

`profiles/arch-desktop.links` despliega:

```text
shared/bash/bashrc                         -> ~/.bashrc
os/linux/dwm/session/autostart.sh          -> ~/.config/dwm/autostart.sh
os/linux/dwm/scripts/wallpaper-rotator.sh  -> ~/.local/bin/wallpaper-rotator
os/linux/dwm/scripts/status-sensors.sh     -> ~/.local/bin/status-sensors
os/linux/x11/scripts/cliphist              -> ~/.local/bin/cliphist
os/linux/x11/scripts/start-x11vnc.sh       -> ~/.local/bin/start-x11vnc
shared/rclone/rclone-sync                  -> ~/.local/bin/rclone-sync
```

El linker no reemplaza archivos reales automaticamente. Comprobar y aplicar:

```sh
scripts/link --dry-run --repair arch-desktop
scripts/link --repair arch-desktop
scripts/doctor arch-desktop
```

El wrapper de Rclone hace `--dry-run` salvo que se indique `--apply`; sus
credenciales permanecen fuera del repositorio.

## Historial de migracion y recuperacion

El antiguo `~/suckless` se retiro de su ruta activa y quedo en cuarentena en:

```text
~/.local/share/dotfiles-migration/quarantine/20260710-223627/suckless
```

La migracion anterior que estaba sin commit en el clon remoto se guardo antes
de actualizar `main`:

```text
stash: pre-dwm-session-20260713-135544
```

Su contenido coincide con commits que ya existen en `main`; el stash se
conserva temporalmente como segunda red de seguridad.

El antiguo `~/.xprofile`, los archivos TigerVNC que iniciaban DWM y el script
que contenia una clave VNC embebida quedaron en la cuarentena fechada. En
`~/.vnc/` solo debe permanecer `passwd` con modo `0600` para x11vnc.

Los ejecutables historicos de `/usr/local/bin` no se borran sin respaldo. El
instalador reproducible los incluye en su `system-files.tar` antes de
reemplazarlos.

## Candidatos a limpiar mas adelante

No borrar todavia; revisar cuando DWM lleve suficiente tiempo estable:

```text
~/.cache/yay
~/yay
~/yay-bin
backup_arch_dwm_final.tar.gz
backup_dwm_x11vnc.tar.gz
backup_full_sistema/
~/.bash_history-*.tmp
```

Tambien deben conservarse por ahora la cuarentena de `suckless` y el stash de
preinstalacion. Solo se retiran despues de probar build, login, salida a SDDM,
XFCE, SSH y XRDP.

## Regla para continuar

- Cambiar una sola pieza de DWM o dmenu por iteracion.
- Compilar sin `sudo`; usar privilegios solo para instalar una build validada.
- Probar primero en Xephyr y despues como sesion real.
- Mantener XFCE, SDDM, SSH y XRDP como salida de emergencia.
- No borrar primero: respaldar o poner en cuarentena.
- No versionar passwords, tokens, claves privadas, caches, builds ni logs.
