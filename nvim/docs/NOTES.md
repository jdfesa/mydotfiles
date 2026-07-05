# Notas

Estado documentado el 2026-07-05.

Objetivo: usar Neovim para notas diarias sin acoplar la configuracion a un
workflow complejo desde el primer dia.

## Vault

Ruta actual:

```text
~/Documents/ObsidianVault
```

Esta ruta se expande desde:

```text
nvim/lua/config/keymaps.lua
```

Si en otra maquina el vault vive en otro lugar, hay tres opciones:

1. Recrear la misma ruta.
2. Crear un symlink desde esa ruta al vault real.
3. Cambiar `notes_dir` en `keymaps.lua` y documentarlo aqui.

## Atajos

| Atajo | Accion |
|---|---|
| `<leader>Nf` | Buscar archivos dentro del vault. |
| `<leader>Ng` | Buscar texto dentro del vault. |
| `<leader>Nd` | Abrir/crear nota diaria. |

Las notas diarias se crean en:

```text
~/Documents/ObsidianVault/daily/YYYY-MM-DD.md
```

## Markdown activo

La capa Markdown viene del extra:

```lua
{ import = "lazyvim.plugins.extras.lang.markdown" }
```

Herramientas relacionadas:

| Herramienta | Capa | Uso |
|---|---|---|
| `render-markdown.nvim` | Plugin Lazy | Render visual dentro del buffer. |
| `markdown-preview.nvim` | Plugin Lazy | Preview HTML cuando haga falta. |
| `marksman` | Mason | LSP Markdown. |
| `markdownlint-cli2` | Mason | Lint Markdown. |
| `markdown-toc` | Mason | Tabla de contenidos. |
| `markdown` / `markdown_inline` | Treesitter | Parsing y highlight Markdown. |

## Comportamiento para prosa

Configurado en:

```text
nvim/lua/config/autocmds.lua
```

Para `markdown`, `text` y `gitcommit`:

- `wrap = true`
- `linebreak = true`
- `conceallevel = 2`

Motivo: codigo y prosa necesitan ergonomias distintas. En codigo se prefiere no
wrap global; en notas se prefiere lectura comoda.

## Por que no `obsidian.nvim` todavia

No se instalo `obsidian.nvim` por ahora.

Motivos:

- Primero conviene dominar LazyVim, buffers, pickers, LSP y Markdown base.
- El vault debe seguir siendo portable y editable fuera de Neovim.
- Agregar una capa Obsidian implica nuevos comandos, atajos y convenciones.
- Todavia no hay una decision estable sobre plantillas, tags, daily notes,
  backlinks o gestion de tareas.

Cuando tenga sentido evaluarlo, criterios:

- Debe mejorar el flujo real, no solo verse interesante.
- Debe convivir con Obsidian sin romper Markdown plano.
- Debe documentarse en `PLUGINS.md`, `KEYMAPS.md` y este archivo.

## Pendientes posibles

- Plantilla para nota diaria.
- Ruta configurable por variable de entorno.
- Soporte reproducible para spellcheck en espanol.
- Evaluar backlinks/tags despues de usar el flujo base varias semanas.
