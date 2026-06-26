# Lazygit

Configuracion para [lazygit](https://github.com/jesseduffield/lazygit), una interfaz terminal para Git.

## Estado

Activa y enlazada desde `~/Library/Application Support/lazygit/config.yml` hacia `~/mydotfiles/lazygit/config.yml`.

## Que aporta

- Tema simple para la linea seleccionada.
- Base conservadora que usa el editor/pager normal de LazyGit.
- Integracion opcional con `git-delta` para diffs mas legibles.

## Instalacion

```bash
brew install lazygit
```

Opcional para mejores diffs:

```bash
brew install git-delta
```

## Activacion

En macOS lazygit busca su config en `~/Library/Application Support/lazygit/config.yml`.

```bash
mkdir -p "$HOME/Library/Application Support/lazygit"
ln -s ~/mydotfiles/lazygit/config.yml "$HOME/Library/Application Support/lazygit/config.yml"
```

Si ya existe un archivo ahi, respaldarlo antes de crear el enlace. En esta maquina se mantiene la fuente de verdad en `~/mydotfiles/lazygit/config.yml`.

## Para que sirve

LazyGit es una interfaz visual en la terminal para operar sobre un repositorio Git sin recordar todos los comandos. No reemplaza a Git: por debajo ejecuta acciones normales como `git status`, `git add`, `git commit`, `git pull`, `git push`, `git stash`, `git checkout` o `git rebase`, pero las organiza en paneles navegables.

El flujo tipico es:

1. Abres `lazygit` dentro de un repo.
2. Ves archivos modificados, ramas, commits y stash en paneles.
3. Seleccionas archivos o hunks para stage.
4. Escribes el mensaje y haces commit.
5. Si quieres, haces push/pull desde la misma UI.

Es especialmente util para revisar cambios antes de commitear, hacer stage parcial, moverte entre ramas, ver historial, manejar stash y resolver operaciones frecuentes sin salir de la terminal.

## Pendiente

- Ajustar colores para que sigan tu paleta principal.
- Activar `git-delta` cuando este instalado.
