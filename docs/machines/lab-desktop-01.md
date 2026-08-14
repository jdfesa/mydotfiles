# Lab Desktop 01

Notas operativas de la maquina Arch Linux accesible actualmente por SSH en
`jd@192.168.8.47`. La direccion viene de DHCP y puede cambiar. Su identidad en
el repositorio es `lab-desktop-01`; el hostname operativo sigue siendo
`arch-desktop` y no necesita coincidir con el identificador estable.

## Objetivo

Usar esta maquina para probar Arch, window managers y configuraciones Linux sin
comprometer el entorno de recuperacion. La fuente de verdad es
`~/mydotfiles`; la maquina actua como runtime con symlinks, builds en cache y
datos locales fuera de Git. Es un host `canary`: puede reinstalarse, no debe
guardar datos sensibles y recibe los experimentos antes que produccion.

## Hardware Contract

El inventario declarativo vive en `hosts/lab-desktop-01/host.toml`. La base
validada incluye i7-4790K, RX 550 mediante `amdgpu`, audio Realtek ALC892 y un
Dell P2419H conectado como `HDMI-A-2` a 1920x1080@60. Estos datos describen la
maquina; no forman parte del nombre de ningun perfil reusable.

## Estado verificado el 2026-08-13

- Hyprland 0.56.2 inicia mediante UWSM sobre Wayland con XWayland disponible.
- `Hyprland --verify-config` y `hyprctl configerrors` no reportan errores; no
  hay plugins instalados.
- El perfil compuesto `arch-hyprland` esta aplicado: sus 18 enlaces terminan
  correctos, sin warnings ni errores. Incluye la base portable de workstation y
  la capa Wayland; no duplica configuracion por hardware.
- `arch-hyprland-preview` permanece como subconjunto compatible y tambien pasa
  su diagnostico de 10 enlaces. El alias historico `arch-desktop` apunta a DWM
  X11 y ya no describe el runtime actual.
- La promocion respaldo el antiguo `~/.bashrc` de plantilla en
  `~/.local/state/mydotfiles/backups/profile-migration/20260813T224514-0300/`
  antes de enlazar la version gestionada. No fue necesario reiniciar ni
  modificar la sesion Hyprland activa.
- `linux` y `linux-lts` estan instalados; XFCE X11, SSH y XRDP permanecen como
  rutas de recuperacion.
- Btrfs, Snapper y grub-btrfs exponen snapshots desde GRUB; tener entradas no
  sustituye una prueba real de rollback ni un backup externo.
- El audio ALC892 persistio despues del reinicio con la salida analogica
  correcta y controles ALSA activos.
- No existen unidades systemd fallidas. La politica de firewall, el monitoreo
  SMART automatico y el backup externo todavia deben cerrarse antes de promover
  el sistema.

El perfil Hyprland actual usa Hyprlang, aceptado por 0.56 pero deprecado por
upstream. La migracion modular a Lua debe realizarse y validarse en este host
antes de una version que retire compatibilidad.

## Instalacion verificada el 2026-08-12

- Reinstalacion limpia sobre Btrfs con subvolumenes separados y Snapper.
- Kernel `linux` principal y `linux-lts` como fallback.
- `jd` administra mediante `wheel`/sudo; root permanece bloqueado.
- Primer boot, TTY, sudo, SSH y XFCE X11 mediante SDDM validados.
- Hyprland esta instalado y su primera configuracion modular esta versionada;
  permanece como sesion opcional mientras XFCE siga siendo la eleccion segura.
- El bootstrap de workstation se realiza por fases documentadas bajo
  `os/linux/packages/`; no se agregan aplicaciones mediante comandos aislados.
- Helium sera el navegador por defecto; Firefox se conserva como fallback desde
  repositorios oficiales porque Helium aun se distribuye como beta en Linux.
