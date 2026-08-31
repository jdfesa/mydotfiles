## Context

Ver [proposal.md](proposal.md) para la motivación. El estado auditado es candidato,
no productivo:

- el host Arch tiene tmux `3.7b` instalado y el package ya está en
  `10-workstation-base.txt`;
- Zellij y Sesh no están instalados;
- `shared/tmux/tmux.conf` existe pero ningún perfil Arch lo enlaza;
- no existe `~/.tmux.conf`, `$XDG_CONFIG_HOME/tmux/tmux.conf` ni server tmux live;
- un smoke test con socket aislado cargó el archivo sin syntax error, pero confirmó
  que `default-terminal "${TERM}"` produce `xterm-kitty` dentro de tmux;
- README, Sesh y Ghostty contienen instrucciones o estados macOS-centric y paths
  fijos a `~/mydotfiles`.

La decisión debe optimizar mantenimiento durante años, recovery por SSH y
reproducibilidad, no la cantidad inmediata de features visuales.

## Goals / Non-Goals

**Goals:**

- establecer un solo owner de sesiones terminales Arch;
- comenzar con una configuración mínima, XDG y sin supply chain runtime;
- demostrar terminal correctness, SSH, TUI y rollback antes de promoción;
- reconstruir estructura de trabajo desde Git sin confundirla con procesos vivos;
- conservar un challenger justo y acotado si la experiencia real contradice la
  decisión.

**Non-Goals:**

- replicar un framework tmux público o tematizar antes de estabilizar behavior;
- restaurar procesos después de reboot;
- introducir un daemon de red, sharing o web client;
- activar una shared config en otra plataforma por accidente;
- resolver package/service provisioning general.

## Decisions

### 1. Select tmux, keep Zellij as a conditional challenger

Comparación revisada al 2026-08-30 con fuentes primarias:

| Criterion | tmux | Zellij | Decision weight |
|---|---|---|---|
| Arch provenance | Official Extra package; small C runtime surface | Official Extra package; larger Rust/WASM distribution | Both trusted; tmux simpler |
| SSH detach/attach | Long-established core workflow | Supported; nested SSH handling was corrected in 0.45.1 | tmux |
| Configuration | Mature command language, formats, hooks and XDG lookup | Excellent KDL config/layouts and live reload | Zellij for ergonomics, tmux for stability |
| Reboot reconstruction | External/declarative scripts or plugins | Built-in session resurrection reruns commands | Zellij, with side-effect caveat |
| Automation | Mature CLI, formats, hooks and `wait-for` | Structured CLI, JSON/NDJSON and event subscription | Tie; tmux is proven here |
| Plugins | Shell plugins commonly fetched through TPM | WASM/WASI permissions and many built-ins | Zellij model is safer if plugins become necessary |
| Learning | Prefix model requires deliberate practice | Discoverable status hints and presets | Zellij |
| Repository fit | Already declared, installed and has candidate sources | No package/config/profile investment | tmux |

Selección: **tmux core-only**. Zellij 0.45 aporta capabilities valiosas, pero
0.45.0 retiró converters históricos/cambió superficies y 0.45.1 corrigió SSH el
2026-08-28. Eso no lo descalifica; justifica evidencia canary antes de reemplazar
un owner más simple.

El tamaño instalado se registra como bootstrap footprint, nunca como benchmark de
RAM/CPU. No existe benchmark upstream comparable; ambos deben medirse con el mismo
escenario local.

Fuentes:

