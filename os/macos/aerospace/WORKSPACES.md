# AeroSpace Workspaces

Esta configuracion usa workspaces con letras, no numeros. La idea es que cada letra tenga una historia facil de recordar y que todas las teclas importantes vivan en la mano derecha del Silakka54.

## Mapa General

| Workspace | Palabra ancla | Proposito | Apps principales |
|---|---|---|---|
| `U` | Universe | Hub principal: codigo, terminal, trabajo activo | Codex, Ghostty, kitty, Terminal, VS Code, Kiro, Antigravity IDE |
| `I` | Internet | Web, referencias, busquedas | Chrome, Safari |
| `O` | Organize | Notas, escritura, documentos | Obsidian, Notes, Typora, TeXShop, PDFelement |
| `P` | People / Planning | Comunicacion y planificacion | Telegram, Discord, Calendar |
| `Y` | Yield | Musica, video, descanso activo | YouTube Music, VLC |
| `N` | Navigate | Archivos, sistema, utilidades, entornos auxiliares | Finder, Activity Monitor, Windows App, Vial, CrossOver |

`Yield` queda reservado para consumo activo de audio/video. No se agregan apps genericas solo porque podrian existir; el ruteo refleja uso real.

## Mano Derecha en el Silakka54

```text
Y  U  I  O  P       <- fila superior: reach up
H  J  K  L  ;       <- home row
N  M  ,  .  /       <- fila inferior: reach down
```

Significados:

- **home row**: fila donde descansan naturalmente los dedos.
- **reach up**: subir un dedo desde home row para alcanzar una tecla.
- **reach down**: bajar un dedo desde home row para alcanzar una tecla.

En criollo: `reach down` significa bajar el dedo para llegar a la fila inferior, por ejemplo de `H` a `N` o de `J` a `M`.

## Prioridad Ergonomica

El workspace mas usado va en la letra mas comoda.

| Dedo | Letra | Comodidad |
|---|---|---|
| Indice arriba | `U` | Mas natural |
| Medio arriba | `I` | Muy comoda |
| Anular arriba | `O` | Muy comoda |
| Menique arriba | `P` | Algo mas exigente |
| Indice arriba extendido | `Y` | Alcance extendido |
| Indice abajo | `N` | Alcance hacia abajo |

Por eso `U` es el workspace principal y `Y` / `N` quedan para usos menos constantes.

## Ruteo Automatico

Las reglas viven en [aerospace.toml](aerospace.toml) bajo `[[on-window-detected]]`.

### U: Universe

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

### I: Internet

| App ID | App |
|---|---|
| `com.google.Chrome` | Google Chrome |
| `com.apple.Safari` | Safari |
| `org.mozilla.firefoxdeveloperedition` | Firefox Developer Edition |
| `org.qutebrowser.qutebrowser` | qutebrowser |
| `com.brave.Browser` | Brave |
| `app.zen-browser.zen` | Zen Browser |

### O: Organize

| App ID | App |
|---|---|
| `md.obsidian` | Obsidian |
| `abnerworks.Typora` | Typora |
| `com.apple.Notes` | Notes |
| `TeXShop` | TeXShop |
| `com.wondershare.PDFelement` | PDFelement |

### P: People / Planning

| App ID | App |
|---|---|
| `com.tdesktop.Telegram` | Telegram |
| `com.hnc.Discord` | Discord |
| `com.apple.iCal` | Calendar |

### Y: Yield

| App ID | App |
|---|---|
| `com.github.th-ch.youtube-music` | YouTube Music |
| `org.videolan.vlc` | VLC |

### N: Navigate

| App ID | App |
|---|---|
| `com.apple.finder` | Finder |
| `com.apple.ActivityMonitor` | Activity Monitor |
| `com.microsoft.rdc.macos` | Windows App |
| `today.vial` | Vial |
| `com.codeweavers.CrossOver` | CrossOver |

## Como Agregar una App

1. Buscar el bundle id:

```bash
aerospace list-apps --format '%{app-bundle-id} | %{app-name}'
```

2. Elegir workspace por intencion, no por impulso.
3. Agregar una regla `[[on-window-detected]]` en [aerospace.toml](aerospace.toml).
4. Actualizar este documento en el mismo cambio.
5. Validar con:

```bash
aerospace reload-config --dry-run --no-gui
```
