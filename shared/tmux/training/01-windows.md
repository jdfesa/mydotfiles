# Level 1: Windows

## Goal

Usar una sesión con tres ventanas en lugar de abrir tres terminales del emulador.
Por ahora no hacen falta paneles, plugins ni varias sesiones.

## Mental Model

- **Sesión:** tu espacio de trabajo.
- **Ventana:** una terminal para una tarea, parecida a una pestaña.
- **Panel:** una división dentro de una ventana; se practica después.

```text
Kitty
└── sesión work
    ├── 1: editor
    ├── 2: comandos
    └── 3: servidor
```

No necesitas crear una sesión por cada terminal. Los escritorios del sistema
siguen existiendo; estas ventanas se organizan dentro de tmux.

## Start Small

Desde un shell **fuera de tmux**:

```sh
rtk proxy tmux new-session -A -s work
```

Crea `work` si no existe o vuelve a ella si ya existe. No reinicia sus tareas.
Si ya estás dentro, no anides tmux: consulta el nivel 2.

**Prefijo = `Ctrl+Espacio`: pulsa ambas teclas, suéltalas y pulsa la acción.**

| Después del prefijo | Acción |
|---|---|
| `c` | Crear otra ventana |
| `1`, `2`, `3`… | Elegir directamente esa ventana |
| `n` / `p` | Ventana siguiente / anterior |
| `w` | Mostrar ventanas; elegir con flechas y Enter; `q` sale |
| `,` | Renombrar ventana; escribir nombre y Enter |
| `?` | Consultar atajos; `q` sale de la ayuda |

## First Exercise

Si `work` ya contiene trabajo importante, conserva sus ventanas y practica
con ventanas nuevas; no borres nada para hacer coincidir los números.

1. En una sesión nueva, prefijo → `,`: renombra la ventana inicial como `editor`.
2. Abre tu editor normalmente allí, si lo necesitas.
3. Prefijo → `c`; renombra la segunda ventana como `comandos`.
4. Prefijo → `c`; renombra la tercera como `servidor`. No necesitas arrancar
   un servidor para practicar.
5. Alterna con prefijo → `1`, después `2` y después `3`.
6. Usa prefijo → `w`; elige una ventana con flechas y Enter.
7. Si pierdes el hilo, prefijo → `?`, luego `q` para volver.

Las ventanas nuevas heredan el directorio del panel activo. Usa `cd` cuando
corresponda: el nombre de una ventana no cambia su directorio.

## Habit Cue

> Cuando quieras abrir otra terminal: `Ctrl+Espacio`, soltar, `c`.
> Si te pierdes: `Ctrl+Espacio`, soltar, `w`.

Repite el circuito en tareas reales. No necesitas más ventanas ni más teclas
para que este nivel sea útil.

## Ready for the Next Level

- Puedes crear/renombrar una ventana sin abrir otro Kitty.
- Vuelves a una tarea con su número o el selector `w`.
- Distingues ventana tmux, pestaña Kitty y escritorio del sistema.

Sigue con [Level 2: Sessions](02-sessions.md), o vuelve al [índice](README.md).
