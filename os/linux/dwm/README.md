# DWM

Configuracion personal de DWM, integrada con dmenu y con una sesion X11
seleccionable desde SDDM. XFCE permanece instalado y operativo como respaldo.

## Fuente y alcance

`src/` es el arbol fuente propio de DWM 6.5, con los parches enumerados en
`src/README.md`. La identidad de esta configuracion es el historial de este
repositorio y sus decisiones locales; no depende del nombre, repositorio o
commit de una configuracion externa usada como punto de partida.

No se vuelve a clonar una configuracion ajena para cada instalacion. Las
actualizaciones futuras se comparan e incorporan deliberadamente para no perder
los cambios personales.

Primeras modificaciones locales de atajos:

- `Mod+f` queda reservado para fullscreen; se retiro el launcher duplicado de
  `fff`, que ademas no esta instalado en `arch-desktop`;
- `focusmaster` usa `Mod+Ctrl+m` en vez de colisionar con `Mod+Ctrl+Space`;
- el toggle de tags de la barra usa `Mod+Ctrl+g` en vez de colisionar con el
  toggle del titulo en `Mod+Ctrl+t`.

DWM, ST, dmenu y DWMBlocks siguen siendo proyectos independientes. Que la
sesion DWM use esos comandos no convierte sus fuentes en una sola aplicacion.

## Estructura

```text
dwm/
  README.md
  src/                    # fuente y config.def.h versionados
  session/
    dwm.desktop           # entrada X11 para SDDM y otros display managers
    dwm-session           # launcher aislado de XFCE
    autostart.sh          # procesos exclusivos de la sesion DWM
  scripts/
    build                 # build reproducible en cache, sin ensuciar src/
    test-nested           # prueba dentro de Xephyr desde XFCE
    install-session       # backup, instalacion de DWM+dmenu y sesion
    rollback-session      # restaura un backup creado por el instalador
    wallpaper-rotator.sh
    status-sensors.sh
```

## Dependencias en Arch Linux

Para compilar:

```sh
sudo pacman -S --needed base-devel libx11 libxft libxinerama libxcb
```

Para probar de forma anidada antes de tocar la sesion instalada:

```sh
sudo pacman -S --needed xorg-server-xephyr
```

La configuracion importada usa `st`, `dmenu_run` y, opcionalmente,
`dwmblocks`, `picom`, `feh`, Nerd Fonts y Noto Color Emoji. Un comando ausente
solo afecta su atajo o funcion asociada; no debe impedir que DWM arranque.

## Flujo de personalizacion

La configuracion efectiva versionada es `src/config.def.h`. No editar el
`config.h` generado dentro del directorio de build.

1. Cambiar una sola decision en `src/config.def.h`: atajo, fuente, color, regla,
   gap o layout.
2. Compilar sin privilegios:

   ```sh
   os/linux/dwm/scripts/build
   os/linux/dmenu/scripts/build
   ```

   Los resultados quedan en `~/.cache/mydotfiles-build/{dwm,dmenu}`. `src/`
   permanece limpio para que Git muestre solamente cambios intencionales.

3. Desde una terminal abierta en XFCE X11, probar la build en Xephyr:

   ```sh
   os/linux/dwm/scripts/test-nested
   ```

4. Instalar solo después de confirmar que la build abre, que `Mod+Enter`
   lanza una terminal y que `Mod+d` abre dmenu:

   ```sh
   os/linux/dwm/scripts/install-session
   ```

5. Cerrar la sesion grafica, elegir `DWM (dotfiles)` en SDDM y entrar. XFCE
   queda disponible en el mismo selector.

Atajos basicos de la base importada:

| Atajo | Accion |
|---|---|
| `Mod+Enter` | Abrir ST |
| `Mod+d` | Abrir dmenu |
| `Mod+q` | Cerrar la ventana activa |
| `Mod+Ctrl+Shift+q` | Reiniciar DWM despues de recompilar |
| `Mod+Ctrl+\` | Recargar colores de Xresources |
| `Mod+Shift+Backspace` | Salir de DWM y volver a SDDM |

La base upstream contiene muchos atajos para programas personales del autor.
Los que no existan en esta maquina son candidatos a eliminar o reasignar. Antes
de agregar un atajo hay que buscar combinaciones duplicadas en `keys[]`; DWM
ejecuta todas las entradas que coinciden.

## Integracion con SDDM sin contaminar XFCE

El instalador coloca archivos locales de sistema en:

```text
/usr/local/bin/dwm
/usr/local/libexec/dotfiles-dwm-session
/usr/local/share/xsessions/dwm.desktop
```

No se usa `~/.xprofile` para iniciar procesos de DWM porque tambien puede ser
leido por otras sesiones X11. El launcher ejecuta únicamente
`~/.config/dwm/autostart.sh`, enlazado por el perfil `arch-desktop`.

El autostart inicia `picom` y `dwmblocks` si están instalados. La rotacion de
wallpapers es opt-in para no fallar cuando no existe el directorio:

```sh
DWM_ROTATE_WALLPAPER=1 WALLPAPERS_DIR="$HOME/Pictures/wallpapers" \
  ~/.config/dwm/autostart.sh
```

Los logs de inicio quedan fuera de Git en:

```text
~/.local/state/mydotfiles/dwm-session.log
```

## Instalacion y rollback

`install-session` compila antes de pedir privilegios, respalda todos los
archivos administrados y solo despues instala. Cada respaldo queda en:

```text
~/.local/state/mydotfiles/backups/dwm-session/<fecha>/
```

Para volver exactamente a los archivos anteriores:

```sh
os/linux/dwm/scripts/rollback-session \
  ~/.local/state/mydotfiles/backups/dwm-session/<fecha>
```

El rollback no toca XFCE, SDDM, SSH ni XRDP. La decision sobre display managers
y sesiones esta documentada en `os/linux/display-managers/README.md`.

## Scripts recuperados

- `wallpaper-rotator.sh`: rota imagenes mediante `feh` sin romper rutas que
  contienen espacios.
- `status-sensors.sh`: genera el bloque de CPU, memoria y GPU usado por
  `dwmblocks`; detecta automaticamente la utilizacion publicada por `amdgpu`
  en sysfs y admite un lector configurable como override.

Sus dependencias se validan en tiempo de ejecucion y no se instalan
automaticamente.
