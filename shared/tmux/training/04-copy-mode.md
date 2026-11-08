# Level 4: Copy Mode

## Goal

Volver al historial de una terminal y copiar texto con teclas de tmux.

## New Keys

| Momento | Acción |
|---|---|
| Prefijo → `[` | Entrar en modo copia |
| Dentro: flechas o `h/j/k/l` | Moverse por el historial |
| Dentro: `v` | Comenzar selección |
| Dentro: `y` | Copiar y salir |
| Dentro: `Esc` | Limpiar selección sin salir |
| Dentro: `q` | Salir sin copiar |
| Prefijo → `P` mayúscula | Pegar el buffer tmux |

Dentro del modo copia no se repite el prefijo para `v`, `y` o `q`.
`p` minúscula después del prefijo sigue siendo la ventana anterior.

## Exercise

1. Genera algunas líneas de texto no sensible en una ventana de práctica.
2. Prefijo → `[`, busca una línea con flechas y pulsa `v`.
3. Amplía la selección y pulsa `y` para copiar y volver al shell.
4. Abre un buffer temporal del editor y pega con prefijo → `P`. No pruebes
   pegar comandos desconocidos en un prompt: un salto de línea podría ejecutarlos.
5. Repite la entrada con `[` y sal sin copiar con `q`.

## Platform Adapter

El gesto tmux es el mismo. macOS usa `pbcopy`; Linux elige `wl-copy` en Wayland
o `xclip` en X11. Sin backend gráfico se conserva el buffer tmux, pero no se
garantiza el clipboard del sistema. Los atajos nativos del emulador para copiar
y pegar no forman parte del contrato común.

## Ready for the Next Level

- Puedes entrar, seleccionar, copiar y salir sin quedar atrapado en el modo.
- Distingues el buffer tmux del clipboard del sistema.

Sigue con [Level 5: Persistence](05-persistence.md), o vuelve al [índice](README.md).
