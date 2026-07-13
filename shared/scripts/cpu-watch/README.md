# CPU Watch

Monitor interactivo de CPU para macOS y Linux. Detecta carga sostenida, muestra
los procesos que mas CPU y memoria consumen y permite enviarles una señal solo
despues de una confirmacion explicita.

La implementacion usa Python 3 y herramientas incluidas en el sistema. No
requiere paquetes de `pip`.

## Ejecucion

Desde el repositorio:

```bash
~/mydotfiles/shared/scripts/cpu-watch/cpu-watch --umbral 30 --muestras 2
```

El ejemplo alerta si el uso global alcanza 30% durante dos mediciones
consecutivas. Para salir, presionar `Ctrl+C` o elegir `q` cuando aparece el menu.

Una captura inmediata, sin monitoreo continuo:

```bash
~/mydotfiles/shared/scripts/cpu-watch/cpu-watch --una-vez
```

## Por que el ejecutable no usa `.py`

El archivo esta escrito en Python, pero se presenta como un comando de Unix. Su
primera linea es un *shebang* que indica que debe ejecutarse con Python 3:

```python
#!/usr/bin/env python3
```

Como tambien tiene permiso de ejecucion, se puede invocar directamente como
`cpu-watch`; no hace falta escribir `python3 cpu-watch.py`.

Omitir la extension tiene varias ventajas para una herramienta de linea de
comandos:

- se comporta como otros comandos del sistema;
- su interfaz no queda atada al lenguaje de implementacion;
- se podria reescribir en otro lenguaje sin cambiar el nombre que usa quien la
  ejecuta;
- coincide con ejecutables del repositorio como `scripts/link` y
  `scripts/doctor`.

La extension `.py` sigue siendo apropiada para modulos que se importan desde
otro codigo, bibliotecas o archivos que se ejecutan expresamente con
`python3`. No usarla aqui es una convencion de CLI, no un requisito tecnico.

## Ubicacion dentro de `mydotfiles`

Los scripts portables y de uso personal se agrupan bajo `shared/scripts/`. De
esta manera no se mezclan al mismo nivel con configuraciones de herramientas
como Btop, Zsh o Neovim:

```text
shared/
  btop/
  zsh/
  nvim/
  scripts/
    README.md
    cpu-watch/
      cpu-watch
      README.md
```

Cada script independiente o pequeña suite debe vivir en
`shared/scripts/<name>/`, con su ejecutable, README y archivos auxiliares. Si
varios scripts colaboran para resolver el mismo problema, comparten esa carpeta
y pueden organizarse internamente bajo `bin/`, `lib/`, `tests/` o la estructura
que necesiten.

Los scripts exclusivos de un sistema pertenecen a
`os/macos/scripts/<name>/`, `os/linux/scripts/<name>/` u
`os/windows/scripts/<name>/`. Los scripts internos de una herramienta se
mantienen dentro de su propia carpeta. La carpeta superior `scripts/` queda
reservada para mantenimiento transversal del repositorio, como enlazar
configuraciones o comprobar perfiles.

## Porcentajes de CPU

macOS muestra dos escalas diferentes:

- **Uso global:** siempre esta entre 0% y 100% y representa toda la maquina.
- **CPU de un proceso:** 100% equivale a un nucleo logico completo. Un proceso
  multihilo puede superar 100%.
- **TOTAL%:** columna calculada por este programa para estimar cuanto aporta un
  proceso a la capacidad completa. En una maquina de 28 nucleos, un proceso al
  100% representa aproximadamente 3.6% del total.

Las alertas individuales estan desactivadas por defecto. Para alertar cuando un
proceso use cuatro nucleos completos:

```bash
~/mydotfiles/shared/scripts/cpu-watch/cpu-watch \
  --umbral 30 \
  --umbral-proceso 400 \
  --muestras 2
```

`--umbral-proceso 0` desactiva expresamente esa condicion.

## Menu interactivo

Cuando se dispara una alerta, el programa indica el motivo y ofrece:

- `Enter`: continuar monitoreando;
- `PID`: confirmar y enviar `SIGTERM`, que solicita un cierre ordenado;
- `!PID`: confirmar y enviar `SIGKILL`, que fuerza la terminacion;
- `q`: salir.

Antes de enviar una señal vuelve a comprobar que el PID siga perteneciendo al
mismo comando. Si `SIGTERM` no logra cerrar el proceso en cinco segundos,
ofrece `SIGKILL` como una segunda confirmacion.

## Opciones principales

```text
--umbral N             carga global que dispara una alerta (0-100)
--umbral-proceso N     CPU individual; 100 equivale a un nucleo, 0 desactiva
--intervalo SEGUNDOS   tiempo entre mediciones
--muestras N           mediciones altas consecutivas requeridas
--top N                cantidad de procesos mostrados
--cooldown SEGUNDOS    espera minima entre alertas repetidas
--una-vez              tomar una captura y salir
```

Los nombres equivalentes en ingles se pueden consultar con `cpu-watch --help`.

## Seguridad y diagnostico

- No ejecutar con `sudo` salvo que sea imprescindible y se entienda el proceso
  que se intenta terminar.
- No matar servicios de macOS como `fileproviderd`, `mds`, `mds_stores`,
  `WindowServer` o `kernel_task` como primera medida. Muchos son administrados
  por el sistema y vuelven a iniciarse; conviene corregir la aplicacion o la
  cola de trabajo que los activa.
- Un pico individual no implica que la CPU global este saturada. Revisar el
  motivo de la alerta y las columnas de uso global y `TOTAL%`.
- Para diagnosticar un problema real, preferir varias mediciones consecutivas
  en lugar de actuar sobre una sola captura.

## Compatibilidad

- macOS: validado con `ps` y dos muestras de `top` para obtener uso reciente.
- Linux: calcula la carga global mediante `/proc/stat` y obtiene procesos con
  `ps`.
