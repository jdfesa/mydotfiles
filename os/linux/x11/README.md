# Linux X11

Configuracion y utilidades especificas para sesiones X11 en GNU/Linux.

## Estructura

```text
x11/
  scripts/        # utilidades operativas de X11
```

Las configuraciones de window managers deben vivir como herramientas propias
dentro de `os/linux/`, por ejemplo `os/linux/dwm/`, aunque dependan de X11.

## Clipboard history

`scripts/cliphist` conserva texto copiado en X11 y permite recuperarlo con
`dmenu`. Guarda el estado en `${XDG_CACHE_HOME:-$HOME/.cache}/cliphist/history`;
el historial personal nunca se versiona.

Dependencias: `xclip`, `dmenu` y, opcionalmente, `notify-send`.

## x11vnc

`scripts/start-x11vnc.sh` comparte la sesion fisica X11, por ejemplo `:0`, usando
`x11vnc`. No guarda contrasenas en Git: espera un archivo local
`~/.vnc/passwd`.

No usar `-passwd <clave>` en scripts versionados. Esa forma deja la contrasena
hardcodeada y puede exponerla en el historial, en Git o en la lista de procesos.
Este repo usa `-rfbauth ~/.vnc/passwd`.

### Setup inicial

Crear la contrasena una vez en la maquina Linux remota:

```sh
mkdir -p ~/.vnc
x11vnc -storepasswd ~/.vnc/passwd
chmod 600 ~/.vnc/passwd
```

### Uso diario desde macOS con Jump Desktop

Este flujo mantiene VNC cerrado a la red. `x11vnc` escucha solo dentro de la
maquina Arch y macOS entra por un tunel SSH.

#### 1. Abrir el tunel SSH en macOS

En una terminal de macOS, no dentro de una sesion SSH, ejecutar:

```sh
ssh -N -L 5901:127.0.0.1:5900 jd@192.168.8.15
```

La terminal queda sin prompt mientras el tunel esta activo. Eso es normal. No
cerrarla mientras se use Jump Desktop.

#### 2. Arrancar x11vnc en Arch

En otra terminal de macOS, entrar a la maquina Arch:

```sh
ssh jd@192.168.8.15
```

Dentro de Arch, arrancar el servidor:

```sh
~/mydotfiles/os/linux/x11/scripts/start-x11vnc.sh
```

Tambien puede ejecutarse desde el symlink recomendado:

```sh
~/.local/bin/start-x11vnc
```

Esta terminal tambien debe quedar abierta, mostrando los logs de `x11vnc`.

#### 3. Conectar Jump Desktop

En Jump Desktop crear o editar una conexion VNC con:

```text
Host: 127.0.0.1:5901
```

No usar:

```text
192.168.8.15:5901
192.168.8.15:5900
```

Jump Desktop se conecta a macOS en `127.0.0.1:5901`; SSH transporta esa conexion
hacia Arch; y dentro de Arch llega a `127.0.0.1:5900`, donde escucha `x11vnc`.

```text
Jump Desktop en macOS
  -> 127.0.0.1:5901 en macOS
  -> tunel SSH
  -> 127.0.0.1:5900 dentro de Arch
  -> x11vnc
```

El script usa `-localhost`, asi que no expone VNC directamente a toda la red.

#### Diagnostico rapido

En macOS, comprobar que el tunel esta abierto:

```sh
lsof -nP -iTCP:5901 -sTCP:LISTEN
```

En Arch, comprobar que `x11vnc` esta vivo:

```sh
pgrep -a x11vnc
ss -ltnp | grep 5900
```

Si Jump Desktop abre y se cierra al instante, normalmente falta una de estas dos
cosas: el tunel SSH en macOS o el proceso `x11vnc` en Arch.

### Variables opcionales

```sh
DISPLAY_NUM=:0 RFB_PORT=5900 ~/mydotfiles/os/linux/x11/scripts/start-x11vnc.sh
X11VNC_PASSWD_FILE=~/.vnc/otra-passwd ~/mydotfiles/os/linux/x11/scripts/start-x11vnc.sh
```
