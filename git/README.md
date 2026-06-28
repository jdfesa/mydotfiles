# Git / GitHub identity

Notas para mantener una identidad de Git util sin exponer correos personales en commits futuros.

## Politica recomendada

- Usar un correo `noreply` de GitHub para commits publicos.
- No documentar correos personales ni institucionales dentro del repo.
- Mantener activado `Keep my email addresses private` en GitHub.
- Activar `Block command line pushes that expose my email` para evitar pushes accidentales con un correo privado.

## Configuracion en GitHub

En GitHub:

```text
Settings -> Emails
```

Verificar:

```text
Keep my email addresses private: On
Block command line pushes that expose my email: On
```

GitHub muestra un correo `noreply` con este formato:

```text
<id+usuario@users.noreply.github.com>
```

Ese es el correo que conviene usar en Git local.

### Por que activar el bloqueo si Git ya usa `noreply`

Son dos capas distintas:

- `git config --global user.email ...` define el camino normal: los commits futuros usan el correo `noreply`.
- `Block command line pushes that expose my email` es una red de seguridad de GitHub: si algun commit llega con un correo privado, GitHub bloquea el push antes de publicarlo.

El bloqueo no cambia commits buenos, no reescribe historial y no afecta pushes normales. Solo aparece cuando detecta un commit que expondria un correo marcado como privado en la cuenta de GitHub.

Casos en los que protege:

- un repo tiene un `user.email` local viejo que pisa el global;
- se usa otra maquina sin configurar;
- una herramienta crea commits con otra identidad;
- se cambia el correo temporalmente y queda olvidado;
- se clona o copia un repo antiguo con `.git/config` ya configurado.

## Bootstrap de Git en una maquina nueva

Esto se hace una vez despues de instalar Git por primera vez en macOS:

```bash
git config --global init.defaultBranch main
git config --global credential.helper osxkeychain
git config --global user.name "Jose David"
git config --global user.email "<id+usuario@users.noreply.github.com>"
```

Verificacion base:

```bash
git config --global --list
git config --global --get init.defaultBranch
git config --global --get credential.helper
git config --global --get user.name
git config --global --get user.email
```

Valores esperados:

```text
init.defaultBranch=main
credential.helper=osxkeychain
user.name=Jose David
user.email=<id+usuario@users.noreply.github.com>
```

Notas:

- `init.defaultBranch=main` evita que nuevos repos nazcan con `master`.
- `credential.helper=osxkeychain` guarda credenciales/tokens en el llavero de macOS.
- `user.email` debe usar el `noreply` de GitHub si el repo puede ser publico.
- La configuracion local de un repo puede pisar la global; verificar con `git config --show-origin --get-all user.email` si algo no cuadra.

## Configuracion local de Git

Global, para todos los repositorios:

```bash
git config --global user.name "Jose David"
git config --global user.email "<id+usuario@users.noreply.github.com>"
```

Solo para este repo:

```bash
git config user.name "Jose David"
git config user.email "<id+usuario@users.noreply.github.com>"
```

Verificar:

```bash
git config --global --get user.email
git config --get user.email
git log -1 --format='%an <%ae>'
```

## Commits antiguos

Cambiar `user.email` no reescribe commits anteriores. Los commits ya publicados conservan la metadata con la que fueron creados.

No reescribir historial salvo que haya una razon fuerte: cambia hashes, requiere force push y no elimina necesariamente copias, forks o caches. La prioridad es cortar la exposicion futura.
