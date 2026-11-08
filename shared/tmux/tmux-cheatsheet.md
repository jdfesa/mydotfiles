# Tmux Cheatsheet

Referencia rápida de la configuración de este repositorio. Para empezar desde
cero o entender la persistencia, consulta [Daily Workflow](daily-workflow.md).
Para practicar progresivamente: [Tmux Training](training/README.md).

## Prefix

**Prefijo = `Ctrl+Espacio`.** Pulsa ambas teclas, suéltalas y después pulsa la
acción. `Prefijo → c` no significa mantener Control mientras pulsas `c`.
La documentación genérica suele usar `Ctrl+b`; aquí está reemplazado.
En un teclado US, `?` se escribe con `Shift+/`.

## Key Commands

Estos comandos se escriben en el shell. Los ejemplos usan RTK; `rtk proxy`
ejecuta el comando sin filtrar su comportamiento interactivo.

| Necesidad | Comando |
|---|---|
| Crear `work` o volver a ella, desde fuera de tmux | `rtk proxy tmux new-session -A -s work` |
| Listar sesiones vivas | `rtk proxy tmux list-sessions` |
| Volver exactamente a `work` | `rtk proxy tmux attach-session -t '=work'` |
| Desconectarse desde dentro sin cerrar el trabajo | `rtk proxy tmux detach-client` |
| Cambiar a `work` desde otra sesión tmux | `rtk proxy tmux switch-client -t '=work'` |
| Consultar atajos cargados, con un servidor activo | `rtk proxy tmux list-keys` |

`=work` fuerza una coincidencia exacta del nombre. Crear/adjuntar desde otro
tmux puede intentar anidar sesiones: usa el selector de sesiones o
`switch-client`, no fuerces el anidamiento.

## Essential Shortcuts

| Después del prefijo | Acción |
|---|---|
| `c` | Crear ventana en el directorio del panel actual |
| `1`…`9` | Elegir ventana por número; aquí empiezan en 1 |
| `n` / `p` | Ventana siguiente / anterior |
| `w` | Elegir ventana en una lista: flechas y Enter; `q` sale |
| `,` | Renombrar ventana; escribir nombre y Enter |
| `s` | Elegir sesión; flechas y Enter; `q` sale |
| `$` | Renombrar sesión |
| `d` | Desconectar este cliente, conservando sesiones y procesos |
| `?` | Mostrar ayuda; `q` sale |
| `:` | Abrir el prompt de comandos de tmux, no el shell |
| `r` | Recargar la configuración instalada; no restaura snapshots |

## Panes

| Después del prefijo | Acción |
|---|---|
| `\` | Dividir izquierda/derecha en el directorio actual |
| `-` | Dividir arriba/abajo en el directorio actual |
| Flechas | Cambiar de panel |
| `m` | Maximizar/restaurar el panel; no cierra los demás |
| `h` / `j` / `k` / `l` | Redimensionar hacia izquierda/abajo/arriba/derecha |

`Ctrl+h/j/k/l` **sin prefijo** es una extensión contextual: depende del terminal,
el plugin y el editor, y reemplaza acciones del shell. Linux tiene el adaptador
Kitty preparado; macOS y el cruce Neovim/tmux no están uniformados. La base
común es **prefijo y flechas**; consulta [Compatibility](training/compatibility.md#contextual-extensions).
No confundirlo con redimensionar **con prefijo**.

## Copy Mode

| Secuencia | Acción |
|---|---|
| Prefijo → `[` | Entrar al historial/modo copia |
| Flechas o `h/j/k/l`, dentro del modo copia | Mover el cursor |
| `v`, dentro del modo copia | Comenzar selección |
| `y`, dentro del modo copia | Copiar y salir |
| `Esc`, dentro del modo copia | Limpiar la selección sin salir |
| `q`, dentro del modo copia | Salir del modo copia |
| Prefijo → `P` mayúscula | Pegar el buffer de tmux |

En macOS, `y` usa `pbcopy`. En Linux usa `wl-copy` o `xclip` según la sesión;
sin backend gráfico, la selección queda disponible en el buffer de tmux.
`Ctrl+Shift+C/V` sigue siendo el portapapeles de Kitty en Linux.

## Save and Restore

Requieren Resurrect cargado; instalar los plugins no es lo mismo que guardar.

| Secuencia | Acción |
|---|---|
| Prefijo → `Ctrl+s` | Guardar el entorno de **todas** las sesiones de este servidor |
| Prefijo → `Ctrl+r` | Restaurar el último entorno guardado |
| Prefijo → `I` mayúscula | Instalar/cargar plugins mediante TPM; requiere red si faltan |

Para guardar: `Ctrl+Espacio`, soltar, luego **`Ctrl+s`**. Para restaurar, la
segunda combinación es **`Ctrl+r`**. No confundirla con `r`, que solo recarga.

Continuum usa un intervalo predeterminado de 15 minutos y depende del refresco
de la barra. **Guarda manualmente antes de reiniciar.** La restauración
automática está desactivada en la configuración versionada.
Restaurar reconstruye el entorno; no resucita procesos ni cambios sin guardar.
Consulta [Persistence](daily-workflow.md#persistence) para los límites.

## Close Safely

Guarda archivos y detén las tareas importantes antes de cerrar terminales.

| Necesidad | Acción |
|---|---|
| Dejar el trabajo vivo y salir | Prefijo → `d` |
| Cerrar un shell que ya terminó su trabajo | `exit` en ese panel |
| Cerrar el panel actual a la fuerza | Prefijo → `x`, confirmar |
| Cerrar la ventana actual con sus paneles | Prefijo → `&`, confirmar |

Para **destruir solo la sesión `work`**, revisa primero la lista de sesiones
y ejecuta deliberadamente:

```sh
rtk proxy tmux kill-session -t '=work'
```

Este comando no pide confirmación, cierra sus terminales y puede perder trabajo
sin guardar. No destruye las otras sesiones ni borra snapshots anteriores.
Para retirar una sesión también del último guardado, consulta
[Retire a Session](daily-workflow.md#retire-a-session).

**No uses `kill-server` ni borres sockets de `/tmp` como rutina de limpieza:**
afectan a todas las sesiones o dificultan recuperarlas.
