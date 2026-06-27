# Direnv

`direnv` carga y descarga variables de entorno automaticamente al entrar y salir de una carpeta.

Su caso de uso principal es trabajar con proyectos que necesitan entorno propio sin ensuciar toda la terminal: claves locales, flags de desarrollo, versiones de herramientas, rutas temporales o variables como `DATABASE_URL`.

## Por que sirve

Sin `direnv`, cada proyecto suele requerir comandos manuales:

```bash
export NODE_ENV=development
export DATABASE_URL=postgres://localhost/app
export PATH="$PWD/bin:$PATH"
```

Con `direnv`, esas reglas viven en un archivo `.envrc` dentro del proyecto. Cuando entras a esa carpeta, `direnv` las carga. Cuando sales, las descarga.

## Instalacion

En una Mac nueva, instalar desde Homebrew:

```bash
brew install direnv
```

Tambien queda en la capa base:

```bash
brew bundle --file ~/mydotfiles/brew/00-base/Brewfile
```

## Activacion en Zsh

La activacion vive en:

```bash
~/mydotfiles/zsh/zshrc
```

El bloque esta protegido para no romper una Mac nueva donde `direnv` todavia no este instalado:

```bash
if command -v direnv >/dev/null 2>&1; then
  eval "$(direnv hook zsh)"
fi
```

Despues de instalar, abrir una terminal nueva o ejecutar:

```bash
source ~/.zshrc
```

## Uso diario

Dentro de un proyecto:

```bash
cd ~/code/mi-proyecto
touch .envrc
```

Ejemplo simple de `.envrc`:

```bash
export NODE_ENV=development
export PATH="$PWD/bin:$PATH"
```

La primera vez que `direnv` detecta un `.envrc`, lo bloquea por seguridad. Para aprobarlo:

```bash
direnv allow
```

Si cambias el `.envrc`, hay que aprobarlo otra vez:

```bash
direnv allow
```

Para ver que esta cargando:

```bash
direnv status
```

Para revocar la autorizacion de ese proyecto:

```bash
direnv deny
```

## Seguridad

`direnv` ejecuta el contenido de `.envrc`, por eso no debe aprobarse a ciegas.

Regla practica:

- En proyectos propios, revisar el `.envrc` y usar `direnv allow`.
- En proyectos descargados o de otra persona, leer el `.envrc` antes de aprobar.
- No subir secretos reales al repositorio. Usar `.envrc.example` para documentar variables necesarias.

## Que versionar

Normalmente se versiona:

```bash
.envrc.example
```

Normalmente no se versiona:

```bash
.envrc
```

Si el `.envrc` no contiene secretos y es parte real del flujo del equipo, puede versionarse. Si tiene tokens, claves o rutas privadas de la maquina, debe quedar fuera de Git.

## Validacion

```bash
command -v direnv
direnv version
type direnv
```

Para comprobar el hook de Zsh:

```bash
echo $DIRENV_DIR
```

Dentro de una carpeta autorizada con `.envrc`, esa variable deberia apuntar al proyecto activo.
