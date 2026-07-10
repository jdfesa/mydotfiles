# Dotfiles Architecture

Este documento describe la arquitectura objetivo del repositorio de dotfiles.
La intencion es mantener una fuente de verdad unica que pueda crecer desde el
setup actual de macOS hacia Linux, Windows y maquinas especificas sin duplicar
configuraciones compartidas.

## Principles

- Un solo repositorio central para los dotfiles personales.
- Configuraciones compartidas por defecto; separacion por sistema operativo solo
  cuando exista una diferencia real.
- Diferencias por maquina aisladas en archivos locales o en una capa `hosts/`.
- Rutas portables usando `$HOME`, `~`, variables de entorno o mecanismos XDG.
- Secretos, tokens, credenciales y rutas privadas concretas quedan fuera de Git.
- Los cambios grandes de arquitectura se documentan con ADRs livianos.

## Current Shape

El repositorio actual esta organizado principalmente por herramienta:

```text
mydotfiles/
  nvim/
  zsh/
  starship/
  tmux/
  kitty/
  ghostty/
  yazi/
  btop/
  lazygit/
  aerospace/
  sketchybar/
  hammerspoon/
  apps/
```

Esta forma es una buena base porque evita duplicar herramientas que existen en
varios sistemas operativos, como Neovim, Git, Starship, Tmux, Yazi o Lazygit.

## Target Layers

La estructura objetivo se piensa por capas:

```text
mydotfiles/
  nvim/
  tmux/
  starship/
  git/
  lazygit/
  yazi/
  btop/
  zsh/

  os/
    macos/
      aerospace/
      sketchybar/
      hammerspoon/
      brew/
    linux/
      dwm/
      i3/
      x11/
      pacman/
      yay/
    windows/
      powershell/
      windows-terminal/
      winget/

  hosts/
    macbook-jd/
    arch-desktop/
    win11-ssd/

  profiles/
    minimal/
    desktop/
    macos-main/
    arch-dwm/
    arch-i3/
    windows-native/

  scripts/
    bootstrap
    link
    install-packages
```

No es necesario migrar todo de inmediato. La regla inicial es mantener estables
las carpetas activas y usar las nuevas capas para configuraciones nuevas o para
separaciones que ya sean necesarias.

## Shared Tooling

Las herramientas que pueden vivir en varios sistemas operativos deben quedarse
como carpetas principales por herramienta, salvo que una diferencia concreta
obligue a crear una variante.

Ejemplos:

- `nvim/`
- `zsh/`
- `starship/`
- `tmux/`
- `git/`
- `lazygit/`
- `yazi/`
- `btop/`
- `fzf/`
- `ripgrep/`
- `zoxide/`

Si una herramienta necesita matices por sistema, primero se intentara resolver
con variables de entorno, deteccion del sistema operativo o archivos locales
ignorados por Git. Solo despues se creara una variante por sistema.

## OS-Specific Tooling

Las herramientas que pertenecen claramente a un sistema operativo deben vivir en
`os/<system>/`.

Ejemplos:

- macOS: AeroSpace, Sketchybar, Hammerspoon, Homebrew.
- Linux: DWM, i3, X11, Wayland, Pacman, Yay.
- Windows: PowerShell, Windows Terminal, Winget.

Durante la transicion, algunas herramientas macOS pueden seguir en la raiz si ya
estan activas y enlazadas. Moverlas no es prioritario hasta que exista un script
de instalacion o un gestor de enlaces que haga la migracion segura.

## Hosts

La capa `hosts/` se reserva para diferencias de una maquina concreta:

- nombre de host;
- rutas fisicas especiales;
- monitores;
- GPU o perifericos;
- teclado conectado;
- detalles de una VM;
- comportamiento temporal de una maquina experimental.

La capa de host no debe duplicar una configuracion completa si solo necesita
cambiar una ruta o una opcion. En esos casos se prefiere usar variables locales.

## Profiles

La capa `profiles/` describe combinaciones de herramientas que forman una
experiencia instalable.

Ejemplos:

- `minimal`: shell, Git, Neovim y herramientas CLI basicas.
- `desktop`: base grafica comun.
- `macos-main`: setup principal actual de macOS.
- `arch-dwm`: Arch Linux con DWM.
- `arch-i3`: Arch Linux con i3.
- `windows-native`: configuracion nativa de Windows.

Un perfil no deberia contener configuraciones completas. Su funcion es declarar
que piezas se activan juntas.

## Paths And Usernames

Se intentara usar `jd` como usuario principal en nuevas instalaciones cuando sea
practico, especialmente en macOS y Linux. Aun asi, los dotfiles no deben depender
de un nombre de usuario fijo.

Preferir:

```sh
$HOME/.config/nvim
~/mydotfiles
$XDG_CONFIG_HOME
```

Evitar:

```sh
/Users/jd/.config/nvim
/home/joe/.config/nvim
```

Las rutas personales, como la ubicacion real de una boveda de Obsidian en
Dropbox, deben exponerse mediante variables de entorno:

```sh
export OBSIDIAN_VAULT="$HOME/Dropbox/path/to/vault"
```

La configuracion compartida debe consumir la variable y no asumir una ruta fija.

## Linking Strategy

La estrategia actual sigue siendo usar symlinks manuales desde el repositorio
hacia las rutas esperadas por cada aplicacion.

Esto se mantiene porque el setup principal actual es macOS y ya funciona. La
migracion a herramientas como `chezmoi` o `stow` se evaluara mas adelante cuando
existan suficientes diferencias reales entre macOS, Arch Linux, Windows, VMs y
hosts especificos.

## Migration Strategy

La transicion debe ser incremental:

1. Documentar arquitectura y decisiones.
2. Crear `os/`, `hosts/` y `profiles/` cuando haya contenido real para ellos.
3. Agregar configuraciones nuevas directamente en la capa correcta.
4. Eliminar rutas absolutas hardcodeadas de configs compartidas.
5. Probar Arch Linux en maquina secundaria o VM.
6. Evaluar `chezmoi` o `stow` con evidencia practica.
7. Mover carpetas activas solo cuando el beneficio sea claro y el rollback sea
   sencillo.

## ADR Policy

Los ADRs viven en `docs/adr/`.

Se crea un ADR para decisiones que afectan la arquitectura del repositorio o su
forma de restaurarse en distintas maquinas. No se crea un ADR para cambios
cotidianos de aliases, temas, keymaps o ajustes menores de una herramienta.

