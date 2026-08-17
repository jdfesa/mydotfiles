## 1. Approved Implementation Setup

- [x] 1.1 Confirmar approval explícito y que branch, `main` y `origin/main` comparten reviewed base; detenerse si difieren y no tocar checkout macOS.
- [x] 1.2 Reauditar fuentes primarias de OpenSpec, Chezmoi, Arch y Windows Terminal; registrar drift o no-drift.
- [x] 1.3 Crear layout human-owned, README, datos deterministas, mappings, semantics, expected manifests y prohibición de referencias desde perfiles productivos.
- [x] 1.4 Crear traceability de cada requirement/scenario hacia check, evidencia, native block o gate humano.

## 2. Containment Before Features

- [x] 2.1 Implementar raíz temporal, marker aleatorio, canonicalización, inventario protegido y descendant checks fail-closed antes de Chezmoi.
- [x] 2.2 Probar rechazo de `/`, home real, checkout, targets activos, parents, marker ausente, root reutilizado y symlink escape.
- [x] 2.3 Implementar HOME/XDG temporal y flags explícitos de source, destination, config, cache, state, temp, non-interactive, no-external, skip-secret y conflict-error.
- [x] 2.4 Verificar `chezmoi dump-config` y fake data efectivos contra el run manifest sin invocar `chezmoi data` redundantemente; rechazar `.chezmoi.homeDir` y ambiente host.
- [x] 2.5 Rechazar scripts/hooks/externals/removals/encryption, secret/runtime lookup, command execution, dynamic reads y missing-key downgrade.
- [x] 2.6 Resolver targets productivos read-only y validar duplicados más intersecciones lógicas/reales.
- [x] 2.7 Escanear fixtures sin filtrar secretos y validar type/mode POSIX, incluidos elevated/executable/world-writable.
- [x] 2.8 Completar review de containment antes del primer apply temporal.

## 3. Starship Literal Canary

- [x] 3.1 Agregar mapping Starship, literal byte-for-byte, hash drift y targets temporales por plataforma.
- [x] 3.2 Implementar state machine hash-bound para render, inventory, status, diff y dry-run de las tres fixtures.
- [x] 3.3 Exigir preview token de nonce/digest exacto antes del apply temporal.
- [x] 3.4 Probar dos runs limpios idénticos y segundo apply/dry-run no-op.
- [x] 3.5 Probar drift temporal, rollback exacto y metadata productiva sin cambios.
- [x] 3.6 Comparar Starship con profile-resolve/link bajo HOME temporal y registrar commands/safeguards/manifests/recovery.
- [x] 3.7 Completar review canary antes de fixtures data-driven/divergentes.

## 4. Git Data-Driven Case

- [x] 4.1 Agregar small template Git legible con `example.invalid`; aplicar guardrails numéricos solo como tripwires del piloto subordinados a semántica/legibilidad.
- [x] 4.2 Renderizar Git Linux/macOS/Windows preservando policy y variando helper explícito.
- [x] 4.3 Probar missing/unexpected/secret-like data, template complexity, permisos, diff, dry-run, idempotencia, drift y rollback.
- [x] 4.4 Comparar `configure-git` sin ejecutarlo ni atribuir ventaja automática a Chezmoi.

## 5. Kitty Shared Base and Platform Entrypoints

- [x] 5.1 Crear snapshots mapping-checked de base Kitty y entrypoints separados sin editar sources productivos.
- [x] 5.2 Reescribir únicamente includes staged para permanecer temporales y comparar hashes shared.
- [x] 5.3 Validar modifiers/clipboard/options Linux/macOS y límites X11/Wayland/session sin leakage.
- [x] 5.4 Ejecutar render, diff, dry-run, apply temporal, determinismo, idempotencia, drift, permisos y rollback Kitty.
- [x] 5.5 Rechazar template spaghetti que colapse entrypoints.

## 6. Windows Terminal and Semantic Keybindings

- [x] 6.1 Fijar fixture Windows Terminal contra documentación Microsoft y versión/schema revisados.
- [x] 6.2 Agregar fixture/target Windows Terminal separado sin target Kitty.
- [x] 6.3 Definir vocabulario que separe OS window, pane/Kitty window, spatial focus y previous-in-order, con statuses application-specific/unsupported cuando corresponda.
- [x] 6.4 Separar physical GUI/meta, application-primary y desktop/window-manager chords; preservar AeroSpace Hyper/Meh y reservar Windows key.
- [x] 6.5 Cross-renderizar Windows en Arch como structural-only y validar JSON/schema/target/line endings/syntax.
- [ ] 6.6 Ejecutar runner Windows nativo revisado para paths, behavior, determinismo, idempotencia, rollback y ACLs; mantener recommendation bloqueada sin esa evidencia.
- [x] 6.7 Confirmar cero commands/cambios macOS y limitar evidencia a auditoría del checkout más cross-render aislado.

## 7. Honest Comparison and Outcome Gates

