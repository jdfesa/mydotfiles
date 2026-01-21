# VS Code Configuration

This directory contains my personal VS Code settings, snippets, and a list of extensions.

## 🚀 Restoration

To restore this configuration on a new machine:

### 1. Link Configuration Files
Run the following commands to link the settings and snippets to the VS Code user directory:

```bash
# Backup existing settings if needed
# mv ~/Library/Application\ Support/Code/User/settings.json ~/Library/Application\ Support/Code/User/settings.json.bak

# Create Symlinks
ln -sf ~/mydotfiles/vscode/settings.json ~/Library/Application\ Support/Code/User/settings.json
rm -rf ~/Library/Application\ Support/Code/User/snippets
ln -sf ~/mydotfiles/vscode/snippets ~/Library/Application\ Support/Code/User/snippets
```

### 2. Install Extensions
To install all the extensions listed in `extensions.txt`:

```bash
cat extensions.txt | xargs -L 1 code --install-extension
```

### 3. Enable Custom CSS (Advanced)
This configuration uses the [Custom CSS and JS Loader](https://marketplace.visualstudio.com/items?itemName=be5invis.vscode-custom-css) extension to modify the UI.

**Pre-requisites:**
1.  Install the extension: `be5invis.vscode-custom-css`
2.  Ensure `settings.json` points to the correct file path (already configured in this repo).

**Activation Steps (Critical):**
1.  Open VS Code Command Palette (`Cmd+Shift+P`).
2.  Run: `> Enable Custom CSS and JS`.
3.  **IMPORTANT**: VS Code will show a notification saying "Restart to take effect". Click "Restart" or manually restart.
4.  **Trobleshooting**: If it says "VS Code is corrupt", click "Don't show again" (this is normal as we are patching the core).

**If "Enable" does nothing:**
- Ensure you have **Admin rights** (it modifies VS Code internal files).
- Try running: `> Reload Custom CSS and JS` instead.
- Check the "Developer Tools" (`Help > Toggle Developer Tools`) for red errors in the Console.

## 📂 File Structure
- **`settings.json`**: Core editor settings.
- **`custom.css`**: UI overrides (fonts, animations).
- **`snippets/`**: Code snippets.
- **`extensions.txt`**: Extension list.
