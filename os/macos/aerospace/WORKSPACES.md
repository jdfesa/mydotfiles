# AeroSpace Workspaces

## Trial Status

Esta distribución de cinco workspaces numéricos está **en prueba** y puede
cambiar según el uso diario. Sustituye los identificadores por letras, pero
conserva las reglas automáticas por aplicación y la separación entre navegar
con `Hyper` y mover ventanas con `Meh`.

La fuente en esta revisión no acredita integración en `main` ni recarga de
AeroSpace o Sketchybar. La aceptación requiere verificar el teclado, el ruteo y
la barra en una sesión real; véase [Repository Tasks](../../../TODO.md#desktop-trial).

## Workspace Map

| Workspace | Uso | Apps principales |
|---|---|---|
| `1` | Navegadores y referencias web | Chrome, Safari, Firefox Developer Edition, qutebrowser, Brave, Zen |
| `2` | Trabajo y terminales | Codex, VS Code, Ghostty, Kitty, Terminal, Kiro, Antigravity |
| `3` | Notas y documentos | Obsidian, Notes, Typora, TeXShop, PDFelement |
| `4` | Finder y utilidades | Finder, Activity Monitor, Windows App, Vial, CrossOver |
| `5` | Calendario, comunicación y multimedia | Calendar, Telegram, Discord, YouTube Music, VLC |

Los identificadores son strings (`"1"`–`"5"`) de AeroSpace, no IDs de Spaces
nativos de macOS. Son los cinco workspaces **persistentes**, no un límite
absoluto: un comando explícito o ventanas anteriores pueden mantener otros.

## Keyboard Access

- `Hyper + 1/2/3/4/5`: ir al workspace correspondiente.
- `Meh + 1/2/3/4/5`: enviar la ventana enfocada al workspace correspondiente.
- `Hyper + Tab`: volver al workspace anterior.
- Los atajos por letras de foco/movimiento (`H/J/K/L`), layouts y modos no cambian.
- Se retiran los antiguos accesos de workspace por `U/I/O/P/Y/N`.

En el Silakka54 se utilizan los números que emite la capa correspondiente;
este cambio no modifica el firmware ni el mapa del teclado. Hay que comprobar
las combinaciones reales con Hyper y Meh, no solo el parseo del TOML.

## Automatic Routing

Las reglas viven en [aerospace.toml](aerospace.toml) bajo
`[[on-window-detected]]`. Se conservan todos los bundle IDs existentes; solo
cambia el destino. Estas reglas no constituyen un renombrado de workspaces ni
una migración automática de todas las ventanas ya abiertas.

### 1: Browsers

| App ID | App |
|---|---|
| `com.google.Chrome` | Google Chrome |
| `com.apple.Safari` | Safari |
| `org.mozilla.firefoxdeveloperedition` | Firefox Developer Edition |
| `org.qutebrowser.qutebrowser` | qutebrowser |
| `com.brave.Browser` | Brave |
| `app.zen-browser.zen` | Zen Browser |

### 2: Work and Terminals

| App ID | App |
|---|---|
| `com.openai.codex` | Codex |
| `com.microsoft.VSCode` | Visual Studio Code |
| `com.mitchellh.ghostty` | Ghostty |
| `net.kovidgoyal.kitty` | kitty |
| `com.apple.Terminal` | Terminal |
| `dev.kiro.desktop` | Kiro |
| `com.google.antigravity` | Antigravity |
| `com.google.antigravity-ide` | Antigravity IDE |

### 3: Notes and Documents

| App ID | App |
|---|---|
| `md.obsidian` | Obsidian |
| `abnerworks.Typora` | Typora |
| `com.apple.Notes` | Notes |
| `TeXShop` | TeXShop |
| `com.wondershare.PDFelement` | PDFelement |

### 4: Finder and Utilities

| App ID | App |
|---|---|
| `com.apple.finder` | Finder |
| `com.apple.ActivityMonitor` | Activity Monitor |
| `com.microsoft.rdc.macos` | Windows App |
| `today.vial` | Vial |
| `com.codeweavers.CrossOver` | CrossOver |

### 5: Calendar, Communication and Media

| App ID | App |
|---|---|
| `com.tdesktop.Telegram` | Telegram |
| `com.hnc.Discord` | Discord |
| `com.apple.iCal` | Calendar |
| `com.github.th-ch.youtube-music` | YouTube Music |
| `org.videolan.vlc` | VLC |

## Migration and Verification

La correspondencia de los destinos anteriores es:

| Identificador anterior | Nuevo destino |
|---|---|
| `I` | `1` |
| `U` | `2` |
| `O` | `3` |
| `N` | `4` |
| `P` y `Y` | `5` |

Antes de aplicar, ejecutar las pruebas aisladas y validar sin recargar:

```bash
python3 os/macos/aerospace/scripts/test-workspaces.py
lua os/macos/sketchybar/tests/test-aerospace.lua
aerospace reload-config --dry-run --no-gui
```

Las pruebas requieren Python 3.11 o superior, Bash y Lua 5.4; no llaman a las
aplicaciones reales ni alteran ventanas. El dry-run verifica la configuración,
no la comodidad del teclado ni el resultado visual.

La aplicación de la prueba se hace por separado, una vez acordada:

1. Recargar AeroSpace según [Reload and Validate](README.md#reload-and-validate).
2. Consultar `aerospace list-workspaces --all` y `aerospace list-windows --all`.
   Las letras con ventanas abiertas pueden seguir existiendo tras la recarga.
3. Tras acordar el traslado, mover cada ventana por su ID al número de la tabla:
   `aerospace move-node-to-workspace --window-id <id> <numero>`.
   No cerrar aplicaciones para vaciar los workspaces anteriores.
4. Cambiar el foco a un workspace numérico y verificar que los anteriores ya
   no tienen ventanas ni siguen apareciendo como workspaces activos.
5. Hacer que Sketchybar relea sus ítems una vez estabilizada la lista, siguiendo
   el [procedimiento controlado de la barra](../sketchybar/TROUBLESHOOTING.md#rescate-solo-aparece-la-app-actual-y-faltan-los-workspaces).
   El módulo Lua toma la lista al inicializar: cambiar el TOML no la reconstruye.
6. Comprobar `Hyper + 1` a `Hyper + 5`, `Meh + 1` a `Meh + 5`, nuevas ventanas
   de cada grupo y los ítems `space.1` a `space.5` en Sketchybar.

El hook de highlight consulta los workspaces del proceso. Puede seguir
resaltando las letras mientras AeroSpace conserve la configuración anterior,
sin imponer la lista numérica antes de la recarga.

## Adding an Application

1. Buscar el bundle ID:

```bash
aerospace list-apps --format '%{app-bundle-id} | %{app-name}'
```

2. Elegir uno de los destinos `1`–`5` según el mapa en prueba.
3. Agregar la regla en [aerospace.toml](aerospace.toml).
4. Actualizar esta guía y la expectativa de ruteo en
   [test-workspaces.py](scripts/test-workspaces.py).
5. Repetir las pruebas aisladas y el dry-run antes de aplicar.
