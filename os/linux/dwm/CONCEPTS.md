# DWM Concepts

Esta guia explica el modelo mental de la configuracion. Las decisiones exactas
de teclas viven en `KEYBINDINGS.md`.

## Qué es DWM

DWM es el window manager de X11: recibe eventos, decide foco y geometria, dibuja
bordes y organiza ventanas. No es un entorno de escritorio completo. La sesion
agrega deliberadamente piezas independientes:

- DWM administra ventanas;
- ST proporciona terminal;
- dmenu lanza comandos;
- DWMBlocks genera el estado;
- picom compone sombras y transparencias;
- feh establece wallpapers cuando se habilita.

Esta separacion explica su bajo consumo y tambien por qué algunas comodidades
de un escritorio tradicional deben elegirse y configurarse explicitamente.

## Configurar significa compilar

En DWM, la configuracion principal es código C. `config.def.h` se incorpora a
la build; no existe un daemon que recargue un archivo TOML. La contrapartida de
ese costo es control directo y pocas capas de abstraccion.

En estos dotfiles la build ocurre en cache, se prueba en Xephyr y se instala con
respaldo. La disciplina alrededor de DWM es parte del producto, no un detalle.

## Tags en lugar de escritorios

Un escritorio tradicional suele ser exclusivo: se esta en el workspace 1 o en
el 2. Un tag de DWM es una etiqueta binaria:

- una ventana puede tener uno o varios tags;
- se puede visualizar uno o varios tags al mismo tiempo;
- los tags vacios se ocultan en esta build;
- `sticky` permite que una ventana siga visible al cambiar de seleccion.

Los numeros actuales son nombres, no una obligación. Mas adelante pueden
renombrarse o enlazarse a letras del Silakka54 si la experiencia real demuestra
que mejora el flujo.

## Master, stack y layouts

El layout tiled divide el monitor en dos zonas:

- master: la tarea principal;
- stack: las tareas secundarias.

`zoom` intercambia una ventana con master. `focusstack` recorre el orden y
`pushstack` lo modifica. Monocle muestra una ventana a la vez; spiral y dwindle
distribuyen ventanas de forma recursiva. Floating permite geometria manual.

DWM no intenta representar cada direccion como un arbol, a diferencia de
AeroSpace. Su modelo natural es master + pila + tags.

## Keyboard-first, no keyboard-only

La configuracion optimiza acciones frecuentes para teclado, pero conserva
movimiento, resize, tags y gaps con mouse. El objetivo no es evitar el mouse por
ideologia, sino no depender de él cuando un atajo sea mas rapido y comodo.

El Silakka54 cambia la ergonomia del acorde: Super, Hyper y Meh son acciones de
pulgar, no combinaciones de cuatro dedos. Aun asi, DWM compara modificadores de
forma exacta. Hyper no puede reemplazar directamente a Super sin hacer colapsar
las familias `Super`, `Super+Shift`, `Super+Ctrl` y `Super+Alt`.

## Qué sugiere la configuracion importada

Es razonable inferir, sin afirmar intenciones que no conocemos, que su autor
priorizaba:

- permanecer en teclado y terminal;
- lanzar herramientas especializadas con una tecla;
- controlar cada parte de la barra y cada gap;
- usar Neovim, Termusic, dmenu y un navegador modal;
- aceptar mantenimiento técnico a cambio de control.

Una configuracion madura para otra persona no es automaticamente adecuada para
este equipo. Sus parches son capacidades; sus atajos y programas son opiniones.

## DWM y AeroSpace

AeroSpace administra ventanas dentro de las restricciones de macOS y ofrece
configuracion TOML, modos y un arbol direccional. DWM es el administrador real
de X11 y ofrece control mas directo, tags combinables y una superficie mínima.

No existe un ganador absoluto. El objetivo es compartir principios utiles:

- Super permanece como base convencional y ergonomica en DWM;
- Hyper puede representar navegar o mirar;
- Meh puede representar mover o actuar;
- las equivalencias se agregan gradualmente, no reemplazando todo de una vez.

## Navegador modal como experimento

`Super+w` apunta a qutebrowser, que no esta instalado. Qutebrowser encaja con la
filosofia keyboard-first y ofrece bloqueo de red y modo oscuro integrados. Su
bloqueador no realiza filtrado cosmético, y su alternativa compatible con
Dark Reader mediante Greasemonkey esta descrita upstream como poco probada.

Para este entorno, uBlock Origin y Dark Reader representan capacidades
importantes. No se descartan extensiones ni navegadores por no ser minimalistas:
la herramienta debe adaptarse al usuario. Qutebrowser se evaluara como
experimento, no como reemplazo obligatorio. Si sus alternativas nativas no
alcanzan el mismo resultado práctico, el navegador principal sera uno que
admita ambas extensiones y qutebrowser podra conservarse como opcion modal.

También deben probarse compatibilidad de sitios, DRM, perfiles, videollamadas,
gestores de contrasenas y cualquier flujo web crítico antes de adoptarlo.

En la auditoria del 2026-07-17, `qutebrowser` y su backend opcional
`python-adblock` estaban disponibles en el repositorio oficial `extra` de Arch.
El experimento no requiere AUR y puede hacerse de forma reversible, pero no se
instalara hasta definir una prueba que compare sus resultados con uBlock Origin
y Dark Reader en el navegador actual.

Referencias oficiales:

- https://qutebrowser.org/doc/faq.html
- https://qutebrowser.org/doc/help/settings.html

## Método de adopcion

1. Usar la configuracion actual en tareas reales.
2. Anotar friccion, acciones repetidas y errores, no impresiones aisladas.
3. Cambiar una decision por iteracion.
4. Actualizar código y documentación juntos.
5. Compilar y probar en Xephyr.
6. Mantener XFCE, SSH y SDDM como recuperación.

El criterio final no es usar menos mouse ni parecerse al autor original. Es que
el sistema se adapte al usuario y pueda reconstruirse sin depender de memoria.
