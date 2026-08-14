# mydotfiles

[![Lint](https://github.com/jdfesa/mydotfiles/actions/workflows/lint.yml/badge.svg)](https://github.com/jdfesa/mydotfiles/actions/workflows/lint.yml)

Repositorio central de configuraciones reproducibles para macOS, GNU/Linux y
Windows. Los archivos versionados son la fuente de verdad y se despliegan en las
rutas esperadas por cada aplicacion mediante symlinks.

> Una fuente de verdad para reconstruir el entorno, entender por que existe cada
> configuracion y detectar enlaces rotos antes de que se conviertan en problemas.

## Quick Access

| Necesidad | Documento o comando |
|---|---|
| Restaurar la Mac desde cero | [Restore macOS](docs/RESTORE.md) |
| Entender la estructura | [Dotfiles Architecture](docs/ARCHITECTURE.md) |
| Entender produccion y canary | [Workstation Lifecycle](docs/WORKSTATION_LIFECYCLE.md) |
| Consultar decisiones | [Architecture Decision Records](docs/adr/README.md) |
| Evaluar dotfiles externos | [External References](references/README.md) |
| Ver los enlaces de macOS | [`profiles/macos-main.links`](profiles/macos-main.links) |
| Diagnosticar los symlinks | `scripts/doctor macos-main` |
| Probar Hyprland en Arch | `scripts/doctor arch-hyprland-preview` |

## Platform Status

| Plataforma | Estado |
|---|---|
| macOS | Produccion: 16 symlinks declarados; no se modifica durante experimentos |
| Arch Linux | Canary: Hyprland/Wayland activo, XFCE X11 y XRDP de recuperacion |
| Windows | Planificada; sin perfil activo todavia |

## Conventions

- Nombres de carpetas, archivos tecnicos y titulos en ingles.
- Contenido explicativo en espanol.
- Ruta canonica del clon: `~/mydotfiles`.
- Rutas portables basadas en `$HOME`, `~` o XDG.
- Una sola fuente canonica por herramienta.
- Secretos, tokens, claves privadas, caches y builds fuera de Git.
- Cada configuracion activa tiene un README y un destino declarado por perfil.
- Las configuraciones importadas no se activan hasta adaptar rutas y dependencias.
- Las fuentes externas se estudian bajo `references/` y nunca se despliegan.

## Repository Layout

```text
mydotfiles/
  shared/                    # herramientas y configuraciones compartidas
    scripts/                 # utilidades portables de uso personal
  os/
    macos/                   # AeroSpace, Sketchybar, Hammerspoon, Borders
      packages/homebrew/     # manifiestos de Homebrew
    linux/                   # DWM, display managers, X11 y paquetes de Linux
    windows/                 # configuracion nativa futura
  profiles/                  # roles instalables y capas de composicion
  hosts/                     # inventario y riesgo de maquinas fisicas
  hardware/                  # teclados y otros perifericos
  references/                # fuentes externas: evidencia, no runtime
  scripts/                   # bootstrap, linking y diagnostico
  docs/                      # arquitectura, ADR e inventarios
```

Las configuraciones compartidas viven bajo `shared/<tool>/`; los scripts
portables se agrupan en `shared/scripts/<name>/`. La raiz queda reservada para
categorias estables.

## Placement Rules

| Tipo | Ubicacion | Ejemplos |
|---|---|---|
| Compartido | `shared/<tool>/` | Kitty, Neovim, Starship, Yazi |
| Script portable | `shared/scripts/<name>/` | CPU Watch y futuras utilidades personales |
| Solo macOS | `os/macos/<tool>/` | AeroSpace, Sketchybar, Hammerspoon |
| Solo Linux | `os/linux/<tool>/` | DWM, i3, X11, Wayland |
| Solo Windows | `os/windows/<tool>/` | PowerShell, Windows Terminal |
| Rol instalable | `profiles/<role>.links` | `arch-workstation`, `arch-hyprland` |
| Fragmento de perfil | `profiles/layers/` | terminal compartida, Wayland, DWM/X11 |
| Maquina concreta | `hosts/<id>/` y `docs/machines/` | inventario, riesgo y notas operativas |
| Periferico | `hardware/<device>/` | Silakka54 |
| Fuente externa | `references/<category>/` | Dossiers y clones temporales ignorados |

DWM comienza en `os/linux/dwm/`; Hyprland en `os/linux/hyprland/`; la
infraestructura transversal permanece separada en `os/linux/x11/` y
`os/linux/wayland/`. Los perfiles combinan esas fuentes sin confundirlas con el
hardware de un host.

`references/` es una zona de estudio no desplegable. Un clon externo permanece
ignorado en `references/inbox/`; las decisiones y evidencia se registran en un
dossier. Solo una adaptacion comprendida y probada puede entrar luego a una
ubicacion canonica activa.

`main-workstation` es el Hackintosh de produccion. `lab-desktop-01`, cuyo
hostname actual es `arch-desktop`, es el canary donde se califican Arch y
Hyprland antes de cualquier adopcion futura.

## Active macOS Layer

- [AeroSpace](os/macos/aerospace/README.md)
- [Sketchybar](os/macos/sketchybar/README.md)
- [Hammerspoon](os/macos/hammerspoon/README.md)
- JankyBorders: `os/macos/borders/`
- [Homebrew](os/macos/packages/homebrew/README.md)

Las herramientas compartidas activas incluyen Kitty, Ghostty, Neovim, Zsh,
Starship, VS Code, Btop, Yazi, Lazygit, Gh Dash, Sesh, Fastfetch, RTK y Engram.
Todas viven bajo `shared/`.

## Symlink Workflow

Los enlaces se declaran en perfiles que pueden incluir fragmentos de
`profiles/layers/`. El perfil actual de la Mac principal sigue siendo
`profiles/macos-main.links` y esta refactorizacion no lo aplica ni modifica en
el sistema real.

Validar el grafo sin tocar `$HOME`:

```sh
scripts/validate-profiles
scripts/profile-resolve arch-hyprland
```

Comprobar el estado sin modificar nada:

```sh
cd ~/mydotfiles
scripts/doctor macos-main
```

Previsualizar cambios:

```sh
scripts/link --dry-run --repair macos-main
```

Crear enlaces ausentes o reparar symlinks que apuntan a ubicaciones antiguas:

```sh
scripts/link --repair macos-main
```

El linker nunca sobrescribe automaticamente un archivo o directorio real. Si un
destino ya existe y no es un symlink, se detiene para permitir una revision y un
respaldo manual.

## Restore macOS

La guia completa, incluidos paquetes, archivos locales, permisos y validacion,
esta en [Restore macOS](docs/RESTORE.md).

```sh
git clone https://github.com/jdfesa/mydotfiles.git ~/mydotfiles
cd ~/mydotfiles
brew bundle --file os/macos/packages/homebrew/00-base/Brewfile
brew bundle --file os/macos/packages/homebrew/10-essential/Brewfile
scripts/link --dry-run macos-main
scripts/link macos-main
scripts/doctor macos-main
```

Los archivos locales ignorados, por ejemplo `shared/zsh/local.zsh`, se crean
desde su correspondiente ejemplo y nunca deben contener secretos versionados.

## Safe Migration

Para mover una configuracion activa:

1. Registrar su enlace actual en el perfil.
2. Ejecutar `scripts/doctor <profile>` y obtener cero errores.
3. Mover la fuente a su ubicacion canonica.
4. Actualizar rutas internas y documentacion.
5. Actualizar el origen en el perfil.
6. Ejecutar `scripts/link --dry-run --repair <profile>`.
7. Reparar los enlaces y volver a ejecutar `scripts/doctor <profile>`.
8. Validar la aplicacion afectada antes de migrar la siguiente.

No se borran configuraciones o scripts encontrados en una maquina remota antes
de leerlos, clasificarlos y conservar un rollback.

## Future Managers

Los symlinks administrados por el perfil son la estrategia actual. GNU Stow o
Chezmoi se evaluaran cuando las diferencias reales entre macOS, Arch y Windows
superen lo que este mecanismo simple puede expresar con claridad.
