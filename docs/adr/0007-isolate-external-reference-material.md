# Isolate External Reference Material

Status: Accepted
Date: 2026-08-14

## Context

Parte de las configuraciones actuales fue copiada o adaptada desde dotfiles
publicos para estudiar un flujo de trabajo avanzado. Mezclar clones externos,
configuracion activa y notas informales hace dificil distinguir que se entiende,
que se atribuye a terceros y que puede desplegarse con seguridad.

Tambien existe un riesgo operativo: sesiones, rutas, teclas o comandos pensados
para otra persona pueden quedar activos en macOS de produccion o en Arch canary.

## Decision

Crear `references/` como limite no desplegable para fuentes externas:

- `references/inbox/` conserva clones temporales ignorados por Git;
- `references/dotfiles/` conserva dossiers versionados de procedencia y revision;
- `references/templates/` normaliza nuevas auditorias;
- `references/tools/` contiene utilidades estaticas de comparacion;
- `scripts/profile-resolve` rechaza cualquier fuente bajo `references/`.

Cada elemento se clasifica como `pending-review`, `keep`, `adapt`, `remove` o
`reference-only`. Una idea aceptada se reimplementa en su capa canonica, se
prueba en canary y solo entonces puede promoverse. El material externo nunca es
una dependencia de runtime.

## Consequences

- La procedencia y las decisiones quedan trazables sin versionar repos ajenos.
- Las configuraciones activas mantienen una unica fuente propia y comprensible.
- Evaluar una fuente requiere documentacion inicial, pero reduce deuda futura.
- La ausencia de licencia explicita bloquea nuevas copias hasta aclarar origen o
  reimplementar la idea desde fuentes permitidas.
- Un dossier puede retirarse al terminar, pero atribuciones y licencias exigibles
  deben persistir junto al material derivado.

