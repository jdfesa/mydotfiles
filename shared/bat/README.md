# Bat

`bat` es un reemplazo moderno para leer archivos en la terminal. Agrega syntax highlighting, paginacion, numeros de linea, marcas de Git y mejor formato visual.

## Estado

Instalado y activado en Zsh mediante aliases seguros. No reemplaza `cat` por ahora.

## Para que sirve

Mejora la lectura diaria de archivos:

```bash
b archivo        # abrir con bat
bp archivo       # abrir con paginador siempre
catp archivo     # salida simple, util para lectura rapida
preview archivo  # vista con numeros de linea y cambios Git
```

Esto tiene impacto directo en el flujo diario porque cambia como inspeccionas archivos desde la terminal. Es una integracion prudente: `cat` sigue siendo el comando original del sistema para pipes, scripts y casos simples.

## Instalacion

```bash
brew install bat
```

Ya esta incluido en `os/macos/packages/homebrew/00-base/Brewfile`.

## Activacion en Zsh

La integracion real vive en `~/.zshrc`:

```bash
if command -v bat >/dev/null 2>&1; then
  alias b='bat'
  alias bp='bat --paging=always'
  alias catp='bat --style=plain --paging=never'
  alias preview='bat --style=numbers,changes --paging=always'
fi
```

El bloque queda protegido para que una maquina nueva no falle si `bat` todavia no fue instalado con Homebrew.

Despues de agregar o modificar este bloque, hay que abrir una terminal nueva o recargar la sesion actual:

```bash
source ~/.zshrc
```

Para confirmar que quedo activo:

```bash
type b
type bp
type catp
type preview
```

Los cuatro deberian aparecer como aliases.

## Por que no reemplazamos cat todavia

`cat` es un comando basico y predecible. Muchas veces se usa en pipes, scripts o salidas sin formato:

```bash
cat archivo | otra-herramienta
```

Por eso empezamos con aliases nuevos. Si despues de usar `bat` unos dias se siente natural, se puede evaluar un alias para `cat`, pero no es necesario para obtener el beneficio principal.

## Relacion con otras herramientas

- `fzf`: puede usar `bat` como preview de archivos.
- `yazi`: puede usar `bat` para previews en terminal.
- `rg`: combina bien con `bat` para inspeccionar resultados de busqueda.
- `colorscheme`: mas adelante podria definir colores o tema visual para `bat`.

## Carpeta en este repo

`bat` no necesita un symlink a `~/.config` para esta integracion inicial. La carpeta `bat/` de este repo es documentacion del flujo.

Si mas adelante agregamos temas propios, cache de syntaxes o configuracion avanzada, se documenta aca y se decide si conviene versionar una config real.

## Restaurar en otra maquina

1. Instalar la herramienta desde el Brewfile base o manualmente:

```bash
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/00-base/Brewfile
```

2. Agregar el bloque de aliases a `~/.zshrc`.
3. Abrir una terminal nueva o ejecutar `source ~/.zshrc`.
4. Validar con `type b` y probar `preview README.md`.

## Pendiente

- Evaluar si `fzf` deberia usar `bat` como preview por defecto.
- Revisar temas de `bat` cuando `colorscheme/` deje de estar en evaluacion.
- Decidir despues de probarlo si conviene o no aliasar `cat`.
