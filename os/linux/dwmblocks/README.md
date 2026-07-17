# DWMBlocks

Configuracion reproducible de DWMBlocks para la barra de estado de DWM.
DWMBlocks se mantiene separado de DWM: ambos se integran en la sesion, pero
tienen fuentes, builds y ciclos de actualizacion independientes.

## Fuente

`src/` parte de `torrinfail/dwmblocks` en el commit `8cedd22`. Se conservaron y
documentaron estos ajustes locales del respaldo historico:

- prototipos correctos para `termhandler(int signum)`, necesarios para compilar
  sin advertencias de funciones incompatibles;
- eliminacion de una variable global sin uso;
- una barra minima con `status-sensors` y fecha/hora.

La configuracion efectiva es `src/blocks.h`. El comando `status-sensors` se
resuelve mediante `PATH`; no se codifican rutas antiguas bajo
`~/.local/scripts`. El perfil `arch-desktop` enlaza el script versionado en
`~/.local/bin/status-sensors`, y el launcher de la sesion DWM incluye
`~/.local/bin` en `PATH`.

No se versionan el clon Git anidado, el binario historico ni otros resultados
de compilacion recuperados del respaldo.

## Dependencias

Para compilar en Arch Linux:

```sh
sudo pacman -S --needed base-devel libx11
```

En tiempo de ejecucion, el bloque de sensores usa las dependencias documentadas
por `../dwm/scripts/status-sensors.sh`. La ausencia de un sensor opcional no
debe impedir que DWMBlocks muestre los demas datos.

En equipos con el driver `amdgpu`, `status-sensors` busca
`gpu_busy_percent` bajo `/sys/class/drm` y muestra la utilizacion sin instalar
un monitor residente ni fijar el numero de tarjeta. `AMDGPU_LOAD_COMMAND`
permanece disponible para reemplazar esa deteccion cuando una GPU no exponga
la interfaz del kernel.

## Build e instalacion

Compilar sin modificar `src/`:

```sh
os/linux/dwmblocks/scripts/build
```

La build queda en `~/.cache/mydotfiles-build/dwmblocks`. Para revisar la
operacion privilegiada sin ejecutarla:

```sh
os/linux/dwmblocks/scripts/install --dry-run
```

Para instalar en `/usr/local/bin/dwmblocks`:

```sh
os/linux/dwmblocks/scripts/install
```

El instalador crea antes un respaldo verificable bajo:

```text
~/.local/state/mydotfiles/backups/dwmblocks/<fecha>/
```

El proceso que ya esta ejecutandose conserva el binario anterior. Despues de
instalar, cerrar la sesion DWM y volver a entrar desde SDDM para que el
autostart inicie la nueva build. No es necesario reiniciar la maquina.

Para restaurar el binario anterior:

```sh
os/linux/dwmblocks/scripts/rollback \
  ~/.local/state/mydotfiles/backups/dwmblocks/<fecha>
```

## Actualizaciones futuras

Una actualizacion upstream se compara primero contra el commit base documentado
y se incorpora deliberadamente. No se reemplaza este snapshot clonando sobre
el directorio ni se compila dentro del repositorio.
