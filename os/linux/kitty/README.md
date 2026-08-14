# Kitty on Linux

Este directorio contiene el entrypoint Linux. Define nombres de modificadores
propios de Linux y los bindings de clipboard `Ctrl+Shift+C/V`, y luego incluye
la base portable de `shared/kitty/common.conf`.

El perfil enlaza archivos individuales dentro de `~/.config/kitty/` para que
el entrypoint Linux pueda cambiar sin afectar macOS.
