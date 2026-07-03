#!/bin/bash

set -u

SBAR="/usr/local/bin/sketchybar"
MODE="${1:-NORMAL}"

if [ ! -x "$SBAR" ]; then
  exit 0
fi

case "$MODE" in
  SERVICE)
    ICON="[S]"
    COLOR="0xffed8796"
    ;;
  RESIZE)
    ICON="[R]"
    COLOR="0xffff0000"
    ;;
  NORMAL|"")
    "$SBAR" --set aerospace_mode drawing=off
    exit 0
    ;;
  *)
    "$SBAR" --set aerospace_mode drawing=off
    exit 0
    ;;
esac

"$SBAR" --set aerospace_mode \
  drawing=on \
  icon="$ICON" \
  icon.color="$COLOR" \
  background.border_color="$COLOR"
