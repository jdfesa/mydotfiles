# Level 5: Persistence

## Goal

Distinguir trabajo vivo de un snapshot y reconstruir el entorno después de
reiniciar. Este nivel necesita Resurrect instalado y cargado.

## New Keys

| Secuencia | Acción |
|---|---|
| Prefijo → `Ctrl+s` | Guardar todas las sesiones de este servidor |
| Prefijo → `Ctrl+r` | Restaurar el último snapshot |

Primero `Ctrl+Espacio`, soltar; después **Control y la letra**. `r` sin Control
tras el prefijo solo recarga la configuración: no restaura nada.

## Exercise Without Restarting Work

1. Guarda los archivos del editor: Resurrect no lo hace por ti.
2. Pulsa prefijo → `Ctrl+s` y espera la confirmación.
3. Comprueba el guardado según [Private State](../daily-workflow.md#private-state).
   Un entorno sin cambios puede reutilizar el archivo anterior.
4. Para una pausa normal, usa `d` y vuelve con el comando habitual. No necesitas
   restaurar una sesión viva.
5. Practica restauración solo tras un reinicio ya planificado, siguiendo
   [Restore After a Restart](../daily-workflow.md#restore-after-a-restart).
   No mates el servidor de trabajo para ensayar.

Continuum usa un intervalo predeterminado de 15 minutos, pero no sustituye el
guardado manual antes de reiniciar. La restauración automática está desactivada.
Se reconstruyen ventanas, directorios y paneles; no sobrevive la memoria de los
procesos ni se relanza cualquier comando.

En Arch, `hostname: command not found` es una utilidad ausente, no una máquina
sin nombre. La [instalación Linux](../../../os/linux/tmux/README.md#installation)
explica `inetutils`. No hay que renombrar el equipo ni habilitar servicios.

## Ready for the Next Level

- Sabes cuándo basta adjuntar y cuándo necesitas restaurar.
- Sabes que guardar afecta a todas las sesiones, no solo a la visible.
- No guardas snapshots ni texto privado de paneles en Git.

Sigue con [Level 6: Session Lifecycle](06-session-lifecycle.md), o vuelve al [índice](README.md).
