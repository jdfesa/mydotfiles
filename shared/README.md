# Shared Configurations

Configuraciones con una base reutilizable en mas de un sistema operativo.

Cada configuracion de herramienta vive en `shared/<tool>/` y conserva una unica
fuente de verdad. Los scripts portables de uso personal se agrupan en
`shared/scripts/<name>/`, evitando mezclar utilidades ejecutables con carpetas
de configuracion al mismo nivel.

Las diferencias pequenas se resuelven mediante includes, variables de entorno
o archivos locales ignorados; no se duplica una configuracion completa por
sistema.

Esta carpeta contiene configuraciones activas, documentacion de herramientas
CLI reutilizables y la coleccion `scripts/`. Las piezas exclusivas de una
plataforma viven en `os/`.

## Herramientas documentadas

- [`rtk/`](rtk/README.md): proxy local que reduce el ruido de comandos antes de
  incorporarlo al contexto de Codex.

## Scripts portables

`shared/scripts/` contiene comandos personales que pueden funcionar en mas de
un sistema. Cada script independiente o pequeña suite usa su propia carpeta:

```text
shared/scripts/
  cpu-watch/
    cpu-watch
    README.md
```

La carpeta `scripts/` de la raiz cumple otra funcion: mantenimiento interno del
repositorio, como linking, bootstrap y diagnostico de perfiles.

`shared/` expresa la ubicacion canonica y la intencion de reutilizacion; no
garantiza que cada archivo ya haya sido probado en todos los sistemas. Por
ejemplo, Kitty o VS Code todavia pueden contener ajustes del Mac principal. Al
crear el perfil de Arch se extraeran esas diferencias mediante includes,
variables o capas pequenas de `os/`, sin duplicar la configuracion completa.
