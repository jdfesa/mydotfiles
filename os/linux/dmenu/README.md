# Dmenu

Configuracion personal de dmenu mantenida como proyecto independiente. DWM lo
usa como lanzador, pero tambien puede servir para scripts, i3 u otros window
managers.

## Fuente

`src/` es el arbol fuente propio de dmenu 5.4 con los parches `center` y
`xresources`. La configuracion se identifica por el historial de estos dotfiles,
no por el usuario, repositorio o commit de una configuracion externa usada como
punto de partida.

No se crea otro clon: `src/` es la copia versionada y modificable. Esto permite
experimentar y revisar cada cambio con Git.

Primera modificacion local: los valores de fuente y colores se duplican siempre
antes de ser reemplazados o liberados. Esto corrige el ownership del parche
Xresources cuando el servidor X no tiene una base de recursos cargada y elimina
las advertencias de tipos que aparecian al compilar con `-Wall`.

## Personalizacion y build

Los defaults viven en `src/config.def.h`: posicion, ancho, fuentes y colores.
Compilar sin modificar el arbol fuente:

```sh
os/linux/dmenu/scripts/build
```

La build queda en:

```text
~/.cache/mydotfiles-build/dmenu/
```

Para probarla desde una sesion X11 sin instalar:

```sh
printf '%s\n' terminal browser files logout \
  | ~/.cache/mydotfiles-build/dmenu/dmenu -i -p 'Test:'
```

La instalacion coordinada de dmenu, DWM y la entrada SDDM se realiza con:

```sh
os/linux/dwm/scripts/install-session
```

Ese procedimiento crea un backup previo y permite rollback. No ejecutar
`sudo make install` directamente desde `src/`, porque generaria artefactos de
build dentro de la fuente versionada y omitiría el respaldo.

## Estructura

```text
dmenu/
  README.md
  src/            # snapshot, configuracion y parches ya aplicados
  scripts/build   # build reproducible sin privilegios
  patches/        # futuros parches separados, cuando corresponda
```
