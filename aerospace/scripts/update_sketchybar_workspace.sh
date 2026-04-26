#!/bin/bash
# Script llamado por aerospace exec-on-workspace-change.
# Actualiza el highlight de los workspaces en Sketchybar via CLI directo.
# AeroSpace pasa $AEROSPACE_FOCUSED_WORKSPACE como variable de entorno.

FOCUSED="$AEROSPACE_FOCUSED_WORKSPACE"
SBAR="/usr/local/bin/sketchybar"
WORKSPACES=(U I O P Y N)

# Colores Catppuccin Mocha (ARGB hex)
COLOR_LAVENDER=0xffb4befe   # borde activo
COLOR_SURFACE1=0xff45475a   # borde inactivo

for ws in "${WORKSPACES[@]}"; do
  if [ "$ws" = "$FOCUSED" ]; then
    $SBAR --set "space.$ws" \
      icon.highlight=on \
      label.highlight=on \
      background.border_color="$COLOR_LAVENDER"
  else
    $SBAR --set "space.$ws" \
      icon.highlight=off \
      label.highlight=off \
      background.border_color="$COLOR_SURFACE1"
  fi
done
