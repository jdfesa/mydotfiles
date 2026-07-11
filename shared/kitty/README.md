# Kitty Configuration

Configuration for [Kitty](https://sw.kovidgoyal.net/kitty/), a fast GPU-based terminal emulator with image support, sessions, remote control, and an extensive theme system.

This configuration started as a copied/personalized setup from another developer's dotfiles. It is a working base, but should be adapted gradually to this repo's workflow.

## Structure

- **Location**: `~/mydotfiles/shared/kitty/`
  - `kitty.conf`: Main configuration file.
  - `active-theme.conf`: Active color theme loaded by `kitty.conf`.
  - `themes/`: Local copy of Kitty themes.
  - `sessions/`: Saved Kitty sessions.
  - `scripts/`: Helper scripts used by session/keymap actions.
- **Symlink**: `~/.config/kitty` -> `~/mydotfiles/shared/kitty`

## Theme

The current theme is loaded from:

```conf
include ~/mydotfiles/shared/kitty/active-theme.conf
```

To change it, edit `active-theme.conf` directly or replace it with one of the files in `themes/themes/`.

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

### 2. Apply this configuration and CLI symlinks

```bash
mkdir -p ~/.config
ln -s ~/mydotfiles/shared/kitty ~/.config/kitty
ln -s /Applications/kitty.app/Contents/MacOS/kitty /usr/local/bin/kitty
ln -s /Applications/kitty.app/Contents/MacOS/kitten /usr/local/bin/kitten
```

If `~/.config/kitty` already exists, back it up or remove it before creating the symlink. The `/usr/local/bin` links make `kitty` and `kitten` available from any terminal.

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
