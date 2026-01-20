#!/bin/bash

ram_top=(
  label.font="$FONT:Semibold:7"
  label=RAM
  icon.drawing=off
  width=0
  padding_right=15
  y_offset=6
)

ram_percent=(
  label.font="$FONT:Heavy:12"
  label=RAM
  y_offset=-4
  padding_right=15
  width=55
  icon.drawing=off
  update_freq=4
  script="$PLUGIN_DIR/ram.sh"
)

sketchybar --add item ram.top right              \
           --set ram.top "${ram_top[@]}"         \
                                                 \
           --add item ram.percent right          \
           --set ram.percent "${ram_percent[@]}"
