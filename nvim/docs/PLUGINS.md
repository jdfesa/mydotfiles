# Plugins

Estado documentado el 2026-07-05.

Este documento responde tres preguntas:

- Que plugins estan instalados/habilitados.
- Que extras de LazyVim estan habilitados.
- Que cosas se decidio no instalar todavia.

En este documento, "activo" significa "declarado y habilitado por LazyVim". No
significa necesariamente "cargado al arranque": muchos plugins son lazy-loaded y
se cargan solo cuando se abre un tipo de archivo, se ejecuta un comando o se usa
un atajo.

## Fuente de verdad

La fuente de verdad de plugins es:

```text
nvim/lazy-lock.json
```

Ese archivo fija el commit usado por cada plugin. No se edita a mano: lo actualiza
`lazy.nvim` cuando se sincronizan o actualizan plugins.

Restauracion:

```bash
nvim --headless "+Lazy! sync" +qa
```

Exploracion interactiva:

```vim
:Lazy
```

## Extras activos

Los extras activos viven en:

```text
nvim/lua/plugins/extras.lua
```

Actualmente estan habilitados:

| Extra | Motivo |
|---|---|
| `lazyvim.plugins.extras.lang.markdown` | Notas diarias, documentacion y Markdown renderizado. |
| `lazyvim.plugins.extras.lang.python` | Python como lenguaje principal de programacion. |
| `lazyvim.plugins.extras.lang.java` | Soporte Java con LSP, debug/test base y Treesitter. |
| `lazyvim.plugins.extras.lang.json` | Configs, APIs y archivos de herramientas. |
| `lazyvim.plugins.extras.lang.toml` | Configs modernas como `pyproject.toml`. |
| `lazyvim.plugins.extras.lang.yaml` | Dotfiles, CI/CD y configuracion. |

Los extras se pueden explorar con:

```vim
:LazyExtras
```

Criterio actual: activar solo lenguajes y formatos que ya forman parte del uso
real o que son transversales al trabajo diario.

## Plugins instalados

Inventario observado desde `lazy-lock.json`: 37 plugins.

### Base de LazyVim

| Plugin | Rol | Comentario |
|---|---|---|
| `LazyVim` | Distro base | Provee defaults, estructura y extras. |
| `lazy.nvim` | Gestor de plugins | Instala, actualiza y usa `lazy-lock.json`. |
| `snacks.nvim` | UI/utilidades modernas | Picker, explorer, scratch, terminal y utilidades usadas por LazyVim. |
| `which-key.nvim` | Descubrimiento de atajos | Muestra menus al presionar `<leader>` y otras teclas. |
| `mini.icons` | Iconos | Requiere Nerd Font para verse bien. |
| `noice.nvim` | UI de mensajes/cmdline | Mejora mensajes, notificaciones y command line. |
| `nui.nvim` | Componentes UI | Dependencia usada por plugins de interfaz. |
| `lualine.nvim` | Statusline | Barra inferior de estado. |
| `bufferline.nvim` | Buffers/tabs visuales | Navegacion visual entre buffers. |
| `persistence.nvim` | Sesiones | Permite restaurar sesiones de trabajo. |

### Busqueda, navegacion y edicion

| Plugin | Rol | Comentario |
|---|---|---|
| `flash.nvim` | Saltos rapidos | Movimiento rapido dentro del buffer. |
| `grug-far.nvim` | Buscar/reemplazar | Reemplazos de texto en proyecto. |
| `todo-comments.nvim` | TODO/FIXME | Encuentra marcas de trabajo en comentarios. |
| `trouble.nvim` | Listas de diagnosticos | Vista estructurada de errores, quickfix y referencias. |
| `gitsigns.nvim` | Git en buffers | Hunk signs, blame y acciones Git por linea. |
| `mini.ai` | Text objects | Mejora objetos de texto para edicion modal. |
| `mini.pairs` | Autopairs | Cierre automatico de parentesis/comillas. |
| `ts-comments.nvim` | Comentarios por Treesitter | Mejor comentario segun contexto/lenguaje. |

### LSP, completion, formato y lint

