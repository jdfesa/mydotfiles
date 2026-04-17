# 🎨 VS Code "Claude Aesthetic" Customization

Esta carpeta documenta e implementa los cambios hiperpersonalizados de VS Code para que luzca exactamente como una herramienta de línea de comandos pura (similar a **Claude Code**).

## 🗂️ Contenido de esta copia de seguridad
- `settings.json.bak`: Una copia intacta de tu configuración original, sin las inyecciones visuales CSS, antes de la modificación de diseño.

## 🛠️ ¿Qué hicimos exactamente?

1. **Custom UI Style (`subframe7536.custom-ui-style`):** Instalamos esta extensión de la comunidad (un fork robusto). Permite sobrescribir el CSS del contenedor `Electron` de VS Code superando los errores de la extensión original APC.
2. **Fuentes Monoespaciadas Globales:** A través de la extensión, obligamos a que el *Explorador de Archivos* y la barra de estado usen `Maple Mono NF CN`.
3. **Barra Organizadora Minimalista:** Empujamos la barra izquierda de herramientas hacia arriba de la sidebar.
4. **Tema de Color:** Utilizamos `dnrm.claude-theme` para igualar los tonos oscuros grises y los acentos beige cálidos de Anthropic.
5. **Barra de Estado Mágica tipo Neovim:** Configuramos variables de Vim para que la barra inferior de VS Code cambie entre Azul, Verde y Rojo dependiendo de si estás tecleando (Insert) o navegando (Normal), y eliminamos sus bordes para hacerla ver 100% plana.

---

## ⚠️ Mensaje de "Instalación de VS Code Corrupta"

VS Code tiene un checksum de integridad para saber si su código fuente fue modificado (por motivos de seguridad). Dado que APC modifica el código CSS interno de la ventana principal de Electron, la próxima vez que inicies VS Code verás este error:

> *"Your VS Code installation appears to be corrupt. Please reinstall."*

**IGNÓRALO.** Es una advertencia inofensiva completamente normal cuando usamos inyección de UI. En el panel de ajustes aparecerá un icono de tuerca amarilla que puedes ocultar permanentemente con la opción `Don't Show Again` de tu editor.

**IMPORTANTE (Cuando Actualizas VS Code):**
Cada vez que Microsoft publique una actualización de VS Code, el motor CSS se reseteará al por defecto (tus fuentes Monoespaciadas del explorador se perderán). 
**Solución:** Simplemente presiona `Cmd + Shift + P` y tipea **`Enable custom ui style`**.

---

## ↩️ Cómo Revertir todo (Desinstalar el Look Claude)

Si sientes que el minimalismo afecta tu flujo de trabajo o no te logras adaptar, volver atrás es extremadamente sencillo:

1. **Apagar la inyección:** Abre la paleta de comandos (`Cmd + Shift + P`), busca y ejecuta **`Disable custom ui style`**. Esto devolverá el explorador y la barra de título a la fuente base de Apple.
2. **Restaurar Configuración Original:** Copia el archivo original que guardamos aquí hacia su lugar.
   ```bash
   cp ~/mydotfiles/vscode-custom/settings.json.bak ~/mydotfiles/vscode/settings.json
   ```
3. Opcionalmente desinstala las extensiones `apc-extension` y `claude-theme`.
4. Reinicia VS Code. Todo volverá a ser tu tema normal de *Catppuccin Mocha*.
