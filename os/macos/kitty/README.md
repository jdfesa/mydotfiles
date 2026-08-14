# Kitty on macOS

Este directorio contiene el entrypoint macOS. Conserva `Command+Option` como
`kitty_mod`, configura la tecla Option derecha como Alt y mantiene los bindings
basados en Command fuera de la configuracion Linux.

La base portable sigue en `shared/kitty/common.conf`; el perfil `macos-main`
enlaza este archivo como `~/.config/kitty/kitty.conf`.