| Plugin | Rol | Comentario |
|---|---|---|
| `nvim-lspconfig` | Configuracion LSP | Capa base para servidores de lenguaje. |
| `mason.nvim` | Instalador de herramientas | Instala LSP/DAP/linters/formatters dentro de Neovim. |
| `mason-lspconfig.nvim` | Puente Mason/LSP | Integra Mason con `nvim-lspconfig`. |
| `blink.cmp` | Completion | Motor de autocompletado usado por LazyVim. |
| `conform.nvim` | Formatting | Orquesta formatters por lenguaje. |
| `nvim-lint` | Linting | Orquesta linters externos. |
| `lazydev.nvim` | Lua para Neovim | Mejora LSP Lua dentro de configs Neovim. |

### Treesitter

| Plugin | Rol | Comentario |
|---|---|---|
| `nvim-treesitter` | Parsing semantico | Highlight, indent y soporte estructural por lenguaje. |
| `nvim-treesitter-textobjects` | Text objects semanticos | Seleccion/navegacion por funciones, clases, etc. |
| `nvim-ts-autotag` | Tags HTML/XML | Cierre/renombrado automatico de tags. |

### Markdown y notas

| Plugin | Rol | Comentario |
|---|---|---|
| `render-markdown.nvim` | Render Markdown en buffer | Hace mas legibles notas y docs sin salir de Neovim. |
| `markdown-preview.nvim` | Preview navegador | Preview HTML de Markdown cuando haga falta. |

### Lenguajes y esquemas

| Plugin | Rol | Comentario |
|---|---|---|
| `nvim-jdtls` | Java LSP avanzado | Integra Eclipse JDT LS con Neovim. |
| `venv-selector.nvim` | Python virtualenvs | Seleccion de entornos Python por proyecto. |
| `SchemaStore.nvim` | Schemas JSON/YAML | Mejora diagnosticos/autocomplete en configs. |
| `friendly-snippets` | Snippets | Coleccion base usada por completion. |

### Temas

| Plugin | Rol | Comentario |
|---|---|---|
| `tokyonight.nvim` | Tema actual | Seleccionado en `nvim/lua/plugins/core.lua`. |
| `catppuccin` | Tema disponible | Viene como opcion instalada, pero no es el tema activo. |

## Plugins no adoptados todavia

Estos no estan instalados a proposito, aunque podrian evaluarse mas adelante:

| Plugin/extra | Estado | Motivo |
|---|---|---|
| `obsidian.nvim` | No instalado | Primero se busca un flujo Markdown simple y portable. |
| Extras AI/Copilot/Claude | No instalados | Evitar dependencias de cuentas, tokens y workflows complejos al inicio. |
| Extras Go/Rust/TypeScript/Docker | No instalados | Se activaran cuando haya uso real o proyecto concreto. |
| Plugins de calendario/task management | No instalados | Todavia no hay criterio claro de flujo diario. |
| Plugins esteticos adicionales | No instalados | Mantener bajo el ruido visual y cognitivo mientras se aprende LazyVim. |

## Politica para agregar plugins

Antes de agregar un plugin nuevo, responder:

1. Que problema concreto resuelve.
2. Si LazyVim ya lo trae por defecto o mediante extra.
3. Si requiere binarios externos, cuentas, tokens o servicios.
4. Que atajos agrega y si chocan con AeroSpace, Hyper/Meh o `<leader>`.
5. Como se restaura en una maquina nueva.

Si pasa ese filtro:

- Plugins propios: crear/editar archivo en `nvim/lua/plugins/`.
- Lenguajes soportados por LazyVim: preferir extras en `nvim/lua/plugins/extras.lua`.
- Dependencias externas: declarar en `brew/10-essential/Brewfile` o documentar Mason.
- Decisiones no obvias: agregar nota en `DECISIONS.md`.

## Que no tocar

- No editar `~/.local/share/nvim/lazy/LazyVim` ni plugins descargados.
- No editar `lazy-lock.json` a mano.
- No versionar `~/.local/share/nvim/mason`.
- No agregar plugins solo porque aparecen en videos o dotfiles ajenos.
- No activar muchos extras de golpe: cada extra puede traer LSPs, formatters,
  atajos, Treesitter parsers y dependencias nuevas.
