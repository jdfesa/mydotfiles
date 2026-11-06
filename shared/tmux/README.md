# Tmux

`tmux.conf` conserva sin cambios la [configuración de
hendrikmi/dotfiles](https://github.com/hendrikmi/dotfiles/blob/01b73ac65c3680d38407f88d2d143f330b09577b/tmux/tmux.conf).
El aviso MIT correspondiente está en [LICENSE](LICENSE).

## macOS

Homebrew instala tmux como parte del manifiesto base. El perfil `macos-main`
enlaza `os/macos/tmux/tmux.conf` en `~/.config/tmux/tmux.conf`. Ese archivo
carga la configuración compartida y mueve la barra de estado abajo, sin cambiar
los atajos de tmux. Ghostty abre o recupera `mydotfiles` al iniciar.

El archivo compartido inicia Zsh, usa `pbcopy` para el portapapeles de macOS y
busca TPM en `~/.tmux/plugins/tpm/tpm`. Si falta TPM, no se cargan los plugins.
Para un despliegue real, revisa primero el perfil con
`scripts/link --dry-run macos-main` y sigue las
[instrucciones de TPM](https://github.com/tmux-plugins/tpm#installation).
Con TPM disponible, el prefijo seguido de `I` mayúscula instala los plugins,
incluido el monitor de CPU y memoria. El historial y los archivos de
restauración pueden contener información privada y deben quedar fuera de Git.

## Quick Start

Si la sesión ya existe, `tmux a` vuelve a la última sesión activa. `tmux ls`
lista las sesiones; usa `tmux a -t mydotfiles` para elegir esa en particular.
Si todavía no existe, crea o recupera la sesión con:

```sh
tmux new-session -A -s mydotfiles -c "$HOME/mydotfiles"
```

Dentro de tmux, pulsa **`Ctrl+Espacio`**, suelta ambas teclas y presiona la
segunda tecla. Para la ayuda, usa `?` (`Shift+/` en un teclado US), **sin**
mantener `Ctrl`.

| Tecla después del prefijo | Acción |
|---|---|
| `?` | Mostrar los atajos; `q` cierra la ayuda |
| `c` | Crear una ventana en el directorio del panel activo |
| `\` | Dividir izquierda/derecha |
| `-` | Dividir arriba/abajo |
| Flechas | Cambiar de panel |
| `m` | Maximizar o restaurar el panel |
| `s` / `w` | Elegir sesión o ventana |
| `d` | Desconectarse sin cerrar la sesión |

Una sesión agrupa ventanas; cada ventana puede tener varios paneles con sus
propias terminales. Al desconectarte con `d`, los procesos siguen ejecutándose
mientras el servidor tmux siga vivo. Tras un reinicio, los plugins pueden
reconstruir una disposición guardada, pero no mantienen vivos esos procesos.

## Keyboard Conflicts

Para que `Ctrl+Espacio` llegue a tmux en macOS, ve a **Ajustes del Sistema →
Teclado → Atajos de teclado → Fuentes de entrada** y desactiva **Seleccionar
la fuente de entrada anterior** si usa esa combinación. Es un ajuste local;
el perfil del repositorio no lo cambia.

`home` y `dotfiles` son nombres de sesiones de Kitty, no sesiones de tmux.
La sesión `dotfiles` de Kitty usa `~/mydotfiles` como directorio.

Para probar cambios sin afectar el servidor habitual, usa un `HOME` y un
socket de tmux separados.
