# 🪟 AeroSpace — Tiling Window Manager

> **Fase actual: 1 — Navegación Básica**
>
> Esta configuración está diseñada para adopción incremental. Empezamos con lo mínimo funcional y vamos sumando features cuando domines las anteriores.

---

## 🧠 ¿Qué es AeroSpace y cómo piensa?

AeroSpace es un **tiling window manager** para macOS inspirado en [i3](https://i3wm.org/). En lugar de ventanas flotando unas encima de otras (como macOS por defecto), las ventanas se organizan automáticamente en un mosaico que ocupa toda la pantalla.

### Concepto Clave: Workspaces ≠ Spaces de macOS

| Concepto | macOS Spaces | AeroSpace Workspaces |
|---|---|---|
| **Qué son** | Escritorios virtuales nativos de macOS (Mission Control) | Espacios virtuales **emulados** por AeroSpace |
| **Cómo cambiás** | `Ctrl + ←/→` o gestos del trackpad (con animación lenta) | Un atajo de teclado, **instantáneo**, sin animación |
| **Límite** | Hasta 16 por monitor | Ilimitados (se pueden nombrar con letras y números) |
| **Control por teclado** | Solo cambiar entre ellos | Crear, mover ventanas, asignar a monitores, todo por teclado |
| **API pública** | No (Apple no ofrece API para gestionarlos) | Sí (AeroSpace tiene CLI completo) |

**¿Cómo funciona la magia?** AeroSpace mueve las ventanas "ocultas" a una esquina invisible de la pantalla (abajo a la derecha). Cuando cambiás de workspace, las trae de vuelta. Todo pasa dentro de **un solo Space de macOS**.

> **Recomendación**: Tené **un solo Space de macOS** y usá exclusivamente los workspaces de AeroSpace. Los Spaces de macOS solo agregan complejidad y bugs.

### El Árbol de Ventanas (Tree)

AeroSpace organiza las ventanas en una estructura de **árbol**:

```
Workspace 1 (raíz)
├── Ghostty (ventana)
└── Contenedor horizontal
    ├── Chrome (ventana)
    └── VS Code (ventana)
```

- **Cada workspace tiene su propia raíz**.
- **Las ventanas son hojas** (no tienen hijos).
- **Los contenedores** agrupan ventanas y tienen dos propiedades:
  - **Layout**: `tiles` (mosaico, todas visibles) o `accordion` (apiladas, solo una visible).
  - **Orientación**: `horizontal` (lado a lado) o `vertical` (una arriba de otra).

### Layouts: Tiles vs Accordion

- **Tiles (Mosaico)**: Todas las ventanas comparten el espacio visible. Es el modo por defecto. Si tenés 3 ventanas, se dividen en tercios.
- **Accordion**: Las ventanas se apilan "una detrás de otra". Solo ves una a la vez, con padding a los costados indicando que hay más ventanas. Navegás con `focus left/right`.

### Normalización

AeroSpace simplifica automáticamente el árbol:

1. **Flatten**: Si un contenedor tiene un solo hijo, se elimina el contenedor (es innecesario).
2. **Opposite orientation**: Contenedores anidados deben tener orientaciones opuestas (horizontal → vertical → horizontal).

Esto hace que la estructura del árbol sea predecible mirando cómo están las ventanas en pantalla.

### Floating (Flotante)

Algunas ventanas pueden "flotar" sobre el mosaico (como en macOS normal). AeroSpace detecta automáticamente diálogos y los flota. También podés alternar manualmente entre floating y tiling.

---

## ⌨️ Atajos Activos (Fase 1)

**Dos modificadores, una lógica:**
- `Alt` (meñique izquierdo en Silakka54) = **Navegación** — ir, mirar
- `Meh` (hold en home row derecha del Silakka54) = **Acción** — mover, enviar

> **Meh** = `Ctrl+Alt+Shift` combinados. En el Silakka54 se activa manteniendo **una sola tecla**. En `aerospace.toml` se escribe como `alt-ctrl-shift`.

> **Regla de diseño**: La fila numérica NO se usa. Todos los atajos están en las filas de letras, accesibles sin levantar las manos del home row.

### Workspaces por Letra (mano derecha)

Los workspaces usan letras mnemotécnicas. Alt (izquierda) + letra (derecha) = dos teclas, cross-hand, sin capas.

```
Mano derecha en el Silakka54:
  Y  U  I  O  P       ← fila accesible
  H  J  K  L  ;       ← home row (reservada para navegación)
  N  M  ,  .  /       ← fila inferior
```

| Atajo | Workspace | Uso |
|---|---|---|
| `Alt + U` | **U** | **U**no — Principal (IDE, editor, dev) |
| `Alt + I` | **I** | **I**nternet — Browsers (Chrome) |
| `Alt + O` | **O** | **O**bsidian — Notas, estudio |
| `Alt + P` | **P** | **P**ersonal — Chat (Telegram, Discord) |
| `Alt + Y` | **Y** | M**ú**sica/**Y**outube — Media (Spotify) |
| `Alt + N` | **N** | **N**avegador — Archivos (Finder, sistema) |
| `Alt + Tab` | — | Volver al workspace anterior (back & forth) |

### Mover Ventana a Workspace (Meh + letra)

| Atajo | Acción |
|---|---|
| `Meh + U/I/O/P/Y/N` | Enviar ventana al workspace correspondiente |

### Navegar entre Ventanas (Alt + H/J/K/L)

| Atajo | Acción |
|---|---|
| `Alt + H` | Foco a la ventana de la **izquierda** |
| `Alt + J` | Foco a la ventana de **abajo** |
| `Alt + K` | Foco a la ventana de **arriba** |
| `Alt + L` | Foco a la ventana de la **derecha** |

### Mover Ventana de Posición (Meh + H/J/K/L)

| Atajo | Acción |
|---|---|
| `Meh + H` | Mover ventana a la **izquierda** |
| `Meh + J` | Mover ventana **abajo** |
| `Meh + K` | Mover ventana **arriba** |
| `Meh + L` | Mover ventana a la **derecha** |

### Fullscreen

| Atajo | Acción |
|---|---|
| `Alt + F` | **Toggle fullscreen** — La ventana ocupa todo el workspace. Las demás siguen ahí pero ocultas. Presionar de nuevo para volver al mosaico. |

### Modo Servicio (mantenimiento)

| Atajo | Acción |
|---|---|
| `Meh + ;` | **Entrar** al modo servicio |
| `Esc` (en modo servicio) | **Recargar configuración** y volver |
| `Enter` (en modo servicio) | Volver sin recargar |
| `R` (en modo servicio) | Resetear layout (aplanar árbol) |
| `F` (en modo servicio) | Toggle floating ↔ tiling |

---

## 🔄 Cómo Recargar la Configuración

Después de editar `aerospace.toml`, necesitás recargar para que los cambios surtan efecto.

### Opción 1: Atajo de teclado (recomendado)
```
Meh + ;   →   Esc
```
Esto entra al modo servicio y la tecla `Esc` recarga la configuración automáticamente.

### Opción 2: Desde la terminal
```bash
aerospace reload-config
```

### Opción 3: Desde el icono de la barra
Click en el icono de AeroSpace en la barra de menú → "Reload Config".

> Si la configuración tiene errores de sintaxis, AeroSpace mostrará una notificación con el error. No se aplicarán los cambios hasta que corrijas el error.

---

## 🎨 Integración con Sketchybar

AeroSpace está integrado con Sketchybar para reemplazar los Spaces nativos de macOS en la barra superior. La integración tiene **dos partes**: los indicadores de workspaces y el indicador de modo activo.

### 1. Indicadores de Workspaces (letras U, I, O, P, Y, N)

- **Configuración Global**: En `sketchybar/settings.lua`, `WINDOW_MANAGER` está configurado en `"aerospace"`.
- **Módulo Personalizado**: El módulo `sketchybar/items/spaces/window_managers/aerospace.lua` crea los ítems de workspace usando `SBAR.add("item", ...)` en vez de `SBAR.add("space", ...)` (que solo funciona con Spaces nativos de macOS).
- **Comunicación**: `aerospace.toml` tiene un hook `exec-on-workspace-change` que ejecuta un script bash externo:
  ```bash
  $HOME/mydotfiles/aerospace/scripts/update_sketchybar_workspace.sh
  ```
  Este script usa el CLI directo de Sketchybar para actualizar el color (highlight) de manera 100% confiable, puenteando los eventos Lua que a veces fallan.
  > 📖 **Para más detalles técnicos**, consulta el documento [**SCRIPTS.md**](SCRIPTS.md).

### 2. Indicador de Modo Activo (`[S]` en rojo)

AeroSpace soporta **modos custom** (como i3). Cada modo cambia qué atajos de teclado están activos. Actualmente tenemos `main` (normal) y `service` (mantenimiento), pero se pueden agregar más (ej: `resize`).

El indicador de modo funciona así:
- Se crea un ítem `aerospace_mode` en el módulo Lua con `drawing = false` (oculto por defecto).
- **AeroSpace controla directamente el ítem vía CLI** — no usa eventos Lua (fallaban silenciosamente).
- Al entrar a un modo: `sketchybar --set aerospace_mode drawing=on`
- Al salir del modo: `sketchybar --set aerospace_mode drawing=off`
- Si se agregan más modos en el futuro, cada uno debe incluir el `exec-and-forget` correspondiente en su binding.

### ⚠️ Nota Técnica Importante: PATH en `exec-and-forget`

El comando `exec-and-forget` de AeroSpace **no hereda el PATH del shell del usuario**. Esto significa que binarios instalados por Homebrew (como `sketchybar`) no se encuentran con solo poner su nombre.

```toml
# ❌ NO funciona — no encuentra sketchybar
'exec-and-forget sketchybar --set aerospace_mode drawing=on'

# ✅ SÍ funciona — ruta absoluta
'exec-and-forget /usr/local/bin/sketchybar --set aerospace_mode drawing=on'
```

El hook `exec-on-workspace-change` **sí** usa `/bin/bash -c`, que carga el PATH, por eso ese sí funciona con solo `sketchybar`. En cambio, `exec-and-forget` ejecuta el comando directamente sin shell.

### Troubleshooting Sketchybar

Si Sketchybar no muestra los workspaces (letras U, I, O...) o el indicador de modo, probá:
```bash
# Reinicio completo (el --reload no siempre recarga los módulos Lua)
brew services restart sketchybar
```

---

## 🗺️ Roadmap de Funcionalidades (TODO)

Funcionalidades disponibles en AeroSpace para ir agregando progresivamente. Marcá con `[x]` las que vayas incorporando.

### Fase 2 — "Puedo ajustar" *(cuando domines la Fase 1)*

- [ ] **Resize mode**: Modo dedicado para redimensionar ventanas con `H/J/K/L`. Solo funciona si hay 2+ ventanas en el workspace (una se agranda, otra se achica).
- [ ] **Toggle layout**: Cambiar entre tiles y accordion con un atajo.
- [ ] **Join-with**: Forzar que dos ventanas se combinen en un contenedor con orientación específica. Útil para crear layouts complejos.
- [ ] **Resize smart**: Atajo rápido para agrandar/achicar sin entrar a un modo dedicado.

### Fase 3 — "Tengo superpoderes" *(cuando domines la Fase 2)*

- [ ] **App routing (`on-window-detected`)**: Automatizar que ciertas apps siempre abran en un workspace específico (ej: Ghostty → U, Chrome → I, Spotify → Y).
- [ ] **Modos con colores en borders**: Cambiar el color del borde según el modo activo (resize = rojo, layout = verde). Usa el script `borders_mode.sh` existente.
- [x] **Integración Sketchybar — Workspaces**: ✅ La barra muestra las letras de cada workspace y resalta el activo.
- [x] **Integración Sketchybar — Indicador de modo**: ✅ Aparece `[S]` en rojo cuando estás en modo servicio. Se oculta al volver a `main`. Usa CLI directo (`--set`) en vez de eventos Lua.
- [ ] **Move workspace to monitor**: Mover un workspace completo a otro monitor.
- [ ] **Workspace-to-monitor assignment**: Asignar workspaces fijos a monitores específicos.

### Fase 4 — "Personalización avanzada" *(opcional)*

- [ ] **`after-startup-command`**: Ejecutar comandos al iniciar AeroSpace (ej: lanzar Sketchybar).
- [ ] **`automatically-unhide-macos-hidden-apps`**: Prevenir que `Cmd+H` oculte apps accidentalmente.
- [ ] **Gaps personalizados**: Agregar separación visual entre ventanas para estética.
- [ ] **Accordion padding**: Configurar cuánto padding muestra el modo accordion.
- [ ] **Per-monitor gaps**: Gaps diferentes según el monitor.
- [ ] **Persistent workspaces con letras**: Usar workspaces con nombres mnemotécnicos (T=Terminal, W=Web, M=Music).

---

## 📁 Archivos en esta Carpeta

| Archivo | Descripción |
|---|---|
| `aerospace.toml` | Configuración activa de AeroSpace (Fase 1) |
| `README.md` | Este documento |
| `scripts/borders_mode.sh` | Script para cambiar color de bordes según modo. **No activo en Fase 1**, se reintegra en Fase 3 |

### Symlink

La carpeta `aerospace/` de este repo está enlazada a `~/.config/aerospace/`:
```bash
ls -la ~/.config/aerospace
# → /Users/jd/mydotfiles/aerospace
```

AeroSpace busca su configuración en `~/.config/aerospace/aerospace.toml`.

---

## 🆘 Troubleshooting

### "Solo veo 1 workspace"
- **Causa**: No tenías `persistent-workspaces` configurados. AeroSpace solo muestra workspaces que tienen ventanas.
- **Solución**: La Fase 1 ya incluye `persistent-workspaces = ["U", "I", "O", "P", "Y", "N"]`.

### "Las ventanas desaparecieron"
- AeroSpace las movió a la esquina inferior de la pantalla (así es como emula workspaces). Ejecutá `aerospace list-windows --all` en la terminal para ver dónde están.
- Si AeroSpace crashea, las ventanas quedan con 1px visible en la esquina. Arrastralas manualmente al centro.

### "Un atajo no funciona"
1. **Karabiner-Elements**: Si tenés Karabiner instalado y activo, es muy probable que esté interceptando las teclas (ej. al tratar de mapear F3) y bloqueando los atajos de AeroSpace. **Solución**: Desactivá Karabiner.
2. Verificá que no hay conflicto con otra app (Raycast, macOS). AeroSpace no puede capturar teclas que ya están ocupadas.
3. Recargá la config: `Meh + ;` → `Esc`.
4. Verificá la config: `aerospace reload-config` en la terminal. Si hay error, te lo muestra.

### "Las ventanas se ven raras / están anidadas"
- Entrá al modo servicio (`Meh + ;`) y presioná `R` para aplanar el árbol del workspace actual.

### "Quiero que una ventana flote (no tile)"
- Entrá al modo servicio (`Meh + ;`) y presioná `F` para alternar entre floating y tiling.

### "¿Cómo veo qué workspaces existen y qué ventanas tienen?"
```bash
# Ver todos los workspaces
aerospace list-workspaces --all

# Ver todas las ventanas y en qué workspace están
aerospace list-windows --all

# Ver los monitores detectados
aerospace list-monitors
```

---

## 📚 Referencias

- [Documentación oficial de AeroSpace](https://nikitabobko.github.io/AeroSpace/guide)
- [Lista de comandos](https://nikitabobko.github.io/AeroSpace/commands)
- [Goodies (integraciones, tips)](https://nikitabobko.github.io/AeroSpace/goodies)
- [Configuración del teclado Silakka54](../silakka54/README.md)
