#!/bin/bash

# AeroSpace Workspaces (1-8 as defined in aerospace.toml)
SPACE_ICONS=("1" "2" "3" "4" "5" "6" "7" "8")

# Add custom event for AeroSpace
sketchybar --add event aerospace_workspace_change

for i in "${!SPACE_ICONS[@]}"
do
  sid=$(($i+1))

  space=(
    space=$sid
    icon="${SPACE_ICONS[i]}"
    icon.padding_left=10
    icon.padding_right=10
    padding_left=2
    padding_right=2
    label.padding_right=20
    icon.highlight_color=$GREEN
    label.color=$GREY
    label.highlight_color=$WHITE
    label.font="sketchybar-app-font:Regular:16.0"
    label.y_offset=-1
    background.color=$BACKGROUND_1
    background.border_color=$BACKGROUND_2
    script="$PLUGIN_DIR/space.sh"
  )

  sketchybar --add item space.$sid left    \
             --set space.$sid "${space[@]}" \
             --subscribe space.$sid aerospace_workspace_change mouse.clicked
done

# We don't need space_creator for local workspaces typically, but keeping it simple for now or removing if unused.
# Removing space_creator as AeroSpace handles creation/static workspaces.

