# 📊 Sketchybar Configuration Documentation

Bienvenido a la documentación interna de tu setup de **Sketchybar**. Este archivo explica cómo funciona cada componente, plugin e item para facilitar futuras modificaciones.

## 🏗 Arquitectura General

Sketchybar funciona mediante un sistema de **Items** (elementos visuales) que ejecutan **Plugins** (scripts bash) en respuesta a **Eventos**.

La configuración se carga desde `sketchybarrc`, que a su vez carga otros archivos:

*   **`sketchybarrc`**: Archivo maestro. Inicializa la barra, define variables globales y carga los items.
*   **`colors.sh`**: Define la paleta de colores (actualmente Catppuccin).
*   **`icons.sh`**: Mapeo de variables a iconos FontAwesome/NerdFonts.

## 📂 Estructura de Directorios

### `items/` (Definición Visual)
Aquí se definen *qué* elementos aparecen en la barra y en qué orden.

*   `spaces.sh`: **Integrado con AeroSpace**. Genera los indicadores de escritorios (1-8).
*   `current_apps.sh`: **Gestor de Ventanas**. Crea el `app_manager`.
    *   Este manager genera **botones individuales dinámicos** (`app.WINDOW_ID`) para cada ventana abierta.
    *   **Click Izquierdo**: Ejecuta `app_click.sh` -> Mueve la ventana clickeada a la **Izquierda** (Split) manteniendo el foco en tu ventana actual.
*   `front_app.sh`: Muestra el nombre de la app activa.
*   `spotify.sh`: Control e información de medios.
*   `battery.sh`, `cpu.sh`, `wifi.sh`: Información del sistema.
*   `apple.sh`: Logo de Apple y menú (estético).

### `plugins/` (Lógica y Comportamiento)
Aquí vive la inteligencia. Son scripts ejecutados por los items.

*   **`space.sh`**: **(CRÍTICO)** Gestiona la lógica de los escritorios.
    *   **Input**: Recibe `$FOCUSED_WORKSPACE` desde AeroSpace.
    *   **Lógica**: Compara el ID del workspace actual con el ID del item. Si coinciden, activa el highlight (Verde).
    *   **Click**: Ejecuta `aerospace workspace <ID>` para cambiar de escritorio.
*   `weather.sh`: Obtiene el clima (usa `secrets.sh` para coordenadas).
*   `spotify.sh`: Interactúa con la API o AppleScript de Spotify.

## 🔗 Integración AeroSpace <-> Sketchybar

La magia de que se ilumine el escritorio correcto ocurre gracias a esta conexión:

1.  **AeroSpace (`aerospace.toml`)**:
    Detecta un cambio de workspace y ejecuta:
    ```bash
    sketchybar --trigger aerospace_workspace_change FOCUSED_WORKSPACE=$AEROSPACE_FOCUSED_WORKSPACE
    ```
2.  **Sketchybar (`items/spaces.sh`)**:
    Suscribe todos los items `space.x` al evento `aerospace_workspace_change`.
3.  **Plugin (`plugins/space.sh`)**:
    Se ejecuta, lee `$FOCUSED_WORKSPACE`, y si coincide con su ID, se pinta de verde.

## 🎨 Personalización

### Cambiar Colores
Edita `colors.sh`.
*   Para cambiar el color del highlight del workspace, edita `items/spaces.sh` -> `icon.highlight_color`.

### Añadir nuevos plugins
1.  Crea el script en `plugins/mi_script.sh` (recuerda `chmod +x`).
2.  Crea la definición en `items/mi_item.sh`.
3.  Añade `source "$ITEM_DIR/mi_item.sh"` en `sketchybarrc`.

---
*Hecho para ser mantenible y escalable.* 🛠
