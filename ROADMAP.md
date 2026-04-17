# 🗺️ Roadmap de Herramientas — Dotfiles de JD

> Basado en tu stack actual: `zsh` + `starship` + `aerospace` + `sketchybar` + `ghostty` + `vscode` + `fastfetch` + `borders`
> Investigado y priorizado al 17/04/2025.
> Marca cada ítem con `[x]` a medida que lo explorés.

---

## ✅ Ya configurado y funcionando

- [x] **Zsh** — Shell principal con autosuggestions y syntax highlighting
- [x] **Starship** — Prompt ultrarrápido multiplataforma (reemplazó a Powerlevel10k)
- [x] **Aerospace** — Tiling window manager estilo i3, sin necesidad de deshabilitar SIP
- [x] **Sketchybar** — Barra de estado personalizable con integración a Aerospace
- [x] **Ghostty** — Terminal GPU-acelerada, cross-platform y minimalista
- [x] **Borders** — Bordes visuales en ventanas activas
- [x] **Fastfetch** — Reemplazo moderno de neofetch para mostrar info del sistema
- [x] **VS Code** — Editor personalizado: Claude Theme + Maple Mono + Vim motions
- [x] **VSCode Vim** — Modal editing con colores dinámicos de barra según modo

---

## 🟡 Siguiente paso — Alto impacto, bajo riesgo

> Instalar cualquiera de estos toma menos de 5 minutos. Empezá de arriba hacia abajo.

### CLI Esencial

- [ ] **`eza`** — Reemplaza el viejo `ls` con colores, íconos de Git y vista de árbol.
  - Instalación: `brew install eza`
  - Config en `.zshrc`: `alias ls='eza --icons'`
  - **Por qué probarlo:** Compatible directo con tu Nerd Font. Impacto visual inmediato en cada `ls` que ejecutés.

- [ ] **`bat`** — Reemplaza `cat` con syntax highlighting, números de línea e integración Git.
  - Instalación: `brew install bat`
  - Config en `.zshrc`: `alias cat='bat'`
  - **Por qué probarlo:** Lo usás imperceptiblemente, pero hace la terminal 10x más legible al leer archivos.

- [ ] **`ripgrep (rg)`** — Búsqueda en código ultrarrápida. Reemplaza `grep`.
  - Instalación: `brew install ripgrep`
  - **Por qué probarlo:** Si trabajás con proyectos Java/Python, sentís la diferencia al buscar texto en miles de archivos. Respeta `.gitignore` automáticamente.

- [ ] **`zoxide`** — Reemplaza `cd` con saltos inteligentes basados en tu historial de uso.
  - Instalación: `brew install zoxide`
  - Config en `.zshrc`: `eval "$(zoxide init zsh)"`
  - **Por qué probarlo:** Escribís `z poo` y te lleva directo a `~/Development/poo-2026`. Aprende tus carpetas frecuentes solo.

- [ ] **`fzf`** — Fuzzy finder interactivo para archivos, historial de comandos y procesos.
  - Instalación: `brew install fzf`
  - Config en `.zshrc`: `source <(fzf --zsh)`
  - **Por qué probarlo:** Se integra con `zoxide`, `bat` y el `Ctrl+R` de Zsh. Es la pieza que une todo el stack.

### Git desde la terminal

- [ ] **`lazygit`** — Interfaz TUI completa para Git (staging, branches, rebase visual).
  - Instalación: `brew install lazygit`
  - **Por qué probarlo:** Si abrís el panel de Git de VS Code frecuentemente, `lazygit` hace lo mismo pero desde cualquier terminal, incluyendo la de NetBeans. Podés invocarla con un shortcut de Ghostty.

### Historial inteligente

- [ ] **`atuin`** — Reemplaza `Ctrl+R` con búsqueda fuzzy del historial, sincronizado entre máquinas.
  - Instalación: `brew install atuin`
  - Config en `.zshrc`: `eval "$(atuin init zsh)"`
  - **Por qué probarlo:** Si trabajás en más de un Mac (Hackintosh + otro), sincroniza tu historial de comandos entre ambos automáticamente.

