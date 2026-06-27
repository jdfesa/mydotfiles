# Zsh Configurations & Fixes

Esta carpeta contiene scripts y configuraciones modulares respaldadas para la terminal Zsh.

## Fuente de verdad

La fuente de verdad versionada es:

```bash
~/mydotfiles/zsh/zshrc
```

El archivo que Zsh lee en el home debe ser un enlace simbolico:

```bash
~/.zshrc -> ~/mydotfiles/zsh/zshrc
```

Lo propio de una maquina concreta vive en:

```bash
~/mydotfiles/zsh/local.zsh
```

`local.zsh` esta ignorado por Git. Usar `local.zsh.example` como plantilla cuando se configure una Mac nueva.

## Integraciones activas

Actualmente incluye:

- `starship`, desactivado solamente cuando la terminal viene desde NetBeans.
- `zsh-autosuggestions` y `zsh-syntax-highlighting`.
- rutas base portables (`/usr/local/bin`, `/opt/homebrew/bin`, `~/.local/bin`).
- carga opcional de `zsh/local.zsh` para GHCup/Cabal, Android, Java, Antigravity, opencode, NVM u otras rutas locales.
- `bat`, usado mediante aliases seguros para lectura enriquecida de archivos sin reemplazar `cat`.
- `eza`, usado mediante aliases para `ls`, `ll`, `la` y `lt`.
- `ripgrep`, usado mediante aliases para busqueda rapida con `rg`.
- `fzf`, inicializado con `source <(fzf --zsh)` para historial y selectores interactivos.
- `direnv`, inicializado de forma opcional para cargar variables por proyecto solo despues de aprobar `.envrc`.
- `zoxide`, inicializado al final del archivo con `eval "$(zoxide init zsh)"`.

Para validar una terminal nueva:

```bash
type z
type zi
type b
type preview
type ls
type ll
type rgi
type rgl
type direnv
type __fzf_select
bindkey '^R'
```

Si aparecen como `not found`, recargar la sesion:

```bash
source ~/.zshrc
```

Ver tambien [`../bat/README.md`](../bat/README.md), [`../direnv/README.md`](../direnv/README.md), [`../eza/README.md`](../eza/README.md), [`../fzf/README.md`](../fzf/README.md), [`../ripgrep/README.md`](../ripgrep/README.md) y [`../zoxide/README.md`](../zoxide/README.md) para los casos de uso, instalacion y restauracion en otra maquina.

## Activacion en esta maquina

Respaldar el archivo actual y crear el enlace:

```bash
mv ~/.zshrc ~/.zshrc.bak-before-mydotfiles
ln -s ~/mydotfiles/zsh/zshrc ~/.zshrc
```

Despues abrir una terminal nueva o ejecutar:

```bash
source ~/.zshrc
```

## netbeans_fix.zsh

Este script soluciona los problemas visuales al usar la terminal integrada del antiguo IDE de Java **Apache NetBeans**, salvaguardando al mismo tiempo la experiencia premium en el resto de tu computadora.

**¿Qué hace y por qué existe?**
La consola heredada de NetBeans no es capaz de procesar la paleta de colores "TrueColor" (RGB 24 bits) de manera nativa. Esto provoca que emuladores avanzados de carga ultrarrápida como **Starship** impriman errores o "basura visual" cruda en la pantalla (como `161m`).

El código de este fix realiza tres pasos fundamentales de manera silenciosa:
1. Inspecciona las variables de entorno del sistema operativo y detecta si la terminal solicitando abrir fue instanciada desde NetBeans.
2. Desactiva la inicialización global de Starship **exclusivamente** para esa instancia de NetBeans. El resto de aplicaciones (VS Code, iTerm, Terminal nativa) correrán Starship normalmente a toda velocidad.
3. Inyecta y elabora "a mano" un prompt auxiliar inteligente forzando colores básicos de 8 bits (totalmente asimilables por NetBeans) y renderizando elegantemente los íconos limpios de Nerd Fonts (`` y ``), condicionados matemáticamente para que aparezcan **únicamente** si el sistema detecta que la carpeta activa es un repositorio Git válido.

### 🚀 ¿Cómo aplicarlo en otra computadora?
La configuracion principal ya lo incluye en `zsh/zshrc`. En una Mac nueva basta con enlazar `~/.zshrc` hacia `~/mydotfiles/zsh/zshrc`.

### ⚠️ Requisitos
Asegúrate de configurar globalmente dentro de NetBeans (en `Tools -> Options -> Appearance -> Colors & Fonts`) la misma tipografía monoespaciada oficial de tu sistema, como **Maple Mono NF CN** (o cualquier Nerd Font instalada), para evitar que los logotipos de la rama y GitHub se transformen en cuadrados rotos por falta de glifos.

### 🖼️ Resultado Visual
![NetBeans Clean Prompt Demo](netbeans_clean_prompt.png)
