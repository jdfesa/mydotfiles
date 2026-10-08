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

La selección diaria de aplicaciones, backends, shortcuts, Bitwarden, ownership
de Kitty y la decisión de diferir Vial están documentadas en
[`DAILY_WORKSTATION.md`](DAILY_WORKSTATION.md).

La integracion P0 agrega, sin activar aplicaciones opcionales:

- autenticacion de bloqueo Quickshell con el stack PAM de password exacto de
  `v4.0.0`;
- bloqueo previo a suspend mediante un servicio de usuario acotado a
  `graphical-session.target`;
- configuracion exacta de portal y `hyprsunset`, con perfil `identity` sin
  tinte como valor inicial;
- el picker oficial de screen sharing fijado por filename, version y SHA-256.

## Limites deliberados

- `~/.config/hypr` continua siendo la sesion estable.
- XFCE/XRDP y la sesion Hyprland estable permanecen como recuperacion.
- No se ejecutan el instalador de la distro, migraciones, provisioning,
  configuracion de Pacman, SDDM, Limine, Snapper, firewall o servicios del host.
- No se instalan en bloque las aplicaciones de la ISO. Solo se aplica el
  manifiesto curado documentado en `DAILY_WORKSTATION.md`; Docker, juegos y
  servicios no solicitados permanecen ausentes.
- El binding y el row de 1Password se reemplazan mediante overrides de usuario
  por Bitwarden; no se parchea el runtime derivado.
- La configuracion activa de macOS no participa en este perfil.

`prepare-user` marca el provisioning de distribucion como completado antes del
primer login. Esto evita que el autostart upstream reescriba navegador, Git,
agentes, audio o GTK, sin recortar el shell del escritorio.

## Por que no extraer la ISO

La ISO contiene este mismo codigo, paquetes binarios, un repositorio offline y
el instalador del sistema. Para el trasplante, el tag Git es la fuente legible y
trazable; los tres binarios especiales se descargan por nombre y SHA-256 desde el
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

# 5. Instalar la entrada adicional de SDDM/UWSM, PAM administrado y activar
#    el monitor de bloqueo previo a suspend en la sesion grafica actual.
os/linux/hyprland/quattro-lab/scripts/install-session --dry-run
os/linux/hyprland/quattro-lab/scripts/install-session

