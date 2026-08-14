# Main Workstation

La maquina fisica `main-workstation` es el Hackintosh de uso diario. Ejecuta
macOS y es el entorno de produccion para trabajo, universidad, notas y
presentaciones.

## Risk Policy

Una falla puede provocar uno o dos dias de reinstalacion y recuperacion. Por lo
tanto:

- no se aplican perfiles, reparan symlinks, instalan paquetes ni reinician
  servicios durante una refactorizacion del repositorio;
- una edicion de archivos versionados no autoriza a ejecutar `scripts/link`;
- cualquier cambio operativo requiere necesidad concreta, backup verificado,
  previsualizacion y aprobacion separada;
- las pruebas de Linux, Hyprland y plugins pertenecen al host canary
  `lab-desktop-01`;
- el perfil activo `macos-main` se conserva compatible hasta realizar una
  migracion explicitamente planificada.

## Current Contract

| Campo | Valor |
|---|---|
| Host estable | `main-workstation` |
| Hostname operativo | `Joses-Mac-Pro` |
| Plataforma | Hackintosh con macOS |
| CPU | Intel Core i7-14700K, informado por el usuario |
| GPU | AMD Radeon RX 580 8 GB |
| Memoria | 32 GiB |
| Perfil actual | `macos-main` |
| Nivel de riesgo | Produccion |

El manifiesto no incluye seriales, UUID ni otros identificadores sensibles.

## Future Linux Evaluation

Instalar Arch en esta maquina no se asume como destino automatico. Solo se
evaluara despues de meses de uso real en el laboratorio, recuperaciones
probadas y una ventana sin clases ni entregas. El host conservaria su identidad
`main-workstation`; cambiarian su plataforma, perfiles seleccionados e
inventario validado.
