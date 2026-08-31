## Purpose

Define un owner reproducible de sesiones terminales Arch que sobreviva
desconexiones, funcione correctamente sobre SSH y sea suficientemente simple de
restaurar y depurar sin descargar plugins durante runtime.

## ADDED Requirements

### Requirement: Official core tmux only
El perfil Arch SHALL obtener tmux desde los repositorios oficiales y SHALL iniciar
con funcionalidad core. El startup MUST NOT descargar ni ejecutar TPM, Sesh,
tmux-resurrect, plugins o código remoto.

#### Scenario: Rebuild from a clean Arch package state
- **WHEN** el rol terminal Arch se converge desde repositorios sincronizados
- **THEN** tmux se instala mediante el package oficial declarado
- **AND** la primera sesión funciona sin Cargo, Go, AUR, Git clone ni network fetch

#### Scenario: Start without optional integrations
- **WHEN** TPM, Sesh y plugins no existen en el host
- **THEN** la configuración carga sin warning, error ni keybinding roto

### Requirement: Explicit Arch profile ownership
La configuración tmux SHALL desplegarse en `$XDG_CONFIG_HOME/tmux/tmux.conf`
mediante una capa Arch explícita. Shell, terminal emulator y otro multiplexor MUST
NOT obtener ownership implícito ni autoarrancar tmux.

#### Scenario: Apply the tmux layer
- **WHEN** el operador enlaza la capa tmux seleccionada
- **THEN** profile resolution, dry-run, link y doctor identifican un único target
  XDG administrado
- **AND** ningún perfil macOS o Windows cambia

#### Scenario: Open a normal terminal
- **WHEN** el operador inicia Kitty, Ghostty, Zsh o una shell no interactiva sin
  invocar el launcher tmux
- **THEN** obtiene la shell normal fuera de cualquier multiplexer

### Requirement: Correct terminal capability boundary
Dentro de tmux, `TERM` SHALL ser `tmux-256color` cuando su terminfo esté disponible,
con fallback documentado y verificado; MUST NOT heredar el `TERM` exterior. Features
adicionales SHALL anunciarse solo para patrones de terminal probados y
`allow-passthrough` MUST permanecer desactivado salvo evidencia y aprobación
posteriores.

#### Scenario: Load from Kitty
- **WHEN** un servidor aislado carga la configuración desde Kitty
- **THEN** el `TERM` interior es tmux-derived y resoluble por `infocmp`
- **AND** true color, undercurl, Unicode y resize pasan los checks declarados

#### Scenario: Load from Ghostty
- **WHEN** un servidor aislado carga la configuración desde Ghostty
- **THEN** solo las capabilities verificadas para su patrón TERM son agregadas
- **AND** no existe un wildcard que declare RGB para terminales desconocidos

#### Scenario: Remote host lacks tmux terminfo
- **WHEN** una conexión SSH llega a un host sin `tmux-256color`
- **THEN** el runbook detecta el problema antes de abrir aplicaciones TUI
- **AND** ofrece el fallback compatible revisado sin sobrescribir terminfo remoto

### Requirement: Disconnect-safe session behavior
tmux SHALL conservar procesos mientras su servidor continúe vivo y SHALL permitir
detach/reattach después de cerrar una terminal o perder SSH. La documentación MUST
distinguir esto de reboot, crash y reconstrucción de workspaces.

#### Scenario: Recover from forced SSH disconnect
- **WHEN** una conexión SSH termina de forma abrupta con un proceso activo en tmux
- **THEN** el proceso continúa en el host
- **AND** un reattach posterior recupera la sesión y su output

#### Scenario: Reboot the host
- **WHEN** el host reinicia
- **THEN** la documentación y el verificador no afirman que procesos anteriores
  siguen vivos
- **AND** el operador puede reconstruir el workspace declarado sin session cache

### Requirement: Declarative safe workspace reconstruction
Workspaces versionados SHALL declarar sesiones, ventanas, panes y working
directories mediante operaciones idempotentes. Comandos con efectos laterales
MUST NOT reejecutarse automáticamente al restaurar un workspace.

