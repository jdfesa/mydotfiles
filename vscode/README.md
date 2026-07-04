# VS Code

Configuracion activa de VS Code, enlazada desde:

```bash
~/Library/Application Support/Code/User/settings.json -> ~/mydotfiles/vscode/settings.json
```

La version actual adopta solo la parte segura de la estetica del repo `dotfiles-main`: color theme Catppuccin Mocha, pero iconos nativos de VS Code y sin CSS externo activo.

## Archivos

- `settings.json`: configuracion activa. VS Code la lee por symlink.
- `custom.css`: CSS experimental basado en `dotfiles-main`. Queda guardado, pero no activo por defecto.
- `extensions.txt`: extensiones recomendadas para que esta configuracion no quede a medias.
- `settings.json.bak`: respaldo historico previo, util para volver a una base mas simple.

## Que cambia

- Tema principal: `Catppuccin Mocha`.
- Iconos de archivos: `vs-seti`, el tema Seti incluido por defecto en VS Code.
- Iconos internos de VS Code: `Default`.
- Activity bar arriba, como en la captura del repo descargado.
- Command palette y scrollbars quedan con comportamiento nativo por ahora.
- Explorer con iconos visibles. Se evita ocultar acciones del titulo del sidebar mientras se aprende la configuracion.
- Status bar con mejor lectura para modo Vim.
- Animaciones desactivadas por ahora para evitar efectos colaterales de `custom-ui-style`.

## Iconos

Hay tres capas distintas:

- `workbench.iconTheme`: iconos de archivos y carpetas del explorer. Ahora usa `vs-seti`.
- `workbench.productIconTheme`: iconos internos de VS Code, como search, source control, debug y layout. Ahora usa `Default`.
- `custom.css`: puede ocultar botones si usa `display: none`. No esta activo por defecto.

Si en el futuro quieres una interfaz mas minimalista, activar CSS solo de a un bloque por vez y documentar por que. El punto de partida debe ser una UI completa y entendible.

## Dependencias

Instalar extensiones desde esta carpeta:

```bash
cat ~/mydotfiles/vscode/extensions.txt | xargs -L 1 code --install-extension
```

Las extensiones de Catppuccin pueden quedar instaladas para probar temas, pero la configuracion activa no depende de sus iconos. Las mas importantes si se reactiva la estetica experimental son:

- `subframe7536.custom-ui-style`
- `brandonkirbyson.vscode-animations`
- `catppuccin.catppuccin-vsc`
- `catppuccin.catppuccin-vsc-icons`
- `alexdauenhauer.catppuccin-noctis-icons`
- `miguelsolorio.fluent-icons`

## CSS experimental

Por defecto esta desactivado:

```jsonc
"custom-ui-style.external.imports": [],
"custom-ui-style.external.loadStrategy": "disable",
"custom-ui-style.stylesheet": {}
```

Para volver a probar el CSS:

```jsonc
"custom-ui-style.external.imports": [
  "file:///Users/jd/mydotfiles/vscode/custom.css"
],
"custom-ui-style.external.loadStrategy": "refetch"
```

Despues:

1. Abrir la command palette.
2. Ejecutar `Enable custom ui style` o `Custom UI Style: Reload`.
3. Recargar VS Code.

Si algo desaparece, ejecutar `Custom UI Style: Rollback, cleanup and restart instantly`.

## Rollback

Si el cambio no convence:

1. Ejecutar `Custom UI Style: Rollback, cleanup and restart instantly` desde la command palette.
2. Restaurar el respaldo simple:

```bash
cp ~/mydotfiles/vscode/settings.json.bak ~/mydotfiles/vscode/settings.json
```

Si quieres volver exactamente al estado anterior de este repo antes de esta prueba y todavia no hiciste commit:

```bash
git restore vscode/settings.json vscode/extensions.txt vscode/README.md
rm ~/mydotfiles/vscode/custom.css
```

## Notas

El repo descargado tambien trae `keybindings.json`, pero no se adopta automaticamente porque cambia demasiado la memoria muscular: explorer estilo Vim, navegacion de paneles, terminal y Markdown. Si mas adelante quieres probarlo, conviene importarlo como experimento separado y documentar cada bloque.

Ghostty y Kitty no se tocan desde esta carpeta. Su estetica actual vive en sus propias configuraciones y ya tiene shaders/tema que te gustan.
