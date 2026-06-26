# Sesh

Configuracion para [sesh](https://github.com/joshmedeski/sesh), selector de sesiones para tmux.

## Estado

Importado como complemento de `tmux`. Ya fue ajustado para apuntar a `~/mydotfiles` en vez del repo original.

## Que aporta

- Entradas fijas para abrir carpetas frecuentes.
- Vista previa con `bat` cuando esta disponible.
- Puede integrarse con tmux mediante `prefix + T`.

## Instalacion

```bash
brew install sesh fzf bat
```

## Activacion

```bash
ln -s ~/mydotfiles/sesh ~/.config/sesh
```

Si ya existe `~/.config/sesh`, respaldarlo antes.

## Pendiente

- Agregar proyectos reales tuyos.
- Decidir si las sesiones abren editor, shell simple o layouts de tmux.
