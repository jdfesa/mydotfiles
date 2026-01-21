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

```

### 2. Install Extensions
To install all the extensions listed in `extensions.txt`:

```bash
cat extensions.txt | xargs -L 1 code --install-extension
```



## 📂 File Structure
- **`settings.json`**: Core editor settings.


- **`extensions.txt`**: Extension list.
