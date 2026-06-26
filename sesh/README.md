# Sesh

Configuracion para [sesh](https://github.com/joshmedeski/sesh), selector de sesiones para tmux.

## Estado

Activo como selector de sesiones. La configuracion apunta a `~/mydotfiles` y no depende de rutas del repo original.

## Que aporta

- Entradas fijas para abrir carpetas frecuentes.
- Sesiones para probar herramientas ya activas: LazyGit, Yazi y Btop.
- Vista previa simple con `sed`, sin depender de `bat`.
- Puede integrarse con tmux mas adelante mediante `prefix + T`.

## Instalacion

```bash
brew install sesh tmux fzf
```

Dependencia opcional para descubrir carpetas frecuentes automaticamente:

```bash
brew install zoxide
```

## Activacion

```bash
ln -s ~/mydotfiles/sesh ~/.config/sesh
```

En esta maquina no habia una config previa en `~/.config/sesh`, asi que el enlace se puede crear directamente. La fuente de verdad queda en `~/mydotfiles/sesh`.

## Para que sirve

`sesh` es un selector de sesiones. La idea es tener una lista de lugares o tareas frecuentes y abrirlas rapido, normalmente dentro de tmux.

En vez de escribir cada vez:

```bash
cd ~/mydotfiles
lazygit
```

puedes elegir la sesion `git mydotfiles` desde `sesh`, y la herramienta entra a esa carpeta y ejecuta el comando configurado.

En esta config inicial hay sesiones para:

- `mydotfiles`: entrar al repo y ver estado Git.
- `git mydotfiles`: abrir LazyGit en el repo.
- `files mydotfiles`: abrir Yazi en el repo.
- `system monitor`: abrir Btop.
- Configuraciones frecuentes como AeroSpace, Kitty, Sketchybar, tmux y sesh.

Por ahora lo usamos como lanzador/selector simple. La integracion profunda con tmux, layouts y atajos queda para una etapa posterior.

## Uso inicial

Listar solo las sesiones de este archivo:

```bash
sesh list -c
```

Abrir el selector interactivo solo con sesiones configuradas:

```bash
sesh picker -c
```

Conectarse directamente a una sesion:

```bash
sesh connect "mydotfiles"
```

Sin flags, `sesh list` tambien intenta consultar [`zoxide`](../zoxide/README.md). Eso puede ser util mas adelante para descubrir carpetas frecuentes automaticamente, pero el primer flujo recomendado es usar `-c`.

## Pendiente

- Agregar proyectos reales tuyos.
- Decidir si las sesiones abren editor, shell simple o layouts de tmux.
- Integrarlo con `tmux/tmux.conf` cuando tmux pase a estar activo.
- Decidir si activamos zoxide en Zsh para usar `sesh` con carpetas aprendidas automaticamente.
