# Profiles

Los perfiles describen capacidades instalables. No representan una maquina
fisica y no contienen copias de configuraciones. Una computadora concreta se
registra bajo `hosts/` y selecciona uno o mas perfiles compatibles.

## Manifest Syntax

Una entrada relaciona una fuente canonica con un destino:

```text
ruta/relativa/al/repo|$HOME/ruta/de/destino
```

Un perfil tambien puede incluir otro manifiesto:

```text
@include layers/shared-workstation
@include layers/linux-hyprland-wayland
```

El nombre del include es relativo a `profiles/` y omite `.links`.
`scripts/profile-resolve` genera un manifiesto plano y rechaza:

- includes ciclicos o inexistentes;
- fuentes ausentes o fuera del repositorio;
- destinos fuera de `$HOME`;
- dos fuentes distintas para el mismo destino.

Una misma relacion repetida por dos caminos se deduplica sin error.

## Layers And Installable Profiles

`profiles/layers/` contiene fragmentos reusables; no son hosts ni fuentes de
configuracion. Los perfiles superiores expresan roles completos:

| Perfil | Responsabilidad |
|---|---|
| `macos-main` | Contrato activo del Hackintosh de produccion |
| `arch-workstation` | Base Arch de usuario, sin elegir X11 o Wayland |
| `arch-dwm` | Base Arch más DWM y utilidades X11 |
| `arch-hyprland` | Base Arch más Hyprland y utilidades Wayland |
| `arch-hyprland-preview` | Subconjunto canary ya aplicado en el laboratorio |

`arch-desktop` es un alias de compatibilidad para el antiguo perfil DWM. El
hostname remoto puede seguir siendo `arch-desktop`, pero la automatizacion nueva
debe usar nombres funcionales.

## Commands

Resolver sin modificar el sistema:

```sh
scripts/profile-resolve arch-hyprland
scripts/validate-profiles
```

Diagnosticar un perfil aplicado:

```sh
scripts/doctor arch-hyprland-preview
```

Previsualizar antes de aplicar:

```sh
scripts/link --dry-run --repair arch-hyprland
```

El linker nunca reemplaza un archivo o directorio real. `--repair` solo cambia
symlinks incorrectos.

## Adding A Tool

1. Crear una unica fuente en `shared/<tool>/` u `os/<system>/<tool>/`.
2. Decidir que capacidad consume la herramienta.
3. Agregar el enlace a una capa existente solo si comparte su ciclo de vida;
   de lo contrario, crear una capa pequena y cohesiva.
4. Ejecutar `scripts/validate-profiles`.
5. Probar el perfil completo dentro de un `$HOME` temporal.
6. Aplicar primero en el host canary y promoverlo solo despues de validacion.

No agregar una herramienta a `macos-main` solamente porque existe en Arch ni
viceversa. La pertenencia depende de una necesidad real y probada.
