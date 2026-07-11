# 📜 Scripts de AeroSpace

Para mantener la configuración de `aerospace.toml` limpia y solucionar limitaciones técnicas, utilizamos scripts externos (bash) que actúan como "puentes" entre AeroSpace y otras herramientas.

Esta es la documentación de los scripts que se encuentran en `aerospace/scripts/`.

---

## Regla General: PATH y Rutas Absolutas

Los comandos ejecutados por AeroSpace, Sketchybar o servicios de macOS no siempre heredan el `PATH` del shell interactivo. Por eso, cualquier script que llame a binarios de Homebrew debe preferir rutas absolutas.

| Binario | Ruta usada |
|---|---|
| `aerospace` | `/usr/local/bin/aerospace` |
| `sketchybar` | `/usr/local/bin/sketchybar` |
| `borders` | `/usr/local/bin/borders` |

Regla practica: si el comando corre desde un hook, daemon, Lua de Sketchybar o `exec-and-forget`, no depender de `which` ni del `PATH` del usuario.

---

## 1. `update_sketchybar_workspace.sh`

**Propósito**: Actualiza el color de resalte (highlight) del workspace activo en Sketchybar cada vez que el usuario cambia de workspace.

### Contexto y Decisión Técnica
Inicialmente, Sketchybar dependía de un evento Lua (`subscribe("aerospace_workspace_change", ...)`) para detectar el cambio de workspace y actualizar el color del ítem. Sin embargo, se detectó que **los eventos Lua personalizados en Sketchybar a veces no reaccionan o se pierden** (un bug silencioso de Sketchybar con los custom events).

**La Solución**:
Se eliminó la dependencia del evento Lua para el highlight. En su lugar, el script bash se ejecuta directamente por AeroSpace y utiliza el CLI de Sketchybar (`sketchybar --set ...`) para forzar el cambio de color de manera directa y 100% confiable.

### Funcionamiento
1. AeroSpace detecta el cambio de workspace (ej. pasamos a la `I`).
2. Dispara el hook `exec-on-workspace-change`.
3. El hook llama a este script pasándole la variable de entorno `$AEROSPACE_FOCUSED_WORKSPACE`.
4. El script itera sobre todos los workspaces conocidos (U, I, O, P, Y, N) y usa `sketchybar --set` para encender el highlight del activo y apagar el de los demás.

> **Nota sobre íconos**: El script solo actualiza el **highlight**. La actualización de los íconos de las aplicaciones dentro del workspace sigue estando a cargo de un watcher periódico (routine) en el código Lua de Sketchybar.

---

## 2. `update_mode_indicator.sh`

**Propósito**: Actualiza el indicador de modo activo de AeroSpace en Sketchybar.

### Contexto y Decisión Técnica

Antes el TOML llamaba directamente a `sketchybar --set aerospace_mode drawing=on/off`. Eso funcionaba para un solo modo, pero al agregar `resize` empezaba a duplicar comandos y dejaba el icono fijo en `[S]`.

**La Solución**:
Centralizar el comportamiento en un script pequeño. AeroSpace solo indica el modo (`SERVICE`, `RESIZE` o `NORMAL`) y el script decide icono, color y visibilidad.

### Modos soportados

| Modo | Indicador | Color | Acción |
|---|---|---|---|
| `SERVICE` | `[S]` | Rosa | Muestra el indicador de mantenimiento |
| `RESIZE` | `[R]` | Rojo | Muestra el indicador de ajuste de tamaños |
| `NORMAL` | — | — | Oculta el indicador |

### Funcionamiento

1. Un binding de AeroSpace entra a un modo custom.
2. El binding llama a `scripts/update_mode_indicator.sh` con el nombre del modo.
3. El script usa `/usr/local/bin/sketchybar` directamente para evitar depender del PATH.
4. Al volver a `main`, AeroSpace llama al script con `NORMAL` y el indicador se oculta.

---

## 3. `borders_mode.sh`

**Propósito**: Cambia el color del borde activo segun el modo de teclado de AeroSpace.

### Contexto y Decisión Técnica

`accordion` y `tiles` son layouts, no modos. Por eso este script solo representa estados temporales del teclado: `NORMAL`, `RESIZE` y `SERVICE`. El layout actual queda fuera para que el color siempre responda a una pregunta simple: "en que modo estoy?".

### Modos soportados

| Modo | Color | Uso |
|---|---|---|
| `NORMAL` | Azul | Modo diario |
| `RESIZE` | Rojo | Ajuste de tamanos |
| `SERVICE` | Rosa | Mantenimiento rapido |

### Funcionamiento

1. Al entrar a `resize` o `service`, el binding de AeroSpace llama a `scripts/borders_mode.sh` con el modo correspondiente.
2. Al volver a `main`, AeroSpace llama al script con `NORMAL`.
3. El script usa `/usr/local/bin/borders` directamente para evitar depender del PATH.
