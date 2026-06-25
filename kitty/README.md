# Kitty Configuration

Configuration for [Kitty](https://sw.kovidgoyal.net/kitty/), a fast GPU-based terminal emulator with image support, sessions, remote control, and an extensive theme system.

## Structure

- **Location**: `~/mydotfiles/kitty/`
  - `kitty.conf`: Main configuration file.
  - `active-theme.conf`: Active color theme loaded by `kitty.conf`.
  - `themes/`: Local copy of Kitty themes.
  - `sessions/`: Saved Kitty sessions.
  - `scripts/`: Helper scripts used by session/keymap actions.
- **Symlink**: `~/.config/kitty` -> `~/mydotfiles/kitty`

## Theme

The current theme is loaded from:

```conf
include ~/mydotfiles/kitty/active-theme.conf
```

To change it, edit `active-theme.conf` directly or replace it with one of the files in `themes/themes/`.

## Installation

### 1. Install Kitty

```bash
brew install --cask kitty
```

### 2. Apply this configuration

```bash
mkdir -p ~/.config
ln -s ~/mydotfiles/kitty ~/.config/kitty
```

If `~/.config/kitty` already exists, back it up or remove it before creating the symlink.

## See Themes

The official theme picker can preview and apply themes:

```bash
kitten themes
```

Theme documentation: [Kitty themes](https://sw.kovidgoyal.net/kitty/kittens/themes/).

## Configure Themes

The local theme collection lives in `themes/`. To refresh it from upstream:

```bash
mkdir -p ~/mydotfiles/kitty/themes/
git clone --depth 1 https://github.com/kovidgoyal/kitty-themes.git ~/mydotfiles/kitty/themes/
rm -rf ~/mydotfiles/kitty/themes/.git/
rm -rf ~/mydotfiles/kitty/themes/.github/
```

## Generate the Default Config

Kitty can generate a commented default config from inside the app with `cmd+,`, or from the CLI:

```bash
kitty +runpy 'from kitty.config import *; print(commented_out_default_config())'
```
