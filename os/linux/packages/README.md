# Linux Packages

Configuracion y documentacion para paquetes en Arch Linux: `pacman`, helpers de
AUR como `yay`, `makepkg` y listas reproducibles de paquetes.

`MAINTENANCE.md` define el procedimiento de actualizacion, verificacion y
recuperacion que debe probarse antes de usar Arch como maquina principal.

## Regla principal

El repo puede documentar que instalar y como reconstruirlo, pero no debe guardar
artefactos generados por builds.

Guardar en Git:

- listas de paquetes revisadas;
- notas de instalacion;
- configuracion versionable de `pacman` o `makepkg`;
- scripts de bootstrap que sean reproducibles.

No guardar en Git:

- caches de `yay` o `pacman`;
- paquetes generados `*.pkg.tar.*`;
- fuentes descargadas automaticamente;
- logs de compilacion regenerables;
- claves, tokens o credenciales.

## Estructura activa

```text
packages/
  pacman/           # pacman.conf, hooks o notas si se versionan
  yay/              # configuracion/notas del helper AUR
  makepkg/          # makepkg.conf de usuario si se decide versionar
  lists/            # listas de paquetes por perfil
  scripts/          # validacion y aplicacion idempotente de manifiestos
```

### Manifiestos actuales

- `lists/10-workstation-base.txt`: herramientas oficiales portables, Git/GitHub,
  terminal, editores, keyring, Helium fallback y diagnostico.
- `lists/20-xrdp-build.txt`: dependencias oficiales de build para los paquetes
  AUR revisados de XRDP; no se confunden con la base diaria.
- `lists/aur-reviewed.txt`: versiones, commits revisados y justificacion de cada
  paquete AUR permitido.

Previsualizar y aplicar una lista oficial:

```bash
os/linux/packages/scripts/install-official-list \
  os/linux/packages/lists/10-workstation-base.txt

os/linux/packages/scripts/install-official-list --execute \
  os/linux/packages/lists/10-workstation-base.txt
```

El instalador usa una actualizacion completa `pacman -Syu`; nunca ejecuta la
actualizacion parcial no soportada `pacman -Sy paquete`.

Configurar la identidad portable de Git sin guardar credenciales:

```bash
os/linux/packages/scripts/configure-git
os/linux/packages/scripts/configure-git --execute
```

La autenticacion de GitHub pertenece al dispositivo y se hace despues con
`gh auth login`; el token queda fuera del repositorio.

## Workstation Phases

1. **Official Foundation**: herramientas CLI, GitHub CLI, shells, editores,
   keyring y Firefox de recuperacion.
2. **Git and Dotfiles**: identidad, autenticacion del dispositivo, clon HTTPS y
   perfil `arch-desktop`.
3. **Default Browser**: `helium-browser-bin` AUR revisado, firma upstream y
   `xdg-settings`; Firefox permanece como alternativa oficial.
4. **Remote Recovery**: XRDP/Xorgxrdp AUR revisados y XFCE X11 por RDP.
5. **Data and Productivity**: `SHARED-DATA`, Dropbox/Obsidian y herramientas de
   trabajo elegidas, cada una con fuente documentada.
6. **Wayland Desktop**: Hyprland y sus modulos, sin mezclar configuracion X11.

No se instala una lista de aplicaciones hipotetica completa de una vez. Cada
fase debe responder a una necesidad real, conservar rollback y terminar con una
validacion antes de continuar.

El procedimiento fijado para Helium vive en `../helium/scripts/install`; no se
delega la revision o construccion inicial a un AUR helper global.

## makepkg

Arch permite configurar rutas de salida en `makepkg.conf`. Cuando tenga sentido,
centralizar builds, paquetes, fuentes y logs fuera del repo usando variables
como:

```sh
BUILDDIR="$HOME/.cache/makepkg/build"
PKGDEST="$HOME/.local/share/makepkg/packages"
SRCDEST="$HOME/.cache/makepkg/sources"
LOGDEST="$HOME/.local/state/makepkg/logs"
```

La configuracion de usuario puede vivir en:

```text
$XDG_CONFIG_HOME/pacman/makepkg.conf
~/.makepkg.conf
```

Preferir `$XDG_CONFIG_HOME/pacman/makepkg.conf` cuando se empiece a versionar.

Referencia: https://man.archlinux.org/man/makepkg.conf.5.en
