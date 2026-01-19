#!/bin/bash

# ~/.mydotfiles/aerospace/scripts/borders_mode.sh
# Usage: ./borders_mode.sh [MODE_NAME]

BORDERS_BIN="/usr/local/bin/borders"
MODE="$1"

# Default Color (Blue)
COLOR="0xff8aadf4"

case "$MODE" in
  "RESIZE")
    COLOR="0xffff0000" # Red
    ;;
  "LAYOUT")
    COLOR="0xffa6da95" # Green
    ;;
  "SERVICE")
    COLOR="0xffed8796" # Pink
    ;;
  "PERSISTENCE")
    COLOR="0xffc6a0f6" # Purple
    ;;
  "NORMAL"|"")
    COLOR="0xff8aadf4" # Blue (Default)
    ;;
esac

# Apply the color
"$BORDERS_BIN" active_color="$COLOR"
