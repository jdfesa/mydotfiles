local M = {}

local sent_key = "jd.mydotfiles.hammerspoon.reminders.sent"
local sent = hs.settings.get(sent_key) or {}

local function parse_local_datetime(value)
  local year, month, day, hour, minute = tostring(value or ""):match("^(%d%d%d%d)%-(%d%d)%-(%d%d) (%d%d):(%d%d)$")
  if not year then
    return nil
  end

  return os.time({
    year = tonumber(year),
    month = tonumber(month),
    day = tonumber(day),
    hour = tonumber(hour),
    min = tonumber(minute),
    sec = 0,
  })
end

local function offsets_for(reminder)
  local offsets = reminder.notify_before_minutes
  if offsets == nil then
    return { 0 }
  end

  if type(offsets) == "number" then
    return { offsets }
  end

  if type(offsets) == "table" then
    return offsets
  end

  return { 0 }
end

local function marker_for(reminder, offset)
  return table.concat({ reminder.id or reminder.title or "reminder", reminder.at or "", tostring(offset) }, "|")
end

function M.notify(reminder, offset, event_time)
  local title = reminder.title or "Recordatorio"
  local subtitle = os.date("%a %d %b, %H:%M", event_time or os.time())

  if offset and offset > 0 then
    subtitle = subtitle .. " (en " .. tostring(offset) .. " min)"
  elseif offset == 0 then
    subtitle = subtitle .. " (ahora)"
  end

  local notification = hs.notify.new(function()
    if reminder.url and reminder.url ~= "" then
      hs.urlevent.openURL(reminder.url)
    end
  end)

  notification:title(title)
  notification:subTitle(subtitle)
  notification:informativeText(reminder.body or "")
  notification:autoWithdraw(false)
  notification:alwaysPresent(true)

  if reminder.url and reminder.url ~= "" then
    notification:hasActionButton(true)
    notification:actionButtonTitle(reminder.action_title or "Abrir")
  end

  notification:send()
  hs.alert.show(title)
end

function M.check(reminders)
  local now = os.time()

  for _, reminder in ipairs(reminders or {}) do
    if reminder.enabled ~= false then
      local event_time = parse_local_datetime(reminder.at)

      if event_time then
        for _, offset in ipairs(offsets_for(reminder)) do
          local trigger_time = event_time - (tonumber(offset) or 0) * 60
          local grace_minutes = tonumber(reminder.grace_minutes) or 10
          local marker = marker_for(reminder, offset)

          if not sent[marker] and now >= trigger_time and now <= trigger_time + grace_minutes * 60 then
            M.notify(reminder, tonumber(offset) or 0, event_time)
            sent[marker] = true
            hs.settings.set(sent_key, sent)
          end
        end
      else
        hs.printf("Invalid reminder date for %s: %s", reminder.id or reminder.title or "unknown", tostring(reminder.at))
      end
    end
  end
end

function M.start(reminders, opts)
  opts = opts or {}

  if M.timer then
    M.timer:stop()
  end

  M.check(reminders)
  M.timer = hs.timer.doEvery(opts.interval_seconds or 30, function()
    M.check(reminders)
  end)

  return M.timer
end

return M
