# Kitty on Linux

Este directorio contiene el entrypoint Linux. Define nombres de modificadores
propios de Linux y los bindings de clipboard `Ctrl+Shift+C/V`, y luego incluye
la base portable de `shared/kitty/common.conf`.

El perfil enlaza archivos individuales dentro de `~/.config/kitty/` para que
el entrypoint Linux pueda cambiar sin afectar macOS.

## Sessions and Tab Titles

Como en macOS, Kitty abre Zsh sin cargar la sesión heredada `home`; tmux
gestiona sesiones, ventanas y paneles. Se desactivan los atajos de sesiones
Kitty `Ctrl+b` y `Ctrl+Shift+s`, sin cambiar la paleta ni la transparencia.

La pestaña muestra el último componente del directorio que ve Kitty. Una
pestaña nueva carga la integración de shell que refresca ese título al volver
al prompt después de `cd`. Dentro de tmux, ese título no sigue cada panel.

`Ctrl+h/j/k/l` se envía a Neovim o tmux cuando uno de ellos está en primer
plano. Con `vim-tmux-navigator`, esas teclas navegan entre paneles desde el
shell; cruzar splits Neovim requiere integración en el editor. Fuera de esas
aplicaciones conservan la navegación de ventanas Kitty. Consulta las
[limitaciones actuales](../../../shared/tmux/training/compatibility.md#contextual-extensions).
El portapapeles externo sigue usando `Ctrl+Shift+C/V`.

Consulta [Tmux on Linux](../tmux/README.md) para instalar y verificar el flujo.
Si Kitty ya estaba abierto antes de actualizar el archivo, inicia un proceso
nuevo con el entrypoint actualizado; una pestaña del proceso anterior por sí
sola no recarga sus opciones. No hace falta cerrar ni recargar el trabajo activo.
