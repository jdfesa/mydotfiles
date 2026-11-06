# Mydotfiles Working Guide

## Documentation and Naming

- Escribe el cuerpo de la documentación en español. Usa inglés para los títulos y subtítulos.
- Usa nombres de archivo en inglés. Como regla general, usa minúsculas y separa las palabras con guiones medios (`kebab-case`), por ejemplo `terminal-shortcuts.md`.
- Como excepción, los documentos convencionales de la raíz llevan el nombre base en mayúsculas y la extensión habitual en minúsculas: `AGENTS.md`, `README.md`, `TODO.md`, `CHANGELOG.md`, etc. Respeta también los nombres exactos que exijan las herramientas.
- Mantén el repositorio como referencia técnica, no como bitácora de conversaciones. Documenta qué hace el cambio, por qué se tomó la decisión y cómo reproducir o verificar el resultado. No incluyas transcripciones, anécdotas personales ni referencias a conversaciones privadas en la documentación, los commits o los PR.

## Cross-Machine Synchronization

- GitHub (`origin`) es la fuente de verdad para los cambios compartidos. `main` es la base común una vez integrados los cambios; una rama de trabajo no actualiza `main` por sí sola.
- Antes de editar o desplegar, identifica la máquina, el clon, la rama y su upstream. Revisa `git status --short --branch` y `git remote -v`; usa `git fetch origin` para actualizar las referencias y comprobar si la rama está adelantada, atrasada o divergió.
- Si la rama correcta tiene upstream, el árbol está limpio y la actualización puede avanzar sin merge, usa `git pull --ff-only` antes de empezar. Si hay cambios locales, commits sin publicar o divergencia, no los sobrescribas: explica el estado y acuerda cómo integrarlos. No uses `reset --hard`, `clean` ni force push para sincronizar.
- La **máquina A**, donde se hace el cambio, modifica y valida la fuente versionada, revisa el diff, hace commit de lo que corresponde y publica la rama acordada en GitHub. Si hace falta un PR, espera a su integración antes de actualizar otros clones desde `main`. Verifica que el commit publicado esté en la rama esperada.
- La **máquina B** trae el cambio desde GitHub en la rama correcta antes de continuar o desplegar. `fetch` solo actualiza referencias; para actualizar los archivos del clon hace falta integrar esos cambios, normalmente con `pull --ff-only`. No uses SSH para sincronizar archivos versionados ni des la sincronización por hecha si falla el push o el pull.

## Secrets and Recovery

- No guardes credenciales, claves privadas, tokens, datos personales ni estado privado de sesiones en Git. Mantén esos archivos fuera del clon cuando sea posible. Si deben vivir dentro del árbol de trabajo, agrégalos a `.gitignore` y comprueba antes de hacer commit que no estén versionados ni preparados para el commit. `.gitignore` no protege archivos ya rastreados ni borra el historial.
- Versiona en GitHub la configuración reproducible, las dependencias y los pasos de instalación y verificación por plataforma. Si hace falta un archivo privado, versiona solo una plantilla sin datos reales y documenta cómo obtener o recrear el archivo fuera de Git.
- El objetivo es recuperar el entorno base en pocos minutos desde un clon limpio, aunque no quede ninguna máquina anterior disponible. Para los secretos indispensables, usa un mecanismo de recuperación separado, como un gestor de secretos o una copia de seguridad cifrada, que no dependa de una sola máquina.
- Copiar por SSH entre máquinas es el último recurso, solo para archivos no versionados y cuando no exista otra vía segura. Limita la transferencia a lo imprescindible y no conviertas esa copia en un requisito del despliegue normal.

## Branches, Commits, and Pull Requests

- Para un cambio importante o que pueda afectar el funcionamiento de una o más máquinas, crea una rama de trabajo desde `main` sincronizada con `origin/main`. Haz el trabajo en esa rama, no directamente en `main`.
- Nombra la rama como `<type>/<description>`: empieza con un tipo de Conventional Commits (`feat`, `fix`, `chore`, `docs`, etc.) y usa una descripción breve en inglés y en `kebab-case`, por ejemplo `feat/terminal-workspaces` o `docs/recovery-guide`. No incluyas `codex` en el nombre de la rama. Escribe todos los mensajes de commit en inglés y en formato Conventional Commits, por ejemplo `feat(tmux): add terminal workspaces`.
- Haz push de la rama a `origin` y abre un pull request contra `main` después del primer push. Escribe el título, la descripción y el resto del texto del PR íntegramente en inglés. Describe de forma directa el cambio, su motivo técnico y cómo se verificó; no te refieras al titular del repositorio en tercera persona. Si el trabajo sigue en curso, abre el PR como borrador y publica los avances en la misma rama.
- Solo evalúa integrar el PR cuando se haya comprobado el comportamiento esperado en los sistemas afectados, hayan pasado las comprobaciones pertinentes y se haya aceptado el resultado. No integres automáticamente por el solo hecho de haber publicado la rama o de que CI esté en verde.
- Después de integrar, verifica que el PR figure como integrado en GitHub, que `main` contenga los cambios y que sigan funcionando desde `main` actualizada. Solo entonces elimina la rama de trabajo en el clon de la máquina donde se trabajó y en `origin`. Si hay commits pendientes de integrar o no se pudo verificar el resultado, conserva la rama.

## Configuration and Deployment

- Distingue entre la fuente del repo, el archivo instalado o enlazado y la configuración que está usando el proceso. Revisa los tres cuando corresponda; un `pull` no recarga una aplicación ni instala enlaces nuevos.
- Mantén la configuración común en `shared/` y las diferencias de Arch/Linux y macOS en `os/linux/` y `os/macos/`. Respeta los perfiles y las capas existentes. Comprueba las rutas, herramientas y atajos en el sistema afectado antes de aplicar un cambio compartido.
- En una auditoría, trabaja en solo lectura sobre las configuraciones activas. Para probar cambios de tmux o Kitty, prefiere una instancia aislada; no reinicies ni cierres aplicaciones o sesiones de trabajo como parte de una prueba. Si la configuración activa es un enlace al repo, ten en cuenta que actualizar el clon puede cambiar lo que se cargará en la próxima apertura o recarga.
- Si esta máquina tiene `$HOME/.codex/RTK.md`, respeta sus instrucciones para los comandos locales.
