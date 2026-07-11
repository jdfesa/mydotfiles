# DWM

Espacio de trabajo para construir una configuracion de DWM limpia y
reproducible. Los antiguos fuentes compilados en `~/suckless` no son la base de
esta carpeta: DWM se incorporara aqui desde su origen, con version, parches,
dependencias y procedimiento de build documentados.

## Estado

DWM todavia no esta administrado por este repositorio. XFCE, SDDM, SSH y XRDP
deben permanecer disponibles como entorno de recuperacion durante el trabajo.

`scripts/` conserva utilidades recuperadas de la configuracion anterior. Que un
script este versionado no significa que DWM o sus dependencias ya deban
instalarse.

## Scripts recuperados

- `wallpaper-rotator.sh`: rota imagenes mediante `feh` sin romper rutas que
  contienen espacios.
- `status-sensors.sh`: genera el bloque de CPU, memoria y GPU usado por
  `dwmblocks`; admite un lector de carga AMD configurable.

Las dependencias se validan en tiempo de ejecucion y no se instalan
automaticamente.