#### Scenario: Open the same workspace twice
- **WHEN** el launcher declarativo se ejecuta dos veces para el mismo workspace
- **THEN** la segunda ejecución se conecta al estado existente sin duplicar
  sesiones, ventanas ni procesos administrados

#### Scenario: Workspace path is absent
- **WHEN** un workspace referencia un directorio inexistente
- **THEN** el launcher falla antes de crear una sesión parcial
- **AND** muestra el path portable que debe corregirse

### Requirement: TUI, input and clipboard compatibility
El rollout SHALL validar Kitty y Ghostty con Zsh, Neovim, FZF, Yazi y LazyGit. Los
keybindings MUST evitar colisiones conocidas, clipboard MUST usar el mínimo acceso
necesario y el sistema MUST NOT guardar scrollback o contenido potencialmente
sensible en Git.

#### Scenario: Use core terminal applications
- **WHEN** el operador navega, selecciona, copia, pega, redimensiona y usa mouse en
  cada TUI declarada
- **THEN** input, focus, Unicode y redraw funcionan sin secuencias perdidas
- **AND** existe una salida documentada ante una colisión

#### Scenario: Copy through OSC52
- **WHEN** el operador copia desde tmux local o remoto en un terminal compatible
- **THEN** el clipboard recibe el texto mediante la policy explícita
- **AND** aplicaciones internas no obtienen lectura o passthrough innecesarios

### Requirement: Nested SSH operation without network listeners
El sistema SHALL soportar tmux local → SSH → tmux remoto, actualización segura de
agent socket cuando corresponda y prefix forwarding documentado. tmux MUST NOT
abrir listeners de red adicionales.

#### Scenario: Control a remote nested session
- **WHEN** el operador conecta desde un tmux local a un host con tmux remoto
- **THEN** puede enviar el prefix interior, detach y reattach sin terminar la
  sesión exterior

#### Scenario: Reattach with SSH agent forwarding
- **WHEN** una sesión usa agent forwarding y el socket cambia al reconectar
- **THEN** el mecanismo documentado actualiza el ambiente necesario sin versionar
  ni imprimir el socket como evidencia pública

### Requirement: Canary evidence before promotion
La capa SHALL pasar pruebas funcionales, mediciones runtime y al menos siete días
de uso canary antes de considerarse estable. Package size MUST NOT presentarse como
medición de RAM o CPU.

#### Scenario: Measure idle runtime
- **WHEN** se ejecuta el escenario revisado de cuatro panes idle
- **THEN** la evidencia registra startup, PSS de server/client y CPU durante 60
  segundos
- **AND** identifica terminal, tmux version, kernel y método de medición

#### Scenario: Detect instability during canary
- **WHEN** aparece pérdida de input, clipboard, sesión, memory growth o regresión
  SSH reproducible
- **THEN** la promoción se bloquea y el incidente se registra con rollback o
  criterio para un challenger

### Requirement: Safe and explicit rollback
Retirar tmux SHALL preservar trabajo visible, desactivar solo su profile layer y
devolver el terminal a una shell normal. Rollback MUST NOT eliminar sessions,
scrollback o package state silenciosamente.

#### Scenario: Roll back the profile layer
- **WHEN** el operador solicita rollback después de revisar sesiones activas
- **THEN** el plan muestra el target XDG que dejará de administrarse
- **AND** nuevas terminales abren Zsh normal sin modificar otros perfiles

### Requirement: Mutually exclusive Zellij challenger
Zellij MUST permanecer fuera del perfil productivo. Un challenger opcional SHALL
usar package oficial, profile/launcher separado, ningún plugin externo y un periodo
máximo de 14 días con los mismos checks, iniciado fuera de tmux.

#### Scenario: Start a fair challenger
- **WHEN** tmux falla un gate documentado y se aprueba evaluar Zellij
- **THEN** tmux auto-start permanece desactivado y solo una capa challenger está
  seleccionada
- **AND** web server y sharing de Zellij permanecen desactivados

#### Scenario: Challenger result is a tie
- **WHEN** Zellij no demuestra una mejora diaria medible y supera los mismos gates
  solo en igualdad
- **THEN** tmux conserva ownership productivo y la capa challenger se retira
