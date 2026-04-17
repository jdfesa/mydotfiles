# 🚀 Starship Prompt

[Starship](https://starship.rs/) es un prompt hiper-rápido, personalizable y **multiplataforma** escrito en Rust. Es el estándar moderno para el diseño de interfaces en la línea de comandos de la industria.

## 🌟 Características clave

- **Multiplataforma y Multi-Shell:** Es su mayor ventaja. Lo que configures aquí funcionará del lado del servidor en Linux (con `bash`, `fish` o `zsh`), en Windows (incluso bajo `PowerShell`) o en tu macOS. Tu mismo y único archivo `starship.toml` sirve para controlar cualquier terminal en cualquier lugar.
- **Performance:** Al estar programado en Rust puro, carga visualmente en milisegundos y jamás ralentiza las pulsaciones de tu Shell como los antiguos prompts.
- **Totalmente Contextual:** Solo muestra lo estrictamente importante: Te avisa de las ramas de `git`, estados del repositorio, el nodo, perfil de AWS, entorno virtual de python, etc., exactamente donde estás posicionado y solo si es necesario.

## 📥 Instalación Manual

Si clonas este repositorio de dotfiles en un nuevo sistema operativo o computadora, estos son los pasos para que Starship arranque:

### 1. Instalar el ejectutable base

- **macOS (mediante Homebrew):**
  ```bash
  brew install starship
  ```
- **Windows / Linux / Otros OS:**
  Visita [starship.rs](https://starship.rs/guide/#🚀-installation) o corre el script oficial universal:
  ```bash
  curl -sS https://starship.rs/install.sh | sh
  ```

### 2. Aplicar la configuración (Enlace Simbólico / Symlink)

El programa nativo espera leer sus reglas siempre desde la ruta predeterminada `~/.config/starship.toml`. Para que aplique nuestras reglas de los dotfiles, hacemos el enlace:

```bash
mkdir -p ~/.config
ln -s ~/mydotfiles/starship/starship.toml ~/.config/starship.toml
```

### 3. Cargar el Prompt en tu Shell (.zshrc / .bashrc)

Finalmente, debes ordenar a tu shell base que lance y dibuje Starship cada vez que presiones Enter.

Para **Zsh** (como en macOS), añade esta línea al final de todo tu `~/.zshrc`:

```bash
eval "$(starship init zsh)"
```

Para **Bash** (`~/.bashrc`):
```bash
eval "$(starship init bash)"
```

> **Nota para IDEs:** Starship es lo suficientemente minimalista como para funcionar perfecto dentro de editores de código (como la terminal integrada en VS Code).
