# Mirrors de Arch con Reflector

Esta política evita que una lista mundial enorme convierta una transacción
grande de `pacman` en una sucesión de fallos DNS, conexión y baja velocidad.
`mydotfiles` conserva la selección reproducible; la lista generada sigue siendo
estado dinámico de este host.

## Síntoma y causa

Los dos intentos aprobados de `pacman -Syu --needed` para la workstation diaria
de Quattro abortaron durante las descargas. Pacman indicó explícitamente que no
actualizó ningún paquete, por lo que ambos abortos fueron seguros. Las descargas
completadas permanecen en la caché y no se deben limpiar antes del reintento que
controlará el operador.

La causa operativa fue `/etc/pacman.d/mirrorlist`: todavía era la lista mundial
del paquete `pacman-mirrorlist`, con cientos de servidores activos (la fuente
tenía unas 504 entradas y el host conservaba más de 400). Para una operación
grande, recorrer servidores de muchos continentes no aporta una reserva útil:
aumenta la probabilidad de DNS lento, rutas inestables, timeouts y mirrors con
rendimiento insuficiente desde esta red.

## Política versionada

La fuente de verdad es:

```text
os/linux/packages/reflector/reflector.conf
```

El aplicador la instala como `root:root` modo `0644` en
`/etc/xdg/reflector/reflector.conf`. El archivo
`/etc/pacman.d/mirrorlist` **no se versiona**: lo genera el servicio oficial
`reflector.service` a partir de la política.

Selección revisada para Reflector 2023-5:

- solo HTTPS y mirrors con `completion-percent 100`;
- sincronización dentro de las últimas 12 horas;
- como máximo 25 candidatos, los sincronizados más recientemente;
- medición local y orden por tasa de descarga;
- como máximo 10 servidores en la lista final;
- timeouts explícitos de 5 segundos, iguales a los defaults de esta versión;
- sin filtro fijo de país.

Reflector primero limita los 25 candidatos recientes, luego mide su tasa y al
final conserva 10. Eso mantiene modesto el benchmark semanal y deja redundancia
para transacciones grandes. Un país cercano no garantiza la mejor ruta desde
esta red; medir el rendimiento es más útil que fijar Argentina u otro país. El
filtro global sigue estando acotado, así que no se vuelve a evaluar la lista
mundial completa.

`reflector` ya aparece una sola vez en
`lists/10-workstation-base.txt`; no se duplica en otro manifiesto.

## Comprobar metadata sin cambiar el sistema

Este chequeo es portable y puede ejecutarse en macOS. Solo inspecciona el repo:

```sh
os/linux/packages/scripts/check-reflector-mirrors --metadata-only
os/linux/packages/scripts/test-reflector-mirrors
```

El test omite automáticamente la parte de plan del host si no encuentra los
archivos del paquete Arch. No modifica la configuración activa de macOS.

## Plan, instalación y validación

El comportamiento predeterminado es un plan sin cambios:

```sh
os/linux/packages/scripts/apply-reflector-mirrors
```

La ejecución privilegiada debe ser revisada y lanzada por el operador:

```sh
os/linux/packages/scripts/apply-reflector-mirrors --execute
```

El aplicador:

1. exige Linux, Reflector, `sudo`, `systemctl` y los archivos esperados del
   paquete;
2. guarda únicamente la configuración actual, el mirrorlist actual y los
   estados enabled/active del timer en
   `~/.local/state/mydotfiles/backups/reflector/<timestamp>/`, con checksums;
3. instala la política y fuerza un refresh inmediato mediante el servicio
   empaquetado;
4. exige de 5 a 10 entradas `Server` HTTPS, config exacta y un servicio
   exitoso reciente;
5. ejecuta `pacman -Syy --noconfirm`, que descarga metadata pero no resuelve ni
   confirma upgrades, y comprueba que `pacman -Si pacman` pueda leerla;
6. recién entonces habilita e inicia `reflector.timer`;
7. ante cualquier error posterior al backup restaura automáticamente los dos
   archivos y el estado anterior del timer.

No usa `pacman -Syu`, no instala paquetes y no limpia `/var/cache/pacman/pkg`.
Después de `-Syy` no se deben instalar paquetes de forma aislada: la próxima
operación de paquetes debe ser el reintento completo `pacman -Syu --needed`
controlado para Quattro.

Chequeo live, no interactivo y sin cambios:

```sh
os/linux/packages/scripts/check-reflector-mirrors
```

Verifica hash/contenido/ownership de la config, forma y protocolo del
mirrorlist, resultado reciente del servicio, timer habilitado y activo, y
metadata legible y reciente de pacman. No abre interfaces gráficas.

## Actualizar la política

No editar el mirrorlist generado ni dejar un cambio manual solo en `/etc`.
Para ajustar antigüedad, candidatos o salidas:

1. revisar `reflector --help` de la versión instalada y las referencias
   oficiales;
2. editar `reflector/reflector.conf` y el contrato exacto del checker;
3. ejecutar los checks metadata, tests, ShellCheck y validaciones de perfiles;
4. publicar el cambio por PR y, después de integrarlo, volver a ejecutar el
   aplicador con `--execute` bajo control del operador.

La selección generada cambiará según el estado de la red y de los mirrors; esa
variación es esperada y nunca se debe copiar al repositorio.

## Timer semanal

Se usa `reflector.timer` oficial, con `OnCalendar=weekly`, persistencia y demora
aleatoria de hasta 12 horas. Si el equipo estaba apagado, systemd recupera la
ejecución pendiente al volver. El timer solo queda habilitado después del
refresh y la validación inmediata; no se reemplaza con un cron propio.

## Rollback

Cada ejecución informa el directorio exacto de backup. Primero previsualizar:

```sh
os/linux/packages/scripts/apply-reflector-mirrors \
  --rollback "$HOME/.local/state/mydotfiles/backups/reflector/<timestamp>"
```

Después de revisar la ruta y los checksums, ejecutar:

```sh
os/linux/packages/scripts/apply-reflector-mirrors --execute \
  --rollback "$HOME/.local/state/mydotfiles/backups/reflector/<timestamp>"
```

El rollback solo acepta un directorio bajo el root administrado, verifica
`SHA256SUMS`, restaura config y mirrorlist como `root:root 0644`, y repone los
estados enabled/active registrados. Si la aplicación falla, el mismo mecanismo
se ejecuta automáticamente. No borra backups ni cachés.

## Reintento de Quattro

Este trabajo solo prepara mirrors confiables. No toca los archivos gate
originales de `quattro-daily-workstation`, no ejecuta el upgrade y no crea su
marcador de finalización. Una vez validado el despliegue, el controlador puede
repetir su comando `pacman -Syu --needed`; los paquetes ya descargados siguen en
la caché y pacman reutilizará lo válido.

## Referencias oficiales

- https://man.archlinux.org/man/reflector.1.en
- https://wiki.archlinux.org/title/Mirrors
