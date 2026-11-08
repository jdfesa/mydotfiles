# Level 6: Session Lifecycle

## Goal

Cerrar trabajo terminado sin destruir el resto del entorno.

## Choose the Operation

| Necesidad | Operación |
|---|---|
| Hacer una pausa | Prefijo → `d` |
| Terminar un shell sin tareas pendientes | `exit` dentro del panel |
| Forzar cierre de un panel | Prefijo → `x`, confirmar |
| Cerrar ventana con todos sus paneles | Prefijo → `&`, confirmar |
| Destruir una sesión concreta | `kill-session` con nombre exacto; no pide confirmación |

Guarda archivos y detén limpiamente servidores antes de cerrar sus terminales.
Los cierres forzados pueden perder trabajo.

## Disposable Session Exercise

Hazlo **solo con una sesión de práctica vacía**, nunca con `work` como ensayo.
Desde fuera de tmux:

```sh
rtk proxy tmux new-session -s training-close
```

Si el nombre ya existe, el comando falla: no reutilices ni destruyas una sesión
anterior sin comprobar su contenido. Si acabas de crearla, renombra su ventana
como `descartable`, desconéctate con `d` y consulta la lista de sesiones.

Solo si confirmas que es la sesión vacía que acabas de crear para practicar:

```sh
rtk proxy tmux kill-session -t '=training-close'
```

Comprueba con `rtk proxy tmux list-sessions` que las demás siguen existiendo.
El `=` exige el nombre exacto, no un prefijo del nombre.

## Snapshots Are Separate

Una sesión destruida puede reaparecer al restaurar un snapshot que la contenga.
Después de retirar una sesión real, guarda el entorno restante si quieres
actualizar el último snapshot. No borra copias históricas: consulta
[Retire a Session](../daily-workflow.md#retire-a-session) antes de limpiar backups.

No uses `kill-server` ni borres sockets para terminar un proyecto: no son el
cierre selectivo de una sesión.

## Ready to Maintain the Habit

- Puedes elegir entre desconectar y terminar sin confundir sus efectos.
- Puedes cerrar una sesión de práctica sin afectar otras.
- Puedes repetir los primeros niveles en tareas reales sin añadir más atajos.

Vuelve al [índice](README.md) o al [contrato actual](keybindings.md).
