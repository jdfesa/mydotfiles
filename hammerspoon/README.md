# Hammerspoon

`Hammerspoon` permite automatizar macOS con Lua. En este repo lo usamos como centro de notificaciones programables y pequenas automatizaciones personales.

## Estado actual

Activo:

- recordatorios manuales por fecha desde `hammerspoon/reminders.lua`;
- notificaciones con `hs.notify`;
- alert visual con `hs.alert` como respaldo;
- Hammerspoon leyendo esta carpeta desde `~/.config/hammerspoon`.

Preparado pero desactivado:

- `GoMaCal`, integracion opcional para leer Google Calendar real.

No activo:

- overlays visuales (`AClock`, `Calendar`, `HCalendar`);
- app launcher;
- hotkeys globales;
- control o movimiento de ventanas.

La prioridad es evitar ruido: si una integracion no esta activa o no tiene un caso de uso claro, debe quedar marcada como opcional o eliminarse.

No reemplaza a AeroSpace, Sketchybar ni Zsh:

- AeroSpace sigue manejando ventanas y workspaces.
- Sketchybar sigue mostrando estado persistente en la barra.
- Zsh sigue siendo el shell.
- Hammerspoon queda para logica viva de macOS: timers, recordatorios, notificaciones y acciones pequenas.

## Para que sirve en este setup

El primer caso de uso es recibir recordatorios de fechas concretas mientras trabajas en macOS.

Ejemplos:

- avisar 1 dia, 1 hora, 10 minutos y en el momento exacto de una fecha importante;
- recordar una reunion, entrega, vencimiento o tarea administrativa;
- abrir una URL cuando haces click en la notificacion;
- mostrar tambien un `hs.alert` visual dentro de la pantalla por si las notificaciones del sistema estan silenciadas.

## Relacion con los dotfiles externos

La carpeta importada en `~/Downloads/dotfiles-master 2/hammerspoon` trae buenas ideas, especialmente `GoMaCal`, que revisa eventos cada 60 segundos y dispara `hs.notify`.

No se copio tal cual porque:

- tenia rutas de otro usuario, por ejemplo `/Users/omerxx/...`;
- activaba hotkeys globales como `cmd-alt-a`, `cmd-alt-c` y `alt-r`;
- mezclaba reloj flotante, launcher y calendario;
- para este setup primero queremos una capa minima de notificaciones, sin tocar ventanas.

La idea rescatada es el uso de `hs.notify` con timers. La implementacion de este repo vive en:

```bash
~/mydotfiles/hammerspoon
```

## Spoons evaluados

Los `Spoons` del repo externo son reutilizables, pero no todos conviene activarlos ahora.

### GoMaCal.spoon

Utilidad: alta.

Es el mas cercano a nuestro objetivo. Ejecuta un binario de calendario, revisa eventos proximos y dispara una notificacion con `hs.notify`. Tambien puede abrir el link de reunion al hacer click.

No se copio directo porque depende de una ruta ajena:

```bash
/Users/omerxx/dotfiles/hammerspoon/calendar-app/calapp
```

La idea si se reutilizo: scheduler + notificaciones accionables. Nuestra version inicial usa `hammerspoon/reminders.lua` para fechas concretas. Mas adelante podemos adaptar `GoMaCal` si queremos leer Google Calendar real.

### AClock.spoon

Utilidad: media/baja para este setup.

Muestra un reloj grande flotante con `hs.canvas`. Puede ser lindo o util como overlay temporal, pero no aporta directamente al flujo de recordatorios. Tambien requiere hotkeys si queremos mostrarlo/ocultarlo, y por ahora evitamos sumar atajos globales.

Decision: no activar por ahora.

### Calendar.spoon

Utilidad: baja/media.

Muestra un calendario mensual en el escritorio usando `hs.canvas`. Puede ser visualmente util, pero se solapa un poco con Sketchybar/desktop widgets y suma elementos permanentes en pantalla.

Decision: dejar como referencia visual, no activar.

### HCalendar.spoon

Utilidad: baja/media.

Muestra un calendario horizontal del mes, tambien con `hs.canvas`, y puede enseñar progreso del mes. Es interesante como widget, pero no es necesario para notificaciones importantes.

Decision: dejar como referencia visual, no activar.

Resumen: `GoMaCal` es el Spoon que vale la pena adaptar despues. `AClock`, `Calendar` y `HCalendar` son reutilizables, pero pertenecen mas a overlays visuales que a automatizaciones esenciales.

## Archivos

- `init.lua`: punto de entrada de Hammerspoon.
- `config.lua`: switches locales para activar integraciones opcionales.
- `reminders.lua`: lista editable de recordatorios por fecha.
- `modules/reminders.lua`: scheduler que revisa fechas y dispara notificaciones.
- `Spoons/GoMaCal.spoon`: Spoon adaptado para leer eventos de Google Calendar.
- `gomacal/`: fuente Go local para compilar el binario `~/.local/bin/gomacal`.

## Instalacion

Hammerspoon se instala como app de macOS:

```bash
brew install --cask hammerspoon
```

Tambien queda documentado en:

```bash
~/mydotfiles/brew/10-essential/Brewfile
```

## Activacion

La fuente de verdad queda en:

```bash
~/mydotfiles/hammerspoon
```

