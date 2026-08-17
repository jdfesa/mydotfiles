# Support Matrix

## Matrix

| Host | Fixture | Status | Containment | Accepted evidence |
| --- | --- | --- | --- | --- |
| Arch real | Linux, macOS, Windows | Implementado y auditado | Path guards + Bubblewrap private `/dev`/`proc`; sin network namespace | Doctor/profile/symlinks Arch más cross-render estructural |
| Ubuntu 22.04 CI | Linux, macOS, Windows | Implementado como `portable-linux` | Host directo + Bubblewrap estricto; sin job container | Evidencia Linux portable, no native Arch/Windows |
| macOS | macOS | Harness preparado, no ejecutado | Path guards; destino temporal | Requiere aprobación nativa separada |
| Windows | Windows | PowerShell adapter preparado, no ejecutado | Path guards y allowlist futura; destino temporal | Requiere runner revisado, behavior y ACLs |

## Boundaries

Python standard library contiene la lógica compartida. POSIX y PowerShell son
adapters finos. Bubblewrap es exclusivo de Linux y el harness falla si no puede
crear la contención estricta; no la degrada para CI. El piloto prohíbe toda
operación de red mediante externals/hooks/refresh, pero la evidencia común no
afirma un network namespace. Cross-rendering nunca cuenta como aceptación nativa
Windows o macOS.

## CI Model

El workflow usa directamente el VM GitHub-hosted `ubuntu-22.04`; elimina el
container Arch anidado que bloqueó el user namespace y no agrega excepciones de
seguridad. Instala tooling antes del sandbox, ejecuta primero un smoke test con
`/` read-only y private `/dev`/`proc`, y después corre la matriz solo mediante el
harness estricto. Si el VM no puede crear Bubblewrap, el check falla sin skip ni
fallback. Esta prueba es Linux portable; la aceptación Arch permanece en el
doctor real de la workstation.
