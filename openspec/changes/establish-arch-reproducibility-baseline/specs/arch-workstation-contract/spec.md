## Purpose

Define un estado deseado Arch componible, portable y con ownership único para que
una máquina nueva pueda planificarse sin depender de memoria, shell history ni
suposiciones heredadas del hardware canary.

## ADDED Requirements

### Requirement: Versioned Arch role graph
El sistema SHALL representar cada rol Arch mediante un schema versionado que
relacione paquetes, configuración de usuario, servicios, archivos privilegiados,
dependencias de runtime, verificadores y gates manuales. Cada target administrado
MUST tener un único owner y cada referencia MUST resolver a una declaración
existente.

#### Scenario: Resolve a complete workstation role
- **WHEN** el operador selecciona un host y un rol Arch válido
- **THEN** el sistema produce un grafo cerrado con todos sus componentes y owners
- **AND** no consulta manifests ni perfiles de otra plataforma

#### Scenario: Reject overlapping ownership
- **WHEN** dos componentes declaran ownership sobre el mismo paquete, target,
  servicio o archivo sin una regla explícita de deduplicación idéntica
- **THEN** la resolución falla antes de producir un plan aplicable
- **AND** identifica ambos owners en el diagnóstico

#### Scenario: Reject an unresolved dependency
- **WHEN** una configuración desplegada requiere un comando, paquete, servicio o
  archivo que ningún componente seleccionado proporciona
- **THEN** la resolución falla con la dependencia y el consumidor concretos

### Requirement: Separate detected facts from declared policy
El contrato SHALL distinguir identidad estable del host, facts detectados,
capacidades requeridas y policy seleccionada. Los facts observados MUST NOT
reescribir automáticamente el manifest versionado.

#### Scenario: Qualify supported hardware
- **WHEN** la detección identifica arquitectura, CPU vendor, GPU, storage class y
  tipo desktop/laptop sin ambigüedad
- **THEN** el plan selecciona únicamente los componentes compatibles declarados
- **AND** muestra los facts que justifican cada selector de hardware

#### Scenario: Stop on unknown hardware
- **WHEN** un selector destructivo o privilegiado depende de hardware ausente,
  desconocido o ambiguo
- **THEN** el sistema se detiene antes de solicitar privilegios o cambiar estado
- **AND** emite una acción de calificación manual, no un default inventado

#### Scenario: Keep host-specific values narrow
- **WHEN** una diferencia puede resolverse mediante detección o una capacidad
  reusable
- **THEN** el sistema MUST NOT exigir una copia completa o un override de host

### Requirement: Supported Arch package transactions
Todo cambio de paquetes oficiales SHALL operar sobre bases sincronizadas mediante
una actualización completa `pacman -Syu`; el sistema MUST NOT ejecutar una
instalación parcial después de refrescar bases. Paquetes AUR o payloads externos
MUST conservar procedencia, revisión y verificación explícitas.

#### Scenario: Plan official package convergence
- **WHEN** faltan paquetes oficiales seleccionados
- **THEN** el plan contiene una única transacción de actualización completa con
  las instalaciones necesarias
- **AND** no contiene `pacman -Sy` ni `pacman -S` contra bases refrescadas

#### Scenario: Detect package drift without destructive cleanup
- **WHEN** el host tiene paquetes explícitos no declarados o falta un paquete
  deseado
- **THEN** el reporte diferencia `missing`, `unexpected` y `version-drift`
- **AND** no elimina ni hace downgrade automáticamente

#### Scenario: Validate reviewed external package
- **WHEN** un rol selecciona un paquete AUR o payload externo
- **THEN** el contrato exige versión, source revision, digest y razón revisados
- **AND** falla si cualquiera de esos datos está ausente o no coincide

### Requirement: Portable user-configuration paths
La configuración de usuario SHALL funcionar desde la raíz del checkout actual y
MUST declarar sus dependencias transitivas. Un target de perfil MUST permanecer
léxica y físicamente debajo del home seleccionado.

#### Scenario: Use a non-conventional checkout
- **WHEN** el repositorio se clona fuera de `~/mydotfiles`
- **THEN** los includes y comandos administrados resuelven mediante destinos XDG,
  symlinks o paths derivados explícitamente
- **AND** el doctor estricto no encuentra referencias runtime al clon convencional

#### Scenario: Reject target traversal
- **WHEN** un manifest usa segmentos `..`, `.`, separadores ambiguos o un ancestor
  symlink que resuelve fuera del home seleccionado
- **THEN** la resolución falla antes de crear o reparar cualquier enlace

### Requirement: Explicit privileged and manual boundaries
El contrato SHALL enumerar archivos root-owned, servicios y gates manuales como
clases distintas. Secretos, autenticación, datos personales y estado mutable MUST
permanecer fuera de Git y MUST tener un mecanismo de restauración y verificación
que no revele su contenido.

#### Scenario: Describe a privileged target
- **WHEN** un rol requiere un archivo o servicio privilegiado
- **THEN** la declaración incluye source, target, owner, group, mode, desired
  enablement y verificador
- **AND** el baseline read-only solo informa la diferencia

#### Scenario: Reach a manual authentication gate
- **WHEN** una fase depende de SSH, GitHub, Bitwarden u otra autenticación
- **THEN** el plan se detiene en un gate nombrado con instrucciones y check seguro
- **AND** no imprime, genera ni versiona la credencial

### Requirement: Explicit lifecycle checkpoints
El lifecycle SHALL separar instalación mínima, adquisición del source, estado de
usuario, estado privilegiado, verificación, reboot y gates manuales. Cada fase MUST
declarar precondiciones, resultado verificable y criterio de resume.

#### Scenario: Resume after interruption
- **WHEN** una ejecución se interrumpe después de completar una fase
- **THEN** la siguiente planificación reconoce el estado convergido
- **AND** retoma desde el primer resultado incompleto sin repetir efectos laterales

