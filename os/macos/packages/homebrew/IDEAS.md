# Brew and Shell Ideas

Ideas tomadas de `~/Downloads/dotfiles-main` para evaluar mas adelante. No estan
activadas en `shared/zsh/zshrc` todavia.

## Principio

Primero se instala una herramienta, luego se prueba manualmente, y recien despues se agrega el hook al shell. Esto evita que una terminal nueva quede lenta o rota por herramientas que aun no forman parte del flujo diario.

## Candidatas

### Atuin

Historial de shell con busqueda enriquecida y sincronizacion opcional.

Impacto en el flujo:

- Reemplaza parte del uso de `Ctrl-r`.
- Permite buscar comandos antiguos por texto, directorio o contexto.
- Puede sincronizar historial entre maquinas si se configura cuenta.

Riesgo:

- Introduce una base de datos local del historial.
- Si se activa sync, hay que decidir politica de privacidad.

Activacion futura en Zsh:

```zsh
if command -v atuin >/dev/null 2>&1; then
  eval "$(atuin init zsh)"
fi
```

### Carapace

Motor de completions para multiples shells.

Impacto en el flujo:

- Mejora completions para comandos modernos.
- Puede complementar o reemplazar parte del sistema de completions de Zsh.

Riesgo:

- Puede solaparse con completions nativas o plugins actuales.
- Conviene probarlo en una rama o sesion temporal.

Activacion futura en Zsh:

```zsh
if command -v carapace >/dev/null 2>&1; then
  source <(carapace _carapace)
fi
```

### Television

Selector fuzzy moderno, similar en espiritu a `fzf`, con canales y previews.

Impacto en el flujo:

- Puede reemplazar algunos usos de `fzf`.
- Aporta canales para archivos, git, procesos, directorios y sesiones.
- Encaja bien con Yazi, Tmux/Sesh y busquedas de proyecto.

Riesgo:

- Duplica parcialmente `fzf`, que ya esta activo.
- Hay que decidir si conviven o si cada uno tiene un rol claro.

Activacion futura en Zsh:

```zsh
if command -v tv >/dev/null 2>&1; then
  eval "$(tv init zsh)"
fi
```

### Scooter

Find and replace interactivo en terminal.

Impacto en el flujo:

- Sirve para refactors pequeños sin abrir un IDE pesado.
- Complementa `rg`, `sd` y el editor.

Riesgo:

- Puede modificar muchos archivos si se usa sin revisar previews.
- Ideal para repos de prueba hasta tomar confianza.

### Procs

Reemplazo moderno de `ps`.

Impacto en el flujo:

- Lista procesos con columnas legibles y busqueda mas comoda.
- Complementa `btop` cuando se quiere una salida puntual en terminal.

Riesgo:

- Bajo; no necesita hook en shell.

### Lla

Alternativa moderna a `ls`, similar a `eza` pero con plugins y formatos propios.

Impacto en el flujo:

- Puede aportar vistas recursivas y formatos distintos.
- Hoy se solapa con `eza`, que ya esta integrado.

Riesgo:

- Si se aliasa `ls`, compite con `eza`. Mejor probar como comando separado.

## Brewfile sugerido

Si se quieren probar como herramientas opcionales:

```ruby
brew "atuin"
brew "carapace"
brew "television"
brew "scooter"
brew "procs"
brew "lla"
```

No se agregan como obligatorias porque todavia no forman parte del flujo diario.
