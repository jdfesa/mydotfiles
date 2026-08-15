-- Adapted from Omarchy v4.0.0 default/hypr/helpers.lua (MIT).

q = q or {}

local function shell_quote(value)
  return "'" .. tostring(value):gsub("'", "'\\''") .. "'"
end

q.shell_quote = shell_quote

local function file_exists(path)
  local file = io.open(path, "r")
  if file then
    file:close()
    return true
  end
  return false
end

function q.command_exists(command)
  if command:find("/", 1, true) then
    return file_exists(command)
  end

  local path = os.getenv("PATH") or "/usr/local/bin:/usr/bin"
  for directory in (path .. ":"):gmatch("([^:]*):") do
    if file_exists((directory ~= "" and directory or ".") .. "/" .. command) then
      return true
    end
  end

  return false
end

function q.launch(command)
  return "uwsm-app -- " .. command
end

function q.optional_launch(executable, command, missing_message)
  if q.command_exists(executable) then
    return q.launch(command)
  end

  return "notify-send -u normal "
    .. shell_quote("Quattro Lab")
    .. " "
    .. shell_quote(missing_message)
end

function q.bind(keys, description, dispatcher, options)
  local opts = options or {}
  if description then
    opts.description = description
  end

  if type(dispatcher) == "string" then
    dispatcher = hl.dsp.exec_cmd(dispatcher)
  end

  return hl.bind(keys, dispatcher, opts)
end

function q.exec_on_start(command)
  hl.on("hyprland.start", function()
    hl.exec_cmd(command)
  end)
end

function q.launch_on_start(command)
  q.exec_on_start(q.launch(command))
end

function q.window(match, rules)
  rules.match = rules.match or {}

  if type(match) == "string" then
    rules.match.class = match
  else
    for key, value in pairs(match) do
      rules.match[key] = value
    end
  end

  hl.window_rule(rules)
end
