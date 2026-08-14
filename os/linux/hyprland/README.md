# Hyprland

Configuracion experimental de Hyprland validada primero en `lab-desktop-01`
(hostname `arch-desktop`). XFCE permanece como entorno X11 de recuperacion hasta
que este entorno Wayland complete un periodo sostenido de uso y pruebas reales
de rollback.

## Clasificacion

Esta carpeta solo contiene configuracion propia del compositor y de sus
componentes directos:

- `config/hyprland.conf` y modulos de `config/conf.d/`;
- `hypridle.conf` para bloqueo y ahorro de energia;
- `hyprlock.conf` para la pantalla de bloqueo.

Las piezas reutilizables por otros compositores Wayland no se duplican aqui:

- Waybar, Mako, Wofi y scripts de captura/sesion viven en `../wayland/`;
- Kitty conserva su fuente canonica en `shared/kitty/`;
- paquetes reproducibles viven en `../packages/lists/30-wayland-desktop.txt`.

## Origen Omarchy

La primera base fue adaptada selectivamente desde Omarchy, sin ejecutar su
instalador ni copiar su administracion de SDDM, Limine, Snapper, Pacman o
aplicaciones. Se revisaron estas revisiones upstream:

- rama estable `master`: `edce5809df36003c96822b456f327fa79ec1cfd7`;
- rama `quattro`: `38542a1f513740559660a468ffbf68ed082b2381`.

Se conservaron ideas de modularidad, gaps, bordes, blur, animaciones y reglas de
entrada. Los comandos `omarchy-*`, sus rutas internas y su capa de aplicaciones
fueron reemplazados por herramientas ya elegidas en este repositorio.

## Activacion segura

Primero previsualizar los enlaces:

```sh
cd ~/mydotfiles
scripts/link --dry-run --repair arch-hyprland-preview
```

El perfil experimental solo enlaza terminal, prompt, metricas y las piezas
Wayland necesarias; no activa las demas capas pendientes de
`arch-workstation`. La entrada principal es:

```text
os/linux/hyprland/config -> ~/.config/hypr
```

Despues de crear el enlace, elegir manualmente `Hyprland (UWSM)` en SDDM. Este
perfil no modifica la configuracion de SDDM, no habilita autologin y no cambia
el gestor de arranque.

El perfil objetivo reusable es `arch-hyprland`; el preview se conserva mientras
el perfil general del host siga incompleto. Los plugins futuros no se agregan al
nucleo implicitamente: cada uno debe documentar version, compatibilidad,
verificacion y rollback, y activarse primero mediante una capa canary separada.

## Validacion y recuperacion

Validar la sintaxis sin iniciar una sesion:

```sh
Hyprland --verify-config --config ~/.config/hypr/hyprland.conf
```

Atajos esenciales:

| Atajo | Accion |
|---|---|
| `Super+Enter` | Kitty |
| `Super+Space` | Wofi |
| `Super+Shift+F` | Thunar |
| `Super+Shift+B` | Helium |
| `Super+Shift+A` | Configuracion de audio |
| `Super+Q` | Cerrar ventana |
| `Super+Alt+L` | Bloquear |
| `Super+Shift+E` | Menu de sesion |
| `Print` | Captura de region |
| `Shift+Print` | Captura completa |

Si la sesion queda inutilizable, cambiar a una TTY con `Ctrl+Alt+F3`, cerrar la
sesion Hyprland o reiniciar SDDM. XFCE no se elimina ni se reemplaza.

## Smoke Test Log

### Primera sesion, 2026-08-12

Confirmado por el usuario:

- compositor, monitor y efectos visuales funcionales;
- Kitty abre correctamente;
- `Super+Shift+F`, `Super+Shift+E` y audio no funcionaron en la primera prueba;
- capturas quedan postergadas hasta elegir una herramienta dedicada.

Diagnostico:

- UWSM recibio un `PATH` sin `~/.local/bin`; esto impedia encontrar
  `wayland-power-menu`. Una prueba con el entorno correcto mostro el menu
  durante dos segundos y confirmo que Wofi y el script funcionan;
- habia una sesion XFCE/XRDP activa simultaneamente con Hyprland para el mismo
  usuario. Thunar reutilizo su instancia X11 y los servicios de usuario
  compartieron notificaciones, PolicyKit y PipeWire entre ambas sesiones;
- PipeWire tenia como salida predeterminada S/PDIF del ALC892 al 40%; la salida
  AMD HDMI estaba desactivada. No se fuerza una salida sin confirmar si el
  usuario usa monitor, parlantes analogicos o S/PDIF.

Correcciones preparadas:

- exportar `~/.local/bin` mediante `environment.d` en el siguiente login;
- iniciar Thunar como aplicacion UWSM y solicitar una ventana nueva;
- agregar `Super+Shift+A` y clic sobre audio en Waybar para abrir Pavucontrol;
- agregar `Super+F10/F11/F12` como mute/bajar/subir volumen para teclados sin
  teclas multimedia;
- reutilizar las metricas CPU/GPU de DWM en Waybar.

El simbolo `~` seguido por un salto de linea y `›` provenia del prompt
predeterminado de Starship: el perfil preview enlazaba Kitty, pero no
`shared/starship/starship.toml`. Se agrego ese enlace al perfil; no se
modifico la configuracion compartida que ya funciona en macOS.

El audio analogico tampoco requeria reiniciar Arch. WirePlumber detectaba el
Realtek ALC892, pero marcaba `Line Out` y `Headphones` como no disponibles y
volvia a S/PDIF despues de reiniciar los servicios. Como solucion de prueba se
selecciono el perfil `pro-audio` y la salida fisica analogica
`alsa_output.pci-0000_00_1b.0.pro-output-0`. Tambien fue necesario desactivar
`Auto-Mute`, desmutear los controles ALSA `Master` y `Front`, dejarlos a 0 dB y
controlar el volumen desde PipeWire al 50 %. El usuario confirmo sonido correcto
en YouTube con auriculares conectados al jack verde trasero. El procedimiento
reproducible completo vive en `os/linux/audio/README.md`.

### Pantalla de bloqueo, 2026-08-13

Se reemplazo el texto visible `Contrasena` por `Password` en Hyprlock. La fecha
tambien fuerza `LC_TIME=C` para que los nombres del dia y del mes permanezcan en
ingles independientemente del locale de la sesion. Este cambio sigue la
convencion general: interfaz y configuracion del sistema en ingles;
documentacion narrativa en espanol; nombres de archivos y directorios en
ingles.
