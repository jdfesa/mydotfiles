# Repository Tasks

Tareas concretas de mantenimiento del repositorio. Las prioridades generales
viven en [ROADMAP.md](ROADMAP.md); las reglas de trabajo, en
[AGENTS.md](AGENTS.md). Este archivo no sustituye los procedimientos técnicos ni
los ADR.

## Status Rules

- `[ ]` indica trabajo pendiente o una decisión todavía sin cerrar; `[x]`
  indica que existe el resultado descrito y su evidencia enlazada.
- Una casilla describe el contenido de la revisión consultada. La integración
  en `main` la confirma el PR; un despliegue real necesita evidencia propia.
- Cada tarea debe tener alcance, motivo y criterio de cierre. Las decisiones
  pendientes no autorizan por sí solas cambios de configuración.
- No registrar como tareas compartidas archivos temporales locales, residuos
  ignorados o supuestos faltantes sin verificarlos en la fuente actual.

## Documentation

- [ ] **Normalizar los README de herramientas.**
  - Alcance inicial: [Ghostty](shared/ghostty/README.md),
    [Btop](shared/btop/README.md), [Fastfetch](shared/fastfetch/README.md) y
    [VS Code](shared/vscode/README.md). Los cuatro ya existen; no hay que
    crearlos de nuevo.
  - Motivo: hay cuerpos en inglés, títulos en español y contenido que describe
    pruebas o estados locales en lugar de un contrato técnico reproducible.
  - Cierre: cuerpo en español, títulos en inglés y explicación de fuente,
    destinos por perfil, dependencias y verificación; sin referencias privadas.

- [ ] **Alinear los ejemplos de activación con el flujo de perfiles.**
  - Alcance inicial: [Btop](shared/btop/README.md) y
    [Fastfetch](shared/fastfetch/README.md), que aún muestran enlaces manuales.
  - Motivo: el mecanismo compartido de despliegue ya resuelve fuentes,
    conflictos y destinos; los ejemplos no deben omitir esas protecciones.
  - Cierre: enlazar el procedimiento de perfiles, previsualización y diagnóstico;
    comprobar las rutas contra los manifiestos sin aplicar cambios en `$HOME`.

- [ ] **Precisar el alcance validado de la recuperación macOS.**
  - Alcance: [Restore macOS](docs/RESTORE.md), el
    [README de Homebrew](os/macos/packages/homebrew/README.md) y los
    [inventarios](docs/inventory/README.md).
  - Motivo: existen manifiestos por capas, pero su propia documentación indica
    que contienen una base importada pendiente de curado.
  - Cierre documental: distinguir dependencias necesarias, opcionales y
    referencias históricas; identificar qué validaciones de recuperación tienen
    evidencia y cuáles siguen pendientes. Curar paquetes o ejecutar una
    restauración se aborda en un cambio separado.

## Decisions Required

Las siguientes revisiones no forman parte de una limpieza automática ni del
mantenimiento exclusivamente documental.

- [ ] **Definir el rollback de VS Code antes de retirar el respaldo.**
  - Evidencia: [README de VS Code](shared/vscode/README.md#rollback) utiliza
    `settings.json.bak` como procedimiento de recuperación.
  - Cierre: decidir si se conserva o se sustituye por recuperación desde una
    revisión de Git; actualizar y verificar las instrucciones antes de eliminarlo.

- [ ] **Revisar la cobertura de archivos locales en Git.**
  - Evidencia: [.gitignore](.gitignore) limita `.venv` y `__pycache__` al teclado
    Silakka54; no tiene patrones generales para respaldos o temporales del editor.
  - Cierre: acordar patrones y excepciones, comprobarlos con `git check-ignore`
    y revisar los archivos ya rastreados. Ignorar un archivo no lo retira de Git.

- [ ] **Evaluar si conviene un hook local exclusivamente de validación.**
  - Evidencia: [CI](.github/workflows/lint.yml) ya ejecuta `lint-shell` y
    `validate-profiles`; el [test del renderizador](hardware/silakka54/test_render.py)
    exige actualmente que no exista `.githooks/pre-commit`.
  - Cierre: decidir si aporta valor frente a la validación manual y CI. Si se
    adopta, resolver dependencias, alcance sobre índice o árbol de trabajo,
    instalación reproducible y compatibilidad del test, sin generar artefactos
    ni hacer staging durante el commit.

- [ ] **Evaluar la redundancia de posición de la barra de tmux.**
  - Evidencia: [la base compartida](shared/tmux/tmux.conf) establece primero
    `bottom` y después `top`; las capas [macOS](os/macos/tmux/tmux.conf) y
    [Linux](os/linux/tmux/tmux.conf) fijan `bottom` al final.
  - Cierre: decidir si se conserva la base upstream intacta, como documenta
    [Tmux](shared/tmux/README.md), o si se justifica modificarla. Cualquier cambio
    debe conservar el resultado por plataforma y probarse en instancias aisladas.

## Completed Foundations

- [x] **Explicitar la sincronización antes de cualquier trabajo en cada máquina.**
  Evidencia: [Cross-Machine Synchronization](AGENTS.md#cross-machine-synchronization)
  distingue `fetch`, actualización de archivos, protección del trabajo local y
  despliegue.
- [x] **Reconciliar el roadmap con las fuentes y perfiles actuales.**
  Evidencia: [Established Capabilities](ROADMAP.md#established-capabilities)
  reconoce Lazygit, Yazi, Btop, tmux, Brewfiles y la ruta `shared/nvim/`, sin
  presentarlos como instalaciones futuras ni garantizar despliegue universal.
- [x] **Separar prioridades y tareas verificables.**
  Evidencia: [Documentation Maintenance](AGENTS.md#documentation-maintenance)
  define el papel de este archivo, del roadmap y de las guías canónicas.
