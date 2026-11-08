# Current Keybinding Contract

Índice vigente, no todos los defaults de tmux. Prefijo único **`C-Space`
(`Ctrl+Espacio`)**; `prefix2` es `None`. Ventanas y paneles empiezan en 1.
No se sustituye Control por Command o Super.

## Sources of Truth

- [Base compartida](../tmux.conf): atajos comunes.
- [Linux](../../../os/linux/tmux/tmux.conf) y [macOS](../../../os/macos/tmux/tmux.conf): adaptadores.
- [Kitty Linux](../../../os/linux/kitty/kitty.conf) y [Kitty macOS](../../../os/macos/kitty/kitty.conf): qué teclas llegan.
- [Compatibility](compatibility.md): evidencia actual, separada del contrato deseado.

`core` es tmux sin plugins; `plugin` exige instalación y carga. No significa
que cualquier sistema/terminal deje pasar la tecla. El nivel indica cuándo
practicarla. Las filas core se contrastan con ambos entrypoints mediante
`scripts/test-linux-terminal`; las filas de plugin quedan fuera de esa prueba
sin plugins.

## Binding Index

`prefix`: pulsar/soltar el prefijo antes de Key. `copy-mode-vi`: ya dentro del
modo copia, sin repetirlo. `root`: sin prefijo, extensión contextual.

| Table | Key | Command | Nivel | Clase | Acción |
|---|---|---|---|---|---|
| `prefix` | `c` | `new-window` | 1 | core | Crear ventana en cwd |
| `prefix` | `1` | `select-window` | 1 | core | Ventana 1 |
| `prefix` | `2` | `select-window` | 1 | core | Ventana 2 |
| `prefix` | `3` | `select-window` | 1 | core | Ventana 3 |
| `prefix` | `n` | `next-window` | 1 | core | Siguiente |
| `prefix` | `p` | `previous-window` | 1 | core | Anterior |
| `prefix` | `w` | `choose-tree` | 1 | core | Selector de ventanas |
| `prefix` | `,` | `rename-window` | 1 | core | Renombrar ventana |
| `prefix` | `?` | `list-keys` | 1 | core | Ayuda; q sale |
| `prefix` | `d` | `detach-client` | 2 | core | Desconectar |
| `prefix` | `s` | `choose-tree` | 2 | core | Selector de sesiones |
| `prefix` | `$` | `rename-session` | 2 | core | Renombrar sesión |
| `prefix` | `\` | `split-window -h` | 3 | core | Izquierda/derecha |
| `prefix` | `-` | `split-window -v` | 3 | core | Arriba/abajo |
| `prefix` | `Left` | `select-pane -L` | 3 | core | Panel izquierdo |
| `prefix` | `Right` | `select-pane -R` | 3 | core | Panel derecho |
| `prefix` | `Up` | `select-pane -U` | 3 | core | Panel superior |
| `prefix` | `Down` | `select-pane -D` | 3 | core | Panel inferior |
| `prefix` | `m` | `resize-pane -Z` | 3 | core | Maximizar/restaurar |
| `prefix` | `h` | `resize-pane -L` | 3 | core | Redimensionar izquierda |
| `prefix` | `j` | `resize-pane -D` | 3 | core | Redimensionar abajo |
| `prefix` | `k` | `resize-pane -U` | 3 | core | Redimensionar arriba |
| `prefix` | `l` | `resize-pane -R` | 3 | core | Redimensionar derecha |
| `prefix` | `[` | `copy-mode` | 4 | core | Historial |
| `copy-mode-vi` | `v` | `begin-selection` | 4 | core | Seleccionar |
| `copy-mode-vi` | `y` | `copy-pipe-and-cancel` | 4 | core | Copiar con backend del sistema |
| `copy-mode-vi` | `Escape` | `clear-selection` | 4 | core | Limpiar selección |
| `copy-mode-vi` | `q` | `cancel` | 4 | core | Salir del modo copia |
| `prefix` | `P` | `paste-buffer` | 4 | core | Pegar buffer tmux |
| `prefix` | `C-s` | `save.sh` | 5 | plugin | Resurrect: guardar |
| `prefix` | `C-r` | `restore.sh` | 5 | plugin | Resurrect: restaurar |
| `prefix` | `I` | `install_plugins` | 5 | plugin | TPM: instalar/cargar |
| `prefix` | `x` | `kill-pane` | 6 | core | Cerrar panel con confirmación |
| `prefix` | `&` | `kill-window` | 6 | core | Cerrar ventana con confirmación |
| `prefix` | `:` | `command-prompt` | consulta | core | Prompt tmux |
| `prefix` | `r` | `source-file` | consulta | core | Recargar, no restaurar |
| `root` | `C-h` | `select-pane -L` | opcional | plugin | Navegación contextual |
| `root` | `C-j` | `select-pane -D` | opcional | plugin | Navegación contextual |
| `root` | `C-k` | `select-pane -U` | opcional | plugin | Navegación contextual |
| `root` | `C-l` | `select-pane -R` | opcional | plugin | Navegación contextual |

## Stability Rules

- Conservar el núcleo en Arch/macOS; resolver interceptores por capa.
- No presentar atajos sin prefijo como equivalentes universales del núcleo.
- Actualizar índice, ejercicio y chuleta cuando se modifica un binding.
- Verificar teclado, shell, terminal, plugins y clipboard antes de declarar
  compatible una nueva plataforma; los mismos gestos no garantizan las rutas
  de ejecutables ni el despliegue.
