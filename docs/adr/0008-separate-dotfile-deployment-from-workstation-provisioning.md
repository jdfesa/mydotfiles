# Separate Dotfile Deployment From Workstation Provisioning

Status: Accepted
Date: 2026-08-30

## Context

El repositorio comenzo administrando configuraciones de usuario mediante
symlinks, pero su objetivo ahora incluye reconstruir workstations macOS, Linux y
Windows. Ese alcance agrega paquetes, servicios, archivos privilegiados,
verificacion y gates manuales que no pertenecen naturalmente a un dotfile
manager.

Chezmoi fue evaluado para configuracion de usuario y permanece en
`keep-and-continue-evaluation`: no existe autorizacion de migracion ni evidencia
Windows nativa. Ansible aparece como candidato para provisioning, pero adoptarlo
sin limites claros duplicaria responsabilidades y aumentaria la complejidad.

## Decision

Separar explicitamente las responsabilidades:

- `scripts/link`, perfiles y symlinks continúan como owner productivo de la
  configuracion de usuario;
- Chezmoi sigue siendo un candidato no adoptado para esa misma capa;
- Ansible se evaluara solamente como posible capa superior para paquetes,
  servicios, archivos root-owned y orquestacion por sistema operativo o host;
- OpenSpec gobierna cambios relevantes, pero no despliega configuracion;
- dos herramientas nunca administraran el mismo target.

Cualquier piloto de Ansible debe ser aislado, comenzar en el canary
`lab-desktop-01`, reutilizar los manifests y checks existentes, demostrar
`check`/`diff`, una segunda ejecucion sin cambios y rollback. No autoriza cambios
en `main-workstation` ni una reescritura de los scripts actuales.

## Consequences

- El crecimiento del repositorio se organiza por lifecycle en lugar de buscar
  una herramienta unica para todo.
- Los symlinks siguen ofreciendo un camino simple y estable mientras se acumula
  evidencia real.
- Chezmoi y Ansible pueden estudiarse sin convertirlos en dependencias
  productivas ni sumar ownership ambiguo.
- Una futura adopcion debe probar que reduce trabajo repetido y complejidad; si
  solo agrega otra capa, se rechaza.
- Windows permanece planificado hasta contar con validacion nativa y una
  estrategia explicita de control y privilegios.
