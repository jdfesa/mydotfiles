# Keep Symlinks Now, Evaluate Chezmoi Later

Status: Accepted
Date: 2026-07-10

## Context

El setup actual de macOS usa symlinks manuales desde `~/mydotfiles` hacia las
rutas esperadas por cada aplicacion. Esta estrategia es simple, transparente y
ya funciona.

Tambien existe interes en soportar macOS, Arch Linux, Windows, VMs, usuarios
distintos y rutas locales distintas. Herramientas como `chezmoi` pueden ayudar
en ese escenario porque soportan templates, diferencias por maquina, scripts y
aplicacion declarativa de archivos.

Adoptar `chezmoi` demasiado pronto podria agregar complejidad antes de tener
suficientes diferencias reales que la justifiquen.

## Decision

Mantener symlinks como estrategia activa por ahora.

Documentar la arquitectura multi-OS y preparar el repositorio para una posible
migracion futura, pero no migrar todo a `chezmoi` todavia.

`chezmoi` se evaluara cuando existan pruebas reales en Arch Linux, Windows o VMs
que muestren friccion clara con symlinks manuales.

## Consequences

Ventajas:

- no se rompe el setup principal de macOS;
- no se introduce una herramienta nueva en el camino critico;
- los cambios iniciales son faciles de revisar y revertir;
- se gana claridad arquitectonica antes de automatizar.

Costos:

- por ahora los symlinks siguen requiriendo documentacion o scripts propios;
- algunas diferencias por sistema operativo deberan resolverse manualmente;
- la restauracion completa en maquinas nuevas aun no sera totalmente
  declarativa.

Esta decision puede revisarse cuando existan perfiles reales como `arch-dwm`,
`arch-i3` o `windows-native`.

