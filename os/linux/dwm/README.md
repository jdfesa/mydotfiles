# DWM

Configuracion de DWM para construir un window manager limpio y reproducible.
DWM se mantiene separado de ST, Dmenu y DWMBlocks porque cada proyecto puede
usarse o reemplazarse de manera independiente.

## Estructura

```text
dwm/
  README.md       # decisiones y procedimiento mantenidos por este repo
  src/            # fuentes y configuracion de DWM
  scripts/        # utilidades exclusivas de la sesion DWM
  patches/        # parches conservados por separado, cuando corresponda
```

El `README.md` que viene con la implementacion importada permanece dentro de
`src/`; este archivo exterior documenta como se integra DWM en los dotfiles.

## Estado

Los fuentes personalizados ya fueron importados en `src/`, pero todavia no se
consideran una instalacion reproducible. Antes de activarlos hay que identificar
su origen, version, parches, dependencias, configuracion efectiva y proceso de
build. XFCE, SDDM, SSH y XRDP deben permanecer disponibles como entorno de
recuperacion durante el trabajo.

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
