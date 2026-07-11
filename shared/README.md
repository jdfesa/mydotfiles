# Shared Configurations

Configuraciones con una base reutilizable en mas de un sistema operativo.

Cada herramienta vive en `shared/<tool>/` y conserva una unica fuente de verdad.
Las diferencias pequenas se resuelven mediante includes, variables de entorno o
archivos locales ignorados; no se duplica una configuracion completa por
sistema.

Esta carpeta contiene configuraciones activas y documentacion de herramientas
CLI reutilizables. Las piezas exclusivas de una plataforma viven en `os/`.

`shared/` expresa la ubicacion canonica y la intencion de reutilizacion; no
garantiza que cada archivo ya haya sido probado en todos los sistemas. Por
ejemplo, Kitty o VS Code todavia pueden contener ajustes del Mac principal. Al
crear el perfil de Arch se extraeran esas diferencias mediante includes,
variables o capas pequenas de `os/`, sin duplicar la configuracion completa.
