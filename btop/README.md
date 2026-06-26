# Btop

Configuracion para [btop](https://github.com/aristocratos/btop), monitor de sistema en terminal.

## Estado

Importado como candidato listo para probar. No esta enlazado al sistema todavia.

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

Si ya existe `~/.config/btop`, respaldarlo antes.

## Notas

`show_cpu_watts = true` puede no mostrar datos en todos los equipos. Si molesta o genera warnings, se puede desactivar en `btop.conf`.
