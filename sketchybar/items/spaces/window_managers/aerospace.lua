-- AeroSpace workspace integration for Sketchybar
-- Uses "item" type instead of "space" type since AeroSpace workspaces
-- are not macOS native spaces (they use string IDs like "U", "I", "O").
---@diagnostic disable: need-check-nil
local app_icons = require("helpers.spaces_util.app_icons")

-- Ruta absoluta necesaria: al iniciar sesión, Sketchybar corre sin el PATH
-- del shell, por lo que 'aerospace' sin ruta completa no se encuentra.
local AEROSPACE = "/usr/local/bin/aerospace"

local function parse_string_to_table(s)
  local result = {}
  for line in s:gmatch("([^\n]+)") do
    table.insert(result, line)
  end
  return result
end

local function get_workspaces()
  local file = io.popen(AEROSPACE .. " list-workspaces --all")
  local result = file:read("*a")
  file:close()
  return parse_string_to_table(result)
end

local function get_current_workspace()
  local file = io.popen(AEROSPACE .. " list-workspaces --focused")
  local result = file:read("*a")
  file:close()
  return parse_string_to_table(result)[1]
end

local aerospace_workspaces = get_workspaces()
local initial_current_workspace = get_current_workspace()

-- Si AeroSpace no estaba corriendo al arrancar (race condition al inicio de macOS),
-- INIT_DONE será false y el retry en init() se encarga de esperar y recargar.
local INIT_DONE = (#aerospace_workspaces > 0)

-- Note: workspace highlights are updated via CLI (bash script) from aerospace.toml
-- App icon labels are updated via a periodic timer below

local Window_Manager = {}

-- Store created workspace items for later updates
local workspace_items = {}

function Window_Manager:init()
  for i, workspace in ipairs(aerospace_workspaces) do
    local selected = workspace == initial_current_workspace

    local space_item = SBAR.add("item", "space." .. workspace, {
      icon = {
        string = workspace,
        padding_left = SPACES.ITEM_PADDING,
        padding_right = 8,
        color = selected and COLORS.mauve or COLORS.text,
        highlight_color = COLORS.mauve,
        highlight = selected,
      },
      label = {
        padding_right = SPACES.ITEM_PADDING,
        color = COLORS.subtext0,
        highlight_color = COLORS.lavender,
        font = "sketchybar-app-font:Regular:16.0",
        y_offset = -1,
        highlight = selected,
      },
      padding_right = GROUP_PADDINGS,
      padding_left = 1,
      background = {
        color = COLORS.base,
        border_width = 2,
        height = 26,
        border_color = selected and COLORS.lavender or COLORS.surface1,
      },
      position = "left",
    })

    workspace_items[workspace] = space_item


    -- Click to switch workspace
    space_item:subscribe("mouse.clicked", function(env)
      if env.BUTTON == "left" then
        SBAR.exec("aerospace workspace " .. workspace)
      end
    end)
  end

  -- Mode indicator — hidden by default.
  -- AeroSpace controls this directly via `sketchybar --set` in aerospace.toml.
  -- No Lua event subscription needed (CLI approach is more reliable).
  SBAR.add("item", "aerospace_mode", {
    position = "left",
    drawing = false,
    icon = {
      string = "[S]",
      color = COLORS.red,
      padding_left = 6,
      padding_right = 6,
    },
    label = {
      drawing = false,
    },
    background = {
      color = COLORS.base,
      border_width = 2,
      height = 26,
      border_color = COLORS.red,
    },
  })

  if INIT_DONE then
    -- AeroSpace estaba listo → actualizar iconos de apps normalmente
    self:update_space_labels()
  else
    -- AeroSpace no estaba listo al arrancar (race condition).
    -- Timer que reintenta cada 3s. Cuando AeroSpace responda,
    -- espera 1s y recarga Sketchybar. Máximo 10 intentos (30s).
    local retry_count = 0
    local MAX_RETRIES = 10
    local retry_watcher = SBAR.add("item", "aerospace_retry", {
      drawing = false,
      updates = true,
      update_freq = 3,
    })

    retry_watcher:subscribe("routine", function()
      retry_count = retry_count + 1
      local ws = get_workspaces()

      if #ws > 0 then
        -- AeroSpace respondió. Detener timer y recargar en 1 segundo.
        retry_watcher:set({ update_freq = 0 })
        SBAR.exec("sleep 1 && /usr/local/bin/sketchybar --reload")
      elseif retry_count >= MAX_RETRIES then
        -- No respondió en 30s. Dejar de intentar.
        retry_watcher:set({ update_freq = 0 })
      end
    end)
  end
end

function Window_Manager:start_watcher()
  local watcher = SBAR.add("item", {
    drawing = false,
    updates = true,
    update_freq = 5,
  })

  watcher:subscribe("routine", function(env)
    self:update_space_labels()
  end)
end

function Window_Manager:update_space_labels()
  for _, workspace in ipairs(aerospace_workspaces) do
    SBAR.exec(
      AEROSPACE .. " list-windows --workspace " .. workspace .. " --format '%{app-name}' ",
      function(apps)
        local icon_line = ""
        for _, name in ipairs(parse_string_to_table(apps)) do
          if name and name ~= "" then
            local icon = app_icons[name] or app_icons["default"] or "?"
            icon_line = icon_line .. icon
          end
        end
        icon_line = icon_line ~= "" and icon_line or "—"
        if workspace_items[workspace] then
          SBAR.animate("tanh", 10, function()
            workspace_items[workspace]:set({ label = icon_line })
          end)
        end
      end
    )
  end
end

return Window_Manager
