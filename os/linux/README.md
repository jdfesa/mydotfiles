# Linux

Configuraciones y utilidades especificas de GNU/Linux.

Esta capa es para piezas que pertenecen al setup Linux y que no deberian vivir
en la raiz compartida del repo.

## Compatibility Disclaimer

Las configuraciones graficas se desarrollan y validan incrementalmente sobre
el hardware real de `arch-desktop`; no se asume que sus valores sean universales.
Una GPU, salida, dispositivo de audio o teclado diferente puede requerir un
override aunque la estructura modular y los componentes sean reutilizables.

Base de validacion actual (2026-08-12):

| Componente | Hardware o software probado |
|---|---|
| CPU | Intel Core i7-4790K, 8 hilos |
| Placa | Intel B85, firmware AMI 4.6.5 |
| GPU principal | AMD Radeon RX 550, driver `amdgpu` |
| GPU integrada | Intel Haswell, driver `i915` |
| Monitor | `HDMI-A-2`, 1920x1080, conectado a la RX 550 |
| Audio | Realtek ALC892, Intel HDMI y AMD HDMI/DP mediante PipeWire |
| Kernel | Arch Linux `7.1.8-arch1-3` |
| Sesion Wayland | Hyprland 0.56.2 + UWSM 0.26.6 |
| Shell grafico | Waybar 0.15.0, Wofi 1.5.3, Mako 1.11.0 |
| Terminal | Kitty 0.48.2 con Zsh 5.9 y Starship 1.26.0 compartidos |

Los detalles vivos y los resultados de cada prueba se mantienen en
`docs/machines/lab-desktop-01.md`, su inventario en
`hosts/lab-desktop-01/host.toml` y el README del componente correspondiente.

## Convencion de idioma

La interfaz y la configuracion efectiva del sistema operativo se mantienen en
ingles. Esto incluye textos visibles, etiquetas, comandos, comentarios tecnicos
y nombres de archivos y directorios.

La documentacion narrativa se escribe en espanol para conservar explicaciones
y procedimientos claros. Dentro de esa documentacion, los identificadores
tecnicos, rutas, nombres de archivos y nombres de directorios permanecen en
ingles.

## Regla principal

Los window managers viven como herramientas propias dentro de `os/linux/`,
aunque dependan de X11 o Wayland.

Ejemplos:

- `dwm/`: configuracion, fuentes, parches, scripts de build y notas de DWM;
- `dwmblocks/`: barra de estado compilada, configuracion y scripts de instalacion;
- `display-managers/`: decision y diagnostico de SDDM, LightDM, GDM y sesiones;
- `audio/`: diagnostico y recuperacion de ALSA, PipeWire y WirePlumber;
- `i3/`: configuracion, scripts y notas de i3;
- `bspwm/`, `openbox/`, `sway/` o similares si se prueban mas adelante.
- `hyprland/`: configuracion modular del compositor Wayland, mantenida como
  sesion opcional mientras XFCE siga siendo el entorno de recuperacion.

`x11/` y `wayland/` quedan para infraestructura compartida por varias sesiones,
no para esconder un window manager importante dentro de una tecnologia base.

Ejemplos de infraestructura:

- `x11/scripts/start-x11vnc.sh`;
- scripts de `xrandr`, `xrdb`, `Xephyr` o display debugging;
- utilidades de Wayland compartidas por Sway, Hyprland u otros compositores.
- Waybar, Mako, Wofi y scripts Wayland reutilizables viven en `wayland/`, no
  dentro de `hyprland/`.

## Que pertenece a esta capa

- DWM, i3 y otros window managers de Linux;
- ST, Dmenu y otras herramientas graficas de Linux que pueden reutilizarse
  entre varios window managers;
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
  audio/            # audio Linux compartido por X11 y Wayland
    README.md

  dwm/              # DWM como herramienta principal
    README.md
    src/
    patches/
    scripts/

  st/               # terminal suckless, independiente de DWM
    README.md
    src/

  dmenu/            # lanzador suckless, independiente de DWM
    README.md
    src/

  dwmblocks/        # barra de estado modular, independiente de DWM
    README.md
    src/
    scripts/

  display-managers/ # login grafico y descubrimiento de sesiones
    README.md

  i3/               # futuro i3 si se prueba
    README.md
    config
    scripts/

  x11/              # piezas transversales de X11
    README.md
    scripts/        # x11vnc, Xephyr, xrandr, xrdb, etc.

  packages/         # pacman, yay, makepkg y paquetes instalables
    README.md
    pacman/
    yay/

  wayland/          # piezas transversales de Wayland si aparecen
    README.md
    scripts/
```

## Rutas en la maquina

El repo guarda la fuente versionada. La maquina Linux usa rutas estandar para
ejecutar, configurar, cachear o guardar estado:

```text
~/mydotfiles/os/linux/        # fuente versionada especifica de Linux
~/.local/bin/                 # comandos personales ejecutables
~/.config/                    # configuraciones de usuario
~/.local/share/               # datos persistentes de usuario
~/.local/state/               # estado y logs persistentes de usuario
~/.cache/                     # caches y builds regenerables
/usr/local/bin/               # comandos locales de sistema
/usr/local/sbin/              # comandos locales administrativos
/usr/local/libexec/           # launchers locales invocados por el sistema
/usr/local/share/xsessions/   # sesiones X11 instaladas localmente
```

Reglas practicas:

- si el archivo se versiona, empieza en `~/mydotfiles`;
- si se ejecuta como comando de usuario, se enlaza desde `~/.local/bin`;
- si modifica el sistema o requiere root, evaluar `/usr/local/bin` o
  `/usr/local/sbin`;
- si es cache, build o resultado regenerable, no va a Git;
- si es secreto, credencial o token, no va a Git.

Ejemplo:

```sh
ln -s ~/mydotfiles/os/linux/x11/scripts/start-x11vnc.sh ~/.local/bin/start-x11vnc
```

## Acceso remoto

Este repo debe favorecer flujos que se puedan manejar remotamente:

- SSH para editar dotfiles, usar Git, compilar y recuperar sesiones;
- VNC o x11vnc para ver/controlar una sesion grafica X11 real;
- XRDP como entrada comoda a un entorno de rescate, por ejemplo XFCE;
- scripts seguros por defecto, sin contrasenas embebidas y preferentemente
  limitados a `localhost` cuando se conecten por tunel SSH.

## Referencias

- `audio/README.md`
- `docs/ARCHITECTURE.md`
- `docs/adr/0004-use-standard-linux-runtime-paths.md`
- XDG Base Directory Specification:
  https://specifications.freedesktop.org/basedir-spec/latest/
- Filesystem Hierarchy Standard, `/usr/local`:
  https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch04s09.html