---

## 🔵 Para explorar más adelante

> Estas herramientas requieren un poco más de contexto o tiempo para configurar bien.

- [ ] **`yazi`** — File manager TUI con preview de imágenes y integración con `fzf` y `bat`.
  - **Nota:** Ya tenés `yazi-vscode.yaziPath` configurado en tu `settings.json` de VS Code. Solo falta probarlo en la práctica.
  - **Por qué probarlo:** Navegación de archivos visual desde la terminal. Alternativa elegante al explorador de VS Code.

- [ ] **`btop`** — Monitor interactivo de procesos, CPU, RAM y red. Reemplaza `htop`.
  - Instalación: `brew install btop`
  - **Por qué probarlo:** Si Sketchybar ya muestra CPU/RAM en la barra, `btop` es su hermano mayor para análisis en profundidad dentro de la terminal.

- [ ] **`tmux`** — Multiplexor: múltiples sesiones de terminal, paneles y layouts persistentes.
  - **Cuándo considerarlo:** Cuando empieces a trabajar con servidores SSH o necesités sesiones que sobrevivan al cierre de Ghostty. No es urgente con tu setup actual.

- [ ] **`Brewfile`** — Lista reproducible de todas tus dependencias de Homebrew.
  - Comando para generarlo: `brew bundle dump --describe --file ~/mydotfiles/Brewfile`
  - **Por qué probarlo:** Tu repo de dotfiles ya está muy ordenado. Un `Brewfile` lo convierte en un setup **100% reproducible** en cualquier Mac nuevo con un solo comando.

- [ ] **`stow`** — Gestor de symlinks para dotfiles. Automatiza los `ln -sf` manuales.
  - Instalación: `brew install stow`
  - **Por qué probarlo:** Tenés varios symlinks creados a mano. `stow` los organiza y los hace reversibles de forma estructurada.

---

## 🔴 Definitivamente NO tocar aún

> Estas herramientas son poderosas pero su costo/beneficio hoy no tiene sentido para tu flujo.

- [ ] **Neovim (como editor principal)**
  - **¿Por qué no?** Ya tenés VS Code perfectamente configurado con Vim motions, Claude Theme e integración Git. Neovim como reemplazo total requiere semanas de configuración en Lua.
  - **Consejo:** Ya estás usando el 80% de sus beneficios via VS Code Vim. Explorarlo como curiosidad en una carpeta separada no hace daño, pero no como editor principal aún.

- [ ] **Yabai (en lugar de Aerospace)**
  - **¿Por qué no?** Aerospace hace exactamente lo mismo sin riesgo. Yabai requiere deshabilitar SIP, una variable de riesgo extra en un Hackintosh. No hay ganancia real.

- [ ] **Warp Terminal (en lugar de Ghostty)**
  - **¿Por qué no?** Ghostty ya está perfectamente configurado. Warp requiere cuenta en la nube y es más "opinionated". Tu setup actual es más minimalista y alineado con tu estética.

- [ ] **Oh My Zsh o Prezto**
  - **¿Por qué no?** Migraste de Powerlevel10k a Starship justamente para escapar de la complejidad de los frameworks de Zsh. Volver sería dar un paso atrás sin ningún beneficio.

---

## 📦 Orden sugerido de instalación

Si querés ir de a uno, arrancá así (de menor a mayor complejidad):

```
1.  eza       → impacto inmediato, cero riesgo
2.  bat       → impacto inmediato, cero riesgo
3.  ripgrep   → útil para proyectos Java/Python
4.  zoxide    → cambia tu flujo de navegación terminal
5.  fzf       → integra todo lo anterior como pegamento
6.  lazygit   → cuando Git desde terminal empiece a incomodarte
7.  atuin     → si trabajás en más de una máquina
8.  yazi      → ya está medio configurado, solo falta probarlo
9.  btop      → curiosidad, monitoreo bonito del sistema
10. Brewfile  → para dejar el repo 100% reproducible
11. stow      → para automatizar los symlinks
12. tmux      → cuando trabajes con SSH o sesiones remotas
```
