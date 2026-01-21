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

### 3. Enable Custom CSS
This configuration includes a `custom.css` file for UI modifications.
1.  Ensure the "Custom CSS and JS Loader" extension is installed.
2.  Open VS Code Command Palette (`Cmd+Shift+P`).
3.  Run: `> Enable Custom CSS and JS`.
4.  Restart VS Code.

## 📂 File Structure
- **`settings.json`**: Core editor settings (theme, font, formatting, etc.).
- **`custom.css`**: Advanced UI overrides (fonts, shadows, etc.).
- **`snippets/`**: Custom code snippets for various languages.
- **`extensions.txt`**: List of all installed extensions.
