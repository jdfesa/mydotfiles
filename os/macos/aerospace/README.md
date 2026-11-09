# AeroSpace

Configuracion personal de [AeroSpace](https://github.com/nikitabobko/AeroSpace) para macOS.

> **Fase actual: 2 - Navegacion + Ajuste**
>
> Esta configuracion esta pensada para adopcion incremental: primero navegar, despues mover, despues ajustar, despues automatizar.

## Principios

- `Hyper` (`cmd-ctrl-alt-shift`) = navegar, mirar, cambiar foco.
- `Meh` (`ctrl-alt-shift`) = actuar, mover, enviar, entrar a modos.
- Cinco workspaces numéricos (`1`–`5`) con distribución en prueba, revisable según el uso diario.
- La configuracion es personal, pero la estructura del repo debe ser clara y mantenible.
- Cada cambio funcional en [aerospace.toml](aerospace.toml) debe actualizar la documentacion correspondiente en el mismo cambio.

## Documentacion

| Documento | Para que sirve |
|---|---|
| [CONCEPTS.md](CONCEPTS.md) | Modelo mental: workspaces, arbol, layouts, modos, Sketchybar |
| [KEYBINDINGS.md](KEYBINDINGS.md) | Chuleta completa de atajos y modos |
| [WORKSPACES.md](WORKSPACES.md) | Distribución numérica en prueba, ruteo de apps y migración |
| [SCRIPTS.md](SCRIPTS.md) | Scripts usados por AeroSpace y Sketchybar |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Problemas comunes, sintomas y soluciones |
| [ROADMAP.md](ROADMAP.md) | Fases, pendientes y criterios para agregar features |

## Uso Diario

### Terminal

| Atajo | Accion |
|---|---|
| `Cmd + Enter` | Abrir una nueva instancia/ventana de Kitty (equivalente a `Super + Enter` de Omarchy) |

El launcher funciona en `main` y toma precedencia sobre el atajo interno de Kitty para crear paneles. Usa `open -n -a kitty` para abrir una nueva instancia con su ventana en cada pulsacion, incluso si Kitty ya esta abierto.

### Workspaces

| Atajo | Accion |
|---|---|
| `Hyper + 1/2/3/4/5` | Ir al workspace |
| `Meh + 1/2/3/4/5` | Enviar ventana al workspace |
| `Hyper + Tab` | Volver al workspace anterior |

### Ventanas

| Atajo | Accion |
|---|---|
| `Hyper + H/J/K/L` | Cambiar foco |
| `Meh + H/J/K/L` | Mover ventana |
| `Hyper + A` | Alternar `tiles` / `accordion` |
| `Hyper + F` | Toggle fullscreen |
| `Meh + B` | Forzar `tiles` horizontales y balancear tamanos |
| `Meh + F` | Toggle floating / tiling de la ventana enfocada |

### Modos

| Secuencia | Accion |
|---|---|
| `Meh + M` | Entrar a resize mode (`[R]`) |
| `Meh + ;` | Entrar a service mode (`[S]`) |
| `Enter` / `Esc` | Salir del modo activo |

Los modos tambien cambian el color del borde activo: azul en normal, rojo en resize y rosa en service.

En resize mode:

| Tecla | Accion |
|---|---|
| `H` / `L` | Achicar / agrandar ancho |
| `K` / `J` | Achicar / agrandar alto |
| `B` | Balancear tamanos |

## Workspaces

| Workspace | Uso en prueba |
|---|---|
| `1` | Navegadores y referencias web |
| `2` | Trabajo y terminales |
| `3` | Notas y documentos |
| `4` | Finder y utilidades |
| `5` | Calendario, comunicación y multimedia |

El detalle de apps y bundle IDs esta en [WORKSPACES.md](WORKSPACES.md).

## Archivos

| Archivo | Descripcion |
|---|---|
| [aerospace.toml](aerospace.toml) | Configuracion activa |
| [scripts/update_sketchybar_workspace.sh](scripts/update_sketchybar_workspace.sh) | Actualiza el workspace activo en Sketchybar |
| [scripts/update_mode_indicator.sh](scripts/update_mode_indicator.sh) | Muestra `[S]`, `[R]` u oculta el modo |
| [scripts/borders_mode.sh](scripts/borders_mode.sh) | Actualiza el color del borde activo por modo |

## Reload and Validate

La distribución es experimental. Cambiar la fuente no acredita recarga ni
validación del uso real. Antes de aplicar, seguir la
[migración de ventanas y barra](WORKSPACES.md#migration-and-verification).

Pruebas aisladas (Python 3.11+, Bash y Lua 5.4):

```bash
python3 os/macos/aerospace/scripts/test-workspaces.py
lua os/macos/sketchybar/tests/test-aerospace.lua
```

Validar sin aplicar:

```bash
aerospace reload-config --dry-run --no-gui
```

Recargar desde terminal:

```bash
aerospace reload-config --no-gui
```

Recargar desde teclado:

```text
Meh + ; -> Esc
```

## Instalacion

La carpeta `aerospace/` debe estar enlazada como configuracion de AeroSpace:

```bash
ln -s ~/mydotfiles/os/macos/aerospace ~/.config/aerospace
```

AeroSpace busca la config en:

```text
~/.config/aerospace/aerospace.toml
```

## Referencias

- [AeroSpace Guide](https://nikitabobko.github.io/AeroSpace/guide)
- [AeroSpace Commands](https://nikitabobko.github.io/AeroSpace/commands)
- [AeroSpace Goodies](https://nikitabobko.github.io/AeroSpace/goodies)
- [Configuracion del Silakka54](../../../hardware/silakka54/README.md)
