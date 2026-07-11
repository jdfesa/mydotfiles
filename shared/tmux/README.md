# Tmux

Configuracion para [tmux](https://github.com/tmux/tmux), pensada como siguiente paso natural para complementar Ghostty/Kitty con sesiones persistentes.

## Para que sirve

`tmux` es un multiplexor de terminal: permite tener varias ventanas y paneles dentro de una misma sesion de terminal, y dejar esa sesion viva aunque cierres la ventana de Ghostty/Kitty.

En el dia a dia sirve para:

- Mantener un proyecto abierto con editor, servidor, logs y Git en paneles separados.
- Cerrar la terminal y volver despues con `tmux attach` sin reconstruir todo.
- Conectarte por SSH y no perder el trabajo si se corta la conexion.
- Usar `sesh` como selector para saltar rapido entre proyectos.

Ejemplo mental:

```text
Ghostty o Kitty = la ventana grafica de terminal
Zsh = el shell donde escribes comandos
tmux = las sesiones, ventanas y paneles persistentes dentro de esa terminal
sesh = el selector rapido para abrir o volver a esas sesiones
```

## Tmux, Zellij y Nushell

`tmux` y `zellij` compiten en la misma categoria: organizar sesiones, paneles y ventanas de terminal.

`nushell` no compite directamente con ellos. `nushell` reemplaza o complementa a `zsh`: cambia el lenguaje con el que escribes comandos y trabaja con datos estructurados, tablas y pipelines mas modernos.

Resumen practico:

- `tmux`: clasico, estable, muy usado, ideal si quieres sesiones persistentes y mucha compatibilidad.
- `zellij`: alternativa moderna a tmux, con interfaz mas guiada, layouts declarativos y mejor experiencia visual inicial.
- `nushell`: shell alternativo; util si quieres pipelines estructurados, pero cambia habitos basicos de terminal.

Recomendacion para este setup: activar primero `tmux` de forma simple, porque ya tenemos `sesh`, `fzf`, `zoxide`, Ghostty/Kitty y documentacion preparada alrededor de ese flujo. Evaluar `zellij` despues si `tmux` se siente incomodo. Dejar `nushell` como experimento separado, no como shell principal por ahora.

## Estado

Importado y separado en dos niveles:

- `tmux.conf`: base adaptada a `~/mydotfiles`, mas segura para probar.
- `tmux.conf.sh`: nota local que reemplaza la referencia importada original, porque no queremos conservar rutas personales o dependencias externas.

## Que queremos rescatar

- TrueColor y compatibilidad con undercurl.
- OSC52/clipboard.
- Copy-mode estilo Vim.
- Mouse y renumeracion automatica de ventanas.
- Integracion opcional con `sesh` y `fzf`.
- Layouts guardados en `layouts/`.
- Sessionizer generico en `tools/prime/tmux-sessionizer.sh`.

## Instalacion

```bash
brew install tmux fzf fd sesh
```

Opcional si luego usamos plugins:

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

## Activacion

```bash
ln -s ~/mydotfiles/shared/tmux/tmux.conf ~/.tmux.conf
```

Si ya existe `~/.tmux.conf`, respaldarlo antes.

## Relacion con Ghostty

Tu `ghostty/config` ya tiene una idea de arranque con tmux. Antes de activarla conviene adaptar el sessionizer para que apunte a `~/mydotfiles` y no a rutas del repo original.

## Pendiente

- Probar `tmux.conf` en una sesion aislada.
- Decidir si `prefix` queda en `C-b` o se adapta a tu teclado Silakka54.
- Integrar `sesh` solo despues de ajustar `sesh/sesh.toml`.
- Evaluar plugins cuando la base ya sea comoda.
- Conectar el sessionizer con Ghostty/Kitty si realmente mejora el flujo.
