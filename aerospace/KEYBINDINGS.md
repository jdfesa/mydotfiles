# AeroSpace Keybindings

Este documento es la chuleta de uso diario. La mnemotecnia de workspaces esta en [WORKSPACES.md](WORKSPACES.md), y los conceptos de layouts/modos estan en [CONCEPTS.md](CONCEPTS.md).

## Modificadores

| Nombre | Modificadores reales | Intencion |
|---|---|---|
| `Hyper` | `cmd-ctrl-alt-shift` | Navegar, mirar, cambiar foco |
| `Meh` | `ctrl-alt-shift` | Actuar, mover, enviar, entrar a modos |

Regla personal de esta configuracion:

- `Hyper + tecla` = ir o mirar.
- `Meh + tecla` = mover, enviar o ejecutar una accion.

## Main Mode

Este es el modo normal. Si no ves `[S]` ni `[R]` en Sketchybar, estas en `main`.

### Ir a Workspace

| Atajo | Accion |
|---|---|
| `Hyper + U` | Ir a `U` |
| `Hyper + I` | Ir a `I` |
| `Hyper + O` | Ir a `O` |
| `Hyper + P` | Ir a `P` |
| `Hyper + Y` | Ir a `Y` |
| `Hyper + N` | Ir a `N` |
| `Hyper + Tab` | Volver al workspace anterior |

### Enviar Ventana a Workspace

| Atajo | Accion |
|---|---|
| `Meh + U` | Enviar ventana a `U` |
| `Meh + I` | Enviar ventana a `I` |
| `Meh + O` | Enviar ventana a `O` |
| `Meh + P` | Enviar ventana a `P` |
| `Meh + Y` | Enviar ventana a `Y` |
| `Meh + N` | Enviar ventana a `N` |

### Foco Entre Ventanas

| Atajo | Accion |
|---|---|
| `Hyper + H` | Foco izquierda |
| `Hyper + J` | Foco abajo |
| `Hyper + K` | Foco arriba |
| `Hyper + L` | Foco derecha |

### Mover Ventana en el Layout

| Atajo | Accion |
|---|---|
| `Meh + H` | Mover ventana izquierda |
| `Meh + J` | Mover ventana abajo |
| `Meh + K` | Mover ventana arriba |
| `Meh + L` | Mover ventana derecha |

### Layout y Pantalla

| Atajo | Accion |
|---|---|
| `Hyper + A` | Alternar `tiles` / `accordion` |
| `Hyper + F` | Toggle fullscreen de AeroSpace |

## Resize Mode

Entrar:

```text
Meh + M
```

Sketchybar muestra `[R]`. La `M` ancla **Measure/Medir**.

Mientras estas en `[R]`, soltas `Meh` y usas teclas simples:

| Tecla | Accion |
|---|---|
| `H` | Achicar ancho |
| `L` | Agrandar ancho |
| `J` | Agrandar alto |
| `K` | Achicar alto |
| `B` | Balancear tamanos del workspace |
| `Esc` / `Enter` | Volver a `main` |

Ejemplo:

```text
Meh + M -> L -> L -> H -> Enter
```

Eso entra a resize, agranda dos pasos, achica uno y sale.

Nota: resize se entiende mejor en layout `tiles`. En `accordion` puede sentirse raro porque no todas las ventanas estan visibles a la vez.

## Service Mode

Entrar:

```text
Meh + ;
```

Sketchybar muestra `[S]`. Este modo es para mantenimiento rapido.

| Tecla | Accion |
|---|---|
| `Esc` | Recargar config y volver a `main` |
| `Enter` | Volver a `main` sin recargar |
| `R` | Resetear layout del workspace con `flatten-workspace-tree` |
| `F` | Toggle floating / tiling |
| `B` | Balancear tamanos y volver a `main` |

## Letras Especiales

`B` significa **Balance**. No es `Meh + B` directo; solo funciona dentro de `resize` o `service`.

`R` en Sketchybar significa **Resize mode**. No es la tecla `R`; es el indicador visual de modo activo.

`S` en Sketchybar significa **Service mode**.

## Practica Recomendada

1. Abrir dos ventanas en el mismo workspace.
2. Confirmar que el workspace esta en `tiles` con `Hyper + A` si hace falta.
3. Entrar a resize con `Meh + M`.
4. Probar `H` y `L`.
5. Presionar `B` para balancear.
6. Salir con `Enter`.
