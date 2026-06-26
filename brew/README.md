# Homebrew

Esta carpeta guarda Brewfiles para reproducir instalaciones de macOS por capas. La idea no es instalar todo de golpe, sino convertir la lista de software en algo ejecutable, revisable y versionado.

## Estado

Importado como base desde `dotfiles-latest-main 2` y pendiente de curado para este equipo.

## Capas

- `00-base/Brewfile`: herramientas CLI y apps base para terminal y dotfiles.
- `10-essential/Brewfile`: herramientas de desarrollo, fuentes, navegadores y utilidades frecuentes.
- `15-nice-to-haves/Brewfile`: apps y herramientas convenientes, pero no criticas.
- `20-optional/Brewfile`: software opcional o dependiente de gustos/proyectos.

## Uso recomendado

Revisar antes de ejecutar. Para instalar una capa:

```bash
brew bundle --file ~/mydotfiles/brew/00-base/Brewfile
```

Para inspeccionar sin instalar:

```bash
sed -n '1,220p' ~/mydotfiles/brew/00-base/Brewfile
```

## Pendiente

- Quitar apps que no uso.
- Separar herramientas realmente esenciales de experimentos.
- Cruzar esta lista con `apps/macos/software_list.md`.
