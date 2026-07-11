# Dependencias

Estado documentado el 2026-07-05.

Este documento separa dependencias por capa. La regla es simple: si algo se
instala fuera del repo, debe quedar declarado aqui o en el Brewfile.

## Capas

| Capa | Ejemplo | Donde vive | Se versiona |
|---|---|---|---|
| Sistema operativo | `neovim`, `ripgrep`, `jdtls` | Homebrew | Si, en Brewfile |
| Plugins Neovim | `snacks.nvim`, `nvim-lspconfig` | `~/.local/share/nvim/lazy` | Si, lockfile |
| Mason | `pyright`, `ruff`, `marksman` | `~/.local/share/nvim/mason` | No |
| Treesitter | parser `python`, `java`, `markdown` | `~/.local/share/nvim/site/parser` | No |
| Estado/cache | shada, logs, cache | `~/.local/state/nvim`, `~/.cache/nvim` | No |

## Sistema operativo

Declaradas en:

```text
brew/10-essential/Brewfile
```

| Paquete | Uso | Version observada |
|---|---|---|
| `neovim` | Editor base | `0.11.4` |
| `ripgrep` | Busqueda de texto para LazyVim/Snacks | `14.1.1` |
| `fd` | Busqueda de archivos para LazyVim/Snacks | `10.3.0` |
| `fzf` | Selector fuzzy usado por terminal y algunas herramientas | `0.66.0` |
| `lazygit` | UI Git desde LazyVim/terminal | `0.55.1` |
| `tree-sitter-cli` | Compilar parsers Treesitter | `0.26.10` |
| `wget` | Descargas usadas por instaladores Mason | `1.25.0` |
| `jdtls` | LSP Java usado por LazyVim | `1.60.0` |
| `font-jetbrains-mono-nerd-font` | Iconos y UI en terminal | Brew cask |

`jdtls` arrastra dependencias Homebrew como Java/OpenJDK, Python, SQLite y GLib.
No hace falta declararlas manualmente si se instala `jdtls` por Brew.

Restauracion completa del Brewfile:

```bash
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/10-essential/Brewfile
```

Restauracion minima para Neovim:

```bash
brew install neovim ripgrep fd fzf lazygit tree-sitter-cli wget jdtls
brew install --cask font-jetbrains-mono-nerd-font
```

## Plugins Lazy

Versionados por `nvim/lazy-lock.json`.

Instalacion/restauracion:

```bash
nvim --headless "+Lazy! sync" +qa
```

Extras activados en `nvim/lua/plugins/extras.lua`:

- `lazyvim.plugins.extras.lang.markdown`
- `lazyvim.plugins.extras.lang.python`
- `lazyvim.plugins.extras.lang.java`
- `lazyvim.plugins.extras.lang.json`
- `lazyvim.plugins.extras.lang.toml`
- `lazyvim.plugins.extras.lang.yaml`

Inventario detallado de plugins:

```text
nvim/docs/PLUGINS.md
```

## Mason

Mason descarga herramientas dentro de `~/.local/share/nvim/mason`. No se versionan en el repo.

Paquetes instalados/esperados:

| Paquete Mason | Uso |
|---|---|
| `pyright` | LSP Python |
| `ruff` | LSP/linter/formatter Python |
| `marksman` | LSP Markdown |
| `markdownlint-cli2` | Linter Markdown |
| `markdown-toc` | Tabla de contenidos Markdown |
| `java-debug-adapter` | Debug Java |
| `java-test` | Test Java |
| `debugpy` | Debug Python |
| `shellcheck` | Lint shell |
| `shfmt` | Format shell |
| `stylua` | Format Lua |
| `tree-sitter-cli` | Copia Mason; tambien se instala por Brew para health/reproducibilidad |

Comando de restauracion:

```bash
nvim --headless "+Lazy load mason.nvim" \
  "+MasonInstall pyright ruff marksman markdownlint-cli2 markdown-toc java-debug-adapter java-test shellcheck debugpy stylua shfmt tree-sitter-cli" \
  +qa
```

No incluir `jdtls` en este comando. La excepcion esta documentada en
`DECISIONS.md` y `SETUP_LOG.md`.

## Mason vs Homebrew

| Herramienta | Gestor elegido | Motivo |
|---|---|---|
| `pyright` | Mason | Herramienta de Neovim/proyecto, facil de restaurar desde `:Mason`. |
| `ruff` | Mason | Integracion directa con extra Python. |
| `marksman` | Mason | Integracion Markdown desde Neovim. |
| `debugpy` | Mason | DAP Python ligado al editor. |
| `stylua` | Mason | Formatter de la config Lua. |
| `shellcheck` / `shfmt` | Mason | Utiles desde Neovim; pueden duplicarse con sistema si hace falta. |
| `tree-sitter-cli` | Homebrew + Mason | Homebrew satisface health/reproducibilidad; Mason lo usa internamente. |
| `jdtls` | Homebrew | Mason fallo con snapshot Eclipse; Brew entrega version estable. |

## Treesitter

Parsers precompilados en `~/.local/share/nvim/site/parser`:

```text
bash
c
diff
dtd
html
java
javascript
jsdoc
json
json5
lua
luadoc
luap
markdown
markdown_inline
ninja
printf
python
query
regex
rst
toml
tsx
typescript
vim
vimdoc
xml
yaml
```

Comando de restauracion:

```bash
nvim --headless "+lua require('nvim-treesitter.install').install({'lua','vim','vimdoc','markdown','markdown_inline','python','java','json','toml','yaml','bash'}, {summary = true, max_jobs = 2}):await()" +qa
```

LazyVim tambien instala parsers faltantes al abrir Neovim, pero precompilarlos
reduce friccion en una maquina nueva.

## Que no se versiona

No agregar al repo:

- `~/.local/share/nvim/lazy`
- `~/.local/share/nvim/mason`
- `~/.local/share/nvim/site/parser`
- `~/.local/state/nvim`
- `~/.cache/nvim`
- `.nvimlog`

La configuracion versiona instrucciones y lockfiles, no artefactos generados.
