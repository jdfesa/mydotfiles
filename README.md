# mydotfiles
# 📁 mydotfiles

Repositorio personal para guardar y versionar mis configuraciones personalizadas (dotfiles).  
Por ahora contiene únicamente mi configuración de [Sketchybar](https://felixkratz.github.io/SketchyBar/) en macOS.

---

## 📦 Estructura actual

```bash
mydotfiles/
└── sketchybar/
```

---

## 🧠 ¿Qué es esto?

Este repositorio guarda mis archivos de configuración para Sketchybar.  
La idea es tener una copia organizada y versionada para no perder nunca los cambios que hago, y para poder restaurar el entorno rápidamente si reinstalo el sistema o me mudo a otra máquina.

---

## 🔗 Enlace simbólico (symlink) actual

Después de mover mi configuración desde `~/.config/sketchybar` a `~/mydotfiles/sketchybar`, creé un symlink para que Sketchybar siga funcionando sin notar el cambio:

```bash
ln -s ~/mydotfiles/sketchybar ~/.config/sketchybar

Este symlink es visible al listar con ls -l ~/.config y debe verse así:
sketchybar -> /Users/jd/mydotfiles/sketchybar
