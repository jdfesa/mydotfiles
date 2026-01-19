#!/bin/bash

# $CONFIG_DIR/plugins/app_manager.sh

source "$CONFIG_DIR/colors.sh"
source "$CONFIG_DIR/plugins/icon_map.sh"

# Anchor item to position apps after
ANCHOR="apps_start"

render_apps() {
    # 1. Get AeroSpace Data
    WINDOWS=$(aerospace list-windows --workspace focused --json)
    FOCUSED_WINDOW_ID=$(aerospace list-windows --focused --format %{window-id})
    # Get Focused Workspace ID (1-8) to position the anchor
    FOCUSED_WORKSPACE_ID=$(aerospace list-workspaces --focused)

    # Move the Anchor to the current workspace
    sketchybar --move apps_start after space.$FOCUSED_WORKSPACE_ID

    # 2. Get currently tracked items
    CURRENT_ITEMS=$(sketchybar --query bar | jq -r '.items[] | select(startswith("app."))')

    # 3. Identify Stale Items
    EXISTING_IDS=()
    for item in $CURRENT_ITEMS; do
        id="${item#app.}"
        if echo "$WINDOWS" | grep -q "\"window-id\":$id"; then
            EXISTING_IDS+=("$id")
        else
            sketchybar --remove "$item"
        fi
    done

    # 4. Add/Update Items & Maintain Order
    # We must explicitly move items every time to ensure they follow the apps_start anchor
    # which just moved.
    
    # Reset Anchor to start
    ANCHOR="apps_start"

    echo "$WINDOWS" | jq -c '.[]' | while read -r window; do
        id=$(echo "$window" | jq -r '."window-id"')
        app=$(echo "$window" | jq -r '."app-name"')
        
        item_name="app.$id"
        exists=false
        if echo "$CURRENT_ITEMS" | grep -q "^$item_name$"; then
            exists=true
        fi

        icon_map "$app"
        icon=$icon_result

        # Stylometry
        if [ "$id" = "$FOCUSED_WINDOW_ID" ]; then
            icon_color=$WHITE
            background_color=$GREY
            icon_font="sketchybar-app-font:Regular:16.0"
        else
            # Lighter grey, more visible ("no tan opaco")
            icon_color=0xffa0a0a0 
            background_color=$BACKGROUND_2 
            icon_font="sketchybar-app-font:Regular:14.0"
        fi

        if [ "$exists" = "false" ]; then
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
            sketchybar --set "$item_name" \
                             icon="$icon" \
                             icon.font="$icon_font" \
                             background.color="$background_color" \
                             icon.color="$icon_color" \
                       --move "$item_name" after "$ANCHOR"
        fi
        
        # Advance Anchor
        ANCHOR="$item_name"
    done
}

render_apps
