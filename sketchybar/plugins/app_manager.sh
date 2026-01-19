#!/bin/bash

# $CONFIG_DIR/plugins/app_manager.sh

source "$CONFIG_DIR/colors.sh"
source "$CONFIG_DIR/plugins/icon_map.sh"

# Anchor item to position apps after
ANCHOR="apps_start"

render_apps() {
    # 1. Get AeroSpace Data
    # list-windows returns: [{"window-id": 123, "app-name": "Chrome", "window-title": "..."}]
    WINDOWS=$(aerospace list-windows --workspace focused --json)
    FOCUSED_ID=$(aerospace list-windows --focused --format %{window-id})

    # 2. Get currently tracked items from Sketchybar
    # We prefix items with "app."
    CURRENT_ITEMS=$(sketchybar --query bar | jq -r '.items[] | select(startswith("app."))')

    # 3. Identify Stale Items (Items in Sketchybar but not in AeroSpace)
    EXISTING_IDS=()
    for item in $CURRENT_ITEMS; do
        id="${item#app.}"
        # Check if id exists in WINDOWS json
        # using string matching for simplicity
        if echo "$WINDOWS" | grep -q "\"window-id\":$id"; then
            EXISTING_IDS+=("$id")
        else
            # Remove stale item
            sketchybar --remove "$item"
        fi
    done

    # 4. Add/Update Items
    # Process each window from AeroSpace
    echo "$WINDOWS" | jq -c '.[]' | while read -r window; do
        id=$(echo "$window" | jq -r '."window-id"')
        app=$(echo "$window" | jq -r '."app-name"')
        title=$(echo "$window" | jq -r '."window-title"')

        item_name="app.$id"

        # Check if we need to add it
        # We can check if it was in EXISTING_IDS, or just try to update and if fail add?
        # Creating valid list for robust check is hard in bash loop.
        # Sketchybar is fast, we can verify existence via query or just blindly add if missing.
        # Efficient approach: just check if it was in CURRENT_ITEMS.

        exists=false
        if echo "$CURRENT_ITEMS" | grep -q "^$item_name$"; then
            exists=true
        fi

        icon_map "$app"
        icon=$icon_result

        # Stylometry
        if [ "$id" = "$FOCUSED_ID" ]; then
            icon_color=$WHITE
            background_color=$GREY # Active highlight
            # Focused: Normal size
            icon_font="sketchybar-app-font:Regular:16.0"
        else
            # Unfocused: Dimmed and smaller ("opacas y mas chicas")
            icon_color=0xff505050 # Darker grey/transparent
            background_color=$BACKGROUND_2 
            icon_font="sketchybar-app-font:Regular:14.0"
        fi

        if [ "$exists" = "false" ]; then
            # Add new item
            sketchybar --add item "$item_name" left \
                       --set "$item_name" \
                             script="$CONFIG_DIR/plugins/app_click.sh" \
                             icon="$icon" \
                             icon.font="$icon_font" \
                             icon.color="$icon_color" \
                             label.drawing=off \
                             background.color="$background_color" \
                             background.padding_left=5 \
                             background.padding_right=5 \
                             background.corner_radius=5 \
                             background.height=24 \
                             icon.padding_left=4 \
                             icon.padding_right=4 \
                             click_script="$CONFIG_DIR/plugins/app_click.sh" \
                       --move "$item_name" after "$ANCHOR"
        else
            # Update existing
            sketchybar --set "$item_name" \
                             icon="$icon" \
                             icon.font="$icon_font" \
                             background.color="$background_color" \
                             icon.color="$icon_color"
        fi
        
        # Update Anchor for next item to keep order? 
        # Actually stickybar adds "after" so if we keep adding "after anchors", order reverses or stays?
        # "move item after anchor" places it immediately after anchor.
        # If we loop, order might invert.
        # To maintain order, we should update ANCHOR to current item
        ANCHOR="$item_name"
    done
}

render_apps
