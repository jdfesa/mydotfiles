# Linux Packages

Configuracion y documentacion para paquetes en Arch Linux: `pacman`, helpers de
AUR como `yay`, `makepkg` y listas reproducibles de paquetes.

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

## Estructura prevista

```text
packages/
  pacman/           # pacman.conf, hooks o notas si se versionan
  yay/              # configuracion/notas del helper AUR
  makepkg/          # makepkg.conf de usuario si se decide versionar
  lists/            # listas de paquetes por perfil
```

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
