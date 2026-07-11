# Fuentes

Fuentes consultadas el 2026-07-05.

Este archivo existe para separar referencias externas de las decisiones locales.
Las decisiones finales viven en `DECISIONS.md`; los comandos reproducibles viven
en `RESTORE.md` y `OPERATIONS.md`.

## LazyVim

- Instalacion oficial: https://www.lazyvim.org/installation
- Keymaps oficiales: https://www.lazyvim.org/keymaps
- Estructura de configuracion: https://www.lazyvim.org/configuration
- Extras: https://www.lazyvim.org/extras
- Python extra: https://www.lazyvim.org/extras/lang/python
- Java extra: https://www.lazyvim.org/extras/lang/java
- Markdown extra: https://www.lazyvim.org/extras/lang/markdown
- JSON extra: https://www.lazyvim.org/extras/lang/json
- TOML extra: https://www.lazyvim.org/extras/lang/toml
- YAML extra: https://www.lazyvim.org/extras/lang/yaml

Notas relevantes:

- LazyVim recomienda usar su starter, quitar `.git` si se va a versionar en un
  repo propio y ejecutar health despues de instalar.
- LazyVim documenta `<leader>` por defecto como `<space>` y usa `which-key.nvim`
  para descubrir atajos.
- LazyVim carga automaticamente archivos bajo `lua/config/` y specs bajo
  `lua/plugins/`.

## AstroNvim

- Gestion de configuracion de usuario: https://docs.astronvim.com/configuration/manage_user_config/
- Mappings oficiales: https://docs.astronvim.com/mappings

Notas relevantes:

- AstroNvim tambien usa `lazy.nvim` como gestor.
- AstroNvim documenta una filosofia de mappings orientados a `<Leader>`.
- AstroNvim documenta `Space` como leader y `,` como localleader.

## Mason

- `mason.nvim`: https://github.com/mason-org/mason.nvim

Notas relevantes:

- Mason es un gestor portable para instalar y administrar LSP servers, DAP
  servers, linters y formatters dentro del entorno de Neovim.
- En esta config Mason se usa para herramientas de Python, Markdown, shell, Lua,
  debug y soporte auxiliar; no se usa para instalar `jdtls`.

## Treesitter

- `nvim-treesitter`: https://github.com/nvim-treesitter/nvim-treesitter

Notas relevantes:

- `nvim-treesitter` administra parsers por lenguaje.
- Los parsers compilados son artefactos generados y se restauran, no se versionan.

## Java

- `nvim-jdtls`: https://github.com/mfussenegger/nvim-jdtls
- Homebrew `jdtls`: https://formulae.brew.sh/formula/jdtls
- Eclipse JDT LS: https://github.com/eclipse-jdtls/eclipse.jdt.ls

Notas relevantes:

- `nvim-jdtls` espera un servidor Eclipse JDT LS instalado y un ejecutable
  `jdtls` disponible.
- Homebrew provee `brew install jdtls`.
- El 2026-07-05 Homebrew listaba `jdtls` estable `1.60.0`.

## Neovim

- Documentacion principal: https://neovim.io/doc/
- `mapleader`: https://neovim.io/doc/user/map.html#mapleader
- Base directories / `stdpath`: https://neovim.io/doc/user/starting.html#base-directories

Notas relevantes:

- Neovim separa configuracion, data, state y cache mediante rutas estandar.
- Esta config versiona solo la configuracion y reconstruye data/cache/state.
