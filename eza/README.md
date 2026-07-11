# Eza

`eza` es un reemplazo moderno de `ls`. Muestra listados mas legibles, con iconos, estado Git, colores y vista de arbol.

## Estado

Instalado y activado en Zsh mediante aliases.

## Para que sirve

Mejora comandos que se usan todo el tiempo al navegar por la terminal:

```bash
ls  # listado normal con iconos
ll  # listado largo, archivos ocultos y estado Git
la  # listado largo con archivos ocultos
lt  # vista de arbol
```

Esto tiene impacto directo en el flujo diario porque cambia como lees carpetas y repositorios desde la terminal. Es una integracion de bajo riesgo: si no gusta, se quitan los aliases y `ls` vuelve al comportamiento original.

## Instalacion

```bash
brew install eza
```

Ya esta incluido en `os/macos/packages/homebrew/00-base/Brewfile`.

## Activacion en Zsh

La integracion real vive en `~/.zshrc`:

```bash
if command -v eza >/dev/null 2>&1; then
  alias ls='eza --icons=auto --group-directories-first'
  alias ll='eza -la --icons=auto --git --group-directories-first'
  alias la='eza -la --icons=auto --group-directories-first'
  alias lt='eza --tree --icons=auto --group-directories-first'
fi
```

El bloque queda protegido para que una maquina nueva no falle si `eza` todavia no fue instalado con Homebrew.

Despues de agregar o modificar este bloque, hay que abrir una terminal nueva o recargar la sesion actual:

```bash
source ~/.zshrc
```

Para confirmar que quedo activo:

```bash
type ls
type ll
type la
type lt
```

Los cuatro deberian aparecer como aliases.

## Carpeta en este repo

`eza` no necesita un symlink a `~/.config` ni una carpeta propia de configuracion para funcionar. La carpeta `eza/` de este repo es documentacion del flujo.

Si mas adelante agregamos colores propios, variables de entorno o integracion con `colorscheme/`, se documentan aca.

## Restaurar en otra maquina

1. Instalar la herramienta desde el Brewfile base o manualmente:

```bash
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/00-base/Brewfile
```

2. Agregar el bloque de aliases a `~/.zshrc`.
3. Abrir una terminal nueva o ejecutar `source ~/.zshrc`.
4. Validar con `type ls` y probar `ll` dentro de un repositorio Git.

## Pendiente

- Evaluar si `lt` necesita un limite por defecto, por ejemplo `--level=2`, para evitar arboles demasiado largos.
- Decidir si se integra con `colorscheme/` cuando exista un selector global de colores.
