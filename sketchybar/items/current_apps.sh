#!/bin/bash

# $CONFIG_DIR/items/current_apps.sh

# 1. Create Anchor Item (Start of list)
sketchybar --add item apps_start left \
           --set apps_start drawing=off \
           --move apps_start after space.8

# 2. Logic Controller (Manager)
# This item doesn't draw anything, it just runs the script on events
app_manager=(
  script="$PLUGIN_DIR/app_manager.sh"
  updates=on
  drawing=off
)

sketchybar --add item app_manager left \
           --set app_manager "${app_manager[@]}" \
           --subscribe app_manager aerospace_workspace_change front_app_switched space_windows_change

