# Setup Log

Bitacora de instalacion y migracion.

## 2026-07-05

### Contexto

- Maquina actual: macOS/Hackintosh.
- Repo de dotfiles: `~/mydotfiles`.
- Config previa de Neovim: AstroNvim v5 practicamente sin personalizacion.
- Decision del usuario: no era necesario respaldar la config anterior de Neovim.

### Acciones realizadas

1. Se inspecciono la config existente en `~/.config/nvim`.
2. Se confirmo que la config AstroNvim era mayormente plantilla base.
3. Se clono el starter oficial de LazyVim en un directorio temporal.
4. Se copio el starter a:

```text
~/mydotfiles/shared/nvim
```

5. Se elimino `.git` del starter para versionarlo dentro de este repo.
6. Se reemplazo `~/.config/nvim` por symlink a:

```text
~/mydotfiles/shared/nvim
```

7. Se limpiaron datos/caches previos de Neovim:

```text
~/.local/share/nvim
~/.local/state/nvim
~/.cache/nvim
```

8. Se sincronizaron plugins con `Lazy! sync`.
9. Se instalaron paquetes Mason necesarios.
10. Se instalaron dependencias Homebrew adicionales.
11. Se valido arranque, health, LSP Java, LSP Python y Markdown.
12. Se agrego documentacion operativa en `shared/nvim/docs`.

### Dependencias Homebrew agregadas

Se agregaron al Brewfile:

```ruby
brew "wget"
brew "jdtls"
```

Motivo:

- `wget`: algunos instaladores de Mason lo necesitan para descargar artefactos.
- `jdtls`: se usa Homebrew como fuente estable para Java LSP.

### Problema encontrado con Mason/JDTLS

Mason intento instalar `jdtls` desde un snapshot de Eclipse.

Observacion del dia:

- `HEAD` respondia correctamente.
- `GET` devolvia `500 Internal Server Error`.
- Homebrew tenia `jdtls 1.60.0` disponible.

Decision:

- No instalar `jdtls` con Mason.
- Instalar `jdtls` con Homebrew.
- Configurar LazyVim para usar `vim.fn.exepath("jdtls")`.

Archivo relacionado:

```text
shared/nvim/lua/plugins/java.lua
```

### Validaciones ejecutadas

Arranque:

```bash
nvim --headless "+lua print('final ok')" +qa
```

Health:

```bash
nvim --headless "+checkhealth lazy lazyvim vim.lsp" "+write! /tmp/nvim-health.txt" +qa
```

Java:

```text
lsp client jdtls
```

Python:

```text
lsp client pyright
lsp client ruff
```

Markdown:

```text
lsp client marksman
wrap true
```

### Estado funcional

- LazyVim arranca.
- Plugins sincronizados.
- `checkhealth lazy lazyvim vim.lsp` sin errores bloqueantes.
- Java usa `jdtls` del sistema.
- Python usa `pyright` y `ruff`.
- Markdown usa `marksman` y wrap local.
- Treesitter tiene parsers base compilados.

### Hallazgos no relacionados directamente

El comando `jq` disponible en la shell fallo por una dependencia Node faltante
(`async`). No se usa para esta configuracion de Neovim, pero conviene revisarlo
en otra tarea si `jq` forma parte del flujo diario.
