#!/bin/bash

# $CONFIG_DIR/plugins/app_click.sh

# Extract Target ID from Item Name (app.123 -> 123)
TARGET_ID="${NAME#*.}"

# Get Currently Focused ID
CURRENT_ID=$(aerospace list-windows --focused --format %{window-id})

if [ "$TARGET_ID" = "$CURRENT_ID" ]; then
  # Already focused, maybe just do nothing or toggle something?
  # User request: "click -> visualize a mi izquierda".
  # If it's already focused, it's probably already visible.
  exit 0
fi

# Execute the dance
# 1. Focus Target
aerospace focus --window-id "$TARGET_ID"

# 2. Move Target Left
aerospace move left

# 3. Refocus Original
aerospace focus --window-id "$CURRENT_ID"
