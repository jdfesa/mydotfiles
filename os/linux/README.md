# Linux

Configuraciones y utilidades especificas de GNU/Linux.

Esta capa es para piezas que pertenecen al setup Linux y que no deberian vivir
en la raiz compartida del repo.

## Regla principal

Los window managers viven como herramientas propias dentro de `os/linux/`,
aunque dependan de X11 o Wayland.

Ejemplos:

- `dwm/`: configuracion, fuentes, parches, scripts de build y notas de DWM;
- `i3/`: configuracion, scripts y notas de i3;
- `bspwm/`, `openbox/`, `sway/` o similares si se prueban mas adelante.

`x11/` y `wayland/` quedan para infraestructura compartida por varias sesiones,
no para esconder un window manager importante dentro de una tecnologia base.

Ejemplos de infraestructura:

- `x11/scripts/start-x11vnc.sh`;
- scripts de `xrandr`, `xrdb`, `Xephyr` o display debugging;
- utilidades de Wayland compartidas por Sway, Hyprland u otros compositores.

## Que pertenece a esta capa

- DWM, i3 y otros window managers de Linux;
- X11 y Wayland;
- Pacman, Yay y paquetes del sistema;
- servicios o scripts que dependan de una sesion grafica Linux.

## Que no pertenece a esta capa

Las herramientas compartidas, como Neovim, Git, Starship, Tmux, Yazi, Btop,
Fzf, Ripgrep o Zoxide, deben seguir en sus carpetas principales salvo que
necesiten una variante especifica de Linux.

Tampoco deben guardarse secretos, contrasenas, tokens ni claves privadas en Git.
Las credenciales locales deben vivir fuera del repo, por ejemplo en `~/.vnc/`,
`~/.ssh/` o archivos locales ignorados.

## Estructura esperada

```text
linux/
  dwm/              # DWM como herramienta principal
    README.md
    patches/
    scripts/

  i3/               # futuro i3 si se prueba
    README.md
    config
    scripts/

  x11/              # piezas transversales de X11
    README.md
    scripts/        # x11vnc, Xephyr, xrandr, xrdb, etc.

  wayland/          # piezas transversales de Wayland si aparecen
    README.md
    scripts/
```

## Acceso remoto

Este repo debe favorecer flujos que se puedan manejar remotamente:

- SSH para editar dotfiles, usar Git, compilar y recuperar sesiones;
- VNC o x11vnc para ver/controlar una sesion grafica X11 real;
- XRDP como entrada comoda a un entorno de rescate, por ejemplo XFCE;
- scripts seguros por defecto, sin contrasenas embebidas y preferentemente
  limitados a `localhost` cuando se conecten por tunel SSH.
