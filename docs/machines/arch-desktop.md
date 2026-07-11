# Arch Desktop

Notas de la maquina secundaria Arch Linux accesible por SSH en
`jd@192.168.8.15`.

## Objetivo

Usar esta maquina para probar Arch, window managers y configuraciones Linux sin
ensuciar el setup principal. La fuente de verdad debe ser `~/mydotfiles`; la
maquina debe quedar como runtime con symlinks y datos locales.

## Estado actual seguro

- `~/mydotfiles` ya existe en la maquina.
- `~/.local/bin/start-x11vnc` apunta a
  `~/mydotfiles/os/linux/x11/scripts/start-x11vnc.sh`.
- `x11vnc` nuevo usa `~/.vnc/passwd` y `-localhost`.
- Jump Desktop desde macOS debe conectarse por tunel SSH. Ver
  `os/linux/x11/README.md`.
- XFCE, SDDM, SSH y XRDP son el respaldo fuerte. No romperlos mientras se migra
  DWM u otros window managers.

## Pendiente inmediato

1. Traer la documentacion nueva en Arch:

   ```sh
   cd ~/mydotfiles
   git pull --ff-only
   ```

2. Corregir PATH para que `~/.local/bin` este disponible en shells
   interactivos. Hoy `~/.bashrc` agrega `~/.local/scripts`, pero no
   `~/.local/bin`.

3. Poner en cuarentena el script viejo inseguro:

   ```text
   ~/start-x11vnc.sh
   ```

   Ese script contiene `-passwd 123456` y no debe usarse.

4. Revisar `~/.vnc/config`. Actualmente contiene `localhost=no`. Si se conserva
   TigerVNC, debe documentarse y dejarse sin exponer VNC directo a la red.

## Archivos importantes a migrar

Estos archivos fueron creados manualmente y pueden contener decisiones utiles.
No borrarlos sin leerlos y migrarlos primero:

```text
~/.local/bin/wallpaper-rotator.sh
~/.local/scripts/status-sensors.sh
~/.local/scripts/cliphist
~/.vnc/xstartup
~/.vnc/xstartup.d/01-dwm.sh
~/.xprofile
~/rclone-sync.sh
```

Destino probable:

```text
os/linux/x11/scripts/       # helpers generales de X11
os/linux/dwm/scripts/       # scripts que solo tengan sentido para DWM
docs/machines/              # inventario, historia y tareas de esta maquina
```

Si un wrapper solo cambia una ruta local, se prefiere una variable o archivo
ignorado. No se crea una capa de configuracion completa por maquina.

`~/.xprofile` necesita especial cuidado porque hoy mezcla cosas de DWM con
arranque general:

- `feh`;
- `picom`;
- wallpaper rotator;
- `dwmblocks`.

La meta es que XFCE quede limpio como respaldo y que DWM tenga su propio
arranque documentado.

## Suckless antiguo

Hay configuraciones antiguas en:

```text
~/suckless/
/usr/local/bin/dwm
/usr/local/bin/dwmblocks
/usr/local/bin/st
/usr/local/bin/dmenu
```

Interpretacion actual:

- `~/suckless/` contiene fuentes/configuraciones viejas de DWM, DWMBlocks, ST y
  Dmenu.
- `/usr/local/bin/*` contiene binarios instalados desde esas fuentes.
- No son la fuente de verdad futura.
- No se van a migrar como base principal si la intencion es empezar DWM desde
  cero y bien documentado.

Plan:

1. Mantener XFCE/RDP como fallback.
2. Crear una nueva estructura limpia en `os/linux/dwm/`, `os/linux/dwmblocks/`,
   `os/linux/st/` y `os/linux/dmenu/` solo cuando se empiece a trabajar en cada
   herramienta.
3. No borrar `/usr/local/bin/dwm` ni los binarios suckless hasta confirmar que
   no se necesitan para entrar a la sesion actual.
4. Cuando haya reemplazo documentado, mover `~/suckless/` a cuarentena o borrar
   si ya no contiene nada que valga conservar.

## Candidatos a limpiar mas adelante

No borrar todavia; revisar cuando la migracion este documentada:

```text
~/.cache/yay
~/yay
~/yay-bin
backup_arch_dwm_final.tar.gz
backup_dwm_x11vnc.tar.gz
backup_full_sistema/
~/.bash_history-*.tmp
```

`~/.cache/yay` es cache/build regenerable. Los clones `~/yay` y `~/yay-bin`
parecen arboles AUR usados para instalar paquetes, no configuraciones
permanentes.

## Regla para continuar

- No borrar primero: poner en cuarentena.
- Migrar una pieza por vez.
- Cada pieza migrada debe tener README, destino claro y symlink documentado.
- XFCE/RDP/SSH quedan como salida de emergencia hasta que DWM sea reproducible.
- Nada con passwords, tokens, claves privadas o rutas sensibles entra a Git.
