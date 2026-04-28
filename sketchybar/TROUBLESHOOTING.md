# Sketchybar — Troubleshooting

Registro de problemas encontrados en producción y sus soluciones confirmadas.
Para problemas genéricos de instalación, ver el [README](README.md#-troubleshooting-solución-de-problemas).

---

## Problema: Los workspaces de AeroSpace no aparecen después de reiniciar

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

### Implementación actual

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

## Manejo de Workspaces vacíos al arrancar (Race Condition)

**Síntoma**: La barra carga pero los workspaces (U, I, O, P, Y, N) aparecen vacíos o sin iconos de apps. Después de unos segundos, aparecen correctamente sin intervención manual.

**Causa**: Sketchybar arranca (vía LaunchAgent `RunAtLoad` o brew) **antes** que AeroSpace. Cuando `aerospace.lua` se ejecuta, `aerospace list-workspaces --all` devuelve una lista vacía porque el binario aún no está disponible o no terminó de inicializar.

### Estado actual de la configuración

Actualmente se utiliza un **retry timer interno** en `aerospace.lua` que:

1. Al cargar, intenta obtener los workspaces con `get_workspaces()`.
2. Si la lista está vacía (`INIT_DONE = false`), crea un item invisible `aerospace_retry` que se ejecuta cada **3 segundos**.
3. En cada tick, consulta a AeroSpace. Si responde (lista de workspaces no vacía):
   - Detiene el timer (`update_freq = 0`)
   - Espera **1 segundo** y ejecuta `sketchybar --reload` (el mismo reload que antes se hacía a mano)
4. **Máximo 10 intentos** (30 segundos). Si AeroSpace nunca responde, deja de intentar.
5. Si AeroSpace **ya estaba listo** al arrancar (`INIT_DONE = true`), el timer nunca se crea — cero overhead.

```lua
-- Fragmento clave en aerospace.lua:
local INIT_DONE = (#aerospace_workspaces > 0)

-- En init():
if INIT_DONE then
  self:update_space_labels()   -- flujo normal
else
  -- Crear retry timer (3s × 10 intentos máximo)
  -- Al detectar AeroSpace → sleep 1 && sketchybar --reload
end
```

**Comportamiento visible**: La barra aparece primero sin los workspaces (o con indicadores vacíos), y ~3-9 segundos después se completa automáticamente.

**Riesgo**: Nulo. Si falla, el peor caso es que los workspaces no aparecen (igual que antes). El timer se autodestruye tras 10 intentos. No toca `aerospace.toml` ni ningún componente del sistema.

---

## ⛔ PELIGRO: Lo que NUNCA hay que hacer

> [!CAUTION]
> Las siguientes acciones pueden **congelar macOS** y dejar la máquina inutilizable, requiriendo un reinicio forzado (manteniendo el botón de encendido).

### ❌ NUNCA usar `after-startup-command` con `sketchybar --reload` en `aerospace.toml`

```toml
# ❌ PELIGRO — CAUSA CONGELAMIENTO DE PANTALLA
after-startup-command = ['exec-and-forget /usr/local/bin/sketchybar --reload']
```

**Qué pasa**: `aerospace reload-config` re-dispara `after-startup-command` (bug conocido de AeroSpace). Esto genera un **loop de reload exponencial**:

```
aerospace reload-config
  → re-ejecuta after-startup-command
    → sketchybar --reload
      → aerospace.lua consulta AeroSpace
        → exec-on-workspace-change dispara scripts
          → los scripts llaman a sketchybar
            → posible re-trigger → LOOP
```

Cada iteración spawna procesos nuevos vía `exec-and-forget` (sin control). Los procesos se acumulan exponencialmente → CPU al 100% → **macOS se congela**.

**Por qué es crítico**: AeroSpace es un **window manager** — controla el input de teclado y mouse de toda la máquina. Si entra en un loop de reload:
- No puede procesar eventos de input (teclado, mouse)
- macOS WindowServer se satura con reposicionamientos
- **La pantalla se congela**, sin poder hacer nada salvo reiniciar forzado

### ❌ NUNCA ejecutar `aerospace reload-config` justo después de agregar hooks de startup

Si necesitás agregar un hook como `after-startup-command` o `after-login-command`, **no recargues la config en caliente**. Hacé un reinicio manual controlado donde puedas forzar quit si algo falla.

### Regla general: archivos de riesgo crítico

| Archivo | Riesgo | Por qué |
|---------|--------|---------|
| `aerospace.toml` | 🔴 **CRÍTICO** | Controla el window manager. Un error congela la pantalla. |
| LaunchAgents (`~/Library/LaunchAgents/`) | 🔴 **CRÍTICO** | Se ejecutan al login. Un loop puede impedir el arranque. |
| `sketchybarrc` / `init.lua` | 🟡 **ALTO** | Corre como daemon. Un crash reinicia en loop (por `KeepAlive`). |

### Cómo recuperarse si la pantalla se congela

1. **Opción 1**: Mantener el botón de encendido ~10 segundos para forzar apagado.
2. **Opción 2**: Si SSH está habilitado, conectarse desde otro dispositivo y matar los procesos: `killall AeroSpace && killall sketchybar`.
3. **Opción 3**: Si podés abrir Terminal (Cmd+Opt+Esc → Force Quit), revertir el cambio: `git checkout -- aerospace/aerospace.toml` en el repo de dotfiles.

---
