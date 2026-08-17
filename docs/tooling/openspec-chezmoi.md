# OpenSpec and Chezmoi Evaluation Toolchain

Status: Isolated pilot implemented; remote evaluation tooling only

## Scope

Este tooling remoto soporta el proof of concept Chezmoi aislado en el host Arch
recuperable. Implementar el piloto e instalar Chezmoi no lo seleccionan como
dotfile manager productivo. `scripts/link` y `scripts/profile-resolve` continúan
authoritative; ningún command de este documento aplica Chezmoi a un home real.

El controller macOS es audit-only. Su Codex, autenticación, configuración,
dotfiles, servicios y aplicaciones activas están fuera de este setup.

## Audited Versions

Estado verificado el 2026-08-16:

| Tool | Version | Provenance | Repository policy |
| --- | --- | --- | --- |
| Codex CLI | `0.147.0` | Instalación user-scoped existente en `$HOME/.local/bin/codex` | Solo auditoría; este setup no instala, actualiza, autentica ni reconfigura Codex. |
| Node.js | `26.7.0-1` (`v26.7.0`) | Package Arch oficial firmado `extra/nodejs` | Runtime remoto de evaluación; no adoptado por un manifest productivo. |
| npm | `12.0.2-1` | Package Arch oficial firmado `extra/npm` | Runtime remoto de evaluación; no adoptado por un manifest productivo. |
| Python | `3.14.7` | Runtime oficial del host Arch auditado | Evidencia raw exacta; compatibilidad ejecutable `>=3.11`. |
| Chezmoi | `2.72.0-1` (`v2.72.0`) | Package Arch oficial firmado `extra/chezmoi` | Candidato de evaluación; no adoptado por un manifest productivo. |
| OpenSpec | `1.9.0` | Package npm oficial `@fission-ai/openspec` y release upstream firmado `v1.9.0` | El command de instalación fija exactamente la versión. |

## Implementation Re-audit

La fase apply volvió a comprobar fuentes primarias y host antes de crear el
experimento. No hubo drift. Windows Terminal permanece fijado como referencia
estructural `1.24.11321.0`, schema
`https://aka.ms/terminal-profiles-schema`, packaged stable path y formato
`command`. Las pruebas no descargan el alias mutable del schema: validan el
subconjunto local y mantienen native acceptance bloqueada.

Arch es rolling. Se registran versiones exactas de la transacción auditada,
provenance y commands reproducibles para el host remoto; no se convierten
Node.js, npm o Chezmoi en dependencias permanentes de workstation-base. Una
decisión posterior debe adoptar o remover entries explícitamente. Reinstalar usa
repositories Arch firmados actuales y full upgrade soportado; no fuerza packages
cacheados ni partial upgrades para repetir strings históricas.

`review.json` registra el runtime Python y el banner Chezmoi completos para
auditoría. Como el soporte
declarado y el gate `doctor` son Python `>=3.11`, la proyección determinista
normaliza cualquier patch compatible a ese contrato; un runtime incompatible no
queda oculto. Arch y el binario upstream agregan metadata de build distinta, por
lo que la proyección normaliza solo ese banner y exige Chezmoi semántico exacto
`2.72.0`. OpenSpec permanece exactamente `1.9.0`; cualquier drift de versión
exige revisión.

## Installation and Verification

Instalar packages Arch oficiales únicamente mediante el privileged gate
revisado:

```sh
sudo pacman -S --needed nodejs npm chezmoi
```

Instalar OpenSpec sin `sudo`, user-scoped y pinned:

```sh
npm install --global --prefix "$HOME/.local" @fission-ai/openspec@1.9.0
```

Verificar:

```sh
pacman -Q nodejs npm chezmoi
node --version
npm --version
python3 --version
chezmoi --version
openspec --version
npm list --global --prefix "$HOME/.local" --depth=0 @fission-ai/openspec
```

