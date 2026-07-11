# Use Layered Dotfiles Organization

Status: Superseded by ADR 0005
Date: 2026-07-10

## Context

> Esta decision conserva el contexto historico. ADR 0005 mantiene las capas,
> pero agrupa las configuraciones compartidas bajo `shared/` para evitar que la
> raiz crezca sin limite.

Separar todo por sistema operativo desde la raiz parece ordenado al principio,
pero duplica configuraciones compartidas. Separar todo solo por herramienta
funciona bien en una maquina, pero se vuelve ambiguo cuando aparecen herramientas
exclusivas de macOS, Linux o Windows.

Tambien existiran diferencias entre maquinas concretas y perfiles de uso:

- macOS principal;
- Arch Linux con DWM;
- Arch Linux con i3;
- Windows nativo;
- VMs de prueba;
- maquinas con distinto usuario local o distinta ubicacion de archivos.

## Decision

Usar una arquitectura por capas:

```text
mydotfiles/
  <tool>/        # herramientas compartidas por defecto
  os/            # diferencias por sistema operativo
  hosts/         # diferencias por maquina concreta
  profiles/      # combinaciones instalables de herramientas
  scripts/       # bootstrap, linking e instalacion
  docs/          # arquitectura y decisiones
```

Las carpetas existentes por herramienta se mantienen como base. Las capas nuevas
se agregaran cuando exista contenido real para ellas.

## Consequences

La raiz del repositorio seguira siendo simple para herramientas compartidas.

Las configuraciones especificas tendran un lugar predecible:

- `os/macos/` para herramientas exclusivas de macOS;
- `os/linux/` para DWM, i3, X11, Wayland, Pacman o Yay;
- `os/windows/` para PowerShell, Windows Terminal o Winget;
- `hosts/<hostname>/` para diferencias de una maquina;
- `profiles/<profile>/` para declarar que piezas se activan juntas.

Esto permite experimentar con Arch Linux sin romper el setup actual de macOS y
sin crear repositorios separados.
