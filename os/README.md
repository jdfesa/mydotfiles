# OS

Capa para configuraciones y utilidades que pertenecen claramente a un sistema
operativo.

Usar esta carpeta cuando una pieza no sea compartida entre macOS, Linux y
Windows. Las herramientas compartidas viven en `shared/`, por ejemplo
`shared/nvim/`, `shared/git/`, `shared/starship/`, `shared/tmux/` o
`shared/yazi/`.

## Estructura esperada

```text
os/
  macos/
  linux/
  windows/
```

No guardar secretos, contrasenas, tokens ni claves privadas en Git.
