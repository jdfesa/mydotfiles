#!/bin/bash

# ~/.mydotfiles/aerospace/scripts/borders_mode.sh
# Usage: ./borders_mode.sh [MODE_NAME]

set -u

BORDERS_BIN="/usr/local/bin/borders"
MODE="${1:-NORMAL}"

if [ ! -x "$BORDERS_BIN" ]; then
  exit 0
fi

# Default Color (Blue)
COLOR="0xff8aadf4"

case "$MODE" in
  "RESIZE")
    COLOR="0xffff0000" # Red
    ;;
  "SERVICE")
    COLOR="0xffed8796" # Pink
    ;;
  "NORMAL"|"")
    COLOR="0xff8aadf4" # Blue (Default)
    ;;
esac

# Apply the color
"$BORDERS_BIN" active_color="$COLOR"
