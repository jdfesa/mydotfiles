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
- Los scripts recuperados se despliegan mediante `profiles/arch-desktop.links`.
- El antiguo `~/suckless` se retiro de su ruta activa y quedo en cuarentena en
  `~/.local/share/dotfiles-migration/quarantine/20260710-223627/suckless`.
- Los binarios antiguos de `/usr/local/bin` permanecen temporalmente porque la
  entrada DWM de SDDM todavia los referencia.

## Scripts recuperados

Los scripts manuales se incorporaron al repositorio con validaciones y rutas
portables:

```text
os/linux/dwm/scripts/wallpaper-rotator.sh
os/linux/dwm/scripts/status-sensors.sh
os/linux/x11/scripts/cliphist
shared/rclone/rclone-sync
```

El perfil `profiles/arch-desktop.links` los despliega bajo `~/.local/bin/`. El
script de Rclone hace `--dry-run` salvo que se indique `--apply`; sus
credenciales permanecen fuera del repositorio.

## Pendiente inmediato

1. Cuando estos cambios esten versionados, sincronizar el clon de Arch desde la
   rama principal. No ejecutar `git pull` mientras el clon remoto contenga esta
   migracion sin commit:

   ```sh
   cd ~/mydotfiles
   git pull --ff-only
   ```

2. La configuracion Bash administrada por el perfil ya agrega `~/.local/bin` al
   `PATH`. Validar una nueva sesion SSH despues de versionar la migracion.

3. El script viejo inseguro ya esta en cuarentena:

   ```text
   ~/.local/share/dotfiles-migration/quarantine/20260710-223627/manual-scripts/start-x11vnc.sh
   ```

   Ese script contiene `-passwd 123456` y no debe usarse.

4. Las configuraciones antiguas de TigerVNC que usaban DWM y `localhost=no`
   estan en `legacy-dwm-startup/` dentro de la cuarentena. En `~/.vnc/` solo
   permanece `passwd`, con modo `0600`, para el `x11vnc` seguro.

## Archivos importantes a migrar

Estos archivos fueron creados manualmente y se revisaron durante la migracion:

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

El antiguo `~/.xprofile` mezclaba cosas de DWM con arranque general:

- `feh`;
- `picom`;
- wallpaper rotator;
- `dwmblocks`.

Fue retirado a `legacy-dwm-startup/` dentro de la cuarentena. XFCE queda limpio
como respaldo; un futuro DWM tendra su propio arranque documentado.

## Suckless antiguo

Las fuentes/configuraciones antiguas se encontraron originalmente en:

```text
~/suckless/
/usr/local/bin/dwm
/usr/local/bin/dwmblocks
/usr/local/bin/st
/usr/local/bin/dmenu
```

Estado despues del inventario:

- `~/suckless/` ya no existe como ruta activa; su contenido esta en la
  cuarentena fechada indicada arriba.
- `/usr/local/bin/*` contiene binarios instalados desde esas fuentes.
- No son la fuente de verdad futura.
- No se van a migrar como base principal si la intencion es empezar DWM desde
  cero y bien documentado.

Plan restante:

1. Mantener XFCE/RDP como fallback.
2. Crear una nueva estructura limpia en `os/linux/dwm/`, `os/linux/dwmblocks/`,
   `os/linux/st/` y `os/linux/dmenu/` solo cuando se empiece a trabajar en cada
   herramienta.
3. No borrar `/usr/local/bin/dwm` ni los binarios suckless hasta confirmar que
   no se necesitan para entrar a la sesion actual.
4. Eliminar la cuarentena solo despues de reconstruir DWM desde cero y confirmar
   que no se necesita consultar ninguna decision antigua.

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
