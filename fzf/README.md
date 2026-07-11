# Fzf

`fzf` es un fuzzy finder para terminal: muestra una lista interactiva y te deja filtrar escribiendo pedazos del texto. Es la pieza que convierte listas largas en seleccion rapida.

## Estado

Instalado y activado en Zsh.

## Para que sirve

En vez de recordar o escribir una ruta, comando o archivo completo, escribis una parte y elegis el resultado.

Ejemplos de uso con la integracion de Zsh:

```bash
Ctrl-R   # buscar en el historial de comandos
Ctrl-T   # insertar archivos o carpetas en el comando actual
Alt-C    # saltar a una carpeta elegida con fzf
```

En macOS, `Alt-C` puede depender de como el emulador de terminal envie la tecla Option. Si no responde, probar `Esc` y luego `C`, o revisar la configuracion de Option/Alt del terminal.

## Relacion con otras herramientas

- `zoxide`: `zi` usa `fzf` para abrir un selector interactivo de carpetas aprendidas.
- `sesh`: usa `fzf` para elegir sesiones/proyectos.
- `tmux`: puede usar `fzf` para sessionizers y paneles de seleccion.
- `rg`, `fd`, `bat` y `eza`: suelen combinarse con `fzf` para busquedas y previews mas potentes.

## Instalacion

```bash
brew install fzf
```

Ya esta incluido en `os/macos/packages/homebrew/00-base/Brewfile`.

## Activacion en Zsh

La integracion real vive en `~/.zshrc`, antes de `zoxide`:

```bash
if command -v fzf >/dev/null 2>&1; then
  source <(fzf --zsh)
fi
```

Despues de agregar o modificar este bloque, hay que abrir una terminal nueva o recargar la sesion actual:

```bash
source ~/.zshrc
```

Para confirmar que quedo activo:

```bash
type __fzf_select
bindkey '^R'
```

`bindkey '^R'` deberia mostrar el widget de historial de `fzf`.

## Carpeta en este repo

`fzf` no necesita un symlink a `~/.config` ni una carpeta propia de configuracion para funcionar. La carpeta `fzf/` de este repo es documentacion del flujo.

Si mas adelante agregamos opciones como colores, previews o comandos por defecto, se pueden documentar aca y mantener la activacion en `~/.zshrc`.

## Restaurar en otra maquina

1. Instalar la herramienta desde el Brewfile base o manualmente:

```bash
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/00-base/Brewfile
```

2. Agregar el bloque de activacion a `~/.zshrc`, antes de `zoxide`.
3. Abrir una terminal nueva o ejecutar `source ~/.zshrc`.
4. Validar con `Ctrl-R` o `bindkey '^R'`.

## Pendiente

- Decidir si conviene personalizar colores para que sigan el selector global de `colorscheme/`.
- Evaluar si conviene activar previews con `bat` en flujos concretos de busqueda.
- Evaluar busquedas interactivas con `rg` cuando el flujo base ya este comodo.
- Integrarlo con scripts concretos de `sesh`, `tmux`, Kitty o Ghostty solo si mejora el flujo diario.
