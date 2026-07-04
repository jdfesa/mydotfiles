# Lazygit

Configuracion para [lazygit](https://github.com/jesseduffield/lazygit), una interfaz terminal para Git.

## Estado

Activa y enlazada desde:

```bash
~/Library/Application Support/lazygit/config.yml -> ~/mydotfiles/lazygit/config.yml
```

Esta version adopta ideas del repo `dotfiles-main`: tema Catppuccin, iconos, file tree visible, commit graph y una preparacion opcional para diffs con `delta`.

## Que aporta

- UI mas legible con colores Catppuccin.
- Iconos Nerd Font y arbol de archivos.
- Panel lateral expandible cuando esta enfocado.
- Historial con grafo activado.
- Diffs con pager conservador por ahora; el bloque de `delta` queda comentado hasta instalar `git-delta`.
- Copiar al clipboard con `y`.
- Comando guiado para Conventional Commits con `<C-v>`.
- Comando para crear PR con GitHub CLI usando `<C-r>`.

## Instalacion

```bash
brew install lazygit
```

Opcionales:

```bash
brew install git-delta gh
```

`git-delta` mejora la lectura de diffs. `gh` solo es necesario para el comando `<C-r>` de crear Pull Request.

## Flujo mental recomendado

Lazygit no reemplaza aprender Git. Lo hace visible:

1. `Files`: revisar cambios y hacer stage parcial.
2. `Branches`: cambiar o crear ramas.
3. `Commits`: leer historial, reordenar, squash/fixup o revertir.
4. `Stash`: guardar cambios temporales.
5. `Status`: ver estado general del repo.

Para acostumbrarte, conviene empezar con un flujo pequeño:

```text
abrir lazygit -> revisar diff -> stage -> commit -> push
```

Despues sumar stage parcial, stash y ramas.

## Custom commands

### `<C-v>` Conventional Commit

Abre un formulario para construir mensajes como:

```text
feat(vscode): adopt catppuccin ui
fix(yazi): repair archive opener
docs(lazygit): add learning sources
```

### `<C-r>` Crear Pull Request

Ejecuta:

```bash
gh pr create --fill --web
```

Esto usa GitHub CLI y abre el flujo web de GitHub.

## Activar delta

Cuando `delta` exista en PATH:

```bash
brew install git-delta
```

Editar `lazygit/config.yml` y cambiar:

```yaml
pager: ""
```

por:

```yaml
pager: delta --dark --paging=never --syntax-theme "Catppuccin Mocha" --wrap-max-lines=10
```

## Rollback

Para volver a la configuracion conservadora anterior:

```yaml
gui:
  theme:
    selectedLineBgColor:
      - "#013e4a"
git:
  paging:
    colorArg: always
    pager: ""
    useConfig: false
```

Si todavia no hiciste commit:

```bash
git restore lazygit/config.yml lazygit/README.md lazygit/SOURCES.md
```

## Fuentes

Ver [SOURCES.md](SOURCES.md) para documentacion oficial y una ruta corta de aprendizaje.
