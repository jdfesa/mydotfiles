# Arquitectura

Estado documentado el 2026-07-05.

Esta configuracion sigue la estructura recomendada por LazyVim: archivos de
configuracion en `lua/config/` y especificaciones de plugins en `lua/plugins/`.

## Arbol principal

```text
nvim/
|-- init.lua
|-- lazy-lock.json
|-- lua/
|   |-- config/
|   |   |-- autocmds.lua
|   |   |-- keymaps.lua
|   |   |-- lazy.lua
|   |   `-- options.lua
|   `-- plugins/
|       |-- core.lua
|       |-- extras.lua
|       |-- java.lua
|       `-- which-key.lua
`-- docs/
```

## Archivos y responsabilidades

| Archivo | Responsabilidad | Cuando tocarlo |
|---|---|---|
| `init.lua` | Punto de entrada | Casi nunca. |
| `lazy-lock.json` | Commits exactos de plugins | Nunca a mano; lo actualiza `lazy.nvim`. |
| `lua/config/lazy.lua` | Bootstrap de `lazy.nvim`, leader/localleader, defaults de Lazy | Solo para cambios estructurales del gestor. |
| `lua/config/options.lua` | Opciones globales de Neovim/LazyVim | Numeros, wrap, LSP Python, spelllang, etc. |
| `lua/config/keymaps.lua` | Atajos propios | Atajos personales que no vengan de LazyVim. |
| `lua/config/autocmds.lua` | Automatismos por evento/filetype | Reglas como wrap para Markdown/texto. |
| `lua/plugins/core.lua` | Ajustes base de plugins core | Tema, Mason base, overrides simples. |
| `lua/plugins/extras.lua` | Extras de LazyVim | Activar/desactivar lenguajes soportados por LazyVim. |
| `lua/plugins/java.lua` | Excepcion Java/JDTLS | Mantener `jdtls` por Homebrew, no Mason. |
| `lua/plugins/which-key.lua` | Grupos visuales de atajos | Etiquetas para grupos propios. |

## Capas de configuracion

### 1. LazyVim base

Se importa desde `lua/config/lazy.lua`:

```lua
{ "LazyVim/LazyVim", import = "lazyvim.plugins" }
```

Esto trae la experiencia base: plugins, defaults, atajos y estructura.

### 2. Plugins propios

Tambien desde `lua/config/lazy.lua`:

```lua
{ import = "plugins" }
```

Todo archivo dentro de `lua/plugins/` se carga como especificacion de plugins.

### 3. Config local

LazyVim carga automaticamente:

```text
lua/config/options.lua
lua/config/keymaps.lua
lua/config/autocmds.lua
```

No hace falta `require` manual para esos archivos.

## Directorios generados

Estos directorios son generados y no deben versionarse:

| Ruta | Contenido | Restauracion |
|---|---|---|
| `~/.local/share/nvim/lazy` | Plugins descargados por Lazy | `Lazy! sync` |
| `~/.local/share/nvim/mason` | LSPs, DAPs, linters, formatters | `MasonInstall ...` |
| `~/.local/share/nvim/site/parser` | Parsers Treesitter compilados | comando Treesitter en `RESTORE.md` |
| `~/.local/state/nvim` | Estado, shada, logs | se regenera |
| `~/.cache/nvim` | Cache | se regenera |

## Que tocar

- Para activar un lenguaje: `lua/plugins/extras.lua`.
- Para agregar un plugin manual: nuevo archivo en `lua/plugins/`.
- Para cambiar comportamiento del editor: `lua/config/options.lua`.
- Para nuevos atajos personales: `lua/config/keymaps.lua`.
- Para reglas por tipo de archivo: `lua/config/autocmds.lua`.
- Para dependencias de macOS:
  `os/macos/packages/homebrew/10-essential/Brewfile` y `DEPENDENCIES.md`.

## Que no tocar

- No editar archivos dentro de `~/.local/share/nvim/lazy/`.
- No editar `lazy-lock.json` manualmente.
- No instalar dependencias del sistema sin agregarlas al Brewfile.
- No agregar configuracion dentro de `~/.config/nvim` si no esta en este repo.
- No activar extras de LazyVim en masa sin documentar impacto.

## Criterio de cambios

Una modificacion de Neovim debe quedar completa en cuatro capas:

1. Codigo/configuracion en `nvim/`.
2. Dependencias externas declaradas.
3. Documento actualizado si afecta restauracion, atajos, plugins o decisiones.
4. Validacion minima ejecutada y anotada si el cambio es sensible.
