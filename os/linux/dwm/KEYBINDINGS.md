# DWM Keybindings

Referencia de los atajos efectivos definidos en `src/config.def.h`. Esta guia
describe la build instalada en `arch-desktop`; no intenta documentar una
configuracion upstream ni los hábitos del autor original.

## Modificador y Silakka54

`Mod` es `Super` (`Mod4` en X11), equivalente conceptual a `Command` en macOS.
X11 reconoce correctamente `Super_L` y `Super_R`.

En la capa base del Silakka54:

- mantener `Esc/LGUI` en el pulgar izquierdo produce `Super`;
- mantener `Backspace/RGUI` en el pulgar derecho produce `Super`;
- tocar esas teclas sin mantenerlas produce `Esc` o `Backspace`;
- mantener `Enter` produce `Hyper`; tocarlo produce `Enter`.

Para abrir una terminal, mantener `Esc/LGUI`, tocar brevemente `Enter` y soltar
ambas teclas. No mantener `Enter`, porque entonces el teclado emite `Hyper`.

## Inicio rapido

| Atajo | Accion | Estado |
|---|---|---|
| `Super+Enter` | Abrir ST | Funciona |
| `Super+d` | Abrir dmenu | Funciona |
| `Super+n` | Abrir Neovim dentro de ST | Funciona |
| `Super+Shift+p` | Abrir el menu de energia | Funciona |
| `Super+q` | Cerrar la ventana enfocada | Funciona; descarta el proceso |
| `Super+Shift+Backspace` | Terminar DWM y volver a SDDM | Funciona; cierra la sesion |
| `Super+Ctrl+Shift+q` | Reiniciar DWM sin cerrar la sesion | Funciona |

`Super+q` no equivale a `:q` de Neovim. Cierra la ventana desde X11 y los
cambios no guardados no se escriben al archivo. Para salir del editor, tocar
`Esc` y usar `:wq`, `:q` o `:q!` deliberadamente.

## Ventanas y pila

| Atajo | Accion |
|---|---|
| `Super+j` | Enfocar la siguiente ventana de la pila |
| `Super+k` | Enfocar la ventana anterior de la pila |
| `Super+Shift+j` | Empujar la ventana hacia abajo en la pila |
| `Super+Shift+k` | Empujar la ventana hacia arriba en la pila |
| `Super+Space` | Intercambiar la ventana enfocada con master |
| `Super+Ctrl+m` | Enfocar master o regresar al foco anterior |
| `Super+Shift+i` | Aumentar el numero de ventanas master |
| `Super+Ctrl+i` | Disminuir el numero de ventanas master |
| `Super+h` | Reducir el ancho del area master |
| `Super+l` | Aumentar el ancho del area master |
| `Super+Shift+Space` | Alternar flotante para la ventana enfocada |
| `Super+Shift+s` | Alternar sticky: seguir visible al cambiar de tag |
| `Super+f` | Alternar fullscreen real |

## Layouts

| Atajo | Accion |
|---|---|
| `Super+t` | Layout tiled: master y pila |
| `Super+Shift+m` | Layout monocle: una ventana ocupa el area completa |
| `Super+s` | Layout spiral |
| `Super+Shift+t` | Layout dwindle |
| `Super+Ctrl+Space` | Volver al layout usado anteriormente |

## Tags

DWM usa tags, no escritorios exclusivos. Una ventana puede pertenecer a varios
tags y la pantalla puede mostrar varios tags simultaneamente.

Para cada numero de `1` a `9`:

| Atajo | Accion |
|---|---|
| `Super+numero` | Ver solamente ese tag |
| `Super+Ctrl+numero` | Agregar o quitar ese tag de la vista |
| `Super+Shift+numero` | Enviar la ventana a ese tag |
| `Super+Ctrl+Shift+numero` | Agregar o quitar ese tag de la ventana |

Otros atajos:

| Atajo | Accion |
|---|---|
| `Super+Tab` | Volver a la seleccion de tags anterior |
| `Super+0` | Mostrar todos los tags |
| `Super+Shift+0` | Asignar la ventana a todos los tags |

## Monitores

| Atajo | Accion |
|---|---|
| `Super+]` | Enfocar el monitor anterior |
| `Super+[` | Enfocar el monitor siguiente |
| `Super+Shift+]` | Enviar la ventana al monitor anterior |
| `Super+Shift+[` | Enviar la ventana al monitor siguiente |

El parche `focusmonmouse` mueve el puntero al monitor que recibe el foco.

## Gaps

| Atajo | Accion |
|---|---|
| `Super+-` / `Super+=` | Reducir / aumentar todos los gaps en 3 px |
| `Super+Shift+=` | Activar o desactivar gaps |
| `Super+Shift+-` | Restaurar gaps predeterminados |
| `Super+Alt+i` / `Super+Alt+Shift+i` | Aumentar / reducir gaps internos |
| `Super+Alt+o` / `Super+Alt+Shift+o` | Aumentar / reducir gaps externos |
| `Super+Alt+6` / `Super+Alt+Shift+6` | Aumentar / reducir interno horizontal |
| `Super+Alt+7` / `Super+Alt+Shift+7` | Aumentar / reducir interno vertical |
| `Super+Alt+8` / `Super+Alt+Shift+8` | Aumentar / reducir externo horizontal |
| `Super+Alt+9` / `Super+Alt+Shift+9` | Aumentar / reducir externo vertical |

