# Restaurar Neovim

Pasos para reconstruir esta configuracion desde cero en otra maquina.

## Principio

La restauracion debe depender del repo y de gestores declarados, no de memoria.

Orden correcto:

1. Sistema operativo.
2. Symlink de config.
3. Plugins Lazy.
4. Herramientas Mason.
5. Parsers Treesitter.
6. Validacion.

## macOS

1. Clonar dotfiles:

```bash
git clone https://github.com/jdfesa/mydotfiles.git ~/mydotfiles
```

2. Instalar dependencias esenciales:

```bash
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/10-essential/Brewfile
```

Si no queres instalar todo el Brewfile, el minimo para Neovim es:

```bash
brew install neovim ripgrep fd fzf lazygit tree-sitter-cli wget jdtls
brew install --cask font-jetbrains-mono-nerd-font
```

3. Crear el symlink:

```bash
mkdir -p ~/.config
ln -s ~/mydotfiles/shared/nvim ~/.config/nvim
```

Si ya existe una config previa y queres reemplazarla:

```bash
mv ~/.config/nvim ~/.config/nvim.bak
ln -s ~/mydotfiles/shared/nvim ~/.config/nvim
```

Importante: en esta instalacion inicial no se respaldo AstroNvim porque el
usuario confirmo que no habia configuracion valiosa. En una maquina futura,
usar backup si hay duda.

4. Sincronizar plugins:

```bash
nvim --headless "+Lazy! sync" +qa
```

5. Preinstalar paquetes Mason usados por esta config:

```bash
nvim --headless "+Lazy load mason.nvim" \
  "+MasonInstall pyright ruff marksman markdownlint-cli2 markdown-toc java-debug-adapter java-test shellcheck debugpy stylua shfmt tree-sitter-cli" \
  +qa
```

No instalar `jdtls` con Mason. En esta config se usa `jdtls` de Homebrew.

6. Precompilar parsers Treesitter base:

```bash
nvim --headless "+lua require('nvim-treesitter.install').install({'lua','vim','vimdoc','markdown','markdown_inline','python','java','json','toml','yaml','bash'}, {summary = true, max_jobs = 2}):await()" +qa
```

7. Validar:

```bash
nvim --headless "+checkhealth lazy lazyvim vim.lsp" "+write! /tmp/nvim-health.txt" +qa
sed -n '1,220p' /tmp/nvim-health.txt
```

## Linux futuro

La config de Neovim es portable, pero la capa de sistema cambia. Instalar
equivalentes con el gestor de paquetes de la distro:

- `neovim >= 0.11`
- `git`
- `ripgrep`
- `fd`
- `fzf`
- `lazygit`
- `tree-sitter-cli`
- `wget`
- `jdtls`
- una Nerd Font configurada en la terminal

Despues usar los mismos pasos de symlink, `Lazy! sync`, Mason y Treesitter.

Notas para Linux:

- En algunas distros `fd` se instala como `fdfind`.
- `jdtls` puede venir en repositorios, SDKMAN, paquetes manuales o gestores de
  lenguaje; la condicion importante es que `command -v jdtls` funcione.
- La fuente Nerd Font puede instalarse por paquete, descarga manual o gestor de fuentes.
- Si no se usa Homebrew, crear un documento equivalente para el gestor elegido.

## Notas

- La ruta de notas configurada es `/Users/jd/Documents/ObsidianVault`.
- En otra maquina conviene recrear esa ruta, migrar el vault, o editar
  `shared/nvim/lua/config/keymaps.lua`.
- `Space N d` crea `daily/YYYY-MM-DD.md` dentro del vault cuando se usa por primera vez.

## Checklist post-restauracion

- `readlink ~/.config/nvim` apunta al repo.
- `nvim --headless "+lua print('ok')" +qa` arranca.
- `:Lazy` no muestra errores de instalacion.
- `:Mason` muestra paquetes instalados.
- `checkhealth lazy lazyvim vim.lsp` no muestra errores bloqueantes.
- Abrir un `.py` muestra clientes `pyright` y `ruff`.
- Abrir un `.java` en proyecto Maven/Gradle muestra cliente `jdtls`.
- Abrir un `.md` activa wrap local y cliente `marksman`.
