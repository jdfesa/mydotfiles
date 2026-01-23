# 🚀 mydotfiles

Repositorio centralizado para gestionar mis configuraciones (dotfiles) de macOS.  
Aquí se encuentran las "fuentes de la verdad" de mis configuraciones, las cuales se despliegan en el sistema mediante **enlaces simbólicos**.

---

## 📂 Estructura del Repositorio

Actualmente gestiono las siguientes herramientas:

- **[Aerospace](https://github.com/nikitabobko/AeroSpace)**: Tiling Window Manager para macOS.
- **[Sketchybar](https://felixkratz.github.io/SketchyBar/)**: Barra de estado personalizada.
- **[JankyBorders](https://github.com/FelixKratz/JankyBorders)**: Bordes de ventana con colores y esquinas redondeadas.
- **[Ghostty](ghostty/README.md)**: Terminal emuladora GPU-accelerated.
- **[Fastfetch](fastfetch/README.md)**: Información del sistema con tema de Serial Experiments Lain.
- **[Silakka54](silakka54/README.md)**: Configuración y visualización automática del teclado.

```bash
mydotfiles/
├── aerospace/   # Configuración de AeroSpace
├── borders/     # Configuración de JankyBorders
├── ghostty/     # Terminal Ghostty (Config, Temas, Shaders)
├── fastfetch/   # Configuración de Fastfetch (Tema Lain)
├── silakka54/   # Teclado Silakka54 (Ver README interno)
├── sketchybar/  # Configuración de Sketchybar
└── README.md
```

---

## ⚙️ Flujo de Trabajo (Symlinks)

Para mantener este repositorio limpio y organizado, utilizamos un enfoque profesional basado en **Enlaces Simbólicos (Symlinks)**.

### ¿Cómo funciona?
1.  **Ubicación Real**: Las carpetas reales con los archivos de configuración viven dentro de este repositorio (`~/mydotfiles`).
2.  **Ubicación del Sistema**: Los programas esperan encontrar sus configs en rutas estándar como `~/.config`.
3.  **El Enlace**: En lugar de copiar archivos, creamos un "acceso directo" (symlink) en `~/.config` que apunta a `~/mydotfiles`.

Esto nos permite editar y versionar todo desde una sola carpeta (`mydotfiles`) y que los cambios se reflejen automáticamente en el sistema.

### 🛠 Cómo agregar una nueva configuración

Si quieres agregar un nuevo programa (ej. `nvim`):

1.  **Mover**: Mueve la carpeta de configuración original al repo.
    ```bash
    mv ~/.config/nvim ~/mydotfiles/
    ```
2.  **Enlazar**: Crea el enlace simbólico desde el repo a la ruta original.
    ```bash
    ln -s ~/mydotfiles/nvim ~/.config/nvim
    ```

### 📥 Instalación (Restaurar dotfiles)

Si clonas este repositorio en una nueva máquina:

1.  Clona el repo:
    ```bash
    git clone https://github.com/jdfesa/mydotfiles.git ~/mydotfiles
    ```
2.  Crea los enlaces necesarios:
    ```bash
    # AeroSpace
    ln -s ~/mydotfiles/aerospace ~/.config/aerospace

    # Sketchybar
    ln -s ~/mydotfiles/sketchybar ~/.config/sketchybar

    # JankyBorders
    mkdir -p ~/.config/borders
    ln -s ~/mydotfiles/borders/bordersrc ~/.config/borders/bordersrc

    # Ghostty
    mkdir -p ~/.config/ghostty
    ln -s ~/mydotfiles/ghostty/config ~/.config/ghostty/config

    # Fastfetch
    ln -s ~/mydotfiles/fastfetch ~/.config/fastfetch
    ```
