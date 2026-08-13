# Linux System Monitor

Metricas ligeras reutilizables entre sesiones Linux. Esta herramienta vivia
originalmente dentro de DWM, pero no depende de X11 ni de ese window manager,
por lo que su fuente canonica se movio fuera de `dwm/`.

`scripts/status-sensors` ofrece tres formatos:

```sh
status-sensors             # texto para DWMBlocks o terminal
status-sensors --waybar    # JSON para el modulo custom de Waybar
status-sensors --notify    # detalle mediante notify-send
```

La utilizacion de CPU se calcula desde `/proc/stat` y no requiere `mpstat`. La
memoria usa `free`; las temperaturas usan `lm_sensors`. Para AMDGPU, el script
descubre dinamicamente `gpu_busy_percent` y comprueba que el dispositivo use el
driver `amdgpu`, por lo que no fija `card1` o `card2`.

## Portabilidad

- CPU y memoria: Linux generico.
- temperaturas: dependen de los sensores expuestos por cada placa y GPU;
- utilizacion GPU automatica: AMDGPU; otros drivers muestran `N/A` hasta agregar
  un lector especifico;
- presentacion: reutilizada por DWMBlocks y Waybar sin duplicar la lectura.
