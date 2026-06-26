# Yazi

Configuracion para [Yazi](https://yazi-rs.github.io/), un gestor de archivos en terminal.

## Estado

Importado como herramienta candidata. No esta activo hasta crear el symlink.

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

Si ya existe `~/.config/yazi`, respaldarlo antes.

## Pendiente

- Adaptar keymaps a tu flujo real.
- Evaluar si conviene integrarlo con Kitty/Ghostty o con scripts de proyectos.
