--- === GoMaCal ===
---
--- Google Calendar meeting notifier for Hammerspoon.

local obj = {}
obj.__index = obj

obj.name = "GoMaCal"
obj.version = "1.0.0-jd"
obj.author = "jd/mydotfiles, adapted from omerxx/gomacal"
obj.homepage = "https://github.com/omerxx/gomacal"
obj.license = "MIT"

obj.command = os.getenv("HOME") .. "/.local/bin/gomacal"
obj.lookahead = "5m"
obj.timer = nil

local sent_key = "jd.mydotfiles.hammerspoon.gomacal.sent"
local sent = hs.settings.get(sent_key) or {}

local function shell_quote(value)
  return "'" .. tostring(value or ""):gsub("'", "'\\''") .. "'"
end

local function trim(value)
  return tostring(value or ""):gsub("^%s*(.-)%s*$", "%1")
end

local function today()
  return os.date("%Y-%m-%d")
end

function obj:setCommand(command)
  if command and command ~= "" then
    self.command = command
  end
  return self
end

function obj:setLookahead(lookahead)
  if lookahead and lookahead ~= "" then
    self.lookahead = lookahead
  end
  return self
end

function obj:parse_event(event_string)
  if not event_string then
    return nil
  end

  local title, time_info, meeting_link, event_id = event_string:match("^(.+) § (.+) § (.*) § (.*)$")
  if not title then
    title, time_info, meeting_link = event_string:match("^(.+) § (.+) § (.*)$")
  end

  if not title or not time_info then
    return nil
  end

  meeting_link = trim(meeting_link)
  event_id = trim(event_id)

  return {
    title = trim(title),
    time_info = trim(time_info),
    meeting_link = meeting_link ~= "" and meeting_link or nil,
    event_id = event_id ~= "" and event_id or nil,
  }
end

function obj:marker_for(event)
  if event.event_id then
    return table.concat({ today(), event.event_id }, "|")
  end

  return table.concat({ today(), event.title or "", event.meeting_link or "" }, "|")
end

function obj:notify(event)
  local notification = hs.notify.new(function()
    if event.meeting_link then
      hs.urlevent.openURL(event.meeting_link)
    end
  end)

  notification:title(event.title)
  notification:subTitle(event.time_info)
  notification:autoWithdraw(false)
  notification:alwaysPresent(true)

  if event.meeting_link then
    notification:hasActionButton(true)
    notification:actionButtonTitle("Entrar")
  end

  notification:send()
  hs.alert.show(event.title)
end

function obj:check_calendar_events()
  local command = shell_quote(self.command)
    .. " --next "
    .. shell_quote(self.lookahead)
    .. " --quiet-empty --no-auth 2>/dev/null"

  local handle = io.popen(command)
  if not handle then
    return
  end

  local result = handle:read("*a")
  handle:close()

  for line in tostring(result or ""):gmatch("[^\r\n]+") do
    local event = self:parse_event(line)
    if event then
      local marker = self:marker_for(event)
      if not sent[marker] then
        self:notify(event)
        sent[marker] = true
        hs.settings.set(sent_key, sent)
      end
    end
  end
end

function obj:start(interval_seconds)
  self:stop()
  self:check_calendar_events()
  self.timer = hs.timer.doEvery(interval_seconds or 60, function()
    self:check_calendar_events()
  end)
  return self
end

function obj:stop()
  if self.timer then
    self.timer:stop()
    self.timer = nil
  end
  return self
end

return obj
