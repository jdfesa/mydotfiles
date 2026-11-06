# Tmux

`tmux.conf` conserva sin cambios la [configuración de
hendrikmi/dotfiles](https://github.com/hendrikmi/dotfiles/blob/01b73ac65c3680d38407f88d2d143f330b09577b/tmux/tmux.conf).
El aviso MIT correspondiente está en [LICENSE](LICENSE).

## macOS

Homebrew instala tmux como parte del manifiesto base. El perfil `macos-main`
enlaza el archivo en `~/.config/tmux/tmux.conf`. Ghostty abre o recupera la
sesión `mydotfiles` sin un script intermedio. Kitty conserva sus atajos
propios; el prefijo de tmux no es `Ctrl+b`.

El archivo inicia Zsh, usa `pbcopy` para el portapapeles de macOS y busca TPM
en `~/.tmux/plugins/tpm/tpm`. Si falta TPM, no se cargan los plugins. Para
un despliegue real, revisa primero el perfil con
`scripts/link --dry-run macos-main` y sigue las
[instrucciones de TPM](https://github.com/tmux-plugins/tpm#installation).
Una vez disponible TPM, `Ctrl+Espacio` seguido de `I` instala los plugins
declarados en el archivo. El historial y los archivos de restauración
pueden contener información privada y deben quedar fuera de Git.

## Quick Start

```sh
tmux new-session -A -s mydotfiles -c "$HOME/mydotfiles"
```

El prefijo es **`Ctrl+Espacio`**. Pulsa y suelta la combinación antes de
presionar la segunda tecla:

| Tecla | Acción |
|---|---|
| `c` | Crear una ventana en el directorio del panel activo |
| `\` | Dividir izquierda/derecha |
| `-` | Dividir arriba/abajo |
| Flechas | Cambiar de panel |
| `m` | Maximizar o restaurar el panel |
| `s` / `w` | Elegir sesión o ventana |
| `d` | Desconectarse sin cerrar la sesión |

Las divisiones también heredan el directorio del panel activo. Ejecuta
`tmux attach-session -t mydotfiles` para volver a la sesión. Tras un reinicio,
los plugins de restauración pueden reconstruir la disposición guardada; no
mantienen vivos los procesos que estaban ejecutándose.

## Keyboard Conflicts

Si `Ctrl+Espacio` no llega a tmux, revisa **Ajustes del Sistema → Teclado →
Atajos de teclado → Fuentes de entrada**. macOS puede reservar esa
combinación para cambiar de fuente de entrada. Este repositorio no modifica
ese ajuste del sistema.

Para probar la configuración sin afectar el servidor habitual, usa un
`HOME` y un socket de tmux separados. No recargues una sesión de trabajo
para hacer la prueba.
