# Yazi

Configuracion para [Yazi](https://yazi-rs.github.io/), un gestor de archivos en terminal.

## Estado

Activo y enlazado desde `~/.config/yazi` hacia `~/mydotfiles/yazi`.

## Que aporta

- Muestra archivos ocultos por defecto.
- Atajos estilo Vim para crear, borrar y copiar.
- Tema Dracula incluido como flavor.

## Instalacion

```bash
brew install yazi
```

## Activacion

```bash
ln -s ~/mydotfiles/yazi ~/.config/yazi
```

En esta maquina no habia una config previa en `~/.config/yazi`, asi que el enlace se puede crear directamente. La fuente de verdad queda en `~/mydotfiles/yazi`.

## Keymaps iniciales

- `<Esc>`: salir de Yazi.
- `o`: crear archivo o carpeta.
- `dd`: enviar seleccion a la papelera.
- `yy`: copiar seleccion.

## Pendiente

- Adaptar keymaps a tu flujo real.
- Evaluar si conviene integrarlo con Kitty/Ghostty o con scripts de proyectos.
- Revisar previews avanzados en una terminal real; `yazi --debug` funciona, pero algunos adaptadores dependen del emulador y de utilidades opcionales.