- GitHub CLI se utilizara para autenticar este dispositivo sin versionar tokens.
- XRDP y Xorgxrdp se construyeron desde commits AUR revisados y quedaron activos
  como recuperacion remota de XFCE X11.
- Codex CLI `0.147.0` tiene su host de Code Mode instalado en
  `~/.local/bin/codex-code-mode-host`; el flujo reproducible vive en
  `os/linux/codex/` y evita compilar V8 localmente.

## Prueba Hyprland del 2026-08-12

La primera sesion real valido compositor, salida HDMI-A-2 a 1920x1080, efectos
y Kitty. Fallaron inicialmente Thunar, el menu de sesion y el audio.

Se confirmo que estaban activas simultaneamente:

- sesion 120: XFCE X11 remota mediante `xrdp-sesman`;
- sesion 122: Hyprland Wayland local mediante SDDM.

Esto explica que `xfwm4` apareciera como cliente de PipeWire, que Thunar
reutilizara la instancia X11 y que Mako/PolicyKit encontraran servicios ya
registrados. Para la proxima prueba se debe cerrar la sesion XRDP por completo.

El entorno systemd/UWSM no incluia `~/.local/bin`, aunque Zsh interactivo si lo
incluye. El perfil preview enlaza ahora
`os/linux/wayland/environment.d/10-mydotfiles.conf`; requiere cerrar y volver a
iniciar sesion para propagarse.

PipeWire detecto tres dispositivos (Intel HDMI, Realtek ALC892 y AMD HDMI),
pero tenia activo `Built-in Audio Digital Stereo (IEC958)` al 40%. AMD HDMI
estaba con perfil `off`. Tras cerrar la sesion XRDP, reiniciar solamente
PipeWire/WirePlumber no corrigio el problema: ambos puertos analogicos seguian
marcados como no disponibles y el perfil volvia a S/PDIF. Se activo
temporalmente `pro-audio`, que expone directamente `hw:1,0` (ALC892 Analog), y
se dejo `alsa_output.pci-0000_00_1b.0.pro-output-0` como sink predeterminado al
50 %. La ausencia de sonido restante era del mezclador ALSA: `Front`, que
controla el jack verde trasero, estaba silenciado. Se desactivo `Auto-Mute`, se
dejaron `Master` y `Front` al 100 %/0 dB sin mute y se mantuvo el volumen de
usuario solo en PipeWire al 50 %. El usuario confirmo reproduccion correcta en
YouTube con auriculares analogicos en el conector verde trasero. El diagnostico
y la recuperacion estan documentados en `os/linux/audio/README.md`; falta
verificar la persistencia despues de un reinicio futuro.

El prompt Kitty distinto de macOS no era una variante intencional: faltaba el
symlink `~/.config/starship.toml` en el perfil preview. Starship usaba entonces
su prompt predeterminado multilínea (`~` y `›`). El enlace Arch apunta ahora a
la misma fuente canónica `shared/starship/starship.toml` usada por macOS, sin
cambiar el contenido compartido.

## Estado historico anterior a la reinstalacion: 2026-07-17

Esta seccion conserva evidencia de la instalacion anterior. No describe las
sesiones instaladas actualmente y no debe usarse como inventario operativo.

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

## Display manager y sesiones historicas

En la instalacion anterior, SDDM ofrecia DWM y XFCE. Despues de la reinstalacion
actual, XFCE X11/Wayland y Hyprland son seleccionables; DWM debe reconstruirse e
instalarse nuevamente antes de volver a aparecer.

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

La build que agrega el power menu en `Super+Shift+p` genero este respaldo:

```text
~/.local/state/mydotfiles/backups/dwm-session/20260717-202007/
```

La build en cache y `/usr/local/bin/dwm` coincidieron con SHA-256:

```text
70ccd7c0713cfdcbd56773c7724e36dbefa5993f04d9fe6b98a93b7ac5753990
```

