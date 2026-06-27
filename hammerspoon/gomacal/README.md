# GoMaCal

`gomacal` es el puente entre Google Calendar y Hammerspoon.

## Estado

Experimental y desactivado.

Esta carpeta no hace nada por si sola. Solo se usa si:

1. compilamos el binario `gomacal`;
2. creamos credenciales OAuth de Google Calendar;
3. hacemos el primer login manual;
4. activamos `google_calendar.enabled = true` en `../config.lua`.

Mientras esa opcion siga en `false`, esta carpeta es referencia preparada, no comportamiento activo.

## Valor vs ruido

Valor:

- evita duplicar manualmente en `reminders.lua` eventos que ya existen en Google Calendar;
- permite detectar links de Meet, Zoom, Teams o Webex;
- permite que Hammerspoon muestre una notificacion accionable antes de una reunion.

Ruido/costo:

- requiere Go;
- requiere Google Cloud OAuth;
- agrega codigo Go dentro de los dotfiles;
- necesita mantenimiento si cambia la API o el flujo de autenticacion.

Decision actual: mantenerlo como experimento documentado, apagado por defecto. Si no lo usamos para calendario real, conviene borrarlo.

El repo externo evaluado es [`omerxx/gomacal`](https://github.com/omerxx/gomacal). La idea original es buena: un binario en Go consulta Google Calendar, imprime eventos proximos en un formato parseable y Hammerspoon usa esa salida para mostrar notificaciones.

Esta version local conserva el contrato util para Hammerspoon, pero adapta rutas y seguridad para este repo.

## Diferencias con upstream

- No usa `/tmp/credentials.json`.
- No guarda el token OAuth en `/tmp/token.json`.
- Usa rutas estables:
  - credenciales: `~/.config/gomacal/credentials.json`
  - token: `~/.local/state/gomacal/token.json`
- Agrega `--no-auth` para que Hammerspoon no abra el navegador automaticamente si todavia falta autenticar.
- Agrega `--quiet-empty` para que el scheduler no escriba ruido cuando no hay eventos.
- Agrega el `event.Id` al final de la salida para evitar notificaciones duplicadas.

## Instalacion

Requiere Go:

```bash
brew install go
```

Compilar el binario local:

```bash
mkdir -p ~/.local/bin
cd ~/mydotfiles/hammerspoon/gomacal
go build -o ~/.local/bin/gomacal .
```

Validar:

```bash
gomacal --help
```

## Google Calendar API

Hay que crear credenciales OAuth de tipo Desktop Application en Google Cloud:

1. Entrar a Google Cloud Console.
2. Crear o elegir un proyecto.
3. Activar Google Calendar API.
4. Crear OAuth Client ID de tipo Desktop application.
5. Descargar el JSON.
6. Guardarlo como:

```bash
~/.config/gomacal/credentials.json
```

No versionar ese archivo. Tiene que quedar fuera de Git.

## Primer login

Ejecutar manualmente:

```bash
gomacal --next 5m
```

La primera vez abre el navegador para autorizar Google Calendar. Despues guarda el token en:

```bash
~/.local/state/gomacal/token.json
```

Ese token tampoco se versiona.

## Uso manual

```bash
gomacal
gomacal --next 5m
gomacal --next 2h
```

Formato de salida:

```text
Titulo § starts in 5m § https://meet.google.com/... § event-id
```

## Activacion en Hammerspoon

Editar:

```bash
~/mydotfiles/hammerspoon/config.lua
```

Cambiar:

```lua
enabled = false
```

por:

```lua
enabled = true
```

Despues recargar Hammerspoon:

```text
Hammerspoon menu bar icon -> Reload Config
```

## Resetear notificaciones de calendario

El Spoon evita duplicar notificaciones ya enviadas.

Para limpiar ese historial desde la consola de Hammerspoon:

```lua
hs.settings.clear("jd.mydotfiles.hammerspoon.gomacal.sent")
hs.reload()
```
