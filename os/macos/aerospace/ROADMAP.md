# AeroSpace Roadmap

La configuracion se incorpora por fases. La prioridad es aprender bien cada capa antes de sumar otra.

## Fase Actual

**Fase 2: Navegacion + Ajuste**

Ya estan activos:

- Workspaces por letras.
- Navegacion y movimiento con `Hyper` / `Meh`.
- Toggle `tiles` / `accordion`.
- Modo service.
- Modo resize.
- Ruteo automatico de apps principales.
- Integracion con Sketchybar para workspaces e indicador de modo.
- Colores de borde por modo de teclado.

## Fase 2: Puedo Ajustar

- [x] **Resize mode**: `Meh + M`, luego `H/J/K/L`.
- [x] **Balance sizes**: `B` dentro de resize o service.
- [x] **Balance directo**: `Meh + B` aplana, fuerza `h_tiles` y balancea el workspace.
- [x] **Floating directo**: `Meh + F` alterna la ventana enfocada entre floating y tiling.
- [x] **Toggle layout**: `Hyper + A`.
- [ ] **Join-with**: agrupar dos ventanas bajo un contenedor comun.
- [ ] **Resize smart directo**: atajo rapido para ajustar sin entrar a un modo.

## Fase 3: Tengo Superpoderes

- [x] **App routing**: reglas `on-window-detected` para apps reales.
- [x] **Sketchybar workspaces**: letras persistentes y workspace activo.
- [x] **Sketchybar mode indicator**: `[S]` y `[R]`.
- [x] **Colores de bordes por modo**: usar `scripts/borders_mode.sh`.
- [ ] **Move workspace to monitor**: mover workspace completo entre monitores.
- [ ] **Workspace-to-monitor assignment**: asignar workspaces fijos a monitores.

## Fase 4: Personalizacion Avanzada

- [ ] **Gaps personalizados**: separar visualmente ventanas si mejora legibilidad.
- [ ] **Accordion padding**: ajustar cuanto se ve de la pila.
- [ ] **Per-monitor gaps**: gaps distintos por monitor.
- [ ] **Unhide macOS hidden apps**: evaluar `automatically-unhide-macos-hidden-apps`.

## No Hacer

- [ ] ~~`after-startup-command` con `sketchybar --reload`~~

Motivo: puede crear loops de reload. Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md#cuidado-con-hooks-de-inicio).

## Criterios Para Agregar Features

- Debe respetar la gramatica `Hyper = navegar`, `Meh = actuar`.
- Debe estar documentado en el mismo cambio.
- Debe tener una mnemotecnia clara.
- Debe poder validarse con `aerospace reload-config --dry-run --no-gui`.
- Debe mejorar el flujo real, no solo existir porque AeroSpace lo permite.
