-- Hammerspoon entrypoint for jd/mydotfiles.
-- Scope: programmable macOS notifications and small automations.

local reminders = require("reminders")
local reminder_scheduler = require("modules.reminders")

local config_ok, config = pcall(require, "config")
if not config_ok then
  config = {}
end

reminder_scheduler.start(reminders, {
  interval_seconds = 30,
})

local google_calendar = config.google_calendar or {}
if google_calendar.enabled then
  local loaded = hs.loadSpoon("GoMaCal")
  if loaded and spoon.GoMaCal then
    spoon.GoMaCal:setCommand(google_calendar.command)
    spoon.GoMaCal:setLookahead(google_calendar.lookahead or "5m")
    spoon.GoMaCal:start(google_calendar.interval_seconds or 60)
  else
    hs.alert.show("GoMaCal Spoon unavailable")
  end
end

-- Manual test helper from the Hammerspoon console:
-- jdNotify("Titulo", "Mensaje", "https://example.com")
function jdNotify(title, body, url)
  reminder_scheduler.notify({
    title = title or "Hammerspoon",
    body = body or "Notificacion de prueba",
    url = url,
    action_title = "Abrir",
  }, 0, os.time())
end

hs.alert.show("Hammerspoon notifications ready")
