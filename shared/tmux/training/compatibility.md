# Shortcut Compatibility

Auditoría de solo lectura del **2026-11-08**, centrada en Arch y macOS. No se
cambiaron atajos globales, terminales ni sesiones activas. Se conserva el
[núcleo aprendido](keybindings.md), no se garantiza una combinación libre
en cualquier aplicación futura.

## Input Route

```text
teclado/remapeador → sistema/gestor de ventanas → terminal
  → tmux (prefijo y tabla de teclas) → shell/editor del panel
```

Una aplicación gráfica sin foco no suele intervenir salvo que registre un
atajo global. Si una capa anterior consume el prefijo, tmux no lo recibe.
Una prueba por SSH no atraviesa el teclado físico del equipo remoto.

## Verified State

| Capa | Arch | macOS | Límite de la evidencia |
|---|---|---|---|
| Sistema/gestor | Hyprland 0.57.1: 225 bindings cargados, ninguno Ctrl solo ni catch-all | Fuentes de entrada: Ctrl+Espacio desactivado; Ctrl+Opción+Espacio activado | IPC/preferencias, sin cambiar nada |
| Fuente del gestor | El proceso carga `~/.config/hypr-quattro/hyprland.lua`, no la entrada Hyprland genérica | AeroSpace enlaza el repo y no declara bindings Ctrl solos | Archivo instalado no equivale a proceso activo |
| Remapeador | No se detectaron procesos Kanata/keyd/IBus/Fcitx consultados | Perfil Karabiner seleccionado sin modificaciones simples globales/por dispositivo ni complejas | No certifica todo mecanismo posible |
| Lanzador | Sin captura Ctrl sola en los bindings consultados | Apertura principal Raycast: `Command-49`, no Ctrl+Espacio | No se enumeraron todos sus atajos de extensiones |
| Kitty | Fuente Linux: no consume Ctrl+Espacio; limpia las sesiones propias Ctrl+b y Ctrl+Shift+s | Fuente macOS: mismo tratamiento del prefijo/sesiones | Parser instalado; no se recargaron procesos existentes |
| tmux | Servidor habitual: `prefix C-Space`, `prefix2 None`, barra inferior | Fuente e inclusión compartida revisadas; no se inició servidor habitual | Pruebas aisladas de ambos entrypoints, no de todo el escritorio |
| Ejercicio de ventanas | Interacción básica comprobada | Pendiente repetirlo físicamente | No extrapolar a todos los niveles/apps |

**Resultado:** no se detecta captura del prefijo en las capas consultadas.
No equivale a «cero conflictos con cualquier app». Las teclas ordinarias
después de soltar el prefijo pertenecen a tmux; no requieren Command/Super.

macOS suele reservar Ctrl+Espacio para fuentes de entrada. Si se reactiva en
otro equipo o al recuperar preferencias, resolver ese interceptor local antes
de validar el núcleo; no cambiar el prefijo compartido sin investigar.

## Contextual Extensions

| Combinación | Diferencia o conflicto | Tratamiento |
|---|---|---|
| Ctrl+h/j/k/l sin prefijo en el shell | El plugin tmux las reserva para navegar. En Zsh normalmente borran, aceptan línea, cortan línea y limpian pantalla | No son núcleo; usar prefijo y flechas. El comando `clear` no depende del atajo |
| Ctrl+h/j/k/l en Kitty macOS | `pass_keys.py` reconoce `nvim`, no `tmux`; puede mover ventanas Kitty en lugar de entregar la tecla | Integración avanzada pendiente; no modificada durante la auditoría |
| Ctrl+h/j/k/l en Kitty Linux | El entrypoint reconoce `nvim` y `tmux` | Adaptador preparado; verificar también el editor |
| Cruzar de split Neovim a panel tmux | tmux declara el plugin; el checkout Neovim no declara `vim-tmux-navigator`, y LazyVim usa Ctrl+h/j/k/l para splits internos | No prometer navegación transparente sin adaptar/probar Neovim |
| Ctrl+Espacio en Neovim/Blink o Zsh | Blink lo usa para completar, Zsh para marcar; tmux lo toma como prefijo antes de la aplicación | Reserva deliberada. No esperar que llegue directamente como completado dentro de tmux |
| Ctrl+s / Ctrl+r | Sin prefijo pueden pertenecer al shell/editor; con prefijo corresponden a Resurrect | Practicar el orden completo; distintos de `s` selector y `r` recarga |

La evidencia Neovim es de fuentes/plugins instalados, no de todos los mapas
dinámicos de un editor activo. En Neovim, `:verbose imap <C-Space>` y
`:verbose nmap <C-h>` muestran quién definió un mapa sin modificarlo.

## Physical Acceptance Checklist

En una ventana de prueba nueva, conservando el trabajo actual:

1. Ejecutar [Level 1](01-windows.md); Ctrl+Espacio no debe cambiar el foco a otra app.
2. Repetir desde el shell y con el editor activo en el panel.
3. Probar prefijo y flechas con dos paneles, no la extensión Ctrl+h/j/k/l.
4. Verificar `?`/`q`, y luego copiar/clipboard cuando corresponda al nivel.
5. Repetir con el teclado real: `\`, `?`, `$` y `&` son caracteres y pueden
   tener otras posiciones físicas.
6. Registrar el resultado técnico por capa sin publicar texto de sesiones ni
   dumps completos de preferencias.

`scripts/test-linux-terminal` crea HOME/socket privados y contrasta filas core
del índice con ambos entrypoints, más parsers Kitty si están disponibles. No
envía teclas al escritorio ni demuestra compatibilidad con todas las apps.

## Future Platforms

Debian, NixOS y Windows no se configuran ni certifican ahora. La intención es
conservar los gestos y adaptar shell/rutas, terminal, plugins y clipboard. En
Windows se puede evaluar tmux dentro de WSL, sin asumir equivalencia con una
consola PowerShell nativa. En NixOS no asumir `/bin/zsh`, ruta que hoy fija la
base compartida. Son condiciones futuras, no tareas desplegadas.

## Sources

- [Kitty mappings](https://sw.kovidgoyal.net/kitty/mapping/).
- [Apple keyboard conventions](https://developer.apple.com/design/human-interface-guidelines/keyboards).
- [vim-tmux-navigator](https://github.com/christoomey/vim-tmux-navigator).
- [Blink keymaps](https://cmp.saghen.dev/configuration/keymap).
- [Tmux Getting Started](https://github.com/tmux/tmux/wiki/Getting-Started).

Las observaciones de procesos/preferencias son una fotografía fechada. Repetir
la auditoría al cambiar terminal, compositor, IME, teclado o remapeador.
