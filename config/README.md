# Shared Configurations

Configuraciones con una base reutilizable en mas de un sistema operativo.

Cada herramienta vive en `config/<tool>/` y conserva una unica fuente de verdad.
Las diferencias pequenas se resuelven mediante includes, variables de entorno o
archivos locales ignorados; no se duplica una configuracion completa por
sistema.

Las herramientas compartidas que todavia estan en la raiz se moveran aqui una
por una despues de verificar su perfil y sus referencias internas.

