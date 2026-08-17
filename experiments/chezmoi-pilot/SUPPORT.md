# Support Matrix

## Matrix

| Host | Fixture | Status | Containment | Accepted evidence |
| --- | --- | --- | --- | --- |
| Linux | Linux, macOS, Windows | Implementado | Path guards + Bubblewrap private `/dev`/`proc`; sin network isolation | Aceptación Linux y cross-render estructural |
| macOS | macOS | Harness preparado, no ejecutado | Path guards; destino temporal | Requiere aprobación nativa separada |
| Windows | Windows | PowerShell adapter preparado, no ejecutado | Path guards y allowlist futura; destino temporal | Requiere runner revisado, behavior y ACLs |

## Boundaries

Python standard library contiene la lógica compartida. POSIX y PowerShell son
adapters finos. Bubblewrap es exclusivo de Linux y el harness falla si no puede
crear la contención estricta; no la degrada para CI. Cross-rendering Arch nunca
cuenta como aceptación nativa Windows o macOS.

## CI Limitation

El workflow usa un Arch container sobre GitHub-hosted Linux. El repositorio no
puede reproducir localmente el modelo exacto de namespaces de ese Docker host.
Un smoke test exige Bubblewrap con `/` read-only, private `/dev`/`proc` y temp
privado. Si Docker lo impide, el PR check debe fallar y el workflow deberá
corregirse sin reducir containment.
