-- Core Quattro bindings adapted from Omarchy v4.0.0 (MIT).

local home = os.getenv("HOME")
local config_root = os.getenv("HYPRLAND_QUATTRO_ROOT") or (home .. "/.config/hypr-quattro")

-- Applications: preserve the Quattro muscle-memory while using local choices.
q.bind("SUPER + RETURN", "Terminal", q.launch("kitty"))
q.bind("SUPER + SHIFT + RETURN", "Browser", q.launch("helium-browser"))
q.bind("SUPER + SHIFT + B", "Browser", q.launch("helium-browser"))
q.bind("SUPER + SPACE", "Application launcher", q.launch("wofi --show drun"))
q.bind("SUPER + SHIFT + F", "File manager", q.launch("thunar --window"))
q.bind("SUPER + SHIFT + N", "Editor", q.launch("kitty --class nvim nvim"))
q.bind(
  "SUPER + SHIFT + SLASH",
  "Passwords",
  q.optional_launch("bitwarden", "bitwarden", "Bitwarden Desktop is not installed; the browser extension remains available")
)
q.bind(
  "SUPER + K",
  "Keybindings",
  q.launch("kitty --class QuattroKeybindings --title "
    .. q.shell_quote("Quattro Lab Keybindings")
    .. " sh -lc "
    .. q.shell_quote("less " .. q.shell_quote(config_root .. "/KEYBINDINGS.txt")))
)
q.bind("SUPER + CTRL + A", "Audio settings", q.launch("pavucontrol"))

-- Window state and workspace navigation.
q.bind("SUPER + W", "Close window", hl.dsp.window.close())
q.bind("SUPER + J", "Toggle window split", hl.dsp.layout("togglesplit"))
q.bind("SUPER + P", "Pseudo window", hl.dsp.window.pseudo())
q.bind("SUPER + T", "Toggle floating", hl.dsp.window.float({ action = "toggle" }))
q.bind("SUPER + F", "Full screen", hl.dsp.window.fullscreen({ mode = "fullscreen" }))
q.bind("SUPER + ALT + F", "Full width", hl.dsp.window.fullscreen({ mode = "maximized" }))

q.bind("SUPER + LEFT", "Focus left", hl.dsp.focus({ direction = "l" }))
q.bind("SUPER + RIGHT", "Focus right", hl.dsp.focus({ direction = "r" }))
q.bind("SUPER + UP", "Focus up", hl.dsp.focus({ direction = "u" }))
q.bind("SUPER + DOWN", "Focus down", hl.dsp.focus({ direction = "d" }))

q.bind("SUPER + SHIFT + LEFT", "Swap window left", hl.dsp.window.swap({ direction = "l" }))
q.bind("SUPER + SHIFT + RIGHT", "Swap window right", hl.dsp.window.swap({ direction = "r" }))
q.bind("SUPER + SHIFT + UP", "Swap window up", hl.dsp.window.swap({ direction = "u" }))
q.bind("SUPER + SHIFT + DOWN", "Swap window down", hl.dsp.window.swap({ direction = "d" }))

q.bind("SUPER + CTRL + LEFT", "Resize left", hl.dsp.window.resize({ x = -25, y = 0, relative = true }), { repeating = true })
q.bind("SUPER + CTRL + RIGHT", "Resize right", hl.dsp.window.resize({ x = 25, y = 0, relative = true }), { repeating = true })
q.bind("SUPER + CTRL + UP", "Resize up", hl.dsp.window.resize({ x = 0, y = -25, relative = true }), { repeating = true })
q.bind("SUPER + CTRL + DOWN", "Resize down", hl.dsp.window.resize({ x = 0, y = 25, relative = true }), { repeating = true })

for workspace = 1, 10 do
  local key = "code:" .. tostring(workspace + 9)
  q.bind("SUPER + " .. key, "Switch to workspace " .. workspace, hl.dsp.focus({ workspace = tostring(workspace) }))
  q.bind("SUPER + SHIFT + " .. key, "Move window to workspace " .. workspace, hl.dsp.window.move({ workspace = tostring(workspace) }))
  q.bind("SUPER + SHIFT + ALT + " .. key, "Move window silently to workspace " .. workspace, hl.dsp.window.move({ workspace = tostring(workspace), follow = false }))
end

q.bind("SUPER + S", "Toggle scratchpad", hl.dsp.workspace.toggle_special("scratchpad"))
q.bind("SUPER + ALT + S", "Move window to scratchpad", hl.dsp.window.move({ workspace = "special:scratchpad", follow = false }))
q.bind("SUPER + TAB", "Next workspace", hl.dsp.focus({ workspace = "e+1" }))
q.bind("SUPER + SHIFT + TAB", "Previous workspace", hl.dsp.focus({ workspace = "e-1" }))
q.bind("SUPER + CTRL + TAB", "Former workspace", hl.dsp.focus({ workspace = "previous" }))

