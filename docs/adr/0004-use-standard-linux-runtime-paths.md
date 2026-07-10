# Use Standard Linux Runtime Paths

Status: Accepted
Date: 2026-07-10

## Context

El repositorio va a crecer desde un setup principal de macOS hacia Arch Linux,
Windows, VMs y hosts especificos. En Linux apareceran window managers, scripts
de acceso remoto, configuraciones de paquetes, helpers de X11/Wayland y builds
de AUR.

Si cada pieza decide su propia ubicacion, el repo se vuelve dificil de restaurar
y los scripts quedan desperdigados entre el home, `/usr/local`, caches y
carpetas temporales.

Tambien existe una diferencia importante entre:

- la fuente versionada de una configuracion;
- el lugar desde donde se ejecuta como comando;
- los datos, caches, logs, builds y secretos locales.

## Decision

Usar el repositorio como fuente de verdad versionada, y desplegar cada pieza a
la ubicacion estandar que corresponda.

Para GNU/Linux:

- configuraciones y scripts versionados especificos de Linux viven en
  `os/linux/`;
- window managers viven como herramientas propias: `os/linux/dwm/`,
  `os/linux/i3/`, `os/linux/sway/`, etc.;
- infraestructura compartida vive bajo su tecnologia base, por ejemplo
  `os/linux/x11/` o `os/linux/wayland/`;
- scripts ejecutables del usuario se enlazan o instalan en `$HOME/.local/bin`;
- configuraciones de usuario se enlazan a `$XDG_CONFIG_HOME`, normalmente
  `$HOME/.config`;
- datos, estado y cache siguen XDG: `$HOME/.local/share`,
  `$HOME/.local/state` y `$HOME/.cache`;
- scripts locales de sistema administrados por el usuario root van en
  `/usr/local/bin` o `/usr/local/sbin`, no en `/usr/bin`;
- builds, caches de AUR, paquetes generados y logs de compilacion no se guardan
  en Git;
- secretos, contrasenas, tokens y claves privadas quedan fuera del repositorio.

`scripts/` en la raiz queda reservado para bootstrap, linking e instalacion
transversal del repositorio. No debe convertirse en una carpeta mezclada de
scripts especificos de macOS, Linux o Windows.

## Consequences

Ventajas:

- las rutas siguen convenciones conocidas de Linux y XDG;
- cada herramienta tiene un lugar estable antes de crecer;
- los comandos pueden ejecutarse desde `$HOME/.local/bin` sin perder la fuente
  versionada en `~/mydotfiles`;
- el repo se mantiene reproducible porque separa fuente, runtime, caches y
  secretos;
- se reduce la friccion para una futura migracion a `chezmoi`, `stow` o
  perfiles declarativos.

Costos:

- hay que documentar symlinks o scripts de instalacion por perfil;
- algunas herramientas necesitaran una pequena envoltura para ser comodas como
  comandos;
- los archivos locales fuera de Git deben recrearse con instrucciones claras.

Referencias:

- XDG Base Directory Specification:
  https://specifications.freedesktop.org/basedir-spec/latest/
- Filesystem Hierarchy Standard, `/usr/local`:
  https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch04s09.html
- Arch `makepkg.conf(5)`:
  https://man.archlinux.org/man/makepkg.conf.5.en
