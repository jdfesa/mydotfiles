# Homebrew

Homebrew sigue siendo simplemente el gestor de paquetes de macOS. Esta carpeta no configura Homebrew como programa: guarda listas versionadas de software para poder reconstruir una Mac de forma reproducible.

Los archivos `Brewfile` son manifiestos: dicen que paquetes, apps y fuentes instalar con Homebrew. Es parecido a tener un `package.json`, pero para herramientas del sistema.

La idea no es instalar todo de golpe, sino convertir la lista de software en algo ejecutable, revisable y versionado.

## Estado

Importado como base externa desde `~/Downloads/dotfiles-latest-main 2` y pendiente de curado para este equipo.

Estos Brewfiles venian de los dotfiles de otro usuario. Por eso no deben tratarse como una lista final ni ejecutarse a ciegas: son una referencia util para descubrir herramientas y acelerar una instalacion nueva, pero cada paquete tiene que validarse contra este setup.

La idea practica es:

1. Clonar `~/mydotfiles` en una Mac nueva.
2. Revisar la capa que se quiere instalar.
3. Ejecutar solo esa capa con `brew bundle`.
4. Documentar aparte la configuracion real de cada herramienta cuando no viva en Homebrew.

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

Para comprobar que falta sin instalar automaticamente:

```bash
brew bundle check --file ~/mydotfiles/brew/00-base/Brewfile
```

## Por que existe

Sin Brewfiles, despues de formatear o usar otra Mac hay que recordar e instalar todo a mano:

```bash
brew install zoxide
brew install fzf
brew install starship
brew install sesh
brew install bat
brew install eza
```

Con Brewfiles, esa decision queda documentada y se puede repetir:

```bash
brew bundle --file ~/mydotfiles/brew/00-base/Brewfile
```

Esto no reemplaza a Homebrew. Solo usa `brew bundle` para leer la lista e instalar lo que falte.

En resumen: Homebrew es la herramienta que instala paquetes; los Brewfiles son la receta reproducible que le dice que instalar.

## Que se guarda aca

- `brew "zoxide"`: herramientas de terminal instaladas por Homebrew.
- `cask "ghostty"`: apps de macOS instaladas por Homebrew Cask.
- `tap "FelixKratz/formulae"`: repositorios extra de formulas.
- `vscode "ms-python.python"`: extensiones de VS Code, cuando corresponde.

## Que no se guarda aca

- Configuracion interna de cada herramienta.
- Historial local, bases de datos o caches.
- Preferencias personales generadas por apps despues de usarlas.

Por ejemplo: `brew/00-base/Brewfile` instala `zoxide`, pero la activacion de `zoxide` vive en `~/.zshrc` y esta explicada en `../zoxide/README.md`.

## Pendiente

- Quitar apps que no uso.
- Separar herramientas realmente esenciales de experimentos.
- Cruzar esta lista con `apps/macos/software_list.md`.
