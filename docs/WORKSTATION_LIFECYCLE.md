# Workstation Lifecycle

Este documento define como una configuracion pasa de experimento a herramienta
de trabajo sin convertir la maquina principal en banco de pruebas.

## Risk Tiers

### Production: `main-workstation`

El Hackintosh actual es el entorno diario. No recibe automaticamente cambios de
Linux, perfiles refactorizados ni experimentos. El contenido de
`profiles/macos-main.links` mantiene su contrato actual y cualquier aplicacion
real requiere una operacion separada y aprobada.

### Canary: `lab-desktop-01`

La maquina Arch con i7-4790K y RX 550 existe para probar el sistema durante
meses, aprender el flujo y medir estabilidad. Puede reinstalarse y no almacena
datos sensibles. Es el primer destino para:

- actualizaciones de Arch;
- cambios de kernel, drivers y sesion;
- diferencias entre X11 y Wayland;
- Hyprland, su futura migracion a Lua y plugins;
- ensayos de backup, rollback y recuperacion.

## Promotion Flow

```text
idea
  -> experimental layer
  -> canary smoke test
  -> sustained canary use
  -> documented recovery drill
  -> stable reusable profile
  -> production-eligible change
```

No existe promocion por tiempo solamente. Un cambio debe demostrar utilidad,
estabilidad, compatibilidad y rollback.

## Hyprland Core And Plugins

`os/linux/hyprland/config/` es el nucleo versionado. Los componentes Wayland
reutilizables siguen bajo `os/linux/wayland/`.

Cuando se adopte el primer plugin, debe tener responsabilidad propia:

```text
os/linux/hyprland/plugins/<plugin>/
  README.md        # origen, version, compatibilidad y rollback
  config/          # solamente configuracion del plugin
  scripts/         # instalacion/verificacion, si son necesarios
```

Cada plugin debe probarse contra la version instalada de Hyprland y nunca entra
implicitamente en `arch-hyprland`. Una futura capa experimental, por ejemplo
`layers/linux-hyprland-plugins`, lo activa solo en el canary. Si un plugin falla,
se retira esa capa sin modificar el nucleo estable.

## Hardware Qualification

Antes de seleccionar un perfil en otro host se registra y valida:

1. CPU, arquitectura y microcode;
2. GPU primaria, driver y aceleracion;
3. salidas, resolucion, escala y disposicion de monitores;
4. audio, microfono y persistencia despues de reiniciar;
5. red, Bluetooth y dispositivos de entrada;
6. suspension, bloqueo y retorno;
7. kernel principal y fallback;
8. TTY, SSH, sesion de recuperacion y medio externo;
9. snapshots y backup externo, que son controles diferentes;
10. aplicaciones criticas, presentacion y screen sharing.

Una diferencia de hardware genera primero una observacion. Solo genera un
override versionado si la deteccion automatica o los defaults portables no
resuelven el caso.

## Supported Repository Scope

Este repositorio cubre actualmente:

- macOS/Hackintosh como produccion;
- Arch Linux con capas X11 y Wayland como laboratorio;
- Windows 11 de forma incremental y secundaria.

NixOS queda fuera del alcance actual. Si se adopta, tendra un repositorio
declarativo separado; esa decision no se implementa durante epocas de clases ni
antes de que exista una prueba real.
