#!/bin/bash
# Script llamado por aerospace exec-on-workspace-change.
# Actualiza el highlight de los workspaces en Sketchybar via CLI directo.
# AeroSpace pasa $AEROSPACE_FOCUSED_WORKSPACE como variable de entorno.

FOCUSED="${AEROSPACE_FOCUSED_WORKSPACE:-}"
AEROSPACE="${AEROSPACE_BIN:-/usr/local/bin/aerospace}"
SBAR="${SKETCHYBAR_BIN:-/usr/local/bin/sketchybar}"

# Consultar el proceso evita duplicar IDs y soporta una migración gradual.
# Las rutas alternativas permiten probar el hook sin tocar la sesión gráfica.
WORKSPACES=$("$AEROSPACE" list-workspaces --all) || exit 1

# Colores Catppuccin Mocha (ARGB hex)
COLOR_LAVENDER=0xffb4befe   # borde activo
COLOR_SURFACE1=0xff45475a   # borde inactivo

while IFS= read -r ws; do
  [ -n "$ws" ] || continue
  if [ "$ws" = "$FOCUSED" ]; then
    "$SBAR" --set "space.$ws" \
      icon.highlight=on \
      label.highlight=on \
      background.border_color="$COLOR_LAVENDER"
  else
    "$SBAR" --set "space.$ws" \
      icon.highlight=off \
      label.highlight=off \
      background.border_color="$COLOR_SURFACE1"
  fi
done <<< "$WORKSPACES"
