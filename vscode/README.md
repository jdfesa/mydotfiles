# VS Code Configuration 🎨 (Claude Aesthetic)

Esta carpeta contiene la configuración hiper-personalizada de VS Code. Recientemente fue modificada para emular la estética de extrema limpieza de **Claude Code (CLI)**: con fuentes monoespaciadas globales, barras de ventana transparentes y la barra de estado flotante estilo Neovim.

## 🗂️ Estructura de Archivos

- **`settings.json`**: El corazón del editor. Posee todas las variables nativas e inyecciones CSS directas para `custom-ui-style`.
- **`settings.json.bak`**: Copia intacta con la configuración anterior base (Catppuccin clásico, sin las inyecciones súper avanzadas) por si deseas retroceder.
- **`extensions.txt`**: Lista absoluta de extensiones esenciales, incluyendo los temas, AI (Copilot, Roo) y soporte para lenguajes.

## 🚀 Restauración en una máquina nueva

### 1. Enlazar Configuración Mágica (Symlink)
Debes hacer que VS Code lea este repositorio directamente:

```bash
# Eliminar archivo local vacío (Si existiera)
rm ~/Library/Application\ Support/Code/User/settings.json

# Crear Enlace
ln -sf ~/mydotfiles/vscode/settings.json ~/Library/Application\ Support/Code/User/settings.json
```

### 2. Instalar Extensiones Críticas
```bash
cat extensions.txt | xargs -L 1 code --install-extension
```

### 3. Habilitar la Estética "Claude" (Inyección CSS)
Por defecto, al instalar `subframe7536.custom-ui-style`, debes activarla manualmente por única vez para que re-parchee el motor de Microsoft.

1. Presiona `Cmd + Shift + P` en VS Code.
2. Tipea **`Enable custom ui style`** y selecciona.
3. Se recargará y aplicará el CSS puro.

> ⚠️ **Nota:** Si en el futuro VS Code se actualiza oficialmente, este parche se perderá y saltará un warning de "Corrupted Installation". Ignóralo, simplemente presiona `Cmd + Shift + P` -> `Enable custom ui style` de nuevo y volverá a la normalidad.

## ↩️ Rollback (Volver al Editor Tradicional)
1. Ejecuta `Cmd + Shift + P` -> **`Disable custom ui style`**.
2. Restaura la vieja configuración:
   ```bash
   cp ~/mydotfiles/vscode/settings.json.bak ~/mydotfiles/vscode/settings.json
   ```
