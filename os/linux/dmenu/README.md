# Dmenu

Configuracion de Dmenu mantenida como herramienta independiente. Puede actuar
como lanzador de DWM, i3 u otros window managers y no forma parte interna de
DWM.

## Estructura

```text
dmenu/
  README.md       # integracion, decisiones y procedimiento del repositorio
  src/            # fuentes y configuracion personalizada de Dmenu
  patches/        # parches separados, cuando corresponda
  scripts/        # build, instalacion o pruebas, cuando sean necesarios
```

Los fuentes importados todavia deben inventariarse antes de compilar o instalar.
La configuracion efectiva, el origen upstream y cualquier parche se documentaran
antes de activar esta copia.
