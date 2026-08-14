# Hosts

Esta carpeta registra maquinas fisicas concretas sin convertirlas en copias de
los dotfiles. Un host tiene identidad estable, inventario de hardware, nivel de
riesgo y perfiles seleccionados. La configuracion reutilizable continua en
`shared/`, `os/` y `profiles/`.

## Host Versus Profile

| Concepto | Responde | Ejemplo |
|---|---|---|
| Host | ¿Que maquina fisica es? | `lab-desktop-01` |
| Hostname | ¿Como se anuncia en la red? | `arch-desktop` |
| Profile | ¿Que capacidades se despliegan? | `arch-hyprland` |
| Layer | ¿Que fragmento reusable compone un perfil? | `layers/linux-hyprland-wayland` |

El CPU, la GPU o el sistema instalado pueden cambiar durante la vida de una
maquina. Por eso no forman parte del identificador estable del host ni originan
un perfil nuevo por cada combinacion.

## Manifest

Cada `hosts/<id>/host.toml` es un inventario declarativo y no contiene secretos.
Registra:

- identidad estable y hostname observado;
- plataforma actual y nivel de riesgo;
- perfiles aplicados actualmente y perfiles objetivo;
- hardware que cambia compatibilidad o recuperacion;
- fecha de la ultima verificacion.

Los scripts actuales no aplican automaticamente un host. Esta separacion es
deliberada: primero se elige y valida un perfil; el manifiesto documenta por que
esa eleccion es adecuada para el hardware.

## Overrides

No crear `hosts/<id>/overrides/` por anticipado. Solo se agrega un override si
una diferencia real no puede resolverse mediante deteccion, un valor portable o
una capa reusable. Ejemplos validos:

- orden explicito de GPU en una maquina multi-GPU;
- layout fijo de monitores de un escritorio permanente;
- seleccion de un dispositivo de audio con nombres estables;
- politica de energia propia de una laptop.

No son overrides validos: copias completas de Neovim, Zsh, Hyprland o listas de
paquetes. Un override debe ser pequeno, documentar su causa y tener una prueba o
procedimiento de validacion.

## Naming

Usar nombres fisicos estables y humanos, por ejemplo `lab-desktop-01` o
`main-workstation`. No usar `arch-i7-4790k`, porque mezcla sistema operativo,
hardware reemplazable e identidad.

No versionar seriales, UUID, direcciones MAC, credenciales ni claves. Una IP de
DHCP puede aparecer en notas operativas, pero nunca constituye la identidad del
host ni debe asumirse estable.
