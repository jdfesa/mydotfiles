# Neovim Docs

Documentacion operativa para reproducir, entender y mantener la configuracion de
Neovim/LazyVim dentro de estos dotfiles.

Esta carpeta existe para que el `README.md` de la herramienta sea corto y el
conocimiento importante quede separado por tema. La idea no es recordar comandos
de memoria: la idea es que una maquina nueva pueda quedar funcional en pocos
minutos y que tu yo futuro sepa que tocar, que no tocar y por que.

## Mapa de documentos

1. [RESTORE.md](RESTORE.md): pasos para levantar la config en otra maquina.
2. [DEPENDENCIES.md](DEPENDENCIES.md): dependencias de sistema, Lazy, Mason y Treesitter.
3. [PLUGINS.md](PLUGINS.md): plugins activos, extras habilitados y plugins no adoptados.
4. [KEYMAPS.md](KEYMAPS.md): modelo mental de teclado y atajos propios.
5. [ARCHITECTURE.md](ARCHITECTURE.md): estructura de archivos y limites de edicion.
6. [NOTES.md](NOTES.md): flujo de notas diarias y Markdown.
7. [DECISIONS.md](DECISIONS.md): decisiones tomadas y motivos.
8. [OPERATIONS.md](OPERATIONS.md): mantenimiento, validacion y troubleshooting.
9. [SETUP_LOG.md](SETUP_LOG.md): bitacora de lo que se toco en esta instalacion.
10. [SOURCES.md](SOURCES.md): fuentes oficiales consultadas.

## Regla de oro

Todo lo que se instale fuera del repo debe quedar declarado en alguna capa
documentada:

- Homebrew/Brewfile para binarios del sistema.
- `nvim/lazy-lock.json` para plugins instalados por `lazy.nvim`.
- `nvim/docs/DEPENDENCIES.md` para paquetes descargados por Mason y parsers de Treesitter.
- `nvim/docs/SETUP_LOG.md` para acciones manuales hechas durante una migracion.
- README o docs de la herramienta si hay symlinks, rutas, decisiones o pasos manuales.

## Contrato de reproducibilidad

Una config es reproducible cuando cumple estas condiciones:

- El repo contiene la configuracion declarativa.
- El gestor del sistema declara los binarios externos.
- Los gestores internos de Neovim tienen comandos claros de restauracion.
- Los directorios generados quedan fuera de Git y se pueden reconstruir.
- Las excepciones estan escritas con fecha y motivo.

En esta configuracion, el contrato queda asi:

| Capa | Donde vive | Se versiona | Como se restaura |
|---|---|---|---|
| Config Neovim | `nvim/` | Si | symlink a `~/.config/nvim` |
| Plugins Lazy | `nvim/lazy-lock.json` | Si | `nvim --headless "+Lazy! sync" +qa` |
| Binarios macOS | `os/macos/packages/homebrew/10-essential/Brewfile` | Si | `brew bundle --file ...` |
| Mason | `~/.local/share/nvim/mason` | No | `:MasonInstall ...` |
| Treesitter parsers | `~/.local/share/nvim/site/parser` | No | comando documentado en `RESTORE.md` |
| Cache/estado | `~/.cache/nvim`, `~/.local/state/nvim` | No | se regenera |
