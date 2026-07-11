# Gh Dash

`gh-dash` es una interfaz terminal para trabajar con GitHub desde el teclado: pull requests, issues, reviews pendientes y notificaciones.

Esta carpeta guarda la configuracion versionada de `gh-dash` para que el flujo sea reproducible en otra Mac.

## Para que sirve

Sirve para convertir GitHub en un tablero diario dentro de la terminal:

- Ver PRs abiertos creados por ti.
- Ver PRs donde te pidieron review.
- Ver PRs o issues donde estas involucrado.
- Revisar notificaciones separadas por no leidas, menciones, reviews, asignaciones y participacion.
- Saltar al repo local con un atajo y abrir LazyGit.

## Instalacion

`gh-dash` se instala como extension del GitHub CLI:

```bash
gh extension install dlvhdr/gh-dash
```

Requiere tener GitHub CLI autenticado:

```bash
gh auth login
```

### Autenticacion paso a paso

Cuando ejecutes:

```bash
gh auth login
```

Usar estas opciones para esta Mac:

```text
Where do you use GitHub? GitHub.com
What is your preferred protocol for Git operations on this host? SSH
Upload your SSH public key to your GitHub account? /Users/jd/.ssh/id_ed25519.pub
```

La clave que se sube es la publica (`.pub`). Nunca subir ni compartir la clave privada:

```bash
~/.ssh/id_ed25519
```

Si GitHub CLI pide un nombre para la clave, usar algo reconocible:

```text
MacBook jd 2026
```

En el login por navegador, `gh` muestra un codigo de un solo uso en la terminal, parecido a:

```text
First copy your one-time code: XXXX-XXXX
Press Enter to open github.com/login/device
```

Ese `XXXX-XXXX` es el codigo que hay que escribir en la pagina de GitHub que dice `Authorize your device`.

Importante: ese codigo no aparece necesariamente en la app movil. En este flujo, el codigo lo genera la terminal. La app movil o app autenticadora puede aparecer despues solamente si GitHub pide 2FA.

Para validar que quedo bien:

```bash
gh auth status
```

Un estado correcto debe verse parecido a esto:

```text
github.com
  ✓ Logged in to github.com account jdfesa (keyring)
  - Active account: true
  - Git operations protocol: ssh
  - Token: gho_************************************
  - Token scopes: 'admin:public_key', 'gist', 'read:org', 'repo'
```

Lo importante es que aparezca `Logged in`, que el protocolo sea `ssh` y que no aparezca `token invalid`.

Si aparece `token invalid`, repetir el login para GitHub.com:

```bash
gh auth login -h github.com
```

Si queda una sesion rota y hace falta empezar de cero:

```bash
gh auth logout -h github.com -u jdfesa
gh auth login -h github.com
```

Para validar:

```bash
gh dash --version
gh dash --help
```

## Activacion

La fuente de verdad es:

```bash
~/mydotfiles/shared/gh-dash/config.yml
```

El archivo que lee `gh-dash` por defecto en macOS debe apuntar a esa fuente:

```bash
mkdir -p ~/.config/gh-dash
ln -s ~/mydotfiles/shared/gh-dash/config.yml ~/.config/gh-dash/config.yml
```

Si ya existe `~/.config/gh-dash/config.yml`, respaldarlo antes de crear el enlace.

## Uso diario

Abrir el dashboard:

```bash
gh dash
```

Dentro de la interfaz:

- `?`: mostrar ayuda contextual.
- `q`: salir.
- `/`: buscar dentro de la vista actual.
- `g`: abrir LazyGit en el repo local, si ese repo esta mapeado en `repoPaths`.

## Secciones configuradas

Pull Requests:

- `My Pull Requests`: PRs abiertos creados por ti.
- `Needs My Review`: PRs donde te pidieron review.
- `Involved`: PRs donde participas pero no eres autor.

Issues:

- `My Issues`: issues abiertas creadas por ti.
- `Assigned`: issues asignadas a ti.
- `Involved`: issues donde participas pero no eres autor.

Notifications:

- `Unread`: notificaciones no leidas.
- `Review Requested`: solicitudes de review.
- `Mentioned`: menciones directas.
- `Participating`: conversaciones donde participas.
- `Assigned`: asignaciones.
- `All`: vista completa.

## Repos locales

El atajo `g` usa `{{.RepoPath}}`, por eso `gh-dash` necesita saber donde vive cada repo local.

La configuracion inicial incluye:

```yaml
repoPaths:
  jdfesa/mydotfiles: ~/mydotfiles
```

Cuando agregues mas repos, se pueden mapear asi:

```yaml
repoPaths:
  jdfesa/mydotfiles: ~/mydotfiles
  jdfesa/otro-repo: ~/code/otro-repo
```

Tambien se pueden usar patrones:

```yaml
repoPaths:
  jdfesa/*: ~/code/*
```

## Que se adapto del repo externo

La configuracion de `~/Downloads/dotfiles-master 2` tenia buenas secciones para PRs, issues y notificaciones. Se conservaron esas ideas, pero se quitaron atajos que dependian de herramientas no activadas todavia, como `tmux`, `wt` y un flujo especifico de `opencode`.

Primero dejamos una base limpia para el trabajo diario con GitHub. Las acciones avanzadas de code review pueden agregarse despues, cuando `tmux` este integrado y sepamos exactamente como quieres revisar PRs.

## Fuentes

- https://github.com/dlvhdr/gh-dash
- https://www.gh-dash.dev/getting-started
- https://www.gh-dash.dev/getting-started/usage/
- https://www.gh-dash.dev/configuration/
