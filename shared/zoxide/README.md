# Zoxide

`zoxide` es una herramienta de navegacion inteligente para la terminal. Aprende las carpetas que visitas con frecuencia y luego te permite saltar a ellas con una busqueda corta.

## Estado

Instalado y activado en Zsh.

## Para que sirve

En vez de escribir rutas largas como:

```bash
cd ~/mydotfiles
```

con zoxide activo podrias escribir:

```bash
z mydot
```

`zoxide` calcula la carpeta mas probable segun tu historial y te lleva ahi.

## Relacion con Sesh

`sesh` puede usar `zoxide` para descubrir carpetas frecuentes automaticamente. Por eso `sesh list` sin flags intenta consultar zoxide.

En nuestro flujo inicial de `sesh` no dependemos de eso. Usamos:

```bash
sesh list -c
sesh picker -c
```

La bandera `-c` limita la lista a las sesiones definidas en
`~/mydotfiles/shared/sesh/sesh.toml`.

## Instalacion

```bash
brew install zoxide
```

Ya esta incluido en `os/macos/packages/homebrew/00-base/Brewfile`.

## Activacion en Zsh

La integracion real vive en `~/.zshrc`, idealmente al final del archivo:

```bash
if command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init zsh)"
fi
```

El bloque queda protegido para que una maquina nueva no falle si `zoxide` todavia no fue instalado con Homebrew. Conviene mantenerlo al final para que el hook de cambio de directorio (`chpwd`) quede registrado despues del resto de la configuracion de Zsh.

Despues de agregar o modificar este bloque, hay que abrir una terminal nueva o recargar la sesion actual:

```bash
source ~/.zshrc
```

Para confirmar que quedo activo:

```bash
type z
type zi
```

Ambos deberian aparecer como funciones cargadas desde `~/.zshrc`.

## Uso inicial

`z` solo puede saltar a carpetas que ya conoce. Zoxide aprende cuando cambias de directorio despues de tener el hook activo:

```bash
cd ~/mydotfiles
z mydotfiles
```

Tambien se puede sembrar una carpeta manualmente:

```bash
zoxide add ~/mydotfiles
```

Comandos utiles:

```bash
z <texto>          # salta a la carpeta mas probable
zi                 # abre selector interactivo con fzf
zoxide query -l    # lista carpetas conocidas
zoxide remove PATH # elimina una entrada aprendida
```

`zi` requiere `fzf`; en este repo ya esta incluido en
`os/macos/packages/homebrew/00-base/Brewfile`.

## Carpeta en este repo

`zoxide` no necesita un symlink a `~/.config` ni una carpeta propia de configuracion para funcionar. La carpeta `zoxide/` de este repo es documentacion del flujo.

La base de datos que aprende tus carpetas frecuentes la administra la herramienta automaticamente en tu home local, fuera del repo. En macOS suele vivir en:

```bash
~/Library/Application Support/zoxide
```

Esa base no se versiona porque representa historial local de uso.

## Restaurar en otra maquina

1. Instalar la herramienta desde el Brewfile base o manualmente:

```bash
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/00-base/Brewfile
```

2. Agregar el bloque de activacion al final de `~/.zshrc`.
3. Abrir una terminal nueva o ejecutar `source ~/.zshrc`.
4. Entrar a algunas carpetas con `cd` o sembrarlas con `zoxide add`.

## Pendiente

- Integrarlo con `sesh` sin tener que usar siempre `-c`.
- Revisar el script de Kitty basado en zoxide antes de usarlo como flujo diario.