q.bind("ALT + TAB", "Next window", hl.dsp.window.cycle_next())
q.bind("ALT + SHIFT + TAB", "Previous window", hl.dsp.window.cycle_next({ next = false }))
q.bind("ALT + TAB", nil, hl.dsp.window.bring_to_top())
q.bind("ALT + SHIFT + TAB", nil, hl.dsp.window.bring_to_top())

q.bind("SUPER + mouse_down", "Next workspace", hl.dsp.focus({ workspace = "e+1" }))
q.bind("SUPER + mouse_up", "Previous workspace", hl.dsp.focus({ workspace = "e-1" }))
q.bind("SUPER + mouse:272", "Move window", hl.dsp.window.drag(), { mouse = true })
q.bind("SUPER + mouse:273", "Resize window", hl.dsp.window.resize(), { mouse = true })

q.bind("SUPER + G", "Toggle window grouping", hl.dsp.group.toggle())
q.bind("SUPER + ALT + G", "Move active window out of group", hl.dsp.window.move({ out_of_group = true }))
q.bind("SUPER + ALT + LEFT", "Move window into group left", hl.dsp.window.move({ into_group = "l" }))
q.bind("SUPER + ALT + RIGHT", "Move window into group right", hl.dsp.window.move({ into_group = "r" }))
q.bind("SUPER + ALT + UP", "Move window into group up", hl.dsp.window.move({ into_group = "u" }))
q.bind("SUPER + ALT + DOWN", "Move window into group down", hl.dsp.window.move({ into_group = "d" }))
q.bind("SUPER + ALT + TAB", "Next grouped window", hl.dsp.group.next())
q.bind("SUPER + ALT + SHIFT + TAB", "Previous grouped window", hl.dsp.group.prev())

-- Universal clipboard behavior copied from Quattro's terminal-aware model.
local function send_shortcut_once(mods, key)
  return function()
    hl.dispatch(hl.dsp.send_key_state({ mods = mods, key = key, state = "down" }))
    hl.timer(function()
      hl.dispatch(hl.dsp.send_key_state({ mods = mods, key = key, state = "up" }))
    end, { timeout = 50, type = "oneshot" })
  end
end

local function active_window_is_terminal()
  local window = hl.get_active_window()
  if not window then
    return false
  end

  for _, tag in ipairs(window.tags or {}) do
    if tag:gsub("%*$", "") == "terminal" then
      return true
    end
  end

  return false
end

local function universal_clipboard_shortcut(default_mods, default_key, terminal_mods, terminal_key)
  return function()
    if active_window_is_terminal() then
      send_shortcut_once(terminal_mods, terminal_key)()
    else
      send_shortcut_once(default_mods, default_key)()
    end
  end
end

q.bind("SUPER + C", "Universal copy", universal_clipboard_shortcut("CTRL", "C", "CTRL", "Insert"))
q.bind("SUPER + V", "Universal paste", universal_clipboard_shortcut("CTRL", "V", "SHIFT", "Insert"))
q.bind("SUPER + X", "Universal cut", send_shortcut_once("CTRL", "X"))

-- Stable local capture, lock and session controls.
q.bind("PRINT", "Capture region", home .. "/.local/bin/wayland-screenshot region")
q.bind("SHIFT + PRINT", "Capture screen", home .. "/.local/bin/wayland-screenshot full")
q.bind("SUPER + CTRL + L", "Lock system", "/bin/sh -lc " .. q.shell_quote("pidof hyprlock || hyprlock --config " .. q.shell_quote(config_root .. "/hyprlock.conf")))
q.bind("SUPER + ESCAPE", "System menu", home .. "/.local/bin/wayland-power-menu", { locked = true })
q.bind("XF86PowerOff", "System menu", home .. "/.local/bin/wayland-power-menu", { locked = true })

-- Audio and media controls remain independent of the future Quickshell shell.
q.bind("XF86AudioRaiseVolume", "Volume up", "wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+", { locked = true, repeating = true })
q.bind("XF86AudioLowerVolume", "Volume down", "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-", { locked = true, repeating = true })
q.bind("XF86AudioMute", "Toggle mute", "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle", { locked = true })
q.bind("XF86AudioMicMute", "Toggle microphone", "wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle", { locked = true })
q.bind("XF86AudioPlay", "Play or pause", "playerctl play-pause", { locked = true })
q.bind("XF86AudioNext", "Next track", "playerctl next", { locked = true })
q.bind("XF86AudioPrev", "Previous track", "playerctl previous", { locked = true })
q.bind("SUPER + F12", "Volume up", "wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+", { locked = true, repeating = true })
q.bind("SUPER + F11", "Volume down", "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-", { locked = true, repeating = true })
q.bind("SUPER + F10", "Toggle mute", "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle", { locked = true })
