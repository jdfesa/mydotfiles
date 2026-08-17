## Purpose

Define un modelo cross-platform reviewable para contenido shared, datos por host,
entrypoints, Windows Terminal y keybindings semánticos sin ocultar diferencias
reales de OS, aplicación o sesión.

## ADDED Requirements

### Requirement: Shared and platform boundaries remain explicit

El piloto SHALL separar contenido portable de entrypoints por plataforma, host,
display protocol y desktop session. MUST NOT mover behavior X11 a Wayland,
Wayland a X11 ni behavior de sesión a un archivo universal.

#### Scenario: Content is byte-identical across platforms
- **WHEN** una configuración no necesita sustitución de plataforma, host, path, sesión o secreto
- **THEN** se modela como un literal shared y varias plataformas pueden apuntar al mismo contenido

#### Scenario: Session behavior differs
- **WHEN** un setting depende de X11, Wayland, window manager, compositor, shell o desktop session
- **THEN** permanece en un archivo platform/session nombrado aunque un template pudiera ocultarlo

### Requirement: Starship is the fully shared literal case

Starship MUST staging el `shared/starship/starship.toml` completo byte-for-byte,
renderizarlo como literal shared para las tres plataformas y probar hashes sin
branches.

#### Scenario: All Starship fixtures render
- **WHEN** fixtures Linux, macOS y Windows renderizan Starship
- **THEN** los tres outputs tienen hash idéntico y target documentado por plataforma

#### Scenario: Starship staging diverges
- **WHEN** el staged literal difiere un byte del canónico
- **THEN** provenance validation falla

### Requirement: Git uses shared policy with explicit fake data

Git SHALL renderizar policy compartida desde un small template con identidad y
credential helper públicos, deterministas y explícitos. MUST usar
`example.invalid`, no leer Git config/credentials host y dejar auth fuera.

#### Scenario: Platform credential helper changes
- **WHEN** se renderizan fixtures equivalentes Linux, macOS y Windows
- **THEN** policy compartida permanece igual y helper sigue el JSON explícito

#### Scenario: Host identity is omitted
- **WHEN** falta identidad fake obligatoria
- **THEN** rendering falla por missing key sin usar identidad del ejecutor

### Requirement: Kitty preserves shared base and platform entrypoints

Kitty MUST conservar `shared/kitty/common.conf`, incluidos bindings portables,
sessions y helpers, y MUST mantener entrypoints Linux/macOS separados con sus
`kitty_mod`, clipboard, chords y opciones nativas. No SHALL colapsarlos en un
template conditional ni inventar chords productivos.

#### Scenario: Linux Kitty is rendered
- **WHEN** se selecciona Linux
- **THEN** output contiene base shared, `kitty_mod super+alt`, clipboard Linux, `super+enter new_window` y `super+t new_tab_with_cwd`, sin opciones macOS

#### Scenario: macOS Kitty is simulated on Arch
- **WHEN** se selecciona macOS en el matrix aislado
- **THEN** output contiene misma base, `kitty_mod cmd+option`, opciones/chords macOS y no lee/escribe macOS activo

#### Scenario: Canonical Kitty behavior changes
- **WHEN** una línea action/chord canónica ya no coincide con `semantics.json`
- **THEN** semantic validation falla en lugar de aceptar una descripción genérica

### Requirement: Windows Terminal remains a separate application

Windows MUST usar un fixture/target Windows Terminal separado. Solo comparte un
vocabulario de intent con Kitty; no reutiliza syntax, paths ni assumptions Kitty.
El fixture conserva schema URL, packaged stable path, command format y referencia
estable `1.24.11321.0` auditados.

#### Scenario: Windows fixture is rendered
- **WHEN** se selecciona Windows
- **THEN** se produce settings JSON en el target aislado y ningún target Kitty

#### Scenario: Common action lacks Windows support
- **WHEN** una acción no puede representarse honestamente en el fixture revisado
- **THEN** mapping la marca unsupported con rationale sin inventar command/chord

### Requirement: Modifier roles have independent meanings

El contrato MUST distinguir physical GUI/meta key, application-primary
(`Command` macOS; `Ctrl` Linux/Windows) y chord/mode de desktop/window-manager
definido por sesión. Una key física no adquiere roles automáticamente. AeroSpace
MUST preservar Hyper (`cmd-alt-ctrl-shift`) y Meh (`alt-ctrl-shift`). Windows key
MUST quedar reservado salvo diseño Windows posterior revisado.

#### Scenario: Application command is mapped
- **WHEN** una action pertenece a la aplicación terminal
- **THEN** usa su convención native/application-specific documentada, no un chord universal forzado

#### Scenario: Session-defined desktop command is mapped
- **WHEN** una action pertenece a desktop, compositor, window manager u OS
- **THEN** usa chord/mode explícito por platform/session fuera de application-primary

