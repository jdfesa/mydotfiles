# Level 2: Sessions

## Goal

Dejar el trabajo vivo, salir y volver sin crear entornos duplicados.

## New Keys

| Después del prefijo | Acción |
|---|---|
| `d` | Desconectar este cliente sin cerrar la sesión |
| `s` | Elegir sesión; flechas, Enter; `q` sale |
| `$` | Renombrar la sesión actual |

## Leave and Return

1. Con las ventanas de `work` abiertas, pulsa prefijo → `d`.
2. Estarás en el shell exterior; las tareas de tmux siguen vivas.
3. Consulta `rtk proxy tmux list-sessions`.
4. Vuelve con el mismo comando del nivel 1:

   ```sh
   rtk proxy tmux new-session -A -s work
   ```

No necesitas guardar un snapshot para una pausa. Esto conserva los procesos
solo mientras la máquina y el servidor tmux sigan funcionando; no sobrevive
a reiniciar por sí mismo. `exit` termina un shell: no equivale a `d`.

## Add a Project Only When Useful

Desde fuera de tmux puedes crear/recuperar otro espacio:

```sh
rtk proxy tmux new-session -A -s dotfiles -c "$HOME/mydotfiles"
```

Dentro de tmux, prefijo → `s` elige entre sesiones existentes. No fuerces el
anidamiento si el comando de entrada avisa que ya estás dentro. Una sesión
sigue siendo suficiente si no necesitas separar proyectos.

## Ready for the Next Level

- Puedes desconectarte y volver a las mismas ventanas.
- Sabes que desconectada no significa destruida.
- No creas una sesión por cada shell.

Sigue con [Level 3: Panes](03-panes.md), o vuelve al [índice](README.md).
