#!/bin/bash

# $CONFIG_DIR/plugins/current_apps.sh

source "$CONFIG_DIR/colors.sh"
source "$CONFIG_DIR/plugins/icon_map.sh"

render_window_list() {
    # 1. Get List of Windows in Focused Workspace from AeroSpace
    # Output format: | app-name | window-title |
    # We only care about app-name for now.
    
    # We use --json for reliable parsing
    CURRENT_WINDOWS=$(aerospace list-windows --workspace focused --json)
    
    # Extract entries
    APPS=$(echo "$CURRENT_WINDOWS" | jq -r '.[]."app-name"')
    
    ICON_STRIP=""
    
    # Process each app
    # Use associative array to avoid duplicates if user wants unique apps, 
    # but user said "apps underneath", so maybe they want to see all windows? 
    # Usually one icon per app instance is clutter, but let's stick to unique apps first 
    # or show multiple if multiple windows.
    # User said "las apps que tengo abiertas".
    
    # Let's show duplicates if multiple windows exist, or maybe unique?
    # "no veo la otra que esta debajo" implies distinct windows.
    # Let's show one icon per window.
    
    while IFS= read -r app_name; do 
        if [ ! -z "$app_name" ]; then
             # Get Icon
             icon_map "$app_name"
             # $icon_result is set by icon_map
             ICON_STRIP+="$icon_result "
        fi
    done <<< "$APPS"
    
    # Update Sketchybar Item
    if [ "$ICON_STRIP" = "" ]; then
        sketchybar --set current_apps label="" drawing=off
    else
        sketchybar --set current_apps label="$ICON_STRIP" drawing=on
    fi
}

render_window_list
