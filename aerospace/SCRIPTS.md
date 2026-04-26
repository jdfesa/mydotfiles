# 📜 Scripts de AeroSpace

Para mantener la configuración de `aerospace.toml` limpia y solucionar limitaciones técnicas, utilizamos scripts externos (bash) que actúan como "puentes" entre AeroSpace y otras herramientas.

Esta es la documentación de los scripts que se encuentran en `aerospace/scripts/`.

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
