# ST

Configuracion de ST mantenida como herramienta independiente. Aunque DWM pueda
usarlo como terminal predeterminado, ST tambien puede ejecutarse desde i3,
XFCE u otros entornos.

## Estructura

```text
st/
  README.md       # integracion, decisiones y procedimiento del repositorio
  src/            # fuentes y configuracion personalizada de ST
  patches/        # parches separados, cuando corresponda
  scripts/        # build, instalacion o pruebas, cuando sean necesarios
```

Los fuentes importados todavia deben inventariarse antes de compilar o instalar.
El `config.h` versionado puede contener decisiones utiles, pero primero hay que
relacionarlo con una version upstream y documentar sus dependencias y parches.
