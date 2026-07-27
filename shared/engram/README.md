# Engram

[Engram](https://github.com/Gentleman-Programming/engram) agrega memoria
persistente a agentes de programacion mediante un binario local, una base
SQLite y un servidor MCP por `stdio`.

## Por que esta instalado

RTK y Engram resuelven problemas diferentes:

- RTK compacta la salida de comandos antes de incorporarla al contexto;
- Engram conserva decisiones, descubrimientos y resúmenes entre sesiones;
- Engram puede evitar repetir contexto, pero tambien agrega instrucciones y
  llamadas MCP. No debe presentarse como un ahorro garantizado de tokens.

La integracion es global para Codex, mientras que las memorias se separan por
proyecto usando el repositorio o directorio actual. Si la deteccion es ambigua,
un proyecto puede declarar un nombre estable en `.engram/config.json`.

## Compatibilidad

Engram es una herramienta compartida y por eso su documentacion canonica vive
en `shared/engram/`, no dentro de una carpeta de un sistema operativo.

| Sistema | Soporte upstream | Estado en estos dotfiles | Instalacion preferida |
|---|---|---|---|
| macOS | Nativo, Intel y Apple Silicon | Verificado el 2026-07-26 con Engram 1.20.0 | Homebrew |
| Arch Linux | Nativo, x86_64 y ARM64 | Soportado, todavia no verificado en `arch-desktop` | Homebrew para Linux, `go install` o binario oficial |
| Windows | Nativo, x86_64 y ARM64 | Soportado, todavia no verificado en una maquina Windows | `go install` o binario oficial |

Comandos alternativos documentados por upstream:

```sh
# macOS o GNU/Linux con Homebrew
brew install gentleman-programming/tap/engram

# Cualquier plataforma con Go
go install github.com/Gentleman-Programming/engram/cmd/engram@latest
```

En Windows, `engram.exe` debe quedar en `PATH`. Upstream recomienda compilarlo
con `go install` para evitar falsos positivos que pueden afectar a binarios
precompilados sin firma.

## Integracion global con Codex

Despues de instalar el binario en cada maquina:

```sh
engram setup codex
```

El comando genera o actualiza estado administrado por Engram:

- macOS y GNU/Linux: `~/.codex/config.toml`,
  `~/.codex/engram-instructions.md` y
  `~/.codex/engram-compact-prompt.md`;
- Windows: `%APPDATA%\codex\` para la configuracion de Codex;
- todos los sistemas: una entrada MCP que ejecuta
  `engram mcp --tools=agent`;
- cuando Codex lo soporta, el marketplace y plugin `engram@engram`.

La ruta del binario se resuelve durante `engram setup codex` y puede cambiar
entre macOS Intel, Apple Silicon, GNU/Linux y Windows. Por eso la configuracion
generada no se copia entre sistemas ni se enlaza desde un perfil.

Es obligatorio cerrar y volver a abrir Codex despues del setup o de reemplazar
el binario. Una tarea que ya esta abierta no recarga MCPs, plugins ni
instrucciones globales.

## Estado local

La memoria local se guarda por defecto en:

```text
macOS y GNU/Linux: ~/.engram/engram.db
Windows:           %USERPROFILE%\.engram\engram.db
```

No se versionan:

- la base SQLite, sesiones, prompts u observaciones;
- los archivos generados bajo `~/.codex` o `%APPDATA%\codex`;
- caches y snapshots de marketplaces o plugins;
- exports de memoria;
- tokens, credenciales o configuracion de Engram Cloud.

La base debe tratarse como un archivo local sensible. No guardar secretos,
tokens, contraseñas, claves privadas ni contenido personal innecesario en las
memorias.

El modo local para Codex no necesita `engram serve`: Codex inicia un proceso MCP
por `stdio` al comenzar cada sesion. El servidor HTTP y Engram Cloud quedan
fuera de este setup hasta que exista una necesidad concreta.

## Verificacion

```sh
engram version
engram doctor
engram stats
codex plugin list
```

La configuracion global debe incluir:

```toml
model_instructions_file = "<ruta de engram-instructions.md>"
experimental_compact_prompt_file = "<ruta de engram-compact-prompt.md>"

[mcp_servers.engram]
command = "<ruta del binario engram>"
args = ["mcp", "--tools=agent"]
```

En la Mac donde se adopto inicialmente se verifico:

- Engram `1.20.0`;
- diagnostico con cuatro controles correctos y sin advertencias;
- base local creada en `~/.engram/engram.db`;
- MCP global registrado;
- plugin `engram@engram` instalado y habilitado;
- cero memorias iniciales, como corresponde a una instalacion nueva.

## Operacion y medicion

Engram instala un protocolo que pide guardar decisiones, fixes, configuraciones
y resúmenes de sesion. Esto mejora continuidad, pero aumenta el contexto global
y la cantidad de llamadas de herramienta.

Como linea base de la instalacion inicial, los dos archivos de protocolo
generados por Engram 1.20.0 sumaban 655 palabras y 4.239 bytes. Esta medida no
equivale directamente a tokens facturados: las instrucciones principales se
cargan globalmente y el prompt de compactacion se usa cuando Codex compacta una
sesion.

Evaluar su valor separadamente de `rtk gain`:

- cuantas veces evita reexplicar una decision;
- si recupera el proyecto correcto;
- si aparecen memorias obsoletas o irrelevantes;
- cuanto tiempo y ruido agregan las llamadas MCP;
- si la base sigue siendo util despues de varias semanas.

Las instrucciones actuales son administradas por Engram. No se editan ni
versionan hasta que exista evidencia de que hace falta un protocolo propio mas
breve.

## Actualizacion

En macOS:

```sh
brew update
brew upgrade engram
engram setup codex
```

Despues de actualizar o repetir el setup, reiniciar Codex y volver a ejecutar
las verificaciones. En Arch Linux y Windows se documentara el mecanismo de
actualizacion definitivo cuando la instalacion se pruebe en cada maquina.

## Referencias

- [Repositorio oficial](https://github.com/Gentleman-Programming/engram)
- [Instalacion multiplataforma](https://github.com/Gentleman-Programming/engram/blob/main/docs/INSTALLATION.md)
- [Integracion con agentes y Codex](https://github.com/Gentleman-Programming/engram/blob/main/docs/AGENT-SETUP.md)
