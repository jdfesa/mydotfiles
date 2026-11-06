# Kitty on macOS

Este directorio contiene el entrypoint macOS. Conserva `Command+Option` como
`kitty_mod`, configura la tecla Option derecha como Alt y mantiene los bindings
basados en Command fuera de la configuracion Linux.

La base portable sigue en `shared/kitty/common.conf`; el perfil `macos-main`
enlaza este archivo como `~/.config/kitty/kitty.conf`.

## Sessions and Tab Titles

Kitty abre un shell normal y muestra en la pestaña el último componente del
directorio que ve el emulador. No inicia la sesión de Kitty §home§ ni usa
los atajos heredados de sesiones (§Ctrl+b§ y §Ctrl+Shift+s§). Los archivos de
sesión compartidos siguen disponibles para otros perfiles. La paleta, la
transparencia y el estilo de la barra no cambian.

tmux gestiona las sesiones, ventanas y paneles; se inicia o adjunta desde el
shell. Si ya existe una sesión, §tmux a§ permite volver a ella. Los cambios de
atajos y títulos se pueden recargar; para comprobar el arranque sin sesión
hay que cerrar y volver a abrir Kitty cuando no haya trabajo pendiente.
