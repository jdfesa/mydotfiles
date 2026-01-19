# ⌨️ Silakka54 Dotfiles Configuration

Bienvenido a la configuración de tu teclado **Silakka54** (Split 5x6 Column Staggered).

Esta carpeta contiene todo lo necesario para gestionar el layout del teclado y generar automáticamente la visualización gráfica del mismo.

## 📂 Estructura de Archivos

*   **`silakka54_main.vil`**: El archivo "fuente de la verdad". Es el layout exportado desde **Vial**. Aquí es donde haces tus cambios de teclas.
*   **`render.sh`**: Script maestro de automatización.
    *   Convierte `.vil` -> JSON intermedio.
    *   Invierte las filas de la mano derecha (porque Vial las exporta al revés).
    *   Invoca `post_process.py` para aplicar estilos.
    *   Ejecuta `keymap-drawer` para generar el SVG.
*   **`post_process.py`**: Script en Python que inyecta lógica visual.
    *   Combina los estilos de `draw_config.yaml`.
    *   Asigna automáticamente colores: Rojo para teclas destructivas (`Esc`, `Bksp`) y Azul para capas (`MO`, `LT`).
*   **`qmk_info.json`**: Definición física del teclado. Le dice al dibujante dónde va cada tecla geométricamente (stagger, pulgares).
*   **`draw_config.yaml`**: Configuración visual (CSS, modo oscuro, fuente JetBrains Mono).
*   **`requirements.txt`**: Librerías de Python necesarias (`keymap-drawer`, `PyYAML`).
*   **`keymap.svg`**: La imagen generada automáticamente. **No la edites manualmnete**.

## 🚀 Cómo Funciona la Automatización

Todo está conectado a través de **Git**.

1.  **Edita tu layout**:
    *   Usa [Vial Web](https://vial.rocks/) o Vial Desktop.
    *   Guarda tu configuración como `silakka54_main.vil` en esta carpeta (sobrescribiendo el anterior).
2.  **Haz Commit**:
    *   Simplemente ejecuta `git add .` y `git commit`.
    *   Un **Git Hook** (`.git/hooks/pre-commit`) detectará que cambiaste el `.vil`.
    *   Ejecutará `render.sh` automáticamente.
    *   Si todo sale bien, la imagen `keymap.svg` se actualizará y se añadirá a tu commit.

## 🛠 Instalación y Mantenimiento

Si cambias de ordenador o necesitas reinstalar el entorno:

1.  **Prerrequisitos**: Python 3 instalado.
2.  **Crear entorno virtual**:
    ```bash
    cd mydotfiles/silakka54
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Probar generación manual**:
    ```bash
    ./render.sh
    ```

## 🎨 Personalización Visual

Si quieres cambiar colores o estilos:

1.  Edita **`draw_config.yaml`** para cambiar el CSS (colores de fondo, fuentes).
2.  Edita **`post_process.py`** si quieres cambiar qué teclas se consideran "destructivas" (rojas) o de "capa" (azules).

---
*Documentación generada para el futuro yo.* 🤖
