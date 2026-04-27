# Browser Customization

This directory contains customized configuration files and themes to create a cohesive, developer-focused, and dark-themed experience for Google Chrome. It leverages several popular extensions and a local Chrome theme to establish a uniform aesthetic based on JetBrains Mono and a specific color palette.

## 📦 Contents

### 1. Chrome Theme (`chrome-theme-catppuccin/`)
A locally unpacked Google Chrome theme based on the Catppuccin color palette. It modifies the browser's native UI (tab bar, bookmarks bar, omnibox) to match the dark aesthetic.

### 2. Mynt - Material You New Tab (`material_newtab.json`)
Configuration backup for the [Mynt](https://chromewebstore.google.com/detail/mynt-material-you-new-tab/jjpokbgpiljgndebfoljdeihhkpcpfgl) extension, which replaces the default new tab page.
- **Aesthetic:** Terminal/code-inspired layout with a dark grid and circuit-like lines.
- **Accent Color:** `#18e299`
- **Features:** Dark loading screen and a digital clock.

### 3. Dark Reader (`Dark-Reader-Settings.json`)
Custom settings for the Dark Reader extension to ensure web pages match the overall theme.
- **Font:** Enforces `JetBrains Mono`.
- **Colors:** Deep dark backgrounds with slightly greenish light text.
- **Selection:** Accent color `#18e299` for text selection.

### 4. Stylus (`stylus.json`)
Global CSS overrides managed via the Stylus extension.
- **Rule:** `Global JetBrains Mono font`
- **Behavior:** Forces the `JetBrains Mono` font across all web pages, applying it specifically to general text, buttons, inputs, textareas, and `<pre>` code blocks.

---

## 🚀 Installation & Setup

### Applying the Chrome Theme
1. Navigate to `chrome://extensions` in your browser.
2. Enable **Developer mode** in the top right corner.
3. Click **Load unpacked** and select the `chrome-theme-catppuccin` directory.
   > **Note:** The theme relies on this directory remaining in its current location. Moving or deleting the folder will break the theme.

### Importing Extension Configurations
For the following extensions, locate their respective settings/backup menus to import the JSON files:

1. **Mynt:** Go to settings -> Backup/Restore -> Import `material_newtab.json`.
2. **Dark Reader:** Go to settings -> Manage Settings -> Import `Dark-Reader-Settings.json`.
3. **Stylus:** Open the Stylus manager -> Manage -> Import `stylus.json`.

*(Note: Unlike the unpacked Chrome theme, the JSON configuration files do not depend on their file path once imported).*

---

## ⏪ Reverting Changes

If you need to revert any of the customizations:
- **Chrome Theme:** Go to `chrome://settings/appearance` and click **Reset to default**. You can then safely remove the `chrome-theme-catppuccin` folder.
- **Mynt & Dark Reader:** Re-import your previous backups from the extensions' settings.
- **Stylus:** Disable the `Global JetBrains Mono font` rule, delete it, or restore a previous backup.