- [x] 7.1 Recopilar métricas equivalentes de escalabilidad, complejidad total, safety, commands, files/adapters, state, drift, rollback, plataformas y documentación.
- [x] 7.2 Verificar thresholds obligatorios de writes/overlap/casos/runs/no-op/rollback/secrets/permisos/semantics/CI/doctor.
- [x] 7.3 Generar scorecard raw no ponderado y documentar unsupported/regressions sin favorecer Chezmoi.
- [x] 7.4 Derivar exactamente un outcome mediante selector explícito e invariantes, enumerando evidencia supporting/blocking.

## 8. Documentation, CI, and Doctors

- [x] 8.1 Generar matrix/scorecard deterministas con `DO NOT EDIT`, command, digest de proyección y paths normalizados.
- [x] 8.2 Agregar CI Linux para containment, fixtures, preview/apply temporal, proyección fresh, docs, determinismo, drift, permisos, rollback y cleanup.
- [x] 8.3 Mantener Windows CI visible pero disabled y bloquear recommendation mediante gate executable de native evidence.
- [x] 8.4 Agregar doctor read-only para versions, containment, features prohibidas, mapping drift, ownership, docs, modes/ACL y outcome.
- [x] 8.5 Ejecutar OpenSpec strict, validators, profile/link tests, doctors aislados, shell lint, generated-doc y pilot tests.

## 9. Review and No Production Cutover

- [x] 9.1 Auditar diff y probar Arch links/config, Kitty, Hyprland, Quattro, services, root-owned paths, real HOME y macOS sin cambios.
- [x] 9.2 Presentar artifacts, evidence, preguntas, failures, scorecard y outcome antes de Git publication.
- [x] 9.3 Documentar no-adoption y separar cualquier cleanup/adoption de packages sin reparar ni desvincular producción.
- [ ] 9.4 Si se recomienda selective migration, crear otra OpenSpec change para un canary literal; no convertir targets aquí.
- [x] 9.5 Completar publication aprobada: commits, push, PR `#14`, checks, rebase merge, branch cleanup y sincronización Arch; verificado después del merge en el follow-up autorizado.

## 10. Publication Audit Corrections

- [x] 10.1 Renombrar contenido JSON con extensión `.json` y actualizar todas las referencias sin agregar YAML dependency.
- [x] 10.2 Implementar proyección determinista completa, digest único y tests de timestamps versus command/hash/manifest/metric drift.
- [x] 10.3 Implementar selector `reject`/continuidad/recommendation, tests sintéticos e invariante Windows nativo.
- [x] 10.4 Corregir semantic vocabulary contra líneas Kitty y commands Windows Terminal exactos; agregar tests de false mapping/collision.
- [x] 10.5 Reemplazar ambiente heredado por allowlist mínima, usar private `--dev /dev` y probar prefix/no-secret inheritance.
- [x] 10.6 Derivar files/LOC/commands desde scopes y regenerar comparación sin totals manuales.
- [x] 10.7 Reemplazar traceability genérica por entries typed y validar cobertura uno-a-uno más IDs/pointers.
- [x] 10.8 Traducir toda prosa explicativa nueva a español profesional UTF-8 preservando headings/keywords técnicos.
- [x] 10.9 Fortalecer CI con path filters, smoke test Bubblewrap, OpenSpec/repository gates y blocker Windows honesto.
- [x] 10.10 Regenerar evidencia/docs estables y ejecutar validation completa para el controller audit aprobado.

## 11. Publication Lifecycle Determinism

- [x] 11.1 Excluir de la proyección los cuatro campos Git dinámicos de publicación y probar feature-to-main, reviewed base, HEAD y dirty sintéticos.
- [x] 11.2 Conservar Python exacto en evidencia raw, proyectarlo al contrato `>=3.11` y mantener Chezmoi/OpenSpec exactos con tests sensibles.
- [x] 11.3 Regenerar evidencia/docs, comparar dos proyecciones fresh y ejecutar validation completa para el controller audit final aprobado.

## 12. Host Bubblewrap CI Correction

- [x] 12.1 Reemplazar el container Arch anidado por `ubuntu-22.04` directo, tooling fijado, smoke-first, triggers sin duplicación y cero relajaciones de seguridad.
- [x] 12.2 Exigir la arquitectura mediante audit/tests, clasificar evidencia `portable-linux`, actualizar WHY/HOW y regenerar evidencia/documentación deterministas.

## 13. Portable OpenSpec Discovery Follow-up

- [x] 13.1 Implementar precedence `OPENSPEC_BIN`, `PATH` y fallback POSIX user-local sin paths absolutos de host ni candidato Windows no probado.
- [x] 13.2 Agregar focused tests para override, `PATH`, stripped-PATH POSIX fallback y diagnóstico missing sin filtración de secretos.
- [x] 13.3 Actualizar WHY/HOW y traceability, regenerar evidencia/docs y ejecutar la suite Arch no interactiva completa antes de publicar el follow-up.
