# 📖 Manual de Uso: Tu Nuevo Entorno

Bienvenido a tu nueva nave espacial. Este manual no es técnico, es lógico. Aquí entenderás cómo moverte, organizar tus ventanas y por qué las cosas pasan como pasan.

## 🧠 Conceptos Básicos (Léeme primero)

Antes de presionar teclas, entiende cómo "piensa" **AeroSpace**:

1.  **Todo es una Baldosa (Tile)**: Las ventanas no flotan una encima de otra. Ocupan el 100% del espacio disponible.
    *   *Si tienes sola UNA ventana*: Ocupará toda la pantalla (menos los huecos).
    *   *Si abres otra*: Se dividirán el espacio automáticamente (50/50).

2.  **El Misterio del "Resize" (Redimensionar)**:
    *   **Pregunta**: *"¿Por qué si presiono Hyper+R y trato de achicar una ventana sola, no pasa nada?"*
    *   **Respuesta**: Porque **no tiene a quién cederle ese espacio**. En este sistema, para hacer una ventana más chica, otra debe hacerse más grande. Si estás solo en el escritorio, no puedes cambiar tu tamaño porque el sistema te obliga a llenar el hueco.

3.  **Aplanamiento (Flattening)**:
    *   Por defecto, el sistema intenta mantener todo simple. Si mueves una ventana a la derecha, simplemente se pone al lado. No crea "cajas dentro de cajas" infinitas... a menos que tú se lo ordenes (ver "Forzar Split").

---

## ⌨️ La Tecla Maestra: HYPER
Tu tecla `Hyper` es la combinación de **Cmd + Alt + Ctrl + Shift**.
En tu teclado (Silakka54), esto está muy accesible (ej. manteniendo `Enter` o tecla dedicada).

*   **HYPER**: Se usa para **NAVEGAR** (Mirar, cambiar de modo).
*   **ALT**: Se usa para **MOVER** (Acciones físicas con la ventana).

---

## 🚦 Modos (El Semáforo)
Para no quedarte sin teclas, usamos "Modos". Cuando entras en un modo, **el color del BORDE de la ventana cambiará**.

### 1. Modo Normal (Borde AZUL)
Aquí pasas el 99% del tiempo.
*   `Hyper + h/j/k/l`: Mover el *foco* (mirar a otra ventana).
*   `Hyper + 1-8`: Cambiar de Escritorio.
*   `Alt + h/j/k/l`: **Mover** la ventana actual de lugar.
*   `Alt + Shift + h/j/k/l`: **⚠️ SUPER PODER: Forzar Split (Join)**.

### 2. Modo Resize (`Hyper + R`) -> Borde ROJO 🔴
*¡Peligro! Estás modificando tamaños.*
*   Mueve `h` (más angosto) o `l` (más ancho).
*   **Recuerda**: Solo funciona si tienes al menos 2 ventanas.
*   `Esc`: Salir (Vuelve a Azul).

### 3. Modo Layout (`Hyper + /`) -> Borde VERDE 🟢
*Organización y estructura.*
*   `v`: Cambiar a orientación **Vertical** (una arriba de otra).
*   `h`: Cambiar a orientación **Horizontal** (una al lado de otra).
*   `a`: **Acordeón** (Apila las ventanas como cartas).
    *   *Nota*: En este modo NO puedes cambiar el tamaño de las ventanas individualmente.
*   `t`: **Mosaico (Tiles)** (Vuelve al modo normal donde todas se ven).
*   `Esc`: Salir.

### 4. Modo Persistencia (`Hyper + P`) -> Borde VIOLETA 🟣
*Memoria del sistema.*
*   `s`: **Save** (Guardar foto de tus ventanas actuales).
*   `l`: **Load** (Restaurar esa foto tras reiniciar).
*   `Esc`: Salir.

### 5. Modo Servicio (`Hyper + ;`) -> Borde ROSA 🌸
*Mantenimiento.*
*   `r`: **Resetear layout (Aplanar)**. Si tus ventanas se ven raras o no las encuentras, pulsa esto.
*   `esc`: Recargar configuración.

---

## 📐 Entendiendo los Layouts (¿Dónde están mis ventanas?)

A veces AeroSpace apila las ventanas y parecen desaparecer. Esto pasa por el **Acordeón**.

### Acordeón vs Tiles
*   **Tiles (Mosaico)**: Todas las ventanas comparten el espacio y ninguna se tapa. Es el modo por defecto.
*   **Acordeón**: Las ventanas se apilan "hacia el fondo". Solo ves una barrita de las que están atrás.
    *   **¿Para qué sirve?**: Si tienes 10 ventanas y quieres enfocarte en una sin que las otras se hagan diminutas.
    *   **¿Cómo salgo?**: `Hyper + /` y luego pulsa `t` (Tiles) o usa el "Botón de Pánico" (`Hyper + ;` luego `r`).

## 🖱️ Barra Interactiva (Sketchybar)
Tu barra no es solo adorno:
1.  **Escritorio Activo**: El número se pone VERDE y los iconos de las apps te siguen.
2.  **Lista de Apps**: Ves iconos de TODAS las ventanas abiertas.
    *   **Click en icono**: Trae esa ventana a tu lado (Split Izquierdo) sin quitarte el foco. ¡Magia!

---

## 🛠️ Arquitectura Técnica (Scripts)

Para que todo esto funcione, usamos scripts personalizados en `~/.mydotfiles/aerospace/scripts/`. Si eres curioso o necesitas arreglar algo, aquí está qué hace cada uno:

### 1. `borders_mode.sh`
*   **Función**: Es el cerebro de los colores.
*   **Uso**: Recibe el nombre del modo (ej. `RESIZE`) y le habla a **JankyBorders** para cambiar el color del borde activo.
*   **Colores**: Azul (Normal), Rojo (Resize), Verde (Layout), Violeta (Persistencia), Rosa (Servicio).

### 2. `save_layout.py`
*   **Función**: "congela" el estado actual.
*   **Lógica**: Lee todas las ventanas abiertas y sus posiciones usando `aerospace list-windows --json` y las guarda en un archivo temporal JSON.

### 3. `restore_layout.py`
*   **Función**: "descongela" el estado.
*   **Lógica**: Lee el archivo JSON guardado e intenta mover las ventanas a sus escritorios originales.

---

## 🆘 Solución de Problemas Comunes

**"No puedo dividir Chrome y Antigravity"**
1.  Usa el **Super Poder**: `Alt + Shift + Flechas`.
2.  Esto fuerza a que se unan.

**"Hyper+R no hace nada"**
1.  ¿Estás solo en el escritorio? -> Es normal.
2.  ¿Hay más ventanas? -> Mira el borde. Si es **ROJO**, usa `H` y `L`.

**"Se rompió todo"**
1.  `Hyper + ;` (Modo Servicio).
2.  `R`: "Aplanar todo" (Resetea la estructura visual).
3.  `Esc`: Recargar configuración.
