# Linkarzu Audit Evidence

## Snapshot

- Audited on: `2026-08-14`
- Source: `https://github.com/linkarzu/dotfiles-latest`
- Default branch: `main`
- Revision: `d674d4cf65fa47084bcf7db52ee74783cc6f9866`
- Revision date: `2026-08-13T14:00:45Z`
- GitHub license result: `NOASSERTION`
- Root license file: no detectado en la revision auditada

La ausencia de una licencia explicita no demuestra que todo el contenido carezca
de licencia propia. Si impide determinar permisos, no se copia nuevo codigo;
primero se identifica el origen o se reimplementa la idea desde documentacion
oficial.

## Methods

- Comparacion SHA-256 de archivos no vacios entre ambos arboles.
- Comparacion de archivos con la misma ruta relativa.
- Similitud de lineas para configuraciones modificadas.
- Revision del historial Git local y de README historicos de cada herramienta.
- Inspeccion manual de rutas, sesiones, comentarios de procedencia y comandos
  que pueden ejecutarse al iniciar una terminal.

La auditoria encontro 387 pares no vacios de contenido exacto; una coincidencia
de archivos vacios fue descartada por no aportar evidencia. La mayoria pertenece
a temas de Kitty y otros activos que pueden tener procedencia transitiva. Los
numeros sirven para ubicar revisiones, no para inferir autoria.

## High-Signal Findings

- `shared/kitty/common.conf` conserva una similitud aproximada de 87.9% con el
  `kitty.conf` auditado.
- Las 11 sesiones locales de Kitty tienen los mismos nombres que el upstream;
  cinco archivos conservan mas de 91% de similitud.
- `shared/ghostty/config` conserva una similitud aproximada de 97.7%; ademas hay
  35 shaders con contenido exacto.
- `shared/btop/btop.conf` conserva aproximadamente 97.6% de similitud.
- `shared/fastfetch/config.jsonc` conserva aproximadamente 82.5% de similitud.
- El historial local registra importaciones separadas de Kitty, tmux, Sesh,
  Yazi, Btop y Lazygit durante junio de 2026.

## Limitations

- La similitud no demuestra quien escribio primero un archivo.
- El snapshot no representa necesariamente versiones anteriores del upstream.
- Los activos de terceros pueden coincidir exactamente en ambos repositorios.
- La inspeccion estatica no confirma estabilidad, rendimiento o ergonomia.
- Este dossier registra evidencia tecnica y no constituye asesoramiento legal.