DWM se reinicio mediante `restartsig` sin cerrar las aplicaciones. El menu se
abrio en `DISPLAY=:0` y una prueba con timeout lo cancelo sin seleccionar lock,
suspend, logout, reboot ni power off. El perfil termino con 8 enlaces validos.

La revision que hace circular la navegacion vertical de dmenu genero este
respaldo antes de instalarse:

```text
~/.local/state/mydotfiles/backups/dwm-session/20260717-204223/
```

La build en cache y `/usr/local/bin/dmenu` coincidieron con SHA-256:

```text
91710f628dbc9b0df2171b50519cef434279d09d2ba4648ee4705790136fb364
```

La prueba sobre el binario instalado verifico que `Up` pasa de `Cancel` a
`Power off`, que `Down` vuelve de la ultima opcion a `Cancel` y que escribir
`j` sigue filtrando texto. No se agregaron atajos de Vim ni modificadores. El
hash de DWM no cambio durante esta instalacion.

### DWMBlocks

La barra historica se recupero desde el respaldo de la maquina. Su base es
`torrinfail/dwmblocks` en el commit `8cedd22`, con ajustes menores para una
compilacion limpia y dos bloques: sensores y fecha/hora.

La configuracion anterior llamaba a la ruta obsoleta
`~/.local/scripts/status-sensors.sh`. La configuracion versionada usa ahora el
comando `status-sensors`, resuelto desde `~/.local/bin` por el launcher de la
sesion. Build, instalacion y rollback se documentan en
`os/linux/dwmblocks/README.md`.

La primera instalacion reproducible de DWMBlocks creo y verifico este respaldo:

```text
~/.local/state/mydotfiles/backups/dwmblocks/20260717-192314/
```

La build en cache y `/usr/local/bin/dwmblocks` coincidieron con SHA-256:

```text
0f19a7e8fd51686040d6dc15db84349925d380e52fec0eac95ac29e875f5bbde
```

El proceso se reinicio de forma aislada, sin cerrar DWM ni sus ventanas. Tras
mas de un intervalo completo de 30 segundos, el log de la sesion no recibio
errores nuevos y la barra continuo activa en `DISPLAY=:0`.

La Radeon RX 550 usa el driver `amdgpu` y publica su utilizacion en
`/sys/class/drm/card1/device/gpu_busy_percent`. El script no fija `card1`:
descubre dinamicamente la tarjeta controlada por `amdgpu`, por lo que conserva
el comportamiento si el orden de DRM cambia en una reinstalacion. No requiere
`radeontop`, `rocm-smi`, `nvtop` ni otro proceso de monitoreo residente.

## Profiles And User Scripts

Los nombres nuevos describen capacidades y no la maquina:

```text
arch-workstation            # base compartida sin elegir sesion grafica
arch-dwm                    # base + DWM/X11
arch-hyprland               # base + Hyprland/Wayland
arch-hyprland-preview       # subconjunto aplicado actualmente en el canary
```

`arch-desktop` queda como alias compatible de `arch-dwm` mientras se migra la
instalacion anterior; no debe usarse en automatizacion nueva.

El perfil objetivo del host es `arch-hyprland`, pero no se aplica de golpe. El
preview preserva los diez enlaces ya validados mientras se resuelve
deliberadamente `~/.bashrc` y se completa la base:

```sh
scripts/link --dry-run --repair arch-hyprland-preview
scripts/link --repair arch-hyprland-preview
scripts/doctor arch-hyprland-preview

# Objetivo futuro, solo despues de revisar el dry-run:
scripts/link --dry-run --repair arch-hyprland
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

## Manuales operativos

- `os/linux/dwm/KEYBINDINGS.md`: todos los atajos efectivos, estado y riesgos;
- `os/linux/dwm/CONCEPTS.md`: modelo mental, tags, layouts y adopcion gradual;
- `os/linux/packages/MAINTENANCE.md`: actualizaciones, recuperación y auditoria
  de preparación antes de migrar el trabajo principal.
