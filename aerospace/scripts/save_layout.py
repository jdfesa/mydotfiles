import subprocess
import json
import os
import sys

# File to store the snapshot
SNAPSHOT_FILE = os.path.expanduser("~/.aerospace-layout.json")

def get_windows():
    """Queries AeroSpace for all windows in JSON format."""
    try:
        # aerospace list-windows --all --json
        result = subprocess.run(
            ['aerospace', 'list-windows', '--all', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error querying AeroSpace: {e}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing AeroSpace output: {e}", file=sys.stderr)
        return []

def save_snapshot():
    """Saves the current window state to the snapshot file."""
    windows = get_windows()
    
    snapshot = []
    for w in windows:
        # We save minimal info needed to restore: App, Title, Workspace
        # Some apps might have multiple windows with same title, heuristic needed later.
        entry = {
            'app-name': w.get('app-name'),
            'window-title': w.get('window-title'),
            'workspace': w.get('workspace')
        }
        snapshot.append(entry)

    try:
        with open(SNAPSHOT_FILE, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        # Notify user via notification center (optional but nice)
        subprocess.run([
            'osascript', '-e', 
            f'display notification "Layout Saved: {len(snapshot)} windows tracked" with title "AeroSpace Snapshot"'
        ])
        print(f"Snapshot saved to {SNAPSHOT_FILE}")
    except Exception as e:
        print(f"Error saving snapshot: {e}", file=sys.stderr)

if __name__ == "__main__":
    save_snapshot()