Usamos `~/.config/hammerspoon` como ruta visible y reproducible:

```bash
mkdir -p ~/.config
ln -s ~/mydotfiles/hammerspoon ~/.config/hammerspoon
defaults write org.hammerspoon.Hammerspoon MJConfigFile "$HOME/.config/hammerspoon/init.lua"
```

Despues abrir Hammerspoon desde `/Applications` o Spotlight.

En el primer arranque, macOS puede pedir confirmaciones de seguridad o permisos. Aceptarlos desde la interfaz de macOS y luego recargar la configuracion desde el icono de Hammerspoon en la menu bar.

## Permisos de macOS

Para notificaciones:

```text
System Settings -> Notifications -> Hammerspoon -> Allow Notifications
```

Si mas adelante agregamos hotkeys, control de apps o automatizaciones sobre ventanas, tambien puede pedir:

```text
System Settings -> Privacy & Security -> Accessibility -> Hammerspoon
```

Por ahora no usamos Hammerspoon para mover ventanas, asi que AeroSpace no deberia tener conflictos.

## Crear un recordatorio

Editar:

```bash
~/mydotfiles/hammerspoon/reminders.lua
```

Ejemplo:

```lua
{
  id = "pagar-servicio-julio",
  enabled = true,
  title = "Pagar servicio",
  body = "Revisar vencimiento y pagar antes de las 18:00.",
  at = "2026-07-10 18:00",
  notify_before_minutes = { 1440, 60, 10, 0 },
  grace_minutes = 30,
  url = "https://example.com",
  action_title = "Abrir",
}
```

Formato de fecha:

```text
YYYY-MM-DD HH:MM
```

La hora usa la zona horaria local de macOS.

## Google Calendar con GoMaCal

La integracion de Google Calendar queda preparada pero desactivada por defecto.

### Por que existe

El sistema actual de `reminders.lua` sirve para fechas escritas manualmente.

`GoMaCal` agregaria valor solo si queremos que Hammerspoon lea eventos reales de Google Calendar y dispare notificaciones automaticamente antes de reuniones o fechas cargadas en calendario.

### Que costo agrega

- Requiere Go para compilar el binario.
- Requiere crear credenciales OAuth en Google Cloud.
- Requiere autorizar Google Calendar una vez desde navegador.
- Agrega mas archivos al repo: un Spoon y una herramienta Go local.

Por eso queda apagado en `hammerspoon/config.lua`:

```lua
google_calendar = {
  enabled = false,
}
```

Mientras `enabled = false`, no consulta Google Calendar, no abre navegador, no usa credenciales y no dispara notificaciones de calendario.

### Cuando conservarlo

Conservar `GoMaCal` si queremos alguno de estos flujos:

- avisos automaticos de reuniones de Google Calendar;
- boton en la notificacion para abrir Meet, Zoom, Teams o Webex;
- recordatorios que no haya que duplicar manualmente en `reminders.lua`.

### Cuando borrarlo

Borrarlo si decidimos que los recordatorios manuales son suficientes o si no queremos depender de Google Calendar API.

Los archivos a borrar serian:

```bash
hammerspoon/Spoons/GoMaCal.spoon
hammerspoon/gomacal
```

Y tambien se podria quitar el bloque `google_calendar` de:

```bash
hammerspoon/config.lua
hammerspoon/init.lua
```

Para configurarla:

1. Compilar el binario local siguiendo [`gomacal/README.md`](gomacal/README.md).
2. Crear `~/.config/gomacal/credentials.json` desde Google Cloud.
3. Ejecutar `gomacal --next 5m` una vez para autorizar la cuenta.
4. Cambiar `google_calendar.enabled` a `true` en `hammerspoon/config.lua`.
5. Recargar Hammerspoon.

El Spoon usa `--no-auth` para no abrir navegadores automaticamente durante el trabajo diario. Si falta el token, no notifica hasta que hagas el primer login manual.

## Probar manualmente

Desde la consola de Hammerspoon:

```lua
jdNotify("Prueba", "Hammerspoon ya puede enviar notificaciones")
```

Con URL:

```lua
jdNotify("Prueba con link", "Click para abrir GitHub", "https://github.com")
```

Cuando el comando `hs` ya este conectado con la app, tambien se puede probar desde la terminal:

```bash
hs -c 'jdNotify("Prueba", "Notificacion enviada desde la terminal")'
```

Si `hs -c` no responde en el primer intento, abrir Hammerspoon manualmente, aceptar permisos de macOS y usar `Reload Config` desde el icono de la menu bar.

## Recargar

Despues de editar `reminders.lua`, recargar desde la app de Hammerspoon:

```text
Hammerspoon menu bar icon -> Reload Config
```

Tambien se puede usar la consola de Hammerspoon:

```lua
hs.reload()
```

## Resetear recordatorios enviados

El scheduler guarda que recordatorios ya fueron enviados para no repetirlos cada 30 segundos.

Si estas probando y queres limpiar ese historial:

```lua
hs.settings.clear("jd.mydotfiles.hammerspoon.reminders.sent")
hs.reload()
```

## Validacion

```bash
test -L ~/.config/hammerspoon
defaults read org.hammerspoon.Hammerspoon MJConfigFile
```

La segunda linea deberia devolver:

```bash
/Users/jd/.config/hammerspoon/init.lua
```
