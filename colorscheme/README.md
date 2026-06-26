# Colorscheme

Sistema de temas importado como referencia para un futuro selector global de colores.

## Estado

No esta listo para uso directo. Los scripts originales cambian varias herramientas a la vez y todavia tienen decisiones que no queremos activar sin revisar.

## Que aporta

- Paletas versionadas en `list/`.
- Archivo activo en `active/active-colorscheme.sh`.
- Selector con `fzf` en `colorscheme-selector.sh`.
- Generacion potencial de temas para terminal, prompt y herramientas CLI.

## Riesgos actuales

- El flujo original recargaba Sketchybar.
- Tambien intentaba tocar wallpaper y reiniciar Yabai.
- Varias rutas venian pensadas para `~/github/dotfiles-latest`.

## Plan de adaptacion

1. Mantenerlo como referencia.
2. Crear una version propia que solo escriba archivos dentro de `~/mydotfiles`.
3. Integrar primero Kitty/Ghostty/Btop.
4. Integrar Starship solo si no rompe tu prompt actual.
5. No tocar wallpaper, Yabai ni servicios del sistema.
