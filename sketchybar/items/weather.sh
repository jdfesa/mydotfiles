#!/bin/bash

sketchybar --add item weather right \
  --set weather \
    script="$PLUGIN_DIR/weather.sh" \
    icon= \
    icon.font="$FONT:Bold:24.0" \
    update_freq=300 \
    label.padding_left=0 \
    icon.padding_right=8 \
    label.color=$LABEL_COLOR \
    icon.color=$ICON_COLOR \
    drawing=on \
  --subscribe weather system_woke
