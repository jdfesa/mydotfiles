# Manual de Uso: Configuración AeroSpace

> [!WARNING]
> **DEFINICIÓN DE TECLA HYPER**
>
> **Hyper = Cmd + Alt + Ctrl + Shift** (Las 4 teclas a la vez).
>
> *Esta configuración se basa en el uso de una tecla dedicada en tu teclado programable.*

Bienvenido a tu entorno de ventanas tiling. Esta configuración está diseñada para "ver" con Hyper y "mover" con Alt, priorizando la **persistencia** de tu flujo de trabajo.

## 1. Sistema de Navegación (Main Mode)

La mayoría del tiempo estarás aquí.

### 🧭 Moverse y Ver (HYPER)
*   **Foco**: `Hyper + h / j / k / l` (Izquierda, Abajo, Arriba, Derecha).
*   **Workspaces**: `Hyper + 1` al `8`.
*   **Volver**: `Hyper + Tab` (Regresa al workspace anterior).
*   **Terminal Rápida**: `Hyper + T` (Abre Ghostty).

### 📦 Mover Ventanas (ALT)
*   **Mover Física**: `Alt + h / j / k / l` (Intercambia de lugar).
*   **Enviar a WS**: `Alt + 1` al `8` (Envía la ventana sin cambiar tu foco).

---

## 2. Sistema de Modos (Hyper + Letra)

Para acciones complejas, usamos "Modos" para no rompernos los dedos.

### 💾 Modo Persistencia (`Hyper + P`)
*El sistema mágico para guardar tu sesión.*
1.  **Antes de irte**: Presiona `Hyper + P` y luego **`s`** (Save).
    *   *Esto guarda una "foto" de dónde está cada ventana.*
2.  **Al volver**: Abre tus apps desordenadas, presiona `Hyper + P` y luego **`l`** (Load).
    *   *Las ventanas volarán automáticamente a su lugar guardado.*
3.  **Salir**: `Esc`.

### 🪟 Modo Layout (`Hyper + /`)
*Cambia cómo se organizan las ventanas.*
*   **`a`**: **Acordeón** (Hace las ventanas colapsables, ideal para muchas columnas).
*   **`t`**: **Tiles** (El mosaico clásico, por defecto).
*   **`v` / `h`**: Fuerza orientación Vertical / Horizontal.
*   **`Esc`**: Salir.

### 📐 Modo Resize (`Hyper + R`)
*Ajusta tamaños.*
*   `h` / `l`: Ancho.
*   `j` / `k`: Alto.
*   `Esc`: Salir.

### 🛠 Modo Servicio (`Hyper + ;`)
*Cosas del sistema.*
*   `r`: **Aplanar** (Resetea layouts extraños si se rompe algo).
*   `Backspace`: Cerrar todo menos la ventana actual (Zen).
*   `Esc`: Recargar Configuración (Reload).

---

## 3. Mapa de Espacios de Trabajo

Se fuerza un orden lógico por monitores (Main = Izquierda, Secondary = Derecha).

| WS | Monitor | Uso Sugerido |
| :--- | :--- | :--- |
| **1** | Main | **Terminal / Dev** (Ghostty, VSCode) |
| **2** | Main | **Web** (Navegadores) |
| **5** | Main | **Media** (Spotify, VLC) |
| **7** | Main | Extras / Temporales |
| **3** | Sec | **Productividad** (Obsidian, Notas) |
| **4** | Sec | **Lectura** (PDFs, Docs) |
| **6** | Sec | **Comunicaciones** (Telegram, Discord) |
| **8** | Sec | Sistema / Archivos |

---

## 4. Solución de Problemas

**¿Las ventanas no se guardan al reiniciar?**
El script de persistencia usa el **Título de la Ventana**. Si Chrome cambia el título de "Youtube" a "Google", puede que no la reconozca perfectamente. Simplemente muévela a su sitio y vuelve a guardar (`Hyper + P` -> `s`).

