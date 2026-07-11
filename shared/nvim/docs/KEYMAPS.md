# Keymaps

Estado documentado el 2026-07-05.

Este documento separa el teclado en capas. La separacion importa porque el
objetivo es que Neovim sea editor principal sin pelearse con AeroSpace, la
terminal ni el sistema operativo.

## Modelo mental

| Capa | Teclas | Dueno | Uso |
|---|---|---|---|
| Sistema operativo | Hyper / Meh | macOS, Karabiner, AeroSpace | Ventanas, espacios, apps, terminal. |
| Neovim global | `<leader>` = `Space` | LazyVim + esta config | Acciones del editor y plugins. |
| Neovim local | `<localleader>` = `,` | Esta config | Acciones locales por lenguaje/proyecto. |
| Modo normal Vim | `g`, `z`, `[`, `]`, etc. | Vim/Neovim | Movimientos y operadores base. |

Decision importante: `Space` queda reservado para Neovim. Hyper/Meh quedan para
el sistema. Esto evita un mapa mental mezclado y hace mas facil migrar a Linux.

## Leader y localleader

Configurado en:

```text
shared/nvim/lua/config/lazy.lua
```

Valores actuales:

```lua
vim.g.mapleader = " "
vim.g.maplocalleader = ","
```

LazyVim usa `<leader>` como capa principal. Su documentacion indica que el leader
por defecto es `<space>` y que usa `which-key.nvim` para descubrir combinaciones.
AstroNvim tambien usa una filosofia orientada a leader y documenta `Space` como
leader y `,` como localleader. Por eso la idea general se parece, pero los atajos
exactos entre distros no son identicos.

## Como aprender los atajos

No memorizar listas largas al inicio. Usar `which-key`:

1. Abrir Neovim.
2. Presionar `Space`.
3. Esperar el menu.
4. Seguir por categoria: `f` para files, `s` para search, `g` para Git, `c` para code, etc.

Comandos utiles:

```vim
:Lazy
:Mason
:checkhealth
```

Atajos LazyVim utiles para empezar:

| Atajo | Uso |
|---|---|
| `<leader><space>` | Buscar archivos en el root. |
| `<leader>/` | Grep/busqueda de texto en el root. |
| `<leader>,` | Buffers abiertos. |
| `<leader>e` | Explorer en root. |
| `<leader>ff` | Buscar archivos. |
| `<leader>sg` | Grep en root. |
| `<leader>sk` | Buscar keymaps. |
| `<leader>cm` | Mason. |
| `<leader>l` | Lazy. |
| `<leader>cf` | Formatear. |
| `<leader>ca` | Code action. |
| `gd` | Ir a definicion. |
| `gr` | Referencias. |
| `K` | Hover/documentacion. |

## Atajos propios

Configurados en:

```text
shared/nvim/lua/config/keymaps.lua
```

Grupo visual agregado a `which-key`:

```text
<leader>N -> notes
```

Atajos:

| Atajo | Accion | Detalle |
|---|---|---|
| `<leader>Nf` | Buscar notas | Usa Snacks picker con `cwd` en el vault. |
| `<leader>Ng` | Buscar texto en notas | Grep dentro del vault. |
| `<leader>Nd` | Nota diaria | Abre/crea `daily/YYYY-MM-DD.md`. |

Ruta actual del vault:

```text
~/Documents/ObsidianVault
```

Si el vault no existe, el atajo no rompe el editor: muestra una notificacion.

## Convenciones para nuevos atajos

- Mantener notas bajo `<leader>N`.
- Usar `<leader>c` para acciones de codigo solo si siguen la semantica LazyVim.
- Usar `<leader>s` para busquedas solo si son busquedas.
- Evitar atajos con Hyper/Meh dentro de Neovim.
- Antes de crear un atajo, revisar `<leader>sk` para evitar colisiones.
- Si un atajo es de un plugin nuevo, documentarlo en este archivo y en `PLUGINS.md`.

## Que no tocar

- No redefinir leader/localleader sin actualizar este documento.
- No copiar mapas completos de otra distro.
- No reemplazar atajos base de Vim mientras se esta aprendiendo el flujo modal.
- No usar combinaciones que ya pertenecen a AeroSpace o al sistema operativo.
