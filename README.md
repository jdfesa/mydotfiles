# 🚀 mydotfiles

Repositorio centralizado para gestionar mis configuraciones (dotfiles) de macOS.  
Aquí se encuentran las "fuentes de la verdad" de mis configuraciones, las cuales se despliegan en el sistema mediante **enlaces simbólicos**.

---

## 🧭 Convenciones de Adaptacion

- **Usuario local**: `jd`.
- **Ruta principal del repo**: `~/mydotfiles`.
- Toda herramienta nueva debe vivir en su propia carpeta y tener su propio `README.md`.
- Las rutas copiadas desde otros dotfiles deben adaptarse a `$HOME`, `~` o `~/mydotfiles`; no deben quedar rutas activas de otra maquina o usuario.
- Si una configuracion importada conserva rutas, keymaps o nombres del autor original, se considera **referencia upstream** y no se enlaza al sistema.
- Tu teclado base es **Silakka54**. No se importan keymaps de Karabiner, Kanata, skhd ni BTT hasta redisenarlos para tu flujo.
- AeroSpace sigue siendo el window manager activo; cualquier idea basada en Yabai se adapta manualmente antes de usarla.

---

## 📂 Estructura del Repositorio

Actualmente el repo se divide en dos grupos:

### Herramientas activas

Estas son las configuraciones que ya forman parte del setup diario o estan integradas con tu flujo actual:

- **[Aerospace](https://github.com/nikitabobko/AeroSpace)**: Tiling Window Manager para macOS.
- **[Sketchybar](https://felixkratz.github.io/SketchyBar/)**: Barra de estado personalizada.
- **[JankyBorders](https://github.com/FelixKratz/JankyBorders)**: Bordes de ventana con colores y esquinas redondeadas.
- **[Ghostty](ghostty/README.md)**: Terminal emuladora GPU-accelerated.
- **[Kitty](kitty/README.md)**: Terminal GPU con soporte de imágenes, sesiones y tema activo.
- **[Fastfetch](fastfetch/README.md)**: Información del sistema con tema de Serial Experiments Lain.
- **[Silakka54](silakka54/README.md)**: Configuración y visualización automática del teclado.
- **[Starship](starship/README.md)**: Prompt para la terminal moderno, rápido y multiplataforma.
- **[VS Code](vscode/README.md)**: Configuración visual y funcional del editor.
- **[Browser](browser/README.md)**: Temas y ajustes del navegador.
- **[Btop](btop/README.md)**: Monitor de sistema en terminal.
- **[Yazi](yazi/README.md)**: File manager terminal.
- **[Lazygit](lazygit/README.md)**: Interfaz terminal para Git.
- **[Sesh](sesh/README.md)**: Selector de sesiones para proyectos y herramientas.
- **[Zoxide](zoxide/README.md)**: Navegacion inteligente por carpetas, activada en Zsh.
- **[Zsh](zsh/README.md)**: Notas para reconstruir `~/.zshrc` y sus integraciones activas.

### Herramientas en evaluación

Estas carpetas fueron importadas como piezas maduras para adaptar poco a poco. No deben enlazarse al sistema hasta revisar su README interno:

- **[Homebrew](brew/README.md)**: Brewfiles por capas para instalar herramientas de forma reproducible.
- **[Tmux](tmux/README.md)**: Sesiones persistentes, layouts y flujo terminal.
- **[Colorscheme](colorscheme/README.md)**: Referencia para un futuro selector global de colores.
- **[Scripts](scripts/README.md)**: Inventario de scripts utiles a adaptar, sin activar dependencias invasivas.

```bash
mydotfiles/
├── aerospace/    # Configuración de AeroSpace
├── borders/      # Configuración de JankyBorders
├── brew/         # Brewfiles por capas (en evaluación)
├── btop/         # Monitor de sistema terminal
├── colorscheme/  # Selector/paletas de colores (referencia)
├── ghostty/      # Terminal Ghostty (config, temas, shaders)
├── kitty/        # Terminal Kitty (config, temas, sesiones)
├── lazygit/      # Git TUI
├── scripts/      # Inventario de scripts a adaptar
├── sesh/         # Selector de sesiones
├── silakka54/    # Teclado Silakka54
├── sketchybar/   # Configuración de Sketchybar
├── starship/     # Prompt multiplataforma
├── tmux/         # Multiplexor terminal (en evaluación)
├── vscode/       # Configuración de VS Code
├── yazi/         # File manager terminal
├── zoxide/       # Navegacion inteligente activada en Zsh
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

    # Kitty
    mkdir -p ~/.config
    ln -s ~/mydotfiles/kitty ~/.config/kitty
    ln -s /Applications/kitty.app/Contents/MacOS/kitty /usr/local/bin/kitty
    ln -s /Applications/kitty.app/Contents/MacOS/kitten /usr/local/bin/kitten

    # Fastfetch
    ln -s ~/mydotfiles/fastfetch ~/.config/fastfetch

    # Starship
    ln -s ~/mydotfiles/starship/starship.toml ~/.config/starship.toml

    # Btop
    ln -s ~/mydotfiles/btop ~/.config/btop

    # Yazi
    ln -s ~/mydotfiles/yazi ~/.config/yazi

    # Lazygit
    mkdir -p "$HOME/Library/Application Support/lazygit"
    ln -s ~/mydotfiles/lazygit/config.yml "$HOME/Library/Application Support/lazygit/config.yml"

    # Sesh
    ln -s ~/mydotfiles/sesh ~/.config/sesh
    ```

3.  Reaplica las integraciones que viven en archivos del home y no usan symlink:

    ```bash
    # Zoxide al final de ~/.zshrc
    if command -v zoxide >/dev/null 2>&1; then
      eval "$(zoxide init zsh)"
    fi
    ```

    Ver [`zsh/README.md`](zsh/README.md) y [`zoxide/README.md`](zoxide/README.md) para los casos de uso y validacion.

### 🧪 Activación de herramientas en evaluación

Las herramientas nuevas se agregan primero al repo, con README propio, y solo se activan cuando ya fueron revisadas. Ejemplos:

```bash
# Tmux
ln -s ~/mydotfiles/tmux/tmux.conf ~/.tmux.conf

```

Antes de crear cualquiera de estos enlaces, respaldar una config existente si la hubiera.

### 🛡️ Protección contra modificaciones accidentales (Blindaje)

Dado que este repositorio es la "fuente de la verdad" de todo el sistema, es una excelente práctica bloquear carpetas de configuraciones que consideres estables y terminadas (por ejemplo, `sketchybar`). Esto evita estropear la configuración con atajos de teclado accidentales desde tu editor (VS Code, etc).

Utilizamos permisos nativos del sistema de archivos para aplicar un **Modo de Solo Lectura**:

1.  **Bloquear una carpeta (Blindar)**
    Previene de forma absoluta la modificación accidental. Si tu editor intenta guardar un cambio, arrojará un error de "Permiso denegado".
    ```bash
    chmod -R a-w <nombre_de_la_carpeta>
    # Ejemplo: chmod -R a-w sketchybar
    ```

2.  **Desbloquear una carpeta (Modificar)**
    Devuelve los permisos de escritura a tu usuario cuando realmente necesites desarrollar nuevos cambios.
    ```bash
    chmod -R u+w <nombre_de_la_carpeta>
    # Ejemplo: chmod -R u+w sketchybar
    ```
