# Arch Linux Maintenance

Guia operativa para mantener `arch-desktop` como sistema rolling release sin
convertir una actualizacion rutinaria en una improvisacion.

## Expectativa correcta

Arch puede ser muy estable en uso diario, pero no es una distribucion de
actualizaciones inmoviles. Entrega cambios rapidamente y espera que el usuario
participe en el mantenimiento. La solidez proviene de un procedimiento de
actualizacion, recuperación y backups verificables.

Antes de convertirla en maquina principal deben existir y probarse:

- dotfiles publicados y reproducibles;
- lista de paquetes oficiales y AUR;
- backup de datos personales;
- acceso por TTY y SSH;
- XFCE y SDDM como sesion de recuperación;
- USB live de Arch u otro Linux;
- procedimiento de `arch-chroot` y rollback de paquetes;
- al menos una restauracion de prueba.

## Antes de actualizar

1. Leer las noticias de https://archlinux.org/ para detectar intervenciones
   manuales.
2. Revisar el estado del repositorio y publicar cambios locales.
3. Confirmar que los backups recientes existen y son legibles.
4. Revisar paquetes pendientes con `checkupdates` cuando este disponible.
5. Evitar actualizar durante una entrega o tarea que no admita interrupciones.

## Actualizacion soportada

Arch soporta actualizaciones completas:

```sh
sudo pacman -Syu
```

No usar `pacman -Sy paquete`: refresca las bases sin actualizar todo el sistema
y crea una actualizacion parcial no soportada. Tampoco ignorar paquetes de
forma permanente sin analizar sus dependencias.

Después de actualizar:

1. Leer toda advertencia de pacman.
2. Revisar archivos `.pacnew` y `.pacsave`; `pacdiff` de `pacman-contrib` ayuda
   a compararlos.
3. Revisar servicios fallidos con `systemctl --failed`.
4. Reiniciar cuando cambien kernel, drivers o componentes centrales.
5. Probar SDDM, DWM, XFCE, red, audio, GPU, SSH y aplicaciones críticas.
6. Registrar cualquier intervención local en estos dotfiles.

## Paquetes AUR

Los paquetes AUR no reciben el mismo soporte que los repositorios oficiales.
Antes de instalarlos se debe revisar el `PKGBUILD`, limitar su cantidad y
documentar por qué son necesarios. Una actualización de bibliotecas puede
requerir recompilarlos.

## Recuperacion

El orden de recuperación preferido es:

1. cambiar de DWM a XFCE desde SDDM;
2. usar una TTY con `Ctrl+Alt+F3`;
3. entrar por SSH desde macOS;
4. usar paquetes conservados en `/var/cache/pacman/pkg` para un downgrade
   puntual documentado;
5. arrancar un USB live, montar el sistema y usar `arch-chroot`.

No resolver bibliotecas rotas creando symlinks manuales ni ejecutar opciones
destructivas de pacman sin comprender la causa.

## Criterio para migrar el trabajo principal

Arch estará lista para ser primaria cuando sobreviva durante un periodo real de
uso a varias actualizaciones, se pueda restaurar desde documentación y todas las
herramientas críticas tengan alternativa o procedimiento de recuperación. Una
semana sin fallos no sustituye una restauracion probada.

## Auditoria de arch-desktop: 2026-07-17

Base verificada:

- filesystem raiz `ext4`, 24% utilizado;
- kernel `linux 6.19.11.arch1-1`;
- SDDM, SSH y XRDP habilitados y activos;
- reloj sincronizado por NTP;
- sin cambios pendientes en `~/mydotfiles`.

Trabajo pendiente antes de considerarla maquina principal:

1. instalar y probar un segundo kernel, preferentemente `linux-lts`;
2. instalar `pacman-contrib` para disponer de `checkupdates` y `pacdiff`;
3. revisar deliberadamente los `.pacnew` de `locale.gen`, `mirrorlist` y
   `makepkg.conf.d/fortran.conf`;
4. resolver o retirar el servicio legado fallido `vncserver@:1.service` cuando
   se confirme que x11vnc y XRDP cubren la recuperación;
5. inventariar los 22 paquetes externos/AUR y retirar paquetes `-debug` que no
   tengan una necesidad comprobada;
6. definir un backup externo para datos y sistema, ya que ext4 no ofrece el
   esquema de snapshots de Btrfs;
7. generar listas reproducibles separadas para paquetes oficiales y AUR;
8. probar una recuperación real desde TTY, SSH y USB live.

Estos puntos son deuda operativa conocida, no fallos que deban corregirse todos
en una sola sesión.

Referencias oficiales:

- https://wiki.archlinux.org/title/System_maintenance
- https://wiki.archlinux.org/title/Pacman
- https://wiki.archlinux.org/title/General_recommendations
