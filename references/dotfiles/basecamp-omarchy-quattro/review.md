# Omarchy Quattro Review

## Decisions

| Area | Estado | Decision | Validation |
|---|---|---|---|
| Modelo de configuracion Hyprland Lua | `adopt` | Probar primero el config upstream exacto bajo un root paralelo | Revision estatica completada; canary pendiente |
| Bindings de tiling, foco y workspaces | `adopt` | Conservar inicialmente todo el mapa upstream y personalizar despues | Canary pendiente |
| Universal copy/cut/paste | `adopt` | Probar el comportamiento upstream completo antes de modificarlo | Canary pendiente |
| Reglas y tags de aplicaciones | `adopt` | Copiar las reglas completas; las apps ausentes se evaluan despues | Inventario de apps pendiente |
| Quickshell integrado | `adopt` | Ejecutar el shell completo desde un checkout oficial fijado | Dependencias declaradas; canary pendiente |
| Menu, bar y notificaciones | `adopt` | Mantener los plugins upstream como centro de la experiencia inicial | Canary pendiente |
| Clipboard manager | `adapt` | Exigir exclusion comprobada de contenido sensible de Bitwarden | Prueba de seguridad pendiente |
| Lock, idle y polkit | `adopt` | Probar los plugins Quickshell en la sesion aislada sin cambiar PAM global | Canary pendiente |
| Audio, red, Bluetooth y energia | `adopt` | Cargar los paneles upstream; no aplicar provisioning del sistema | Dependencias declaradas; hardware pendiente |
| Temas y generador semantico | `adopt` | Copiar los 22 temas y sus plantillas como parte del runtime fijado | Canary pendiente |
| 1Password | `defer` | Conservar el binding upstream durante el baseline; reemplazar por Bitwarden despues | No instalar 1Password |
| Bitwarden | `keep` | Mantener como gestor y adaptar regla/binding Quattro | Prueba de launcher pendiente |
| Instalador, boot, pacman y repos Omarchy | `remove` | No forman parte del trasplante | Fuera de alcance confirmado |
| Apps preinstaladas de Omarchy | `reference-only` | Evaluar individualmente, nunca instalar en bloque | Pendiente por aplicacion |

## Canary Architecture

1. Mantener `Hyprland (uwsm-managed)` como sesion estable.
2. Agregar `Hyprland Quattro Lab` como segunda sesion SDDM/UWSM.
3. Usar un config root distinto y una variable de runtime propia; nunca cargar
   codigo desde `references/inbox/`.
4. Materializar el runtime upstream completo y fijado fuera de `references/`,
   con los dotfiles personalizables versionados en el perfil.
5. Ejecutar Lua y Quickshell completos desde el primer baseline, deshabilitando
   solamente el provisioning de distribucion que alteraria el host.
6. Sustituir apps y decisiones opinionadas solamente despues de que el baseline
   arranque y pueda compararse con upstream.
7. Promover componentes a la sesion estable solamente despues de pruebas y un
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
