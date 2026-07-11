# Group Shared Configurations Under Shared

Status: Accepted
Date: 2026-07-10

## Context

ADR 0002 definio una arquitectura por capas, pero mantuvo cada herramienta
compartida directamente en la raiz. Con mas de treinta carpetas superiores y la
incorporacion de macOS, Arch Linux y Windows, esa regla ya no ofrece una
separacion visual suficiente.

Separar todo por sistema operativo tampoco es adecuado: duplicaria Neovim,
Kitty, Starship, Tmux, Yazi y otras herramientas compartidas.

Tambien hace falta distinguir configuraciones versionadas, integraciones de un
sistema, notas de una maquina y combinaciones instalables.

## Decision

Usar estas ubicaciones canonicas:

```text
shared/<tool>/                 # configuracion compartida
os/<system>/<tool>/            # configuracion exclusiva de un sistema
os/<system>/packages/          # manifiestos del gestor de paquetes
profiles/<profile>.links       # declaracion de symlinks
hardware/<device>/             # firmware y perifericos
scripts/                       # automatizacion del repositorio
docs/machines/<machine>.md     # notas operativas de una maquina
docs/                          # arquitectura, ADR e inventarios
```

Una herramienta compartida tiene una sola fuente bajo `shared/`. Las diferencias
pequenas se resuelven mediante includes, variables o archivos locales. Una
herramienta exclusiva se coloca bajo su sistema operativo.

DWM vive en `os/linux/dwm/`; AeroSpace vive en `os/macos/aerospace/`; Kitty vive
en `shared/kitty/` mientras siga compartiendo una base entre macOS y Linux.

Los nombres de carpetas, archivos tecnicos y titulos se escriben en ingles. El
contenido explicativo se escribe en espanol.

No se crea una capa `hosts/` por anticipado. La configuracion reutilizable vive
en `shared/` u `os/`, la seleccion instalable vive en `profiles/`, las notas de
una maquina viven en `docs/machines/` y los valores puramente locales quedan
fuera de Git. Una futura capa por maquina requerira un problema real y una nueva
decision.

La migracion se hace por grupos y solo despues de declarar los enlaces actuales
en un perfil verificable.

## Consequences

Ventajas:

- la raiz queda limitada a categorias estables;
- se evita duplicar configuraciones compartidas;
- cada nueva herramienta tiene un destino predecible;
- DWM puede crecer sin mezclarse con notas de un host;
- los perfiles desacoplan la ubicacion interna de los destinos del sistema;
- la estructura sigue siendo compatible con symlinks, Stow o Chezmoi.

Costos:

- los symlinks existentes deben repararse al mover cada carpeta;
- referencias internas a `~/mydotfiles/<tool>` deben actualizarse;
- los README historicos necesitan acompañar la migracion;
- cada movimiento estructural exige actualizar perfiles, rutas internas y
  documentacion en el mismo cambio.

Este ADR reemplaza ADR 0002 como definicion de la estructura canonica.
