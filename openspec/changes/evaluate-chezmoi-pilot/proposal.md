## Why

El profile resolver y el linker conservador de symlinks son simples y seguros,
pero todavía no demuestran si los archivos renderizados, los datos por host o
una configuración nativa de Windows pueden administrarse con mayor claridad.
Antes de otorgar cualquier ownership productivo hace falta un piloto Chezmoi
aislado y guiado por evidencia que pruebe si la abstracción adicional se gana su
lugar.

## Strategic Context

La meta de largo plazo es que este único repositorio permita reconstruir una
estación personal útil en Linux, macOS o Windows mediante pocas acciones
documentadas. El flujo futuro debe separar prerrequisitos, adquisición del
checkout, configuración de usuario, paquetes y servicios, verificación y gates
manuales inevitables como autenticación, permisos, reinicios y secretos. La red
y la instalación de paquetes, no la orquestación, deben dominar el tiempo total.

Este cambio sigue siendo un piloto acotado. Solo evalúa si Chezmoi simplifica la
fase de configuración de usuario al crecer en herramientas, máquinas, sesiones y
plataformas. No afirma que Chezmoi sea el provisioner completo ni incorpora
paquetes, servicios, autenticación o estado mutable. La comparación prioriza, en
orden: escalabilidad; complejidad y carga cognitiva totales; mantenibilidad,
determinismo y ownership; recuperación segura tras reinstalar; y cambios
versionados con idempotencia, drift, rollback y documentación.

## What Changes

- Agregar un experimento Chezmoi no productivo que solo pueda renderizar y
  aplicar dentro de un destino temporal nuevo, nunca en un home real.
- Comparar Chezmoi honestamente con `scripts/link` más
  `scripts/profile-resolve`, preservando el deployment actual como productivo.
- Ejercitar cuatro modelos representativos: Starship completamente compartido;
  Git compartido con datos explícitos de host/plataforma; base Kitty compartida
  con entrypoints Linux/macOS separados; y Windows Terminal como implementación
  Windows separada bajo un contrato semántico común.
- Separar physical GUI/meta key, application-primary modifier y chords de
  desktop/window-manager definidos por sesión; preservar las familias Hyper/Meh
  actuales de AeroSpace y mantener Windows key reservado.
- Distinguir explícitamente una OS window, un pane/Kitty window, navegación
  espacial y navegación por orden; chords parecidos no prueban equivalencia.
- Definir cuándo el contenido es literal, usa un small template o se separa por
  plataforma, priorizando límites semánticos y legibilidad. Los límites
  numéricos conservadores son tripwires exclusivos del piloto.
- Especificar coexistencia canary-first, owner único, dry-run, diff,
  idempotencia, rollback, drift, secretos, permisos, factibilidad Windows,
  documentación generada, CI y evidencia doctor.
- Producir una proyección determinista completa de la evidencia y un scorecard
  con criterios medibles para `reject`, `keep-and-continue-evaluation` o
  `recommend-selective-migration`.
- Proporcionar un path de no-adoption que elimine el experimento sin modificar
  targets productivos.

### Scope

- Sources, fixtures, harnesses y documentación locales al repositorio e
  implementados únicamente para esta evaluación aprobada.
- Simulación con destino temporal en Arch para datos Linux, macOS y Windows;
  una recomendación de adoption exige evidencia Windows nativa separada.
- Comparación read-only con manifests de perfiles y sources canónicos actuales.

### Non-goals

- Aplicar Chezmoi al `$HOME` real del ejecutor, a otro home real o a un target de
  perfil activo.
- Convertir, desvincular, reemplazar o eliminar dotfiles o symlinks actuales.
- Cambiar configuración activa de macOS o Arch, servicios, paquetes no
  relacionados, manifests productivos, autenticación, Kitty, Hyprland, Quattro
  o archivos root-owned.
- Transferir a Chezmoi paquetes, servicios privilegiados, estado mutable,
  caches, sesiones de autenticación, inventario de hardware o provisioning.
- Tratar un piloto exitoso como autorización de cutover productivo.

### Exit Criteria

- **Reject Chezmoi** si escribe fuera de la raíz temporal marcada, permite
  ownership doble, filtra secretos, no puede restaurar rollback/idempotencia o
  representa Windows Terminal mediante equivalencias falsas.
- **Keep the current deployment and continue evaluation** si los controles
  críticos pasan, pero falta evidencia Windows nativa, queda incompleto un
  criterio obligatorio o no existe un beneficio claro de complejidad.
- **Recommend a later selective migration** únicamente si todos los thresholds
  obligatorios pasan, dos ejecuciones son deterministas, el segundo apply es
  no-op, el rollback restaura el baseline exacto, pasa Windows nativo y la
  política comparativa permite la recomendación. Aun así se requiere otro cambio
  target-by-target y aprobación explícita.

## Capabilities

### New Capabilities

- `chezmoi-pilot-safety`: ejecución temporal fail-closed, owner único,
  coexistencia, dry-run, rollback, drift, secretos, ambiente y permisos.
- `cross-platform-dotfile-model`: modelos representativos shared/data-driven,
  entrypoints por plataforma, Windows Terminal, semántica de teclas y
  clasificación file-versus-template.
- `chezmoi-pilot-evaluation`: comparación, outcome derivado, evidencia
  determinista, documentación, traceability, CI/doctor y no-adoption.

### Modified Capabilities

Ninguna. El repositorio no tenía capacidades behaviorales OpenSpec y este cambio
no modifica el contrato del linker productivo.

## Impact

- La implementación queda confinada a un experimento marcado, scripts de
  validación, evidencia reviewable, documentación generada y CI/doctor.
- Las dependencias locales de evaluación son Chezmoi `2.72.0-1`, OpenSpec
  `1.9.0`, Node.js/npm y Python. Su presencia no las incorpora a un manifest
  productivo.
- Perfiles, symlinks, dotfiles canónicos y estados macOS/Windows permanecen
  intactos hasta que otro cambio transfiera ownership de un target por vez.
