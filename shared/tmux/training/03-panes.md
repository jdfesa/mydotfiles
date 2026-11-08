# Level 3: Panes

## Goal

Ver dos tareas simultáneamente. Conserva ventanas para tareas distintas y
paneles cuando necesites verlas lado a lado.

## New Keys

| Después del prefijo | Acción |
|---|---|
| `\` | Dividir izquierda/derecha |
| `-` | Dividir arriba/abajo |
| Flechas | Cambiar de panel |
| `m` | Maximizar/restaurar sin cerrar los demás |
| `h/j/k/l` | Redimensionar izquierda/abajo/arriba/derecha |

## Exercise

1. Crea una ventana vacía con prefijo → `c`; llámala `paneles` con `,`.
2. Prefijo → `\`: aparecen dos terminales lado a lado.
3. Prefijo → flecha izquierda/derecha: cambia de panel.
4. En uno de ellos, prefijo → `-`: aparece una división arriba/abajo.
5. Cambia de panel con prefijo y flechas; suéltalo antes de la flecha.
6. Prefijo → `m`: el panel ocupa la ventana. Repite para recuperar los demás.
7. Cuando esto resulte cómodo, prueba prefijo → `h/j/k/l` para ajustar tamaño.
   No son las teclas de navegación de este nivel.

`\` es la barra inversa, no `/`. Su posición depende de la distribución del
teclado: se busca el carácter, no una posición física universal.

## Keep the Portable Path

La navegación de este entrenamiento es **prefijo y flechas**. `Ctrl+h/j/k/l`
sin prefijo es una extensión dependiente de plugins, terminal y editor. Hay
diferencias Linux/macOS y conflictos con el shell: consulta
[Compatibility](compatibility.md#contextual-extensions). No necesitas esa
extensión para trabajar con paneles.

## Ready for the Next Level

- Distingues cambiar de ventana de cambiar de panel.
- Puedes maximizar y recuperar la disposición anterior.
- No necesitas otras teclas del núcleo para pasar de Arch a macOS.

Sigue con [Level 4: Copy Mode](04-copy-mode.md), o vuelve al [índice](README.md).
