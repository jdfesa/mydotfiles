# Separate Hosts From Profiles

Status: Accepted
Date: 2026-08-13

## Context

El nombre `arch-desktop` llego a representar tres cosas distintas: el hostname
de la maquina i7-4790K, un manifiesto de symlinks y la idea generica de una
estacion Arch. Esa ambiguedad no escala cuando otra maquina, por ejemplo la
estacion principal i7-14700K, pueda usar Arch con diferente GPU, audio y
monitores.

Crear un perfil por cada combinacion de CPU, GPU, sistema y compositor produce
una matriz interminable. Copiar configuraciones completas por maquina tambien
hace divergir herramientas portables.

ADR 0005 habia postergado una capa `hosts/` hasta que existiera un problema
real. La segunda maquina y la diferencia de riesgo entre produccion y
laboratorio satisfacen ahora ese criterio.

## Decision

Separar cuatro responsabilidades:

```text
shared/                    # fuentes portables por herramienta
os/                        # integraciones de plataforma, protocolo y sesion
profiles/                  # combinaciones instalables por rol
hosts/                     # inventario y seleccion de una maquina fisica
```

Un **perfil** describe una capacidad reusable, como `arch-workstation`,
`arch-dwm` o `arch-hyprland`. No incluye CPU ni hostname en su nombre.

Un **host** representa una maquina fisica con identificador estable, como
`lab-desktop-01` o `main-workstation`. Su manifiesto registra hardware, riesgo,
plataforma y perfiles seleccionados sin guardar secretos.

Los perfiles pueden incluir fragmentos de `profiles/layers/` mediante:

```text
@include layers/shared-workstation
@include layers/linux-hyprland-wayland
```

El resolver detecta includes ciclicos, fuentes ausentes y dos fuentes que
intenten ocupar el mismo destino. Las capas no sustituyen a `shared/` u `os/`:
solo componen enlaces hacia esas fuentes canonicas.

Los nombres anteriores permanecen temporalmente como aliases compatibles. En
particular, `arch-desktop.links` resuelve al perfil funcional `arch-dwm`, pero
la automatizacion nueva debe usar nombres por rol.

## Consequences

Ventajas:

- una segunda maquina reutiliza perfiles sin fingir que tiene el mismo
  hardware;
- agregar una herramienta portable modifica una capa compartida, no cada host;
- X11, Wayland, DWM y Hyprland conservan limites explicitos;
- el hardware queda documentado sin contaminar configuraciones portables;
- las diferencias de produccion y laboratorio son visibles.

Costos:

- los perfiles pasan a tener una etapa de resolucion;
- los inventarios deben mantenerse cuando cambia hardware;
- un override de host requiere justificar por que la deteccion portable no
  alcanza;
- los aliases antiguos deben retirarse solo despues de migrar y validar el host
  correspondiente.

Esta decision reemplaza solamente la postergacion de `hosts/` en ADR 0005; el
resto de ADR 0005 continua vigente.
