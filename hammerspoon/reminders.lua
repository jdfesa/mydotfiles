-- Date-based reminders.
--
-- Date format: YYYY-MM-DD HH:MM in local macOS time.
-- Keep examples disabled until they become real reminders.

return {
  {
    id = "example-important-date",
    enabled = false,
    title = "Ejemplo: fecha importante",
    body = "Editar hammerspoon/reminders.lua y activar este recordatorio.",
    at = "2026-07-01 09:00",
    notify_before_minutes = { 1440, 60, 10, 0 },
    grace_minutes = 30,
    url = "",
    action_title = "Abrir",
  },
}
