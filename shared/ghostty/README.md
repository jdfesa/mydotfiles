# 👻 Ghostty Configuration

Configuration for [Ghostty](https://github.com/ghostty-org/ghostty), the fast, feature-rich, and cross-platform terminal emulator.

## 📂 Structure
*   **Location**: `~/mydotfiles/shared/ghostty/`
    *   `config`: **El Cerebro**. Archivo principal donde definimos atajos, fuentes y comportamiento.
    *   `ghostty-theme`: **La Piel**. Archivo con la paleta de colores hexadecimales.
    *   `shaders/`: **Efectos Visuales**. Una colección de pequeños programas gráficos (.glsl) que alteran como se ve la terminal (efecto CRT, Bloom/Brillo, Matrix, etc).
*   **Symlink**: `~/.config/ghostty` -> `~/mydotfiles/shared/ghostty`
    *   *Note*: The theme and shaders are loaded relative to the main config file.

## 🎨 Aesthetic & Theme
*   **Theme**: Loading from external file `ghostty-theme`.
*   **Font**: `JetBrainsMono Nerd Font` (Size: 15).
*   **Background**:
    *   **Opacity**: `0.78` (Semi-transparent).
    *   **Blur**: `true` (macOS/KDE style blur).
*   **Window**:
    *   **Padding**: `x=4,2`, `y=6,0` (Balanced spacing).
    *   **Decorations**: `native` (Native macOS titlebar).

## ⚡ Key Features
*   **Quick Terminal**: Toggle with `Cmd + S`.
    *   *Animation*: 0.08s slide-in.
*   **Shell Integration**:
    *   Auto-attaches to **Tmux** if installed (`tmux-sessionizer`).
    *   Falls back to `zsh` if Tmux is missing.
*   **MacOS Option Key**: Mapped to `Right Option` as Alt (preserves Left Option for macOS special chars).

## 🔄 How to Reload
Ghostty supports **Hot Reload**.
*   **Edit the file**: Changes apply immediately upon saving.
*   **Force Reload**: `Cmd + Shift + ,` (Comma).

## 🛠️ Usage
No manual action needed. The config is loaded automatically by Ghostty on startup.
