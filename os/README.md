# OS

Capa para configuraciones y utilidades que pertenecen claramente a un sistema
operativo.

Usar esta carpeta cuando una pieza no sea compartida entre macOS, Linux y
Windows. Las herramientas compartidas siguen viviendo en la raiz del repo por
herramienta, por ejemplo `nvim/`, `git/`, `starship/`, `tmux/` o `yazi/`.

## Estructura esperada

```text
os/
  macos/
  linux/
  windows/
```

No guardar secretos, contrasenas, tokens ni claves privadas en Git.
