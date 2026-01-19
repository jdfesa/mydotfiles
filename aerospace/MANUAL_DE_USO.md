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
Para no quedarte sin teclas, usamos "Modos". Cuando entras en un modo, **aparecerá un indicador ROJO en la barra superior**.

### 1. Modo Normal (Por defecto)
Aquí pasas el 99% del tiempo.
*   `Hyper + h/j/k/l`: Mover el *foco* (mirar a otra ventana).
*   `Hyper + 1-8`: Cambiar de Escritorio.
*   `Alt + h/j/k/l`: **Mover** la ventana actual de lugar.
*   `Alt + Shift + h/j/k/l`: **⚠️ SUPER PODER: Forzar Split (Join)**.
    *   Úsalo cuando quieras "meter" la ventana actual dentro de otra.
    *   Ejemplo: Tienes Chrome. Quieres Terminal a su derecha. Foco en Terminal -> `Alt + Shift + Izq` (Hacia Chrome).

### 2. Modo Resize (`Hyper + R`)
*Aparece "RESIZE" en la barra.*
*   Mueve `h` (más angosto) o `l` (más ancho).
*   **Recuerda**: Solo funciona si tienes al menos 2 ventanas.
*   `Esc`: Salir.

### 3. Modo Layout (`Hyper + /`)
*Aparece "LAYOUT" en la barra.*
*   `v`: Cambiar a orientación **Vertical** (una arriba de otra).
*   `h`: Cambiar a orientación **Horizontal** (una al lado de otra).
*   `a`: Acordeón (Colapsa las ventanas inactivas).
*   `Esc`: Salir.

### 4. Modo Persistencia (`Hyper + P`)
*Aparece "PERSISTENCE" en la barra.*
*   `s`: **Save** (Guardar foto de tus ventanas actuales).
*   `l`: **Load** (Restaurar esa foto tras reiniciar).

---

## 🖱️ Barra Interactiva (Sketchybar)
Tu barra no es solo adorno:
1.  **Escritorio Activo**: El número se pone VERDE y los iconos de las apps te siguen.
2.  **Lista de Apps**: Ves iconos de TODAS las ventanas abiertas.
    *   **Click en icono**: Trae esa ventana a tu lado (Split Izquierdo) sin quitarte el foco. ¡Magia!

---

## 🆘 Solución de Problemas Comunes

**"No puedo dividir Chrome y Antigravity"**
1.  Usa el **Super Poder**: `Alt + Shift + Flechas`.
2.  Esto fuerza a que se unan.

**"Hyper+R no hace nada"**
1.  ¿Estás solo en el escritorio? -> Es normal.
2.  ¿Hay más ventanas? -> Mira la barra. Si dice "RESIZE", usa `H` y `L`.

**"Se rompió todo"**
1.  `Hyper + ;` (Modo Servicio).
2.  `R`: "Aplanar todo" (Resetea la estructura visual).
3.  `Esc`: Recargar configuración.
