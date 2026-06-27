# Zsh Configurations & Fixes

Esta carpeta contiene scripts y configuraciones modulares respaldadas para la terminal Zsh.

## Integraciones activas en ~/.zshrc

El archivo real `~/.zshrc` vive fuera del repo, pero las decisiones importantes quedan documentadas aca para poder reconstruir la maquina despues de un formateo.

Actualmente incluye:

- `starship`, desactivado solamente cuando la terminal viene desde NetBeans.
- `zsh-autosuggestions` y `zsh-syntax-highlighting`.
- rutas locales de herramientas (`~/.local/bin`, GHCup/Cabal, Android, Java, Antigravity, opencode).
- `fzf`, inicializado con `source <(fzf --zsh)` para historial y selectores interactivos.
- `zoxide`, inicializado al final del archivo con `eval "$(zoxide init zsh)"`.

Para validar una terminal nueva:

```bash
type z
type zi
type __fzf_select
bindkey '^R'
```

Si aparecen como `not found`, recargar la sesion:

```bash
source ~/.zshrc
```

Ver tambien [`../fzf/README.md`](../fzf/README.md) y [`../zoxide/README.md`](../zoxide/README.md) para los casos de uso, instalacion y restauracion en otra maquina.

## netbeans_fix.zsh

Este script soluciona los problemas visuales al usar la terminal integrada del antiguo IDE de Java **Apache NetBeans**, salvaguardando al mismo tiempo la experiencia premium en el resto de tu computadora.

**¿Qué hace y por qué existe?**
La consola heredada de NetBeans no es capaz de procesar la paleta de colores "TrueColor" (RGB 24 bits) de manera nativa. Esto provoca que emuladores avanzados de carga ultrarrápida como **Starship** impriman errores o "basura visual" cruda en la pantalla (como `161m`).

El código de este fix realiza tres pasos fundamentales de manera silenciosa:
1. Inspecciona las variables de entorno del sistema operativo y detecta si la terminal solicitando abrir fue instanciada desde NetBeans.
2. Desactiva la inicialización global de Starship **exclusivamente** para esa instancia de NetBeans. El resto de aplicaciones (VS Code, iTerm, Terminal nativa) correrán Starship normalmente a toda velocidad.
3. Inyecta y elabora "a mano" un prompt auxiliar inteligente forzando colores básicos de 8 bits (totalmente asimilables por NetBeans) y renderizando elegantemente los íconos limpios de Nerd Fonts (`` y ``), condicionados matemáticamente para que aparezcan **únicamente** si el sistema detecta que la carpeta activa es un repositorio Git válido.

### 🚀 ¿Cómo aplicarlo en otra computadora?
Para recrear la misma experiencia fluida en un entorno o Mac nuevo, solo necesitas:
1. Copiar el bloque de código íntegro del archivo `netbeans_fix.zsh`.
2. Pegarlo en tu archivo oculto maestro de Zsh (`~/.zshrc`), asegurándote de reemplazar con este código la línea por defecto donde inicializas tu emulador, es decir, el típico `eval "$(starship init zsh)"`.

### ⚠️ Requisitos
Asegúrate de configurar globalmente dentro de NetBeans (en `Tools -> Options -> Appearance -> Colors & Fonts`) la misma tipografía monoespaciada oficial de tu sistema, como **Maple Mono NF CN** (o cualquier Nerd Font instalada), para evitar que los logotipos de la rama y GitHub se transformen en cuadrados rotos por falta de glifos.

### 🖼️ Resultado Visual
![NetBeans Clean Prompt Demo](netbeans_clean_prompt.png)
