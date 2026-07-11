# AeroSpace

Configuracion personal de [AeroSpace](https://github.com/nikitabobko/AeroSpace) para macOS.

> **Fase actual: 2 - Navegacion + Ajuste**
>
> Esta configuracion esta pensada para adopcion incremental: primero navegar, despues mover, despues ajustar, despues automatizar.

## Principios

- `Hyper` (`cmd-ctrl-alt-shift`) = navegar, mirar, cambiar foco.
- `Meh` (`ctrl-alt-shift`) = actuar, mover, enviar, entrar a modos.
- Workspaces por letras, no por numeros.
- La configuracion es personal, pero la estructura del repo debe ser clara y mantenible.
- Cada cambio funcional en [aerospace.toml](aerospace.toml) debe actualizar la documentacion correspondiente en el mismo cambio.

## Documentacion

| Documento | Para que sirve |
|---|---|
| [CONCEPTS.md](CONCEPTS.md) | Modelo mental: workspaces, arbol, layouts, modos, Sketchybar |
| [KEYBINDINGS.md](KEYBINDINGS.md) | Chuleta completa de atajos y modos |
| [WORKSPACES.md](WORKSPACES.md) | Mnemotecnia, ergonomia del Silakka54 y ruteo de apps |
| [SCRIPTS.md](SCRIPTS.md) | Scripts usados por AeroSpace y Sketchybar |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Problemas comunes, sintomas y soluciones |
| [ROADMAP.md](ROADMAP.md) | Fases, pendientes y criterios para agregar features |

## Uso Diario

### Workspaces

| Atajo | Accion |
|---|---|
| `Hyper + U/I/O/P/Y/N` | Ir al workspace |
| `Meh + U/I/O/P/Y/N` | Enviar ventana al workspace |
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

| Workspace | Mnemotecnia | Uso |
|---|---|---|
| `U` | Universe | Dev, terminal, trabajo activo |
| `I` | Internet | Browser y referencias |
| `O` | Organize | Notas, escritura, documentos |
| `P` | People / Planning | Comunicacion y calendario |
| `Y` | Yield | Musica y video |
| `N` | Navigate | Finder, sistema y utilidades |

El detalle de apps y bundle IDs esta en [WORKSPACES.md](WORKSPACES.md).

## Archivos

| Archivo | Descripcion |
|---|---|
| [aerospace.toml](aerospace.toml) | Configuracion activa |
| [scripts/update_sketchybar_workspace.sh](scripts/update_sketchybar_workspace.sh) | Actualiza el workspace activo en Sketchybar |
| [scripts/update_mode_indicator.sh](scripts/update_mode_indicator.sh) | Muestra `[S]`, `[R]` u oculta el modo |
| [scripts/borders_mode.sh](scripts/borders_mode.sh) | Actualiza el color del borde activo por modo |

## Recargar y Validar

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