# 6. Verificar runtime, PAM, servicio, portal, nightlight y picker sin bloquear.
os/linux/hyprland/quattro-lab/scripts/check-runtime
```

`install-dependencies` no agrega el repositorio Omarchy a
`/etc/pacman.conf`. Descarga `quickshell-git`, `xdg-terminal-exec` y
`hyprland-preview-share-picker` por sus payloads exactos, valida los SHA-256
fijados y luego usa `pacman -U`. Antes ejecuta una actualización completa
`pacman -Syu --needed` junto con las dependencias oficiales; nunca instala
paquetes contra bases refrescadas mediante una actualización parcial.

## Modelo de estado

| Clase | Fuente de verdad | Destino o resultado |
|---|---|---|
| Configuracion de usuario | archivos versionados bajo `config/`, `systemd/user/` y `bin/` | symlinks en `~/.config` y `~/.local/bin` creados por el perfil |
| Compatibilidad Hyprland | `config/hypr/{xdph,hyprsunset}.conf` | links versionados dentro del source estable que aparecen en `~/.config/hypr`; el symlink raiz estable no se reemplaza |
| Copias root-owned | templates bajo `system/pam.d/` y archivos bajo `session/` | `/etc/pam.d/omarchy-lock-*` y `/usr/local/{libexec,share}` mediante `install-session` |
| Runtime derivado | `runtime/source.lock` | checkout Git limpio en `~/.local/share/mydotfiles/omarchy-quattro/runtime` |
| Paquetes especiales | `runtime/special-packages.lock` | paquetes de sistema instalados desde payloads oficiales verificados |
| Estado derivado | temas del runtime | `~/.local/state/omarchy/current`; no se versionan historia, cache ni notificaciones |

`config/omarchy/shell.toml` es una preferencia deliberadamente versionada y
mantiene `[font] base-size = 12`. No es estado generado.

El instalador respalda solo sus cuatro rutas administradas antes de escribir.
Instala PAM como `root:root` modo `0644` y compara el contenido instalado con
el template. El PAM de fingerprint solo se instala cuando `fprintd-list`
confirma un dedo enrolado para el usuario; en este desktop password es
obligatorio y fingerprint permanece ausente mientras no exista esa evidencia.

## Actualizacion reproducible

1. actualizar `source.lock` y los payloads lockeados en una rama revisable;
2. consultar primero la metadata del DB oficial estable de Omarchy;
3. ejecutar `sync-runtime` (nunca modifica un checkout dirty o en otro commit);
4. ejecutar `install-dependencies`, `scripts/link --repair`, `prepare-user` e
   `install-session` en ese orden;
5. terminar con `check-runtime` y `scripts/doctor arch-hyprland-quattro-lab`.

### Qt y pantalla negra sin barra ni menus

Quickshell usa APIs privadas de Qt: despues de actualizar Qt puede necesitar
una recompilacion **aunque su version de codigo no cambie**. El payload
Omarchy fijado no pertenece a un repositorio habilitado en Pacman, por lo que
`pacman -Syu` no actualiza automaticamente esa recompilacion.

El incidente del 2026-10-04 fue el payload `quickshell-git` pkgrel `-1`,
compilado contra Qt 6.11.1, frente al Qt 6.11.2 actualizado. El loader fallaba
con `undefined symbol` y `Qt_6_PRIVATE_API`; Hyprland seguia funcionando, pero
el shell abandonaba tras seis intentos de arranque. El lock ahora fija pkgrel
`-3`, publicado por Omarchy con el mismo commit y compilado para Qt 6.11.2.

Antes de reiniciar o revertir el sistema, comprobar:

```sh
quickshell --private-check-compat
hyprctl configerrors
journalctl --user -b -t omarchy-shell --no-pager -n 40
```

Si Quickshell falla, revisar el rebuild en el DB oficial estable de Omarchy,
comparar las versiones Qt en `.BUILDINFO`, actualizar el filename/SHA-256 del
lock y el check de version, e instalar **solo** el payload verificado con
`sudo pacman -U`. Luego ejecutar `omarchy-restart-shell` como usuario y
`check-runtime`; no hace falta cerrar las aplicaciones ni reiniciar Hyprland.
No reinstalar el payload viejo solo porque su checksum siga siendo valido,
ni hacer downgrade aislado de Qt. `check-runtime` ahora ejecuta tambien el
chequeo de compatibilidad para detectar futuros cambios de ABI.

### Qt 6.12: menu negro por colision de `Color`

QtQuick 6.12 incorpora un singleton `Color` que oculta `qs.Commons.Color`
del runtime v4.0.0. El shell sigue respondiendo por IPC, pero los colores de
menus, barra, bloqueo y paneles quedan `undefined`. Es una regresion QML
distinta del aviso de ABI; recompilar Quickshell por si solo no la corrige.
Referencias: [reporte upstream](https://github.com/omacom/omarchy/issues/14548)
y [tipo incorporado en Qt 6.12](https://doc.qt.io/qt-6/qml-qtquick-color.html).

La compatibilidad de Quattro se limita a su `config/compat-bin`: los wrappers
`quickshell` y `qs` generan y verifican un overlay bajo
`~/.local/share/mydotfiles/omarchy-quattro/qtquick-compat/<sha256>`. Solo copian
el shell y fijan `import QtQuick 6.11` en sus consumidores de `Color`; el resto
del runtime se enlaza al checkout original, que permanece limpio y fijado.
Esto limita los tipos QML visibles, **no** baja la version de Qt instalada.
Los paths de arranque, IPC y kill se traducen juntos; `OMARCHY_PATH` se cambia
solo dentro de Quickshell para que tambien cargue los plugins corregidos.
Se requiere Python 3, declarado en `runtime/arch-packages.txt`.

```sh
os/linux/hyprland/quattro-lab/scripts/prepare-shell-compat
os/linux/hyprland/quattro-lab/scripts/test-shell-compat
omarchy-restart-shell
```

Los overlays son derivados, publicados atomicamente y verificados byte a byte;
no contienen preferencias del usuario. El wrapper rechaza un checkout upstream
dirty o fuera del commit fijado. Al actualizar el runtime, revisar esta capa
junto al lock. Para rollback, retirar los links `compat-bin/{quickshell,qs}` y
reiniciar el shell con `/usr/bin/quickshell kill -p <overlay>/shell` seguido de
`omarchy-restart-shell`; no modificar ni restaurar manualmente archivos QML
upstream. Mientras Qt sea 6.12, ese rollback vuelve a exponer el bug.

El 2026-10-08 el DB estable de Omarchy seguia publicando el payload `-3`,
compilado contra Qt 6.11.2. El check de ABI se mantiene estricto: la correccion
del menu no oculta ese aviso ni declara el binario recompilado.

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

La entrada de SDDM y las copias PAM se revierten con el directorio de respaldo
informado al instalar. Tambien se restaura el estado previo enabled/active del
servicio de usuario:

```sh
os/linux/hyprland/quattro-lab/scripts/rollback-session --dry-run \
  "$HOME/.local/state/mydotfiles/backups/hyprland-quattro-lab/<timestamp>"
os/linux/hyprland/quattro-lab/scripts/rollback-session \
  "$HOME/.local/state/mydotfiles/backups/hyprland-quattro-lab/<timestamp>"
```

Cada backup contiene `system-files.tar`, su SHA-256, la lista exacta de rutas y
el estado previo del servicio. El rollback valida que no haya miembros fuera de
las cuatro rutas administradas antes de extraer. El runtime, los paquetes y el
estado de usuario se conservan para diagnostico; el rollback nunca toca otros
archivos PAM/systemd, `~/.config/hypr`, las sesiones legacy ni macOS.

## Proveniencia

Omarchy se distribuye bajo licencia MIT. La licencia upstream se conserva en
`LICENSE.omarchy`; hashes, tag y revision viven en `runtime/`.