La policy npm bloqueó el `postinstall` opcional de OpenSpec. El script auditado
solo imprime un hint opt-in de shell completion; CLI e integración funcionan sin
él. No se debilita la policy para mostrar ese hint.

## Codex Integration

Inicializar únicamente la integración core soportada desde repository root:

```sh
openspec init --tools codex --profile core --no-animation
```

OpenSpec `1.9.0` usa integración Codex skills-only. La inicialización auditada
solo administra `.agents/skills/.openspec-target` y directorios
`.agents/skills/openspec-*`; no genera `.codex` ni reemplaza `.agents` ajeno.

Inventory generado:

- `.agents/skills/.openspec-target` (`codex`);
- `.agents/skills/openspec-apply-change/SKILL.md`;
- `.agents/skills/openspec-archive-change/SKILL.md`;
- `.agents/skills/openspec-explore/SKILL.md`;
- `.agents/skills/openspec-propose/SKILL.md`;
- `.agents/skills/openspec-sync-specs/SKILL.md`;
- `.agents/skills/openspec-update-change/SKILL.md`;
- `openspec/config.yaml`.

Los seis skills declaran `generatedBy: "1.9.0"`, mode `0644` y coincidieron
byte-for-byte con una inicialización aislada. `openspec update` puede reemplazar
contenido managed y exige version bump revisado; no se usa como upgrade shortcut
unpinned.

## CI Runtime

CI usa directamente el VM GitHub-hosted fijado `ubuntu-22.04`; no usa un job
container. `apt-get` instala Bubblewrap, certificados, curl, Git y ShellCheck
desde Ubuntu antes del sandbox. `actions/setup-python@v6` selecciona el contrato
Python `3.11` y `actions/setup-node@v6` fija Node.js `26.7.0`; npm se fija en
`12.0.2` y OpenSpec en `1.9.0` bajo `$HOME/.local`.

Chezmoi se descarga desde el release oficial `v2.72.0` como
`chezmoi-linux-amd64` y se verifica antes de instalar con:

```text
ba563f716d5c00a2e91d4aeb199b417c6b219db2896f890fd422fc72610b2d90
```

El primer PR check probó que el anterior container Arch bloqueaba el user
namespace antes de Bubblewrap. Ejecutar sobre el VM directo elimina esa capa y
reduce complejidad, pero no relaja el boundary del piloto: siguen prohibidos
privileged mode, capabilities, bypass de seccomp/AppArmor, sysctl, skip y
fallback fuera del harness. Esta ejecución es evidencia Linux portable; native
Arch continúa verificándose en la workstation real y native Windows permanece
bloqueado.

## Primary Sources

- OpenSpec `v1.9.0`: https://github.com/Fission-AI/OpenSpec/releases/tag/v1.9.0
- OpenSpec Codex integration: https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
- Arch Node.js: https://archlinux.org/packages/extra/x86_64/nodejs/
- Arch npm: https://archlinux.org/packages/extra/any/npm/
- Arch Chezmoi: https://archlinux.org/packages/extra/x86_64/chezmoi/
- Chezmoi global flags: https://www.chezmoi.io/reference/command-line-flags/global/
- Chezmoi source-state attributes: https://www.chezmoi.io/reference/source-state-attributes/
- Kitty actions: https://sw.kovidgoyal.net/kitty/actions/
- Kitty mapping: https://sw.kovidgoyal.net/kitty/mapping/
- Kitty configuration: https://sw.kovidgoyal.net/kitty/conf/
- Windows Terminal stable `1.24.11321.0`: https://github.com/microsoft/terminal/releases/tag/v1.24.11321.0
- Windows Terminal actions: https://learn.microsoft.com/en-us/windows/terminal/customize-settings/actions
- Windows Terminal settings/schema: https://learn.microsoft.com/en-us/windows/terminal/faq
- Chezmoi `v2.72.0`: https://github.com/twpayne/chezmoi/releases/tag/v2.72.0
- GitHub-hosted runners: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- Ubuntu Bubblewrap: https://packages.ubuntu.com/jammy/bubblewrap
