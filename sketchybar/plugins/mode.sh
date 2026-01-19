#!/bin/bash

# $CONFIG_DIR/plugins/mode.sh

# The mode name is passed via the MODE environment variable from AeroSpace
if [ "$MODE" = "" ] || [ "$MODE" = "NORMAL" ]; then
  sketchybar --set $NAME label="" drawing=off
else
  sketchybar --set $NAME label="$MODE" drawing=on
fi
