# Tmux Layouts

Layouts guardados para restaurar arreglos de panes.

## Layouts importados

- `7030`: layout con pane principal y pane secundario.
- `2x3`: layout de seis panes.

## Crear un layout nuevo

Dentro de una ventana de tmux, ajustar los panes y guardar el layout:

```bash
LAYOUT_NAME="new-layout"
LAYOUT_KEYBIND="L"

mkdir -p ~/mydotfiles/tmux/layouts/$LAYOUT_NAME
tmux display-message -p '#{window_layout}' > ~/mydotfiles/tmux/layouts/$LAYOUT_NAME/layout.txt
```

Crear `apply_layout.sh` dentro de la carpeta del layout:

```bash
#!/bin/bash

LAYOUT=$(cat ~/mydotfiles/tmux/layouts/new-layout/layout.txt)
tmux select-layout "$LAYOUT"
```

Luego hacerlo ejecutable:

```bash
chmod +x ~/mydotfiles/tmux/layouts/$LAYOUT_NAME/apply_layout.sh
```

Y agregar un bind en `tmux/tmux.conf`:

```tmux
bind L run-shell "~/mydotfiles/tmux/layouts/new-layout/apply_layout.sh"
```
