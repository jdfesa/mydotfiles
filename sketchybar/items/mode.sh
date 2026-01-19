#!/bin/bash

# $CONFIG_DIR/items/mode.sh

sketchybar --add event mode_change

mode_item=(
  script="$PLUGIN_DIR/mode.sh"
  icon=􀀁
  label.font="sketchybar-app-font:Bold:16.0"
  label.color=$RED
  icon.drawing=off
  drawing=off
  background.color=$BACKGROUND_1
  background.border_color=$RED
  background.border_width=2
)

sketchybar --add item mode_indicator center \
           --set mode_indicator "${mode_item[@]}" \
           --subscribe mode_indicator mode_change
