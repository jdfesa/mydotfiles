# Omarchy Quattro Review

## Decisions

| Area | Estado | Decision | Validation |
|---|---|---|---|
| Modelo de configuracion Hyprland Lua | `adapt` | Usar como base para la migracion 0.57, con namespace y rutas propias | Revision estatica completada; canary pendiente |
| Bindings de tiling, foco y workspaces | `adapt` | Conservar el comportamiento coherente y retirar comandos Omarchy innecesarios | Comparacion con mapa local pendiente |
| Universal copy/cut/paste | `adapt` | Probar el comportamiento Mac/Windows sin sacrificar shortcuts de terminal | Canary pendiente |
| Reglas y tags de aplicaciones | `adapt` | Adoptar solamente aplicaciones realmente usadas | Inventario de apps pendiente |
| Quickshell integrado | `adapt` | Portar como capa independiente despues del nucleo Lua; no instalar la distribucion | Cierre transitivo de dependencias pendiente |
| Menu, bar y notificaciones | `adapt` | Son el centro de la experiencia; habilitar por plugins en la sesion lab | Quickshell pendiente |
| Clipboard manager | `adapt` | Exigir exclusion comprobada de contenido sensible de Bitwarden | Prueba de seguridad pendiente |
| Lock, idle y polkit | `reference-only` | Mantener hyprlock/hypridle/polkit actual hasta validar PAM y bloqueo | No apto para primera fase |
| Audio, red, Bluetooth y energia | `reference-only` | No reemplazar controles estables hasta probar cada panel por separado | Dependencias y hardware pendientes |
| Temas y generador semantico | `adapt` | Portar paletas/plantillas despues de estabilizar el shell | Auditoria de activos pendiente |
| 1Password | `remove` | No instalar; reservar o reasignar su binding a Bitwarden | Decision del usuario |
| Bitwarden | `keep` | Mantener como gestor y adaptar regla/binding Quattro | Prueba de launcher pendiente |
| Instalador, boot, pacman y repos Omarchy | `remove` | No forman parte del trasplante | Fuera de alcance confirmado |
| Apps preinstaladas de Omarchy | `reference-only` | Evaluar individualmente, nunca instalar en bloque | Pendiente por aplicacion |

## Canary Architecture

1. Mantener `Hyprland (uwsm-managed)` como sesion estable.
2. Agregar `Hyprland Quattro Lab` como segunda sesion SDDM/UWSM.
3. Usar un config root distinto y una variable de runtime propia; nunca cargar
   codigo desde `references/inbox/`.
4. Empezar con Lua, bindings y reglas portables, conservando Waybar/Mako y los
   mecanismos actuales de lock/idle.
5. Incorporar Quickshell en la sesion lab cuando su cierre de dependencias este
   declarado y empaquetado.
6. Promover componentes a la sesion estable solamente despues de pruebas y un
   rollback documentado.

## Acceptance Gates

- La sesion estable, XFCE y XRDP siguen arrancando.
- Logout mediante UWSM no deja unidades colgadas.
- Screen sharing y file pickers funcionan mediante xdg-desktop-portal.
- Lock, DPMS y suspend/resume son predecibles.
- Audio Realtek mantiene el perfil funcional.
- Bitwarden no deja secretos recuperables en el historial del portapapeles.
- Un paquete ausente deshabilita una funcion; no aborta toda la sesion.
- Ninguna actualizacion de Omarchy puede sobrescribir los archivos locales.

## Exit Criteria

La evaluacion termina cuando cada componente elegido vive en `os/linux/` o
`shared/`, conserva atribucion cuando corresponde, declara sus dependencias y
supera las pruebas en la sesion canary. El clon ignorado se elimina al cerrar
el dossier.
