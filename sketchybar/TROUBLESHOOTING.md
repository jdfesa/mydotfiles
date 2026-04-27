# Sketchybar — Troubleshooting

Registro de problemas encontrados en producción y sus soluciones confirmadas.
Para problemas genéricos de instalación, ver el [README](README.md#-troubleshooting-solución-de-problemas).

---

## [BUG] Los workspaces de AeroSpace no aparecen después de reiniciar

**Síntoma**: La barra carga, pero los ítems `space.U`, `space.I`, etc. no se crean. En su lugar aparecen ítems genéricos (`item_0`, `item_1`...) sin letra ni iconos de apps. Funciona si se recarga manualmente con `sketchybar --reload` o `brew services restart sketchybar` *después* de que el sistema ya cargó.

**Verificación rápida**:
```bash
sketchybar --query space.U
# Si devuelve: [!] Query: Invalid query, or item 'space.U' not found
# → Confirmado: el bug está activo.
```

### Causa raíz

Sketchybar arranca al inicio de sesión (vía Login Items o `launchd`) **antes de que el entorno del shell del usuario esté disponible**. El proceso de Sketchybar corre con un `PATH` mínimo del sistema (`/usr/bin:/bin:/usr/sbin:/sbin`) que **no incluye** `/usr/local/bin`, donde Homebrew instala `aerospace`.

El módulo Lua [`items/spaces/window_managers/aerospace.lua`](items/spaces/window_managers/aerospace.lua) ejecutaba `io.popen("aerospace list-workspaces --all")` con el nombre relativo `aerospace`. Al no encontrarlo, `io.popen` devuelve una cadena vacía sin error visible. El resultado: la tabla de workspaces queda vacía, el bucle `for i, workspace in ipairs(...)` no itera, y los ítems `space.*` nunca se crean.

> Este es el mismo principio documentado en AeroSpace para `exec-and-forget`, pero en dirección opuesta (Sketchybar → AeroSpace).
> Ver: [`aerospace/README.md` — Nota Técnica: PATH en exec-and-forget](../aerospace/README.md#️-nota-técnica-importante-path-en-exec-and-forget)

### Solución aplicada

Definir una constante con la ruta absoluta al binario y usarla en todas las llamadas:

```lua
-- items/spaces/window_managers/aerospace.lua

-- Ruta absoluta necesaria: al iniciar sesión, Sketchybar corre sin el PATH
-- del shell, por lo que 'aerospace' sin ruta completa no se encuentra.
local AEROSPACE = "/usr/local/bin/aerospace"

local function get_workspaces()
  local file = io.popen(AEROSPACE .. " list-workspaces --all")
  ...
end
```

Afecta tres llamadas en el mismo archivo: `get_workspaces()`, `get_current_workspace()`, y `update_space_labels()`.

**Confirmar ruta del binario** si cambia en el futuro:
```bash
which aerospace
# /usr/local/bin/aerospace  ← actualizar la constante si difiere
```

### Regla general

Cualquier `io.popen(...)` o `SBAR.exec(...)` dentro de la config Lua de Sketchybar que llame a un binario instalado por Homebrew **debe usar ruta absoluta**. El PATH del proceso no es el del shell.

| Binario | Ruta absoluta |
|---|---|
| `aerospace` | `/usr/local/bin/aerospace` |
| `sketchybar` | `/usr/local/bin/sketchybar` |
| Otros (`jq`, etc.) | verificar con `which <binario>` |

---
