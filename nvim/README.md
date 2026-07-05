# Neovim

Configuracion principal de Neovim basada en LazyVim.

## Intencion

Esta config busca reemplazar gradualmente VS Code/Obsidian para tareas diarias sin pelearse con el resto del sistema:

- `Hyper` y `Meh` quedan para AeroSpace, terminal y ventanas.
- `Space` queda como leader dentro de Neovim.
- `,` queda como localleader, igual que en la config AstroNvim anterior.

## Extras activos

- `lazyvim.plugins.extras.lang.markdown`: notas Markdown, preview y render.
- `lazyvim.plugins.extras.lang.python`: Pyright, Ruff y selector de virtualenv.
- `lazyvim.plugins.extras.lang.java`: jdtls, Java debug adapter y Java test.
- `lazyvim.plugins.extras.lang.json`
- `lazyvim.plugins.extras.lang.toml`
- `lazyvim.plugins.extras.lang.yaml`

Java usa `jdtls` desde Homebrew (`/usr/local/bin/jdtls`). No se usa el paquete `jdtls` de Mason porque el snapshot de Eclipse puede fallar al descargarse desde Mason.

El spellcheck queda en ingles por ahora para evitar warnings de diccionario faltante. El diccionario espanol se puede agregar despues si se quiere revisar notas desde Neovim.

## Atajos propios

Los atajos base son los de LazyVim. Los propios empiezan con `Space N`:

| Atajo | Accion |
|---|---|
| `Space N f` | Buscar archivos en `/Users/jd/Documents/ObsidianVault` |
| `Space N g` | Buscar texto en `/Users/jd/Documents/ObsidianVault` |
| `Space N d` | Abrir/crear nota diaria en `daily/YYYY-MM-DD.md` |

## Atajos base a aprender primero

| Atajo | Accion |
|---|---|
| `Space Space` | Buscar archivos del proyecto |
| `Space /` | Buscar texto en el proyecto |
| `Space ,` | Cambiar buffer |
| `Space e` | Explorador |
| `Space l` | Lazy plugin manager |
| `Space c a` | Code action |
| `Space c f` | Formatear |
| `g d` | Ir a definicion |
| `g r` | Referencias |
| `K` | Documentacion/hover |

## Mantenimiento

Despues de instalar o cambiar plugins:

```bash
nvim --headless "+Lazy! sync" +qa
```

Dentro de Neovim:

```vim
:checkhealth
:Mason
```

## Symlink esperado

```bash
~/.config/nvim -> ~/mydotfiles/nvim
```

## Documentacion operativa

La documentacion detallada vive en `docs/`. Esta carpeta explica que se instalo,
por que se instalo, que plugins estan activos, que atajos son propios y como
restaurar la config en otra maquina.

- [docs/RESTORE.md](docs/RESTORE.md): restaurar esta config en otra maquina.
- [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md): dependencias del sistema, Mason, Treesitter y plugins.
- [docs/PLUGINS.md](docs/PLUGINS.md): plugins activos y decisiones de adopcion.
- [docs/KEYMAPS.md](docs/KEYMAPS.md): mapa mental de teclado y atajos propios.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): que tocar y que no tocar.
- [docs/NOTES.md](docs/NOTES.md): flujo de notas y Markdown.
- [docs/DECISIONS.md](docs/DECISIONS.md): decisiones tomadas y tradeoffs.
- [docs/OPERATIONS.md](docs/OPERATIONS.md): mantenimiento, validacion y troubleshooting.
- [docs/SETUP_LOG.md](docs/SETUP_LOG.md): bitacora de instalacion/migracion.
- [docs/SOURCES.md](docs/SOURCES.md): fuentes oficiales consultadas.
