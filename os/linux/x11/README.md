# Linux X11

Configuracion y utilidades especificas para sesiones X11 en GNU/Linux.

## Estructura

```text
x11/
  scripts/        # utilidades operativas de X11
```

Las configuraciones de window managers deben vivir como herramientas propias
dentro de `os/linux/`, por ejemplo `os/linux/dwm/`, aunque dependan de X11.

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

### Uso diario

En la maquina Linux remota, arrancar el servidor:

```sh
~/mydotfiles/os/linux/x11/scripts/start-x11vnc.sh
```

Desde la maquina cliente, abrir el tunel SSH:

```sh
ssh -L 5900:localhost:5900 jd@192.168.8.15
```

Luego abrir el cliente VNC contra:

```text
localhost:5900
```

El script usa `-localhost`, asi que no expone VNC directamente a toda la red.

### Variables opcionales

```sh
DISPLAY_NUM=:0 RFB_PORT=5900 ~/mydotfiles/os/linux/x11/scripts/start-x11vnc.sh
X11VNC_PASSWD_FILE=~/.vnc/otra-passwd ~/mydotfiles/os/linux/x11/scripts/start-x11vnc.sh
```
