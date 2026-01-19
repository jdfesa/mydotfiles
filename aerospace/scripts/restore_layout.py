import subprocess
import json
import os
import sys
import difflib

SNAPSHOT_FILE = os.path.expanduser("~/.aerospace-layout.json")

def get_windows():
    """Queries AeroSpace for all windows in JSON format."""
    try:
        result = subprocess.run(
            ['aerospace', 'list-windows', '--all', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error querying AeroSpace: {e}", file=sys.stderr)
        return []

def load_snapshot():
    if not os.path.exists(SNAPSHOT_FILE):
        return []
    try:
        with open(SNAPSHOT_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading snapshot: {e}", file=sys.stderr)
        return []

def restore_layout():
    snapshot = load_snapshot()
    if not snapshot:
        print("No snapshot found.")
        return

    current_windows = get_windows()
    
    restored_count = 0
    
    # Simple logic: iterate through snapshot and try to find a matching window
    # We will track which current windows have been "claimed" to avoid double moving
    claimed_ids = set()

    for saved in snapshot:
        saved_app = saved.get('app-name')
        saved_title = saved.get('window-title')
        target_workspace = saved.get('workspace')
        
        if not saved_app or not target_workspace:
            continue

        best_match = None
        best_score = 0.0

        for curr in current_windows:
            win_id = curr['window-id']
            if win_id in claimed_ids:
                continue

            curr_app = curr.get('app-name')
            if curr_app != saved_app:
                continue
            
            # Fuzzy match title
            curr_title = curr.get('window-title', '')
            # Ratio returns 0-1 float
            score = difflib.SequenceMatcher(None, saved_title, curr_title).ratio()
            
            # If exact match or very high score
            if score > 0.8: 
                if score > best_score:
                    best_score = score
                    best_match = win_id
            
            # Fallback: if app name matches and we haven't found a high title match yet, 
            # consider it if the title is generic (like "Terminal")
            elif score > 0.4 and best_score < 0.5:
                 if score > best_score:
                    best_score = score
                    best_match = win_id

        if best_match:
            # Move the window
            claimed_ids.add(best_match)
            print(f"Moving {saved_app} ('{saved_title}' -> '{current_windows[0]['window-title']}') to {target_workspace}")
            
            try:
                subprocess.run(
                    ['aerospace', 'move-node-to-workspace', str(target_workspace), '--window-id', str(best_match)],
                    check=False # Don't crash if one fails
                )
                restored_count += 1
            except Exception as e:
                print(f"Failed to move window {best_match}: {e}")

    # Notify
    subprocess.run([
        'osascript', '-e', 
        f'display notification "Restored {restored_count} windows to their saved positions." with title "AeroSpace Restore"'
    ])

if __name__ == "__main__":
    restore_layout()
