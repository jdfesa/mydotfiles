# Linux Display Managers

Un display manager presenta la pantalla grafica de inicio de sesion. No es el
entorno de escritorio ni el window manager: SDDM puede iniciar XFCE, DWM u otra
sesion que tenga un archivo valido en `xsessions/` o `wayland-sessions/`.

## Decision para `arch-desktop`

Se mantiene **SDDM**. Ya esta habilitado, funciona con XFCE y no hay una razon
operativa para reemplazarlo mientras se prueba DWM. XFCE X11 sigue siendo la
sesion de recuperacion; DWM se agrega como alternativa, no como reemplazo.

Solo debe haber un servicio de display manager habilitado a la vez. Instalar
otro no agrega un nuevo escritorio al selector: para eso se instala una sesion.

## Opciones habituales

| Display manager | Enfoque | Cuando tiene sentido |
|---|---|---|
| SDDM | General, interfaz Qt, X11 y Wayland | KDE o equipos con varias sesiones; es la opcion actual |
| LightDM | Ligero, greeters intercambiables | XFCE y escritorios livianos |
| GDM | Integrado con GNOME | GNOME y flujos Wayland administrados por GNOME |
| LXDM | Muy simple y orientado a X11 | Equipos livianos que no necesitan una integracion moderna |
| greetd | Login minimalista y configurable | Configuraciones deliberadamente manuales, sobre todo Wayland |

No hay un ganador universal. Para esta maquina pesa mas conservar un camino de
recuperacion conocido que cambiar la apariencia del login.

## Donde aparecen las sesiones

```text
/usr/local/share/xsessions/*.desktop       # sesiones X11 instaladas localmente
/usr/share/xsessions/*.desktop             # sesiones X11 de paquetes del sistema
/usr/local/share/wayland-sessions/*.desktop
/usr/share/wayland-sessions/*.desktop
```

La sesion DWM de este repositorio se instala como:

```text
/usr/local/share/xsessions/dwm.desktop
/usr/local/libexec/dotfiles-dwm-session
```

SDDM muestra `DWM (dotfiles)` junto con XFCE. La sesion elegida puede quedar
recordada para el proximo login, pero XFCE no se desinstala ni se deshabilita.

## Diagnostico sin cambiar nada

```sh
systemctl status display-manager
readlink -f /etc/systemd/system/display-manager.service
find /usr/local/share/xsessions /usr/share/xsessions \
  /usr/local/share/wayland-sessions /usr/share/wayland-sessions \
  -maxdepth 1 -type f -name '*.desktop' -print 2>/dev/null
```

Para volver desde DWM al selector de SDDM se usa `Mod+Shift+Backspace`. Si DWM
no responde, cambiar a una TTY con `Ctrl+Alt+F3`, iniciar sesion y ejecutar:

```sh
sudo systemctl restart sddm
```

Ese reinicio cierra cualquier sesion grafica activa. SSH y XRDP deben probarse
antes de experimentar con el login local.
