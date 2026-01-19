#!/bin/bash

source "$CONFIG_DIR/colors.sh"

# Extract SID from name (e.g. space.1 -> 1)
SID="${NAME#*.}"

update() {
  # AEROSPACE_FOCUSED_WORKSPACE is passed via the trigger or environment
  if [ "$FOCUSED_WORKSPACE" = "$SID" ]; then
    sketchybar --set $NAME icon.highlight=on \
                           label.highlight=on \
                           background.border_color=$GREY
  else
    sketchybar --set $NAME icon.highlight=off \
                           label.highlight=off \
                           background.border_color=$BACKGROUND_2
  fi
}

mouse_clicked() {
  # AeroSpace command to switch workspace
  aerospace workspace "$SID"
}

case "$SENDER" in
  "mouse.clicked") mouse_clicked
  ;;
  "aerospace_workspace_change") update
  ;;
  *) update
  ;;
esac

