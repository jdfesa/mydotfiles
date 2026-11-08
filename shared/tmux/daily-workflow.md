# Tmux Daily Workflow

Guía para trabajar con menos ventanas del emulador y poder retomar el entorno.
Los atajos corresponden a `shared/tmux/tmux.conf` y sus entrypoints de Linux y
macOS. La [chuleta](tmux-cheatsheet.md) sirve para consultas rápidas.
Para aprender gradualmente, usa [Tmux Training](training/README.md) y su
[índice vigente](training/keybindings.md).

## Contents

- [Mental Model](#mental-model)
- [First Five Minutes](#first-five-minutes)
- [Daily Routine](#daily-routine)
- [Add Panes Later](#add-panes-later)
- [Persistence](#persistence)
- [Retire a Session](#retire-a-session)
- [When Stuck](#when-stuck)

## Mental Model

- **Kitty/Ghostty:** el emulador que muestra la terminal.
- **Sesión tmux:** un espacio de trabajo con nombre; agrupa ventanas.
- **Ventana tmux:** una tarea, similar a una pestaña; contiene uno o más paneles.
- **Panel:** una terminal dentro de una ventana; ejecuta su propio shell/programa.

```text
Emulador de terminal
└── sesión work
    ├── 1: editor
    ├── 2: comandos
    └── 3: servidor
```

Empieza con una sesión y tres ventanas, no con una sesión por terminal.
En Arch puedes seguir usando `Super+número` para los escritorios; dentro de la
terminal, tmux organiza las tareas. Sus ventanas no son ventanas del compositor.

**Prefijo = `Ctrl+Espacio`.** Pulsa ambas teclas, suéltalas y pulsa la acción.
Por ejemplo, para crear ventana: `Ctrl+Espacio`, soltar, `c`.

## First Five Minutes

### 1. Enter One Workspace

Desde un shell **fuera de tmux**, entra en el directorio de trabajo y ejecuta:

```sh
rtk proxy tmux new-session -A -s work
```

Crea `work` si no existe o vuelve a ella si ya existe. La primera ventana se
abre en el directorio desde el que se crea la sesión. Adjuntar no reinicia
comandos ni cambia los directorios de una sesión existente.

Si Kitty ya estaba abierto antes de cambiar su configuración, usa un proceso
nuevo para cargarla sin recargar el trabajo activo. En Arch:

```sh
rtk proxy kitty --detach --config "$HOME/mydotfiles/os/linux/kitty/kitty.conf"
```

Kitty no inicia tmux automáticamente: ejecuta el comando de entrada dentro de
esa nueva instancia. Las instrucciones de despliegue están en
[Tmux on Linux](../../os/linux/tmux/README.md) y el [README](README.md#macos).

### 2. Give Each Window a Job

1. Prefijo → `,`, escribir `editor`, Enter. Abrir el editor normalmente.
2. Prefijo → `c`, luego prefijo → `,`, escribir `comandos`, Enter.
3. Prefijo → `c`, luego prefijo → `,`, escribir `servidor`, Enter.

En esta configuración `c` crea la ventana en el directorio del panel activo;
usa `cd` si esa tarea necesita otro directorio. Las ventanas empiezan en 1.

### 3. Switch Instead of Opening Another Terminal

- Prefijo → `1`, `2` o `3`: elegir una ventana directamente.
- Prefijo → `n` / `p`: siguiente / anterior.
- Prefijo → `w`: lista de ventanas; flechas, Enter para elegir, `q` para salir.

Cuando haga falta otra terminal para una tarea, prueba primero prefijo → `c`.
Si no encuentras dónde estabas, usa prefijo → `w`. No hace falta memorizar
todos los atajos para empezar.

### 4. Leave and Return

Prefijo → `d` desconecta el cliente y vuelve al shell exterior. Las sesiones
y los programas siguen vivos mientras el servidor tmux y la máquina sigan
funcionando. No es necesario guardar un snapshot para esta desconexión.

Desde el shell exterior, repite el comando de entrada para volver:

```sh
rtk proxy tmux new-session -A -s work
```

`exit` no equivale a desconectar: termina el shell de ese panel. Al cerrar su
último panel desaparece la ventana; al cerrar la última ventana, la sesión.

## Daily Routine

| Momento | Acción |
|---|---|
| Empezar el día sin reinicio | Entrar a `work`; no crear otra sesión con el mismo propósito |
| Necesitar otro shell | Prefijo → `c`; nombrar la ventana con prefijo → `,` |
| Buscar una tarea | Prefijo → `w` |
| Hacer una pausa | Prefijo → `d`; los procesos continúan |
| Antes de reiniciar | Guardar archivos, prefijo → `Ctrl+s` y comprobar el guardado |
| Después de reiniciar | Consultar sesiones; si no existen, seguir el procedimiento de restauración |
| Terminar un espacio de trabajo | Guardar archivos, detener tareas y retirar solo esa sesión |

Cuando una sola sesión resulte cómoda, puedes separar proyectos. Desde fuera
de tmux, por ejemplo:

```sh
rtk proxy tmux new-session -A -s dotfiles -c "$HOME/mydotfiles"
```

Dentro de tmux usa prefijo → `s` para elegir sesión. No ejecutes el comando de
entrada dentro de otra sesión para anidar tmux; si ya estás dentro, el selector
o `rtk proxy tmux switch-client -t '=dotfiles'` cambia a una sesión existente.

## Add Panes Later

Usa ventanas para tareas distintas y paneles cuando necesites ver dos cosas a
la vez, por ejemplo editor y logs.

| Después del prefijo | Acción |
|---|---|
| `\` | Dividir izquierda/derecha |
| `-` | Dividir arriba/abajo |
| Flechas | Cambiar de panel |
| `m` | Maximizar/restaurar el panel sin cerrar los demás |
| `h/j/k/l` | Redimensionar; no navegar |

Con el plugin de navegación y Kitty Linux actualizado, `Ctrl+h/j/k/l` **sin
prefijo** permite navegar entre paneles desde el shell, pero reemplaza acciones
del shell y no garantiza cruzar splits Neovim. Kitty macOS aún tiene otra regla
de envío. La base común son las flechas con prefijo; consulta la
[auditoría de extensiones](training/compatibility.md#contextual-extensions).

## Persistence

### Three Different Operations

| Operación | Qué conserva | Qué no garantiza |
|---|---|---|
| Desconectar (`d`) | Sesiones, terminales y procesos vivos en ese servidor | Sobrevivir a reinicio, apagado o caída del servidor |
| Guardar con Resurrect | Snapshot de sesiones, ventanas, paneles, directorios y disposición | Memoria de procesos, trabajo sin guardar o un backup del proyecto |
| Restaurar con Resurrect | Reconstrucción desde el último snapshot y relanzamiento de programas admitidos | Continuar una compilación, conexión o servidor en su estado anterior |

Guardar/restaurar afecta al entorno de **todas las sesiones de ese servidor**,
no únicamente a la sesión visible. No es una colección independiente de
snapshots por proyecto.

### Current Repository Behavior

- **Resurrect:** prefijo → `Ctrl+s` guarda; prefijo → `Ctrl+r` restaura.
- **Continuum:** intervalo predeterminado de 15 minutos; usa el refresco de la
  barra para intentar guardados periódicos. Con todos los clientes desconectados
  no conviene depender de él: guarda manualmente antes de salir/reiniciar.
- **Restauración automática:** desactivada; la línea
  `@continuum-restore 'on'` está comentada. Restaurar sigue siendo una acción
  explícita, para no recuperar sesiones antiguas sin querer.
- **Captura de paneles:** activada. Los snapshots también pueden guardar texto
  del historial visible/scrollback, no solo nombres y directorios.
- **Arranque automático al encender:** no está habilitado por esta configuración.

Todo lo anterior requiere plugins **instalados y cargados**. La presencia de
las líneas `@plugin` por sí sola no lo garantiza.

### Save Before a Restart

1. Guarda archivos en el editor y detén las tareas que no deban interrumpirse.
2. Pulsa `Ctrl+Espacio`, suelta, pulsa **`Ctrl+s`**.
3. Espera la confirmación de Resurrect y comprueba que existe un snapshot en
   el directorio descrito en [Private State](#private-state). Si la disposición
   no cambió, Resurrect puede conservar el archivo anterior en vez de crear
   otro; una fecha sin cambios no demuestra por sí sola un fallo.
4. Reinicia solo después; no confíes en que el intervalo automático ya pasó.

Este guardado no escribe archivos abiertos del editor ni captura la memoria
de programas. Resurrect puede relanzar aplicaciones admitidas, pero no incluye
todos los procesos arbitrarios. No se habilita la restauración indiscriminada
de comandos: podría repetir acciones con efectos externos.

### Restore After a Restart

1. Desde un shell exterior, consulta `rtk proxy tmux list-sessions`.
2. Si `work` ya está viva, adjunta con `rtk proxy tmux attach-session -t '=work'`;
   no hace falta restaurarla.
3. Si no queda ninguna sesión viva, inicia una sesión de recuperación:

   ```sh
   rtk proxy tmux new-session -s recovery
   ```

4. Pulsa prefijo → **`Ctrl+r`** para restaurar el último snapshot disponible.
5. Usa prefijo → `s` o `w` para elegir el entorno recuperado. Comprueba los
   directorios y vuelve a iniciar manualmente servidores y tareas necesarias.

Una sesión nueva con un solo panel puede ser reemplazada durante la
restauración. Hazlo en una sesión de recuperación sin trabajo importante;
no uses restaurar como sustituto rutinario de adjuntar.

Continuum no guarda inmediatamente al arrancar: deja el intervalo inicial
para recuperar el estado anterior. **Restaura antes de guardar un entorno
vacío**, porque guardar actualizaría el snapshot señalado como último.

La restauración automática es una capacidad opcional de Continuum, pero
habilitarla requiere un cambio de configuración revisado. Se ejecuta al
arrancar el servidor tmux, no por recargar el archivo ni por adjuntar a un
servidor existente. No es necesaria para este flujo manual.

### Private State

En las versiones de plugins verificadas, la ruta de Resurrect se elige así:

1. `@resurrect-dir`, si se configuró explícitamente.
2. `~/.tmux/resurrect`, si ese directorio ya existía al cargar el plugin.
3. `${XDG_DATA_HOME:-$HOME/.local/share}/tmux/resurrect`, en caso contrario.

El enlace `last` apunta al snapshot más reciente. Consulta su fecha y la del
archivo apuntado sin publicar su contenido. Los guardados pueden incluir
comandos, rutas y texto sensible: deben permanecer fuera del clon y de Git.
Son estado privado local, no un mecanismo de sincronización entre máquinas.

Para conservarlos ante pérdida del disco, hace falta una copia de seguridad
privada y cifrada; versionar los dotfiles no conserva esos snapshots ni los
archivos de los proyectos.

## Retire a Session

**Desconectar no termina una sesión.** Para terminar solo `work`:

1. Guarda sus archivos y detén limpiamente servidores/tareas desde cada panel.
2. Consulta `rtk proxy tmux list-sessions` y comprueba el nombre exacto.
3. Ejecuta deliberadamente:

   ```sh
   rtk proxy tmux kill-session -t '=work'
   ```

El comando no pide confirmación. Destruye esa sesión y cierra sus terminales;
puede perder trabajo sin guardar. El `=` exige coincidencia exacta para no
seleccionar otra sesión por prefijo. No destruye las otras sesiones; si las hay,
el cliente puede pasar a una de ellas debido a `detach-on-destroy off`.

### Saved State Is Separate

Matar `work` **no la elimina de snapshots anteriores**. Si restauras uno que
la contiene, puede volver a aparecer.

- Si quedan otras sesiones y quieres que el último snapshot ya no incluya
  `work`, entra a una de ellas y guarda con prefijo → `Ctrl+s` después del cierre.
- Si era la última sesión, no hay un entorno vivo desde el que guardar:
  cuando inicies el siguiente espacio de trabajo, guarda ese nuevo entorno
  en lugar de restaurar el anterior.
- Esto actualiza `last`, pero no borra copias históricas. Si además necesitas
  eliminar datos privados guardados, revisa/archiva o elimina deliberadamente
  esos backups fuera de Git; no uses borrados globales como parte del flujo diario.

No uses `kill-server` para terminar un proyecto: destruye **todas** las sesiones
de ese servidor. No elimines sockets de `/tmp` para «empezar limpio»; un socket
no es una copia de seguridad ni su borrado es un cierre ordenado.

## When Stuck

| Problema | Consulta o acción |
|---|---|
| No recuerdo dónde estaba | Prefijo → `w` para ventanas o `s` para sesiones |
| No recuerdo los atajos | Prefijo → `?`; `q` sale |
| No sé si estoy dentro de tmux | `rtk proxy printenv TMUX`; una variable vacía/ausente suele indicar que estás fuera |
| Un atajo no responde | Confirmar que se soltó el prefijo, que el servidor cargó la config y que Kitty/compositor no intercepta la tecla |
| Duda sobre el prefijo cargado | Con servidor activo: `rtk proxy tmux show-options -gv prefix`; debe mostrar `C-Space` |
| `Ctrl+s`/`Ctrl+r` no guarda/restaura | Verificar bindings con `rtk proxy tmux list-keys -T prefix C-s` y el equivalente `C-r`; comprobar TPM/plugins |
| Resurrect avisa `hostname: command not found` en Arch | Instalar `inetutils` según la [guía Linux](../../os/linux/tmux/README.md#installation); proporciona la utilidad que resuelve rutas del plugin |
| Un plugin está instalado pero no cargado | Instalar/verificar según la guía de plataforma; no recargar servidores de trabajo a ciegas |
| No se guarda automáticamente | Revisar barra activa y que `status-right` siga incluyendo `continuum_save.sh`; varios servidores pueden limitar el autosave |
| Tras reiniciar no hay sesión | Adjuntar no reconstruye: usar Resurrect si existe un snapshot |
| Una sesión eliminada reaparece | Se restauró un snapshot antiguo; seguir [Saved State Is Separate](#saved-state-is-separate) |

Para probar cambios técnicos, usa un `HOME` y un socket temporales. Nunca mates
ni reinicies el servidor de trabajo como prueba de persistencia.

## References

- [Tmux Getting Started](https://github.com/tmux/tmux/wiki/Getting-Started).
- [Configuración de referencia](https://github.com/hendrikmi/dotfiles/blob/01b73ac65c3680d38407f88d2d143f330b09577b/tmux/tmux.conf), con aviso [MIT](LICENSE).
- [Tmux Resurrect](https://github.com/tmux-plugins/tmux-resurrect) y su
  [lista de programas restaurables](https://github.com/tmux-plugins/tmux-resurrect/blob/master/docs/restoring_programs.md).
- [Tmux Continuum](https://github.com/tmux-plugins/tmux-continuum) y su
  [FAQ](https://github.com/tmux-plugins/tmux-continuum/blob/master/docs/faq.md).
