# Hyprland Theme Radar

Radar visual para una sesion de trabajo minimalista, coherente y predecible.
Estas fuentes se estudian como referencia: no autorizan ejecutar instaladores
externos ni convertir otro repositorio en dependencia de runtime.

## Criterios

Un tema candidato debe:

- cambiar primero colores, tipografia, espaciado y fondos, no comportamiento;
- reutilizar Hyprland, Waybar, Wofi, Mako, Hyprlock y Kitty ya instalados;
- evitar plugins binarios, shells adicionales y generadores en segundo plano;
- conservar contraste legible y estados visibles para foco, urgencia y error;
- poder retirarse restaurando un conjunto pequeno de archivos versionados;
- pasar el canary completo sin mezclar la prueba con la migracion a Lua.

## Shortlist

| Prioridad | Tema | Encaje | Riesgo | Decision inicial |
|---|---|---|---|---|
| 1 | Tokyo Night Storm | Ya es la base de Hyprland, Waybar, Wofi, Mako y Hyprlock | Bajo | Refinar la implementacion actual antes de sumar mecanismos nuevos |
| 2 | Kanagawa Wave | Oscuro, calido y sobrio; buena separacion sin aspecto neon | Bajo si es solo paleta | Primer candidato alternativo para el canary |
| 3 | Everforest Dark Medium | Descansado, organico y con acentos moderados | Bajo si es solo paleta | Segundo candidato, especialmente para sesiones largas |
| 4 | Catppuccin Mocha | Ecosistema amplio y colores muy consistentes entre aplicaciones | Medio: invita a tematizar demasiadas piezas | Usar una variante contenida, sin selector dinamico |
| 5 | Matte Black / Vantablack | Maximo minimalismo y poca distraccion | Medio por contraste y estados ambiguos | Solo prototipo con verificacion de accesibilidad |

La recomendacion actual es mantener **Tokyo Night Storm** como baseline,
prototipar **Kanagawa Wave** como primera alternativa y dejar **Everforest** en
tercer lugar. Esto permite comparar tres atmosferas sin cambiar el stack.

## Fuentes para estudiar

### Basecamp Omarchy

- Repositorio: <https://github.com/basecamp/omarchy>
- Temas: <https://github.com/basecamp/omarchy/tree/dev/themes>
- Arquitectura: <https://github.com/basecamp/omarchy/blob/quattro/docs/theming.md>
- Licencia declarada: MIT.

Es la referencia mas util para paletas coherentes y para el patron
`colors.toml -> templates -> staging -> activacion atomica`. Este repositorio ya
adapto selectivamente ideas de Omarchy; no debe ejecutar su instalador ni copiar
su administracion completa del sistema.

### nixer112/dotfiles

- Repositorio: <https://github.com/nixer112/dotfiles>

Referencia visual reciente de Kanagawa con Hyprland, Waybar y Wofi. Sirve para
comparar densidad, jerarquia y contraste. No se encontro una licencia explicita
durante esta revision, por lo que queda como `reference-only`: no copiar codigo,
scripts ni recursos.

### end-4/dots-hyprland

- Repositorio: <https://github.com/end-4/dots-hyprland>
- Licencia declarada: GPL-3.0.

Buen radar de interaccion y accesibilidad, pero su combinacion de Quickshell,
QML, Material colors y servicios auxiliares aumenta mucho la superficie de
fallo. Estudiar detalles aislados; no usarlo como base del escritorio diario.

### ML4W dotfiles

- Repositorio: <https://github.com/mylinuxforwork/dotfiles>
- Licencia declarada: GPL-3.0.

Util para observar canales estables, configuracion modular y temas adaptativos.
Es un entorno completo con instalador propio y cientos de integraciones; queda
fuera del nucleo minimalista.

### JaKooLit/Hyprland-Dots

- Repositorio: <https://github.com/JaKooLit/Hyprland-Dots>

Catalogo amplio de layouts de Waybar, Rofi y variantes de color. Su actualizacion
continua, scripts y selector dinamico lo hacen valioso para ideas, no para
instalar encima de una configuracion ya controlada.

### Catalogo visual Omarchy

- Lista: <https://github.com/Wheel-Smith/awesome-omarchy>

Sirve para descubrir paletas como Rose Pine, Nord, Gruvbox, Ristretto u Osaka
Jade. Los temas comunitarios no se consideran auditados por aparecer en la
lista; cada fuente necesita revision y licencia propias antes de adaptar algo.

## Arquitectura recomendada

El tema no debe poseer la sesion. La direccion preferida es:

```text
theme tokens
  -> Hyprland borders/background
  -> Waybar CSS
  -> Wofi CSS
  -> Mako colors
  -> Hyprlock colors
  -> Kitty palette
```

Los tokens se renderizaran fuera de la sesion o quedaran como archivos
versionados estaticos. No se introduce inicialmente Pywal, Wallust, Matugen,
Quickshell, EWW, AGS ni un daemon de cambio de wallpaper. Si mas adelante un
selector aporta valor real, se prueba como capa canary separada y con cambio
atomico; nunca reescribe archivos fuente en el lugar.

## Orden de trabajo

1. Migrar el compositor a Lua sin modificar la apariencia.
2. Extraer la paleta Tokyo Night actual a tokens propios.
3. Crear variantes estaticas Kanagawa y Everforest con la misma estructura.
4. Comparar contraste, densidad y consumo sin agregar dependencias.
5. Probar launcher, notificaciones, bloqueo, audio, red, tray, capturas,
   screen sharing, suspension/reanudacion y salida de sesion.
6. Promover solo el tema que conserve el comportamiento y el rollback simples.

No hay promocion por apariencia ni por cantidad de dias: deben cumplirse las
pruebas funcionales y el flujo definido en `docs/WORKSTATION_LIFECYCLE.md`.
