# Wayland

Infraestructura de sesion reutilizable por Hyprland, Sway u otros compositores
Wayland. Los compositores siguen viviendo como herramientas propias bajo
`os/linux/<compositor>/`; esta carpeta evita duplicar barras, launchers,
notificaciones y scripts que no dependen de uno solo.

## Componentes iniciales

- `waybar/`: barra modular;
- `mako/`: daemon de notificaciones;
- `wofi/`: launcher de aplicaciones;
- `scripts/wayland-screenshot`: captura con Grim, Slurp y wl-clipboard;
- `scripts/wayland-power-menu`: menu de bloqueo, salida y energia.

La paleta inicial usa colores Tokyo Night tomados de la referencia Omarchy,
pero los archivos son configuraciones propias y no dependen de comandos
`omarchy-*`.

## Limites

- Kitty separa sus entrypoints en `os/linux/kitty/` y `os/macos/kitty/`, con
  una base portable en `shared/kitty/common.conf`.
- Hyprlock e Hypridle viven con Hyprland porque pertenecen a su ecosistema.
- Los paquetes se declaran en `../packages/lists/30-wayland-desktop.txt`.
- No se guardan fondos descargados sin licencia clara; la primera iteracion usa
  un fondo solido y deja el sistema de wallpapers para una etapa posterior.

## Sesiones graficas simultaneas

UWSM, D-Bus y systemd mantienen servicios por usuario, no completamente por
sesion grafica. Ejecutar XFCE/XRDP y Hyprland al mismo tiempo con el usuario
`jd` puede causar que:

- Thunar abra su ventana en la sesion X11 existente;
- Mako y XFCE Notify compitan por `org.freedesktop.Notifications`;
- dos agentes PolicyKit intenten registrarse;
- PipeWire conserve una salida elegida desde la otra sesion.

Las pruebas de aceptacion deben hacerse despues de cerrar realmente la sesion
XRDP, no solo desconectar el cliente. Si se necesita concurrencia permanente,
se evaluara un usuario dedicado para XRDP en vez de agregar workarounds a cada
aplicacion.
