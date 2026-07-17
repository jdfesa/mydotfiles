# Restore macOS

Esta guia reconstruye la configuracion principal de macOS desde una instalacion
limpia. El objetivo verificable es terminar con `scripts/doctor macos-main`
informando `16 ok, 0 warning(s), 0 error(s)`.

## Scope

El repositorio restaura automaticamente:

- los archivos versionados;
- los 16 symlinks declarados en `profiles/macos-main.links`;
- configuraciones de terminal, shell, editores y herramientas CLI;
- configuraciones exclusivas de macOS como AeroSpace, Sketchybar y Hammerspoon;
- la receta de paquetes declarada mediante Brewfiles.

Requieren intervencion manual:

- permisos de privacidad de macOS;
- inicios de sesion en aplicaciones;
- claves SSH, tokens, credenciales y datos personales;
- `shared/zsh/local.zsh` y otras rutas locales ignoradas;
- archivos sincronizados mediante iCloud, Dropbox u otro servicio.

## 1. Prepare macOS

Abrir Terminal y comprobar Git:

```sh
git --version
```

En una instalacion limpia, macOS puede pedir instalar Command Line Tools.
Completar ese paso antes de continuar.

Instalar Homebrew desde [brew.sh](https://brew.sh/) si todavia no existe:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Seguir la instruccion que Homebrew muestra para agregar `brew` al `PATH`, abrir
otra terminal y validar:

```sh
brew --version
```

## 2. Clone the Source of Truth

Varias configuraciones usan `~/mydotfiles` como ruta canonica. Clonar ahi:

```sh
git clone https://github.com/jdfesa/mydotfiles.git ~/mydotfiles
cd ~/mydotfiles
```

Antes de instalar o enlazar, revisar que el repositorio este limpio:

```sh
git status --short
```

Activar los hooks versionados del repositorio:

```sh
git config core.hooksPath .githooks
```

Esto restaura, entre otros controles, la regeneracion automatica del diagrama de
Silakka54 cuando cambia su archivo `.vil`.

## 3. Install Packages

El perfil de symlinks es exacto y verificable. Los Brewfiles, en cambio, siguen
en proceso de curado: aceleran la reconstruccion, pero no representan una imagen
exacta de todas las aplicaciones instaladas hoy.

La base propuesta y las herramientas principales viven en estas dos capas.
Revisarlas antes de ejecutar:

```sh
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/00-base/Brewfile
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/10-essential/Brewfile
```

Las aplicaciones menos esenciales se mantienen separadas y se instalan solo si
siguen siendo necesarias:

```sh
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/15-nice-to-haves/Brewfile
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/20-optional/Brewfile
```

No abrir todavía las aplicaciones recién instaladas: algunas crean una
configuracion por defecto que luego bloquearia el linker.

### Configurar RTK para Codex

La capa `10-essential` instala RTK para reducir la salida ruidosa de tests,
builds, Git y otras herramientas antes de incorporarla al contexto de Codex.
Inicializarlo despues de instalar los paquetes:

```sh
rtk telemetry disable
rtk init --global --codex
rtk --version
rtk telemetry status
```

`rtk init` genera sus instrucciones bajo `~/.codex`; no modifica credenciales
ni requiere versionar esos archivos. La decision, el uso y los limites estan
documentados en [`shared/rtk/README.md`](../shared/rtk/README.md).

## 4. Recreate Local Files

Crear la configuracion local de Zsh desde la plantilla:

```sh
cp ~/mydotfiles/shared/zsh/local.zsh.example \
  ~/mydotfiles/shared/zsh/local.zsh
```

Editar solamente las rutas que existan en la nueva Mac. Este archivo esta
ignorado por Git y no debe contener secretos que necesiten respaldo remoto.

Las claves SSH y credenciales se restauran mediante su mecanismo privado; nunca
se copian a este repositorio.

## 5. Apply the macOS Profile

Previsualizar los 16 destinos:

```sh
cd ~/mydotfiles
scripts/link --dry-run macos-main
```

En una Mac limpia deberian aparecer como `would create`. Si aparece `blocked`,
el destino es un archivo o directorio real. Revisarlo y respaldarlo manualmente;
el linker nunca lo sobrescribe.

Crear los enlaces:

```sh
scripts/link macos-main
scripts/doctor macos-main
```

El resultado esperado es:

```text
Doctor result: 16 ok, 0 warning(s), 0 error(s).
```

## 6. Complete macOS Integration

Configurar Hammerspoon para leer la ruta enlazada:

```sh
defaults write org.hammerspoon.Hammerspoon \
  MJConfigFile "$HOME/.config/hammerspoon/init.lua"
```

Si los comandos de Kitty no quedaron disponibles mediante Homebrew, enlazarlos
sin privilegios administrativos:

```sh
mkdir -p "$HOME/.local/bin"
[ -e "$HOME/.local/bin/kitty" ] || \
  ln -s /Applications/kitty.app/Contents/MacOS/kitty "$HOME/.local/bin/kitty"
[ -e "$HOME/.local/bin/kitten" ] || \
  ln -s /Applications/kitty.app/Contents/MacOS/kitten "$HOME/.local/bin/kitten"
```

Abrir las aplicaciones principales:

```sh
open -a AeroSpace
open -a Hammerspoon
brew services restart sketchybar
```

En `System Settings -> Privacy & Security -> Accessibility`, habilitar las apps
que macOS solicite, especialmente AeroSpace y Hammerspoon.

## 7. Restore Tool-Specific State

- Neovim: seguir [`shared/nvim/docs/RESTORE.md`](../shared/nvim/docs/RESTORE.md)
  para plugins, Mason y Treesitter.
- VS Code: instalar las extensiones declaradas:

  ```sh
  xargs -L 1 code --install-extension \
    < ~/mydotfiles/shared/vscode/extensions.txt
  ```

- Sketchybar: consultar
  [`os/macos/sketchybar/README.md`](../os/macos/sketchybar/README.md) si faltan
  fuentes o SbarLua.
- Hammerspoon: consultar
  [`os/macos/hammerspoon/README.md`](../os/macos/hammerspoon/README.md) para
  permisos y GoMaCal.

## 8. Validate the Restored Environment

```sh
cd ~/mydotfiles
scripts/doctor macos-main
scripts/lint-shell
aerospace reload-config --dry-run --no-gui
kitty +runpy 'from kitty.config import load_config; load_config()'
nvim --headless "+lua print('nvim-config-ok')" +qa
sesh list -c
```

Comprobar que las capas principales de Homebrew estan satisfechas:

```sh
brew bundle check --file os/macos/packages/homebrew/00-base/Brewfile
brew bundle check --file os/macos/packages/homebrew/10-essential/Brewfile
```

## Recovery Rules

- No borrar una configuracion previa antes de inspeccionarla.
- Respaldar destinos reales antes de reemplazarlos por symlinks.
- No usar `scripts/link --repair` sobre un enlace incorrecto sin revisar primero
  adonde apuntaba.
- Ejecutar `scripts/doctor macos-main` despues de mover carpetas o restaurar una
  maquina.
- Mantener esta guia actualizada cada vez que aparezca un paso manual nuevo.
