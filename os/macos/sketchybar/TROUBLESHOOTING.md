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
> Ver: [AeroSpace SCRIPTS.md](../aerospace/SCRIPTS.md), donde se documenta la regla de usar rutas absolutas en scripts y comandos ejecutados por servicios.

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
   - Crea los items de workspace directamente en el proceso actual.
   - Actualiza sus iconos.
   - Elimina el watcher `aerospace_retry`.
4. **Máximo 10 intentos** (30 segundos). Si AeroSpace nunca responde, elimina el watcher y deja de intentar.
5. Si AeroSpace **ya estaba listo** al arrancar (`INIT_DONE = true`), el timer nunca se crea — cero overhead.

```lua
-- Fragmento clave en aerospace.lua:
local INIT_DONE = (#aerospace_workspaces > 0)

-- En init():
if INIT_DONE then
  self:create_workspace_items()
  self:update_space_labels()
else
  -- Crear retry timer (3s × 10 intentos máximo)
  -- Al detectar AeroSpace → crear items y eliminar el timer
end
```

**Comportamiento visible**: La barra aparece primero sin los workspaces (o con indicadores vacíos), y ~3-9 segundos después se completa automáticamente.

**Por qué no usa reload**: en este caso, `sketchybar --reload` desde el callback
volvia a ejecutar la configuracion repetidamente. Cada ciclo intentaba crear otra
vez todos los items, generaba mensajes `Item already exists` y hacia crecer
`sketchybar.out.log` continuamente. La inicializacion diferida evita recargar la
configuracion completa.

**Fallback**: Si AeroSpace no responde durante los 10 intentos, los workspaces no se crean en ese arranque. El resto de la barra sigue disponible y un reinicio controlado del servicio permite reintentar.

---

## Problema: El log de Sketchybar crece hasta llenar el disco

**Síntoma**: El sistema empieza a quedarse sin espacio sin una causa evidente. Sketchybar sigue funcionando, pero el archivo de log crece de forma silenciosa durante horas o días.

**Caso real detectado**: `sketchybar.out.log` llegó a ocupar **22 GB**.

**Archivos involucrados**:
```bash
/usr/local/var/log/sketchybar/sketchybar.out.log
/usr/local/var/log/sketchybar/sketchybar.err.log
```

El `LaunchAgent` de Homebrew para Sketchybar redirige stdout y stderr a esos archivos:

```bash
~/Library/LaunchAgents/homebrew.mxcl.sketchybar.plist
```

### Verificación rápida

```bash
du -sh /usr/local/var/log/sketchybar/*.log
ls -lh /usr/local/var/log/sketchybar/*.log
tail -n 80 /usr/local/var/log/sketchybar/sketchybar.out.log
df -h /usr/local/var/log/sketchybar
```

Si el log contiene muchas líneas como esta:

```text
[i] sketchybar: [?] Regex: No match found for regex '/brew.package\..*/'
```

el ruido viene del módulo de Brew intentando borrar ítems `brew.package.*` aunque no existan.

También se detectó ruido desde el módulo de música cuando `media-control get` devolvía `null`, generando errores repetidos sobre `music.anchor` y artwork ausente.

### Causas observadas

1. El módulo `brew` ejecutaba `brew update && brew outdated` y dejaba que parte del output terminara en el log de Sketchybar.
2. `SBAR.remove("/brew.package\\..*/")` generaba una línea de log cada vez que no había ítems que coincidieran con ese regex.
3. El módulo `music` consultaba `media-control` cada segundo. Si no había reproducción activa o `media-control` respondía `null`, el módulo intentaba pintar valores inválidos y ensuciaba el log.

### Solución aplicada

1. Vaciar el log gigante sin borrar el archivo:

```bash
truncate -s 0 /usr/local/var/log/sketchybar/sketchybar.out.log
truncate -s 0 /usr/local/var/log/sketchybar/sketchybar.err.log
```

No usar `rm` para esto: mantener el archivo evita problemas con el `LaunchAgent` que ya tiene esa ruta abierta.

2. Desactivar módulos ruidosos o de bajo valor:

```lua
-- settings.lua
music = { enable = false },
```

3. En el módulo Brew, silenciar `brew update` / `brew outdated` y evitar llamar a `SBAR.remove(...)` si antes no se renderizaron paquetes:

```lua
local rendered_package_count = 0

local function render_popup(outdated)
  if rendered_package_count > 0 then
    SBAR.remove("/brew.package\\..*/")
    rendered_package_count = 0
  end
  ...
end

SBAR.exec("/bin/zsh -lc '/usr/local/bin/brew update >/dev/null 2>&1 && /usr/local/bin/brew outdated 2>/dev/null'", function(outdated)
  ...
end)
```

4. Recargar solo Sketchybar para probar:

```bash
sketchybar --reload
```

**No tocar AeroSpace para este problema.** No agregar hooks de reload en `aerospace.toml`.

### Confirmación

Después de vaciar logs, recargar Sketchybar y esperar unos segundos:

```bash
du -sh /usr/local/var/log/sketchybar/*.log
tail -n 40 /usr/local/var/log/sketchybar/sketchybar.out.log
```

El resultado esperado es que los logs queden en `0B` o unos pocos KB y no vuelvan a crecer con el mismo patrón repetitivo.

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
