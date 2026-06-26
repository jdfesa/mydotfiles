# Colorscheme

Sistema de temas importado como referencia para un futuro selector global de colores.

## Estado

Parcialmente adaptado. El selector local ya solo actualiza `colorscheme/active/active-colorscheme.sh` dentro de `~/mydotfiles`; no toca wallpaper, Yabai, Sketchybar ni servicios del sistema.

## Que aporta

- Paletas versionadas en `list/`.
- Archivo activo en `active/active-colorscheme.sh`.
- Selector local con `fzf` en `colorscheme-selector.sh`.
- Generacion potencial de temas para terminal, prompt y herramientas CLI.

## Riesgos actuales

- El flujo original recargaba Sketchybar, tocaba wallpaper y reiniciaba Yabai; eso no se importa.
- Las paletas usan variables internas `jd_colorXX` para compartir colores entre scripts.
- Todavia falta generar archivos concretos para Kitty, Ghostty, Btop o Starship.

## Plan de adaptacion

1. Mantener las paletas como referencia.
2. Usar el selector solo para elegir el archivo activo.
3. Integrar primero Kitty/Ghostty/Btop.
4. Integrar Starship solo si no rompe tu prompt actual.
5. No tocar wallpaper, Yabai ni servicios del sistema.