## Barra

| Atajo | Accion |
|---|---|
| `Super+Shift+b` | Mostrar u ocultar la barra completa |
| `Super+Ctrl+t` | Mostrar u ocultar el titulo |
| `Super+Ctrl+s` | Mostrar u ocultar el estado |
| `Super+Ctrl+g` | Mostrar u ocultar tags |
| `Super+Ctrl+e` | Invertir colores de tags y titulo |
| `Super+Ctrl+r` | Mostrar u ocultar el simbolo de layout |
| `Super+Ctrl+f` | Mostrar u ocultar el indicador flotante |
| `Super+Ctrl+\` | Recargar colores desde Xresources |

## Aplicaciones verificadas

| Atajo | Comando | Estado en Arch |
|---|---|---|
| `Super+m` | `st -e termusic` | Disponible |
| `Super+w` | `qutebrowser` | No instalado |
| `Super+n` | `st -e nvim` | Disponible |
| `Super+Shift+h` | `st -e htop` | Disponible |
| `Super+p` | `darktable` | Disponible |
| `Super+v` | `cliphist sel` | Disponible |
| `Super+c` | `cliphist add` | Disponible |

`Super+c` copia la seleccion primaria de X11 al clipboard y la agrega al
historial. `Super+v` abre la seleccion del historial mediante dmenu.

## Multimedia y sistema

| Atajo | Accion | Estado |
|---|---|---|
| `Super+F12` | Siguiente pista de Termusic | Disponible |
| `Super+F11` | Play/pause de Termusic | Disponible |
| `Super+Shift+F11` | Play/pause del reproductor predeterminado | Disponible |
| `Super+F10` | Pista anterior de Termusic | Disponible |
| `Super+F8` | Bloquear con slock | Disponible |
| `Super+Shift+F8` | Bloquear y suspender | Disponible |
| `Super+F6` | Subir volumen 5% | Disponible |
| `Super+F5` | Bajar volumen 5% | Disponible |
| `Super+F7` | Iniciar status timer | Comando ausente |
| `Super+Shift+F7` | Limpiar status timer | Comando ausente |

### Power menu

`Super+Shift+p` abre un menu dmenu en ingles:

- `Lock`;
- `Suspend`;
- `Log out`;
- `Reboot`;
- `Power off`.

Suspend, logout, reboot y power off requieren una segunda confirmacion. `No`
aparece primero para que presionar Enter accidentalmente no confirme. Escape
cancela cualquiera de los dos menus.

## Atajos heredados sin comando

Estas combinaciones existen en el código pero no hacen nada en la maquina
actual porque el comando del autor original no esta instalado:

| Atajo | Comando ausente |
|---|---|
| `Super+Shift+n` | `dmenunotes` |
| `Super+Shift+a` | `dmenuvids` |
| `Super+Ctrl+a` | `dmenuaudioswitch` |
| `Super+Shift+d` | `rip` |
| `Super+r` | `rec` |
| `Super+Shift+grave` | `define` |
| `Super+Shift+w` | `wallpapermenu` |
| `Super+F1` | `screenshot` |
| `Super+Shift+F1` | `screenshot color` |
| `Super+F2` | `vb` |
| `Super+Shift+F2` | `dmenutemp` |
| `Super+F3` | `phototransfer` |

No se deben recrear por imitacion. Cada función se conserva, reemplaza o
elimina despues de comprobar si resuelve una necesidad real.

## Acciones peligrosas

| Atajo | Efecto |
|---|---|
| `Super+q` | Cierra la ventana y puede perder cambios no guardados |
| `Super+Shift+q` | Cierra todas las ventanas excepto la enfocada |
| `Super+Ctrl+Shift+q` | Reinicia DWM; no cierra aplicaciones |
| `Super+Shift+Backspace` | Termina la sesion grafica DWM |

## Mouse

| Gesto | Accion |
|---|---|
| `Super+arrastrar izquierdo` | Mover ventana |
| `Super+arrastrar derecho` | Redimensionar ventana |
| `Super+clic medio` | Restaurar gaps |
| `Super+rueda` | Aumentar o reducir gaps |
| Clic izquierdo en tag | Ver tag |
| Clic derecho en tag | Alternar tag en la vista |
| `Super+clic izquierdo` en tag | Enviar ventana al tag |
| `Super+clic derecho` en tag | Alternar tag para la ventana |
| Clic medio en titulo | Intercambiar con master |
| Clic medio en el fondo | Mostrar u ocultar barra |
| Clic izquierdo en estado | Actualizar el bloque de sensores |

Los demás clics del estado no tienen actualmente un bloque receptor. El atajo
`Shift+clic derecho` sobre el estado apunta a una ruta historica de DWMBlocks
que ya no existe y es candidato a eliminar o corregir.

## Fuente de verdad y mantenimiento

La fuente de verdad sigue siendo `src/config.def.h`. Al cambiar `keys[]` o
`buttons[]`, actualizar este documento en el mismo commit. Antes de instalar:

```sh
os/linux/dwm/scripts/build
os/linux/dwm/scripts/test-nested
```

Los estados de disponibilidad fueron verificados en `arch-desktop` el
2026-07-17.
