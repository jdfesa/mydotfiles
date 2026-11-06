# Tmux

Tmux mantiene las sesiones en el equipo donde corre su servidor. Cerrar la
terminal o desconectarse no mata los procesos de una sesión; reiniciar el
equipo o detener el servidor sí termina el trabajo que estaba en ejecución.

## Configuration

`tmux.conf` conserva el prefijo nativo `Ctrl+b` y no carga plugins, layouts
guardados ni scripts. Al crear una ventana o dividir un panel, la nueva
terminal abre en el directorio del panel activo. No se cambia `TERM` ni se
añade un comando de portapapeles específico del sistema.

## macOS

Homebrew instala tmux como parte del manifiesto base. El perfil `macos-main`
enlaza el archivo en `~/.config/tmux/tmux.conf`. Antes de desplegar el perfil,
revisa el plan de `scripts/link --dry-run macos-main`.

Kitty en macOS deja pasar `Ctrl+b` a tmux. Ghostty abre o recupera la sesión
`mydotfiles` con tmux directamente, sin un script intermedio; si no puede,
abre Zsh. No se cambian los perfiles de Arch o Debian.

## Quick Start

```sh
tmux new-session -A -s mydotfiles -c "$HOME/mydotfiles"
```

Una **sesión** agrupa el trabajo de un proyecto, una **ventana** funciona como
una pestaña y un **panel** es una terminal dentro de esa ventana. Pulsa y
suelta `Ctrl+b` antes de la segunda tecla:

| Tecla | Acción |
|---|---|
| `c` | Crear una ventana en el directorio actual |
| `%` / `"` | Dividir izquierda/derecha o arriba/abajo, en el directorio actual |
| Flechas | Cambiar de panel |
| `s` / `w` | Elegir sesión o ventana |
| `z` | Maximizar o restaurar el panel |
| `d` | Desconectarse sin cerrar la sesión |

Para volver, ejecuta el mismo `new-session -A` desde el shell, fuera de tmux.
Puedes ver las sesiones disponibles con `tmux list-sessions`.

## Isolated Test

```sh
tmux -L macos-trial -f "$HOME/mydotfiles/shared/tmux/tmux.conf" new-session -A -s trial
```

Este socket separado permite probar la configuración sin recargar el servidor
habitual. Tras desconectarte, usa `tmux -L macos-trial attach-session -t trial`
para comprobar que sigue viva.
