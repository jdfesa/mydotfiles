# RTK

[RTK (Rust Token Killer)](https://github.com/rtk-ai/rtk) es un proxy local para
comandos de terminal. Filtra y compacta salidas ruidosas antes de que lleguen al
contexto de un asistente de programacion.

## Por que esta instalado

Los tests, linters, builds, diffs y logs pueden incorporar miles de lineas poco
utiles a una sesion de Codex. RTK conserva la informacion relevante y reduce el
ruido, ayudando a aprovechar mejor la ventana de contexto. No agrega memoria,
no amplia cuotas y no modifica la autenticacion de Codex.

Es especialmente util en proyectos con Vitest, ESLint, TypeScript, Git, Docker
o suites de pruebas extensas. Cuando se necesita un formato exacto o el resumen
no alcanza, se usa el comando original o el log completo guardado localmente.

## Instalacion y configuracion

En macOS, el paquete pertenece a la capa de desarrollo de Homebrew:

```sh
brew bundle --file ~/mydotfiles/os/macos/packages/homebrew/10-essential/Brewfile
```

Inicializar la integracion global con Codex y mantener deshabilitada la
telemetria propia de RTK:

```sh
rtk telemetry disable
rtk init --global --codex
```

La integracion indica a Codex que prefiera comandos como `rtk git status`,
`rtk vitest` o `rtk eslint src/`. Todo se ejecuta localmente y la salida
compactada vuelve a la misma tarea de Codex.

## Verificacion

```sh
rtk --version
rtk telemetry status
rtk gain
rtk discover
```

`rtk gain` muestra el ahorro registrado y `rtk discover` identifica comandos
ruidosos que no pasaron por RTK.

## Estado local no versionado

Este repositorio documenta la decision y la instalacion, pero no administra el
estado generado por RTK:

- `~/.codex/RTK.md` y su referencia en `~/.codex/AGENTS.md` son generados por
  `rtk init`;
- la base de estadisticas, los logs completos, caches y marcadores permanecen
  locales;
- ninguna credencial, cookie o sesion de Codex pertenece a esta configuracion.

Estos archivos no se enlazan desde un perfil porque son estado administrado por
la herramienta y pueden cambiar entre versiones. Si en el futuro se adopta una
configuracion propia estable, su fuente canonica vivira en esta carpeta.

## Desinstalacion

```sh
rtk init --global --codex --uninstall
brew uninstall rtk
```
