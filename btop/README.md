# Btop

Configuracion para [btop](https://github.com/aristocratos/btop), monitor de sistema en terminal.

## Estado

Activo y enlazado desde `~/.config/btop` hacia `~/mydotfiles/btop`.

## Que aporta

- Tema personalizado en `themes/btop-theme.theme`.
- Navegacion con teclas Vim.
- Vista de CPU, memoria, red y procesos.
- Configuracion orientada a terminales con TrueColor.

## Instalacion

```bash
brew install btop
```

## Activacion

```bash
ln -s ~/mydotfiles/btop ~/.config/btop
```

En esta maquina la carpeta previa quedo respaldada en `~/.config/btop.bak-before-mydotfiles`. La fuente de verdad queda en `~/mydotfiles/btop`.

## Notas

`show_cpu_watts = false` queda desactivado para evitar warnings o permisos extra en macOS. Se puede activar mas adelante si el equipo lo soporta bien.
