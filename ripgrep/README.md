# Ripgrep

`ripgrep` es una herramienta de busqueda de texto ultrarrapida. El comando se llama `rg`.

## Estado

Instalado y activado en Zsh mediante aliases. No reemplaza `grep` por ahora.

## Para que sirve

Busca texto dentro de proyectos respetando `.gitignore` por defecto. Es especialmente util en repositorios grandes de Java, Python, scripts y dotfiles.

Uso base:

```bash
rg "texto"
rg "class Usuario"
rg "TODO"
rg "zoxide" ~/mydotfiles
```

Aliases activos:

```bash
rgi "texto"  # busqueda case-insensitive
rgl          # lista archivos que rg puede buscar
rgp "texto"  # busqueda con numeros de linea y 2 lineas de contexto
```

Esto tiene impacto directo en el flujo diario porque reduce la friccion de encontrar codigo, configuraciones, rutas o TODOs sin abrir el editor.

## Instalacion

```bash
brew install ripgrep
```

Ya esta incluido en `brew/10-essential/Brewfile`.

## Activacion en Zsh

La integracion real vive en `~/.zshrc`:

```bash
if command -v rg >/dev/null 2>&1; then
  alias rgi='rg -i'
  alias rgl='rg --files'
  alias rgp='rg --line-number --context 2'
fi
```

El bloque queda protegido para que una maquina nueva no falle si `ripgrep` todavia no fue instalado con Homebrew.

Despues de agregar o modificar este bloque, hay que abrir una terminal nueva o recargar la sesion actual:

```bash
source ~/.zshrc
```

Para confirmar que quedo activo:

```bash
type rg
type rgi
type rgl
type rgp
```

## Por que no reemplazamos grep

`grep` sigue siendo parte basica del sistema y aparece en scripts, documentacion y comandos compartidos. `rg` es mejor para busqueda interactiva en proyectos, pero no hace falta aliasar `grep` para obtener el beneficio.

## Relacion con otras herramientas

- `bat`: sirve para inspeccionar archivos encontrados con `rg`.
- `fzf`: puede combinarse con `rg` para busquedas interactivas.
- `eza`: ayuda a navegar el arbol de archivos antes o despues de buscar.
- `yazi`: puede apoyarse en `rg` para busquedas dentro del file manager.

## Carpeta en este repo

`ripgrep` no necesita un symlink a `~/.config` ni una carpeta propia de configuracion para esta integracion inicial. La carpeta `ripgrep/` de este repo es documentacion del flujo.

Si mas adelante agregamos una configuracion global, por ejemplo `~/.ripgreprc`, se documenta aca antes de activarla.

## Restaurar en otra maquina

1. Instalar la herramienta desde el Brewfile essential o manualmente:

```bash
brew bundle --file ~/mydotfiles/brew/10-essential/Brewfile
```

2. Agregar el bloque de aliases a `~/.zshrc`.
3. Abrir una terminal nueva o ejecutar `source ~/.zshrc`.
4. Validar con `type rgi` y probar `rg "texto" ~/mydotfiles`.

## Pendiente

- Evaluar una busqueda interactiva `rg + fzf + bat` cuando queramos unir el stack.
- Decidir si conviene versionar un `~/.ripgreprc`.
