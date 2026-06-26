# Tmux

Configuracion para [tmux](https://github.com/tmux/tmux), pensada como siguiente paso natural para complementar Ghostty/Kitty con sesiones persistentes.

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
ln -s ~/mydotfiles/tmux/tmux.conf ~/.tmux.conf
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
