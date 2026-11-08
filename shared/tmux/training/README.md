# Tmux Training

Entrenamiento progresivo para trabajar dentro de tmux sin abrir una terminal
del emulador por cada tarea. Se practica un núcleo de teclas estable, no todos
los atajos de una vez. La verificación prioritaria es **Arch y macOS**.

## Start Here

1. Practica [Level 1: Windows](01-windows.md) hasta crear y elegir ventanas sin
   consultar cada paso.
2. Repite esas teclas durante el trabajo real; añade otro nivel cuando el
   anterior resulte natural, no por calendario.
3. Si una tecla no responde, consulta [Compatibility](compatibility.md) antes
   de sustituirla o cambiar el prefijo.

## What Prefix Means

**En esta configuración, prefijo = `Ctrl+Espacio`, no Control solo.** No es
una tecla física llamada «prefijo»: es la combinación que avisa a tmux de que
la siguiente tecla será una orden para él.

Por ejemplo, **prefijo → `c`** significa:

1. Mantener **Control** y pulsar **Espacio**.
2. **Soltar ambas teclas**.
3. Pulsar **`c` sola** para crear una ventana.

No significa mantener Control mientras se pulsa `c`, ni pulsar
Control+Espacio+c simultáneamente.

| Notación | Cómo se pulsa |
|---|---|
| Prefijo → flecha derecha | Control+Espacio, soltar ambas, flecha derecha sola |
| Prefijo → `Ctrl+s` | Control+Espacio, soltar ambas, después Control+s |
| `Ctrl+h` **sin prefijo** | Control+h directamente, sin pulsar antes Control+Espacio |

«Sin prefijo» describe una combinación directa; no indica que se deba añadir
un atajo nuevo. Esta explicación no cambia los mapas del terminal ni de Neovim.

## Levels

| Nivel | Objetivo | Teclas nuevas |
|---|---|---|
| [1 — Windows](01-windows.md) | Editor, comandos y servidor en una sesión | `c`, números, `n/p`, `w`, `,`, `?` |
| [2 — Sessions](02-sessions.md) | Desconectarse, volver y elegir espacio | `d`, `s`, `$` |
| [3 — Panes](03-panes.md) | Ver dos tareas y cambiar de panel | `\`, `-`, flechas, `m`; luego `h/j/k/l` con prefijo |
| [4 — Copy Mode](04-copy-mode.md) | Consultar historial y copiar | `[`, luego `v`, `y`, `q`; `P` con prefijo |
| [5 — Persistence](05-persistence.md) | Guardar y reconstruir el entorno | `Ctrl+s` / `Ctrl+r` después del prefijo |
| [6 — Session Lifecycle](06-session-lifecycle.md) | Cerrar solo lo que terminó | `exit`, `x`, `&` y cierre exacto de sesión |

Son ejercicios consultables, no una bitácora personal. Los criterios de salida
permiten comprobar cada habilidad sin guardar historial privado.

## Current Configuration

| Capa | Estado |
|---|---|
| [Contrato de teclas](keybindings.md) | Índice vigente; filas core contrastadas con tmux en pruebas |
| [Base compartida](../tmux.conf) | Prefijo único `C-Space`, ventanas desde 1, divisiones en cwd |
| [Linux](../../../os/linux/tmux/tmux.conf) | Barra inferior, clipboard Wayland/X11, batería condicional |
| [macOS](../../../os/macos/tmux/tmux.conf) | Misma base y barra inferior; clipboard `pbcopy` |
| [Auditoría](compatibility.md) | Evidencia por capa y límites; no certificación de todas las apps |
| Debian, NixOS y Windows | Fuera del despliegue actual; no declarados validados |

La interacción básica con ventanas está comprobada en Arch. Los parsers y
pruebas aisladas no sustituyen la práctica física de cada nivel y escritorio.

## Daily Reminder

> Si hace falta otro shell: prefijo, soltar, `c`.
> Si no encuentras la tarea: prefijo, soltar, `w`.
> Si solo haces una pausa: prefijo, soltar, `d`.

Los escritorios y los atajos del emulador son capas distintas. El núcleo tmux
no usa Command ni Super.

## Reference Material

- [Daily Workflow](../daily-workflow.md): explicación completa del ciclo diario.
- [Tmux Cheatsheet](../tmux-cheatsheet.md): consulta rápida sin ejercicios.
- [Tmux Setup](../README.md): instalación por plataforma.

## Change Policy

Antes de cambiar una tecla del núcleo: identificar quién la intercepta, probar
aisladamente, actualizar contrato/chuleta/ejercicio y verificar Arch y macOS.
Preferir corregir un adaptador o atajo global antes que cambiar por plataforma
lo aprendido. No recargar sesiones ni cambiar preferencias globales durante
una auditoría.