#### Scenario: Current AeroSpace action is represented
- **WHEN** se documenta una action AeroSpace existente
- **THEN** conserva la línea Hyper o Meh canónica exacta

#### Scenario: Windows desktop chord is not designed
- **WHEN** una action exigiría chord de OS/desktop Windows
- **THEN** Windows key permanece reservado y la action se difiere/declara unsupported

#### Scenario: Physical key is remapped
- **WHEN** la misma posición física emite modifiers distintos en dos hosts
- **THEN** documentación registra posición y rol emitido por separado

### Requirement: Semantic actions reflect actual application behavior

El vocabulario MUST distinguir OS window, pane/Kitty window, navegación espacial
y navegación por orden. Cada platform mapping MUST declarar mapped,
application-specific, contextual, unsupported o deferred, además de native
action y source concreto. Chords similares no prueban equivalencia.

#### Scenario: Kitty creates a pane-like window
- **WHEN** el canonical entrypoint usa `new_window`
- **THEN** se mapea a `terminal.new-pane`, nunca a Windows Terminal `newWindow`

#### Scenario: Windows Terminal creates an OS window
- **WHEN** fixture usa command `newWindow`
- **THEN** se mapea a `terminal.new-os-window` y Kitty actual queda unsupported para ese intent

#### Scenario: Order and spatial focus differ
- **WHEN** Kitty usa `previous_window` y Windows Terminal usa `moveFocus:left`
- **THEN** se registran `terminal.previous-pane-in-order` y `terminal.focus-pane-left` separados

#### Scenario: Contextual Kitty navigation is represented
- **WHEN** `ctrl+h` usa `pass_keys.py`
- **THEN** mapping refleja pass-through Neovim o `neighboring_window(left)` y valida ambas líneas canónicas

#### Scenario: False native action mapping is introduced
- **WHEN** un semantic action declara un native action incompatible
- **THEN** focused validation falla

#### Scenario: Platform chord collides
- **WHEN** dos intents distintos reclaman el mismo chord en una plataforma
- **THEN** collision validation falla

### Requirement: Semantic mapping is complete but not falsely universal

Todo intent versionado MUST tener status para macOS, Linux y Windows, con cero o
más chords. Generated docs MUST mostrar status, native action, differences,
collisions y reserved chords.

#### Scenario: Platform mapping is complete
- **WHEN** se genera la matriz
- **THEN** cada action tiene tres statuses y sources concretos

#### Scenario: Literal chords differ
- **WHEN** dos aplicaciones implementan un intent compatible con chords distintos
- **THEN** validation pasa solo si cada native action preserva el intent declarado

### Requirement: File modeling prioritizes semantic boundaries

Un literal se usa para bytes idénticos sin datos. Un small template MAY usarse
para sustituciones escalares locales/deterministas más legibles que archivos
separados. Diferencia de significado, aplicación, formato o sesión MUST producir
archivos separados sin importar tamaño.

Para este piloto solamente, cinco scalar keys, un conditional no nested y diez
líneas divergentes son stop-and-review guardrails. No son policy productiva y no
prevalecen sobre semántica o legibilidad.

#### Scenario: Literal candidate contains substitution
- **WHEN** un supuesto literal necesita sustitución
- **THEN** se reclasifica como small template o archivo separado

#### Scenario: Pilot template crosses a review guardrail
- **WHEN** excede un límite local, usa nested conditionals, commands o dynamic reads
- **THEN** validation exige simplificar/separar sin universalizar el número

#### Scenario: Semantic divergence fits within the guardrails
- **WHEN** queda bajo los números pero mezcla aplicaciones, formatos o meanings
- **THEN** validation todavía exige archivos separados

#### Scenario: Pilot guardrail is proposed as repository policy
- **WHEN** una recomendación cita los números como regla productiva universal
- **THEN** human review rechaza el claim sin otra decisión/evidencia

#### Scenario: Different applications share an intent
- **WHEN** Kitty y Windows Terminal comparten intent pero difieren en syntax/behavior
- **THEN** permanecen archivos separados y mappings application-specific

### Requirement: Cross-platform simulation is labeled honestly

Arch SHALL cross-render fixtures estructurales sin afirmar runtime nativo. Una
recomendación MUST quedar bloqueada hasta Windows nativo para paths, schema,
line endings, idempotencia, rollback y ACLs. macOS nativo no se ejecuta sin otra
aprobación explícita.

#### Scenario: Arch matrix passes all fixtures
- **WHEN** pasan Linux, macOS y Windows en Arch
- **THEN** evidencia se etiqueta structural cross-rendering

#### Scenario: Native Windows evidence is unavailable
- **WHEN** no existe runner/host Windows revisado
- **THEN** outcome máximo es continuidad, nunca migration recommendation

#### Scenario: macOS remains audit-only
- **WHEN** se necesita evidencia macOS
- **THEN** usa canónicos y cross-render aislado con cero ejecución/configuración macOS
