# 🚀 mydotfiles

Repositorio centralizado para gestionar mis configuraciones (dotfiles) de macOS.  
Aquí se encuentran las "fuentes de la verdad" de mis configuraciones, las cuales se despliegan en el sistema mediante **enlaces simbólicos**.

Ver tambien [Dotfiles Architecture](docs/ARCHITECTURE.md) para la estrategia multi-OS y [Architecture Decision Records](docs/adr/README.md) para las decisiones de arquitectura.

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

Actualmente el repo combina herramientas compartidas con capas especificas por
sistema operativo, host o perfil cuando existe una diferencia real.

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
- **[Neovim](nvim/README.md)**: Editor diario basado en LazyVim para notas y programacion.
- **[VS Code](vscode/README.md)**: Configuración visual y funcional del editor.
- **[Browser](browser/README.md)**: Temas y ajustes del navegador.
- **[Bat](bat/README.md)**: Lectura enriquecida de archivos en terminal sin reemplazar `cat`.
- **[Btop](btop/README.md)**: Monitor de sistema en terminal.
- **[Yazi](yazi/README.md)**: File manager terminal.
- **[Git](git/README.md)**: Identidad de commits y privacidad del correo en GitHub.
- **[Lazygit](lazygit/README.md)**: Interfaz terminal para Git.
- **[Gh Dash](gh-dash/README.md)**: Dashboard terminal para GitHub, PRs, issues y notificaciones.
- **[Hammerspoon](hammerspoon/README.md)**: Automatizaciones y notificaciones programables de macOS con Lua.
- **[Sesh](sesh/README.md)**: Selector de sesiones para proyectos y herramientas.
- **[Direnv](direnv/README.md)**: Variables de entorno por proyecto, cargadas solo despues de aprobar `.envrc`.
- **[Eza](eza/README.md)**: Reemplazo moderno de `ls` con iconos, Git y vista de arbol.
- **[Fzf](fzf/README.md)**: Selector fuzzy para historial, archivos, carpetas y sesiones.
- **[Ripgrep](ripgrep/README.md)**: Busqueda ultrarrapida de texto y archivos con `rg`.
- **[Zoxide](zoxide/README.md)**: Navegacion inteligente por carpetas, activada en Zsh.
- **[Zsh](zsh/README.md)**: Notas para reconstruir `~/.zshrc` y sus integraciones activas.

### Herramientas en evaluación

Estas carpetas fueron importadas como piezas maduras para adaptar poco a poco. No deben enlazarse al sistema hasta revisar su README interno:

- **[Homebrew](brew/README.md)**: Brewfiles por capas para instalar herramientas de forma reproducible.
- **[Tmux](tmux/README.md)**: Sesiones persistentes, layouts y flujo terminal.
- **[Colorscheme](colorscheme/README.md)**: Referencia para un futuro selector global de colores.
- **[Scripts](scripts/README.md)**: Scripts transversales de bootstrap, linking e instalacion del repo.

### Capas especificas

- **[OS](os/)**: configuraciones y utilidades que pertenecen claramente a un sistema operativo, como Linux/X11, macOS o Windows.

```bash
mydotfiles/
├── aerospace/    # Configuración de AeroSpace
├── bat/          # Lectura enriquecida de archivos
├── borders/      # Configuración de JankyBorders
├── brew/         # Brewfiles por capas (en evaluación)
├── btop/         # Monitor de sistema terminal
├── colorscheme/  # Selector/paletas de colores (referencia)
├── direnv/       # Variables de entorno por proyecto
├── eza/          # Reemplazo moderno de ls
├── fzf/          # Selector fuzzy integrado con Zsh
├── gh-dash/      # Dashboard terminal para GitHub
├── git/          # Identidad Git y privacidad de correo
├── hammerspoon/  # Notificaciones y automatizaciones macOS
├── ghostty/      # Terminal Ghostty (config, temas, shaders)
├── kitty/        # Terminal Kitty (config, temas, sesiones)
├── lazygit/      # Git TUI
├── nvim/         # Neovim basado en LazyVim
├── os/           # Capas especificas por sistema operativo
├── ripgrep/      # Busqueda ultrarrapida con rg
├── scripts/      # Bootstrap, linking e instalacion transversal
├── sesh/         # Selector de sesiones
├── silakka54/    # Teclado Silakka54
├── sketchybar/   # Configuración de Sketchybar
├── starship/     # Prompt multiplataforma
├── tmux/         # Multiplexor terminal (en evaluación)
├── vscode/       # Configuración de VS Code
├── yazi/         # File manager terminal
├── zoxide/       # Navegacion inteligente activada en Zsh
├── zsh/          # Configuracion principal de Zsh
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

    # Neovim
    ln -s ~/mydotfiles/nvim ~/.config/nvim

    # Fastfetch
    ln -s ~/mydotfiles/fastfetch ~/.config/fastfetch

    # Starship
    ln -s ~/mydotfiles/starship/starship.toml ~/.config/starship.toml

    # Zsh
    ln -s ~/mydotfiles/zsh/zshrc ~/.zshrc

    # Btop
    ln -s ~/mydotfiles/btop ~/.config/btop

    # Yazi
    ln -s ~/mydotfiles/yazi ~/.config/yazi

    # Lazygit
    mkdir -p "$HOME/Library/Application Support/lazygit"
    ln -s ~/mydotfiles/lazygit/config.yml "$HOME/Library/Application Support/lazygit/config.yml"

    # Gh Dash
    mkdir -p ~/.config/gh-dash
    ln -s ~/mydotfiles/gh-dash/config.yml ~/.config/gh-dash/config.yml

    # Hammerspoon
    mkdir -p ~/.config
    ln -s ~/mydotfiles/hammerspoon ~/.config/hammerspoon
    defaults write org.hammerspoon.Hammerspoon MJConfigFile "$HOME/.config/hammerspoon/init.lua"

    # Sesh
    ln -s ~/mydotfiles/sesh ~/.config/sesh

    # Direnv
    # No requiere symlink: se instala con Homebrew y se activa desde zsh/zshrc.
    ```

3.  Crea `~/mydotfiles/zsh/local.zsh` a partir de `zsh/local.zsh.example` para rutas especificas de esa maquina.

    Ver [`zsh/README.md`](zsh/README.md), [`bat/README.md`](bat/README.md), [`direnv/README.md`](direnv/README.md), [`eza/README.md`](eza/README.md), [`fzf/README.md`](fzf/README.md), [`gh-dash/README.md`](gh-dash/README.md), [`hammerspoon/README.md`](hammerspoon/README.md), [`ripgrep/README.md`](ripgrep/README.md) y [`zoxide/README.md`](zoxide/README.md) para los casos de uso y validacion.

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
