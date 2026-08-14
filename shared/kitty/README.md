# Kitty Configuration

Base compartida de [Kitty](https://sw.kovidgoyal.net/kitty/) para Linux y
macOS. Las opciones portables viven aqui; cada sistema operativo mantiene su
propio entrypoint y sus propios modificadores.

## Structure

- **Location**: `~/mydotfiles/shared/kitty/`
  - `common.conf`: opciones y bindings realmente compartidos.
  - `active-theme.conf`: tema cargado por `common.conf`.
  - `themes/`: Local copy of Kitty themes.
  - `sessions/`: Saved Kitty sessions.
  - `scripts/`: Helper scripts used by session/keymap actions.
- **Linux entrypoint**: `os/linux/kitty/kitty.conf`.
- **macOS entrypoint**: `os/macos/kitty/kitty.conf`.
- **Deployment**: cada perfil enlaza su entrypoint como
  `~/.config/kitty/kitty.conf`; ya no se enlaza el directorio compartido
  completo.

## Theme

The current theme is loaded from:

```conf
include ~/mydotfiles/shared/kitty/active-theme.conf
```

Para cambiarlo, editar `active-theme.conf` o reemplazarlo por uno de los
archivos de `themes/themes/`.

## Clipboard on Linux

El entrypoint Linux asigna `Ctrl+Shift+C` a `copy_to_clipboard` y
`Ctrl+Shift+V` a `paste_from_clipboard`. Estos bindings no se cargan en macOS.
En aplicaciones TUI que capturan el mouse, mantener `Shift` mientras se
arrastra para forzar la seleccion de Kitty.

## Installation

### 1. Install Kitty

Official installer:

```bash
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
```

Homebrew alternative:

```bash
brew install --cask kitty
```

### 2. Aplicar el perfil correspondiente

```bash
scripts/link --dry-run --repair arch-hyprland
scripts/link --dry-run --repair macos-main
```

La migracion desde el layout anterior requiere eliminar solamente el symlink
de directorio `~/.config/kitty` y volver a aplicar el perfil. El linker crea un
directorio real y enlaza dentro de el `kitty.conf` y `pass_keys.py`; nunca
reemplaza archivos reales.

## See Themes

The official theme picker can preview and apply themes:

```bash
kitten themes
```

Theme documentation: [Kitty themes](https://sw.kovidgoyal.net/kitty/kittens/themes/).

## Configure Themes

The local theme collection lives in `themes/`. To refresh it from upstream:

```bash
mkdir -p ~/mydotfiles/shared/kitty/themes/
git clone --depth 1 https://github.com/kovidgoyal/kitty-themes.git ~/mydotfiles/shared/kitty/themes/
rm -rf ~/mydotfiles/shared/kitty/themes/.git/
rm -rf ~/mydotfiles/shared/kitty/themes/.github/
```

## Generate the Default Config

Kitty can generate a commented default config from inside the app with `cmd+,`, or from the CLI:

```bash
kitty +runpy 'from kitty.config import *; print(commented_out_default_config())'
```
