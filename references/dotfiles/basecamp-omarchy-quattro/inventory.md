# Omarchy Quattro Inventory

## Scope

La auditoria usa la release oficial `v4.0.0` como referencia inmutable. El
objetivo no es instalar la distribucion Omarchy ni ejecutar su instalador, sino
identificar que partes de Quattro pueden adaptarse al Arch existente y probarse
en una sesion canary paralela.

La copia completa permanece ignorada en
`references/inbox/basecamp-omarchy-quattro/`. Ningun archivo de `references/`
forma parte del runtime.

## Component Map

| Area upstream | Tamano observado | Portabilidad | Relacion local |
|---|---:|---|---|
| `config/hypr/` + `default/hypr/` | 50 archivos Lua | Alta para configuracion base; media para helpers que invocan `omarchy-*` | Sustituiria gradualmente el Hyprlang actual antes de Hyprland 0.57 |
| `shell/` | 95 archivos QML | Media-baja sin su runtime; requiere Quickshell y servicios auxiliares | Se ejecuta completo solo dentro de Quattro Lab |
| `bin/` | 425 comandos/scripts | Variable | Se conserva completo para no romper contratos entre plugins y comandos |
| `themes/` | 22 temas | Media | Paletas y plantillas son adaptables; fondos y activos requieren auditoria individual |
| `default/themed/` | 17 plantillas | Media | Puede inspirar un generador propio de tema semantico |
| `config/omarchy/shell.json` | 1 configuracion | Alta una vez portado el shell | Modelo declarativo util para layout y plugins |
| `install/` + `etc/` + `default/pacman/` | Sistema completo | Baja y fuera de alcance | No importar repositorios, bootloader, instalador ni politica global de actualizaciones |

## Runtime Coupling

- El bootstrap Lua espera `OMARCHY_PATH` y carga modulos desde
  `/usr/share/omarchy` salvo que se reconfigure.
- Los defaults de Hyprland contienen mas de cien referencias a comandos
  `omarchy-*`; por ello copiar solamente dotfiles produce una sesion incompleta.
  El baseline conserva el arbol `bin/` entero y recorta despues de medir uso.
- El shell importa Quickshell, Hyprland, PipeWire, MPRIS, Notifications, PAM,
  Polkit, SystemTray, UPower, Bluetooth y Networking.
- La maquina canary ya tiene Hyprland `0.56.2`, UWSM, NetworkManager,
  WirePlumber y los portales; no tiene Quickshell, Lua 5.1 ni los comandos
  Omarchy.

## Local Collision Points

| Local | Riesgo |
|---|---|
| `~/.config/hypr` | Es un symlink al Hyprlang canonico actual; no debe apuntarse al arbol Quattro |
| Waybar, Mako, Wofi, hyprlock, hypridle, hyprpaper | Quattro los reemplaza parcial o totalmente; deben coexistir por perfil durante la prueba |
| SDDM/UWSM | Debe ofrecer una segunda entrada `Hyprland Quattro Lab`, manteniendo la sesion estable |
| XFCE/XRDP | Deben permanecer intactos como recuperacion |
| Bitwarden | Conservar; no activar ni instalar 1Password |

## Transitive Sources

Quattro agrupa herramientas y activos con proyectos propios: Hyprland,
Quickshell, fuentes, temas, iconos, fondos y aplicaciones. La licencia MIT del
repositorio permite adaptar el codigo de Omarchy, pero no reemplaza la revision
de licencia de activos obtenidos de terceros.