- [Arch tmux package](https://archlinux.org/packages/extra/x86_64/tmux/)
- [tmux Getting Started](https://github.com/tmux/tmux/wiki/Getting-Started)
- [tmux FAQ](https://github.com/tmux/tmux/wiki/FAQ)
- [tmux manual](https://man.archlinux.org/man/tmux.1)
- [Arch Zellij package](https://archlinux.org/packages/extra/x86_64/zellij/)
- [Zellij configuration](https://zellij.dev/documentation/configuration.html)
- [Zellij session resurrection](https://zellij.dev/documentation/session-resurrection.html)
- [Zellij programmatic control](https://zellij.dev/documentation/programmatic-control.html)
- [Zellij 0.45.0](https://github.com/zellij-org/zellij/releases/tag/v0.45.0)
- [Zellij 0.45.1](https://github.com/zellij-org/zellij/releases/tag/v0.45.1)
- [Zellij plugin permissions](https://zellij.dev/documentation/plugin-api-permissions.html)

### 2. Use an explicit layer and stage promotion

La fuente permanece en `shared/tmux/` porque la configuración puede ser portable,
pero solo Arch obtiene activation en este change:

```text
profiles/layers/linux-tmux.links
  shared/tmux/tmux.conf|$HOME/.config/tmux/tmux.conf
  shared/tmux/layouts|$HOME/.config/tmux/layouts
  shared/tmux/scripts/tmux-workspace|$HOME/.local/bin/tmux-workspace
```

El primer apply usa directamente `layers/linux-tmux` en el canary. Después de los
gates y siete días, la promoción agrega esa layer a `arch-workstation`; como
consecuencia la heredan los perfiles Arch compuestos. No se toca `macos-main`.

Esta secuencia evita crear perfiles `arch-<desktop>-tmux` combinatorios y permite
rollback retirando un único include. El package ya instalado no obtiene ownership
por estar presente: manifest, layer y host selection deben coincidir.

### 3. Deploy XDG files, not `~/.tmux.conf`

tmux buscará `$XDG_CONFIG_HOME/tmux/tmux.conf`; ese será el único target. Layouts
y workspaces usarán destinos XDG, nunca la ubicación física del checkout. README y
reload binding mostrarán el path efectivo.

El material importado se clasifica:

- options core comprendidas y probadas: conservar;
- `tools/prime/tmux-sessionizer.sh`: no enlazar hasta reemplazar roots fijos y
  demostrar idempotencia;
- Sesh/TPM/plugin snippets: retirar del config productivo y documentar como
  candidatos;
- layouts con `~/mydotfiles`: reescribir contra XDG o argumentos explícitos;
- Ghostty auto-attach: mantener desactivado y fuera de este ownership.

### 4. Set a correct terminal boundary

La configuración usará:

```tmux
set -g default-terminal 'tmux-256color'
set -as terminal-features ',xterm-kitty:RGB'
set -as terminal-features ',xterm-ghostty:RGB'
set -g allow-passthrough off
set -g set-clipboard external
```

Las dos líneas `terminal-features` solo entran después de verificar el TERM real y
rendering; un patrón que no exista se omite. Se elimina
`terminal-overrides ",*:RGB"`: declarar capability global falsea terminales
desconocidos. `tmux-256color` debe existir en Arch y en cualquier host remoto que
ejecute aplicaciones dentro de tmux. Si un remoto carece de terminfo, el runbook
usa un fallback `screen-256color` únicamente después de `infocmp`; no copia
terminfo o fuerza TERM silenciosamente.

`allow-passthrough` permanece off porque permite que aplicaciones interiores
alcancen features del terminal exterior y no existe una necesidad probada. Clipboard
comienza en `external`, que permite a tmux copiar hacia el terminal sin autorizar
que cualquier aplicación interna controle el clipboard mediante escapes. Cambiar
ambas policies requiere evidencia y otro review.

### 5. Keep startup explicit

No se agregará `tmux attach || tmux` a Zsh, Bash, Kitty o Ghostty. Entradas
documentadas:

```text
tmux new-session -A -s main
tmux attach-session -t <name>
tmux-workspace <declared-name>
```

Esto preserva shells no interactivas, comandos one-shot, debugging y una salida
clara si tmux falla. Un launcher de terminal dedicado puede evaluarse después; no
se convierte en default durante el canary.

Prefix inicial: `C-b`, el default upstream. Cambiarlo antes de medir solo agrega una
diferencia y puede complicar nested SSH. La prueba con Silakka54 decide ergonomía;
un cambio futuro puede adoptar otro prefix sin alterar el architecture contract.

### 6. Reconstruct topology, not process state

`tmux-workspace` recibirá un nombre allowlisted y declarará:

- session name;
- window names;
- pane layout;
- working directories portables;
- comandos seguros y explícitamente marcados como start-once, si existen.

El launcher hace preflight de todos los directories, crea de forma idempotente y
usa `new-session -A`/existence checks. No ejecuta `eval`, no descubre proyectos
desde history y no vuelve a lanzar servers/builds automáticamente. En empate, una
shell vacía es más segura que repetir un efecto lateral.

Estado live y scrollback viven únicamente en el server tmux y pueden contener datos
sensibles; no se serializan en Git. TPM/resurrect/continuum quedan fuera hasta que
una necesidad real justifique supply chain, privacy y rollback adicionales.

### 7. Validate SSH as an end-to-end behavior

La matriz mínima cubre:

```text
terminal -> tmux local -> SSH -> shell remote
terminal -> tmux local -> SSH -> tmux remote
terminal -> SSH -> tmux remote -> forced disconnect -> reattach
```

Se prueba prefix interior (`C-b C-b`), TERM/terminfo, resize, OSC52 y pérdida de
conexión. Si agent forwarding está habilitado, un hook explícito y documentado
actualiza `SSH_AUTH_SOCK` al attach sin persistirlo en Git/evidence. El feature se
omite si el workflow no usa forwarding.

tmux usa sockets Unix locales y no requiere listener TCP. La verificación registra
sockets esperados y confirma que no aparece network listener nuevo.

### 8. Use a fixed canary matrix and real measurements

Automated/rootless:

- lint del config y scripts;
- server con socket temporal, config XDG aislada y clean environment;
- `show-options`/`show-environment` contra invariants;
- workspace first/second run e invalid-path fixtures;
- profile resolve/link/doctor dentro de HOME temporal.

Interactive/live:

- create, rename, split, resize, zoom, chooser, detach, attach y kill;
- Kitty/Ghostty true color, undercurl, Unicode, mouse y resize;
- Zsh, Neovim, FZF, Yazi y LazyGit;
- OSC52 local/remoto;
- nested SSH y disconnect real;
- 80x24 sin depender obligatoriamente de Nerd Font;
- cuatro panes idle: cold/warm startup, total PSS, CPU 60 s y memory trend 30 min;
- sustained output y siete días de uso canary.

Targets iniciales: CPU idle menor a 1 % de un core en el escenario idle y ausencia
de growth continuo; PSS/startup se registran antes de fijar thresholds absolutos.
Una medición fallida no se oculta con package size.

### 9. Keep a fair, mutually exclusive Zellij escape hatch

Solo un fallo tmux reproducible de ergonomía, SSH, clipboard, terminal correctness
o reconstruction permite proponer el challenger. La prueba:

- dura como máximo 14 días;
- usa package oficial Arch;
- se inicia fuera de tmux y usa una layer/launcher diferente;
- habilita solo plugins built-in y conserva web server/sharing off;
- ejecuta la misma matriz y medición;
- prueba resurrection después de reboot aclarando que los comandos se reejecutan;
- reemplaza tmux solo ante mejora diaria documentada y sin degradar mandatory
  gates; un empate conserva tmux.

No se mantiene “ambos por si acaso”: nesting duplica ownership de sessions,
keybindings, mouse, clipboard y capability translation.

### 10. Record the decision and operational model

La implementación agrega
`docs/adr/0009-adopt-tmux-for-arch-terminal-multiplexing.md` con status Accepted y
scope Arch, más README/runbook bajo `shared/tmux/`. La documentación distingue:

- terminal emulator;
- shell;
- tmux server/client/session/window/pane;
- workspace declaration;
- disconnect versus reboot;
- canary, promotion y rollback.

Estados Sesh y Zellij quedan explícitos como `not adopted`; una carpeta source no
se denomina activa sin package, profile target y evidencia live coherentes.

## Risks / Trade-offs

- **[tmux tiene mayor curva inicial]** → conservar prefix default, quick reference
  pequeño y canary explícito sin auto-start.
- **[TERM incorrecto rompe remote TUIs]** → `infocmp` local/remoto, fallback
  documentado y matriz SSH antes de promoción.
- **[Clipboard/OSC52 amplía exposición]** → `set-clipboard external`, passthrough
  off y pruebas exactas; no persistir buffers.
- **[Workspace scripts se convierten en otro framework]** → nombres allowlisted,
  shell vacía por default, sin eval/plugin/discovery y tests de segunda ejecución.
- **[No hay resurrection nativa]** → declarar el límite; evaluar Zellij solo si
  reconstruction manual demuestra costo real.
- **[Shared source cambia aunque scope sea Arch]** → ninguna otra plataforma enlaza
  tmux; tests verifican que sus profiles no cambian.
- **[Live sessions complican rollback]** → listar y revisar sesiones antes de
  retirar la layer; jamás matar o borrar automáticamente.

## Migration Plan

1. Capturar baseline del config actual, package/live state y keybindings sin
   activar tmux.
2. Refactorizar sources a XDG, core-only y paths portables; agregar tests con
   socket/HOME temporales.
3. Crear la layer `linux-tmux`, ejecutar profile dry-run y enlazarla solo en
   `lab-desktop-01` después de aprobación.
4. Ejecutar la matriz funcional, SSH y de terminales; corregir únicamente defects
   observados.
5. Medir runtime y completar siete días de canary, registrando incidentes y
   configuración exacta.
6. Revisar el gate; si pasa, incluir la layer en `arch-workstation` y actualizar
   host/docs. Si falla, retirar el link y volver a shell normal.
7. Solo ante failure criteria aprobados, abrir otro change para el challenger
   Zellij; no instalarlo dentro de esta implementación.

Rollback conserva el package y server hasta que el operador cierre trabajo. Se
retira el include/profile link, se valida una shell fresh fuera de tmux y recién
después se decide si matar sesiones o remover package mediante acción separada.
