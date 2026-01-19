#!/bin/bash

# $CONFIG_DIR/items/current_apps.sh

current_apps=(
  script="$PLUGIN_DIR/current_apps.sh"
  icon.drawing=off
  label.font="sketchybar-app-font:Regular:16.0"
  label.color=$WHITE
  background.padding_left=10
  background.padding_right=10
  associated_display=active
)

sketchybar --add item current_apps left \
           --set current_apps "${current_apps[@]}" \
           --subscribe current_apps aerospace_workspace_change front_app_switched space_windows_change
