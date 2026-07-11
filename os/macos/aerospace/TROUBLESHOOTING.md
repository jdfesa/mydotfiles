# AeroSpace Troubleshooting

Este documento agrupa sintomas, causas probables y soluciones. Para atajos diarios ver [KEYBINDINGS.md](KEYBINDINGS.md). Para scripts e integracion con Sketchybar ver [SCRIPTS.md](SCRIPTS.md).

## Checklist Rapido

```bash
aerospace reload-config --dry-run --no-gui
aerospace list-workspaces --all
aerospace list-windows --all
aerospace list-monitors
```

Si el dry-run pasa, el TOML es valido. Si un comportamiento sigue raro, revisar conflictos de teclado, estado de Sketchybar o layout del workspace.

## Solo Veo 1 Workspace

**Causa probable**: faltan workspaces persistentes o AeroSpace no leyo la config activa.

**Solucion**:

- La config define `persistent-workspaces = ["U", "I", "O", "P", "Y", "N"]`.
- Recargar con `Meh + ; -> Esc`.
- Verificar con `aerospace list-workspaces --all`.

## Las Ventanas Desaparecieron

**Causa probable**: AeroSpace emula workspaces moviendo ventanas no visibles fuera del area normal.

**Solucion**:

```bash
aerospace list-windows --all
```

Si AeroSpace crashea, algunas ventanas pueden quedar casi invisibles en una esquina. En ese caso, arrastrarlas manualmente al centro o reiniciar AeroSpace.

## Un Atajo No Funciona

**Causas probables**:

- Karabiner-Elements intercepta la tecla.
- Raycast, macOS u otra app ya usa el mismo atajo.
- La config no fue recargada.
- Estas en un modo distinto (`[R]` o `[S]`) y las teclas activas cambiaron.

**Solucion**:

1. Mirar Sketchybar: si ves `[R]` o `[S]`, salir con `Enter` o `Esc`.
2. Recargar con `Meh + ; -> Esc`.
3. Validar config:

```bash
aerospace reload-config --dry-run --no-gui
```

4. Revisar conflictos con Karabiner/Raycast si el atajo sigue sin responder.

## Estoy en Resize y No Pasa Nada

**Causa probable**: estas en layout `accordion`, hay una sola ventana visible o la ventana enfocada no esta en tiling.

**Solucion**:

- Usar resize principalmente en `tiles`.
- Cambiar layout con `Hyper + A`.
- Para el caso comun de comparar dos ventanas, usar `Meh + B` para forzar `tiles` horizontales y balancear.
- Entrar a resize con `Meh + M`.
- Probar `H/L` para ancho y `J/K` para alto.
- Balancear con `B`.

## Las Ventanas Estan Anidadas o Raras

**Causa probable**: el arbol del workspace quedo con una estructura poco util despues de mover ventanas.

**Solucion**:

```text
Meh + ; -> R
```

Eso ejecuta `flatten-workspace-tree` y vuelve a `main`.

## Quiero que una Ventana Flote

**Solucion**:

```text
Meh + F
```

Eso alterna la ventana enfocada entre `floating` y `tiling`. Tambien se puede hacer desde service mode con `Meh + ; -> F`.

## AeroSpace Corre, Pero la CLI Dice `server is not running`

**Causa probable**: el proceso de AeroSpace esta vivo, pero el cliente CLI no pudo conectar al server/socket de esa sesion.

Verificar si la app esta viva:

```bash
ps -axo comm | grep AeroSpace
```

Si aparece `/Applications/AeroSpace.app/...`, el problema no es que AeroSpace este cerrado.

**Soluciones posibles**:

- Recargar desde el icono de AeroSpace en la barra de menu.
- Reiniciar AeroSpace.
- Volver a probar `aerospace list-workspaces --all`.

Nota: dentro de entornos con sandbox puede fallar la conexion al socket aunque AeroSpace este corriendo. En ese caso, probar el mismo comando desde una terminal normal.

## Sketchybar No Muestra Workspaces o Indicador de Modo

**Causas probables**:

- Sketchybar arranco antes que AeroSpace.
- Sketchybar no encontro `/usr/local/bin/aerospace`.
- El item `aerospace_mode` no existe porque Sketchybar no recargo el modulo Lua.

**Solucion**:

```bash
brew services restart sketchybar
```

Verificacion:

```bash
sketchybar --query space.U
```

El detalle de la integracion esta en [SCRIPTS.md](SCRIPTS.md) y en [../sketchybar/TROUBLESHOOTING.md](../sketchybar/TROUBLESHOOTING.md).

## Despues de Editar el TOML

Validar antes de confiar:

```bash
aerospace reload-config --dry-run --no-gui
```

Recargar:

```bash
aerospace reload-config --no-gui
```

O con teclado:

```text
Meh + ; -> Esc
```

## Cuidado con Hooks de Inicio

No agregar `after-startup-command` para recargar Sketchybar ni para disparar comandos que llamen a `reload-config`. Puede generar loops de reload y congelar la sesion grafica.

La regla segura para este repo:

- Sketchybar maneja sus propios retries.
- AeroSpace no debe forzar `sketchybar --reload` al iniciar.
- Los hooks de AeroSpace deben ser pequenos, previsibles y documentados.
