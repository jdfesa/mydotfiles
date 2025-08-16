#!/bin/bash

sketchybar --add item network right \
  --set network \
    script="$PLUGIN_DIR/network.sh" \
    update_freq=5 \
    icon.drawing=off \
    label.color=$LABEL_COLOR \
    label.font="$FONT:Semibold:12.0" \
    drawing=on
