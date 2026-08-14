# Linkarzu Dotfiles Review

## Decisions

| Area | Estado | Decision | Validation |
|---|---|---|---|
| Kitty core | `adapt` | Conservar la idea de base comun con entrypoints por sistema, pero revisar cada binding | Pendiente en canary |
| Kitty foreign sessions | `remove` | Sustituir proyectos, teclados y rutas ajenas por sesiones propias solo cuando sean necesarias | Valor ajeno confirmado |
| Kitty `Ctrl+b` namespace | `remove` | No debe competir con el prefijo estandar de tmux | Colision reproducida en macOS |
| Ghostty core | `adapt` | Revisar atajos, shaders y autoarranque de tmux antes de considerarlo propio | Revision manual pendiente |
| Ghostty shaders | `pending-review` | Verificar origen, licencia, costo grafico y necesidad por shader | Conjunto activo identificado |
| Colorscheme | `adapt` | Conservar una paleta comun solo si cada consumidor queda entendido | Prueba multiplataforma pendiente |
| Homebrew manifests | `adapt` | Retener unicamente paquetes requeridos por el flujo propio | Auditoria de paquetes pendiente |
| Tmux | `adapt` | Construir una configuracion minima propia y probar persistencia en canary | Experimento stock iniciado |
| Sesh | `reference-only` | No activar hasta estabilizar el modelo de sesiones con tmux | Postergado |
| Btop | `adapt` | Revisar opciones sensibles a terminal y hardware | Prueba macOS/Arch pendiente |
| Fastfetch | `adapt` | Simplificar a informacion util y portable | Revision pendiente |
| Yazi | `adapt` | Mantener solo bindings y plugins comprendidos | Revision pendiente |
| Lazygit | `keep` | La configuracion activa ya fue reducida y reescrita con fuentes oficiales | Revalidar en ambos sistemas |
| Neobean ideas | `reference-only` | Estudiar ideas puntuales sin convertir Neobean en base local | Registrado en decisiones de Neovim |

## Promotion Rules

Una adaptacion no se promueve por parecer profesional o por funcionar en la
maquina del autor. Debe reducir friccion real, respetar el mapa de teclas propio,
usar rutas portables, declarar dependencias y superar pruebas en Arch canary.

macOS de produccion solo recibe cambios pequenos, reversibles y ya entendidos.
No se aplicara en bloque ninguna configuracion incluida en este dossier.

## Exit Criteria

El dossier puede cerrarse cuando todas las filas dejen de estar pendientes y
cada elemento aceptado tenga implementacion, documentacion y validacion propias.
El clon temporal debe eliminarse. Si quedan archivos derivados, la atribucion y
las condiciones de licencia necesarias deben persistir fuera del dossier antes
de retirarlo.
