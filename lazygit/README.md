# Lazygit

Configuracion para [lazygit](https://github.com/jesseduffield/lazygit), una interfaz terminal para Git.

## Estado

Importada como candidato de baja friccion. No esta enlazada al sistema todavia.

## Que aporta

- Tema simple para la linea seleccionada.
- Integracion con `git-delta` como pager para diffs mas legibles.
- `editPreset: nvim-remote`, util si mas adelante integramos Neovim/tmux.

## Instalacion

```bash
brew install lazygit git-delta
```

## Activacion

En macOS lazygit busca su config en `~/Library/Application Support/lazygit/config.yml`.

```bash
mkdir -p "$HOME/Library/Application Support/lazygit"
ln -s ~/mydotfiles/lazygit/config.yml "$HOME/Library/Application Support/lazygit/config.yml"
```

Si ya existe un archivo ahi, respaldarlo antes de crear el enlace.

## Pendiente

- Decidir si `nvim-remote` queda activo o si conviene usar el editor terminal por defecto.
- Ajustar colores para que sigan tu paleta principal.
