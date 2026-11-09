-- AeroSpace workspace integration for Sketchybar
-- Uses "item" type instead of "space" type since AeroSpace workspaces
-- are not macOS native spaces (their names are strings, including "1"–"5").
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

-- La inicialización se completa por callbacks; nunca bloquear el hilo Lua
-- con io.popen/pclose mientras SbarLua administra procesos asíncronos.
local aerospace_workspaces = {}

-- Note: workspace highlights are updated via CLI (bash script) from aerospace.toml
-- App icon labels are updated via a periodic timer below

local Window_Manager = {}

-- Store created workspace items for later updates
local workspace_items = {}

function Window_Manager:create_workspace_items(current_workspace)

  for _, workspace in ipairs(aerospace_workspaces) do
    local selected = workspace == current_workspace

    if not workspace_items[workspace] then
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
          SBAR.exec(AEROSPACE .. " workspace " .. workspace)
        end
      end)
    end
  end
end

function Window_Manager:init()

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

  local init_done = false
  local pending = false
  local retry_count = 0
  local MAX_RETRIES = 10
  local retry_active = true
  local retry_watcher = SBAR.add("item", "aerospace_retry", {
    drawing = false,
    updates = true,
    update_freq = 3,
  })

  local function stop_retry()
    if retry_active then
      retry_active = false
      SBAR.remove("aerospace_retry")
    end
  end

  local function try_initialize()
    if init_done or pending then
      return
    end
    pending = true

    -- SbarLua decodifica JSON: los IDs numéricos siguen siendo strings.
    SBAR.exec(AEROSPACE .. " list-workspaces --all --json", function(rows, exit_code)
      local workspaces = {}
      if (exit_code == nil or exit_code == 0) and type(rows) == "table" then
        for _, row in ipairs(rows) do
          if type(row) == "table" and type(row.workspace) == "string" and row.workspace ~= "" then
            table.insert(workspaces, row.workspace)
          end
        end
      end
      if #workspaces == 0 then
        pending = false
        return
      end

      SBAR.exec(AEROSPACE .. " list-workspaces --focused --json", function(focused, focus_exit_code)
        if (focus_exit_code ~= nil and focus_exit_code ~= 0)
          or type(focused) ~= "table" or type(focused[1]) ~= "table"
          or type(focused[1].workspace) ~= "string" then
          pending = false
          return
        end

        aerospace_workspaces = workspaces
        init_done = true
        pending = false
        self:create_workspace_items(focused[1].workspace)
        self:update_space_labels()
        stop_retry()
      end)
    end)
  end

  retry_watcher:subscribe("routine", function()
    if init_done then
      return
    end
    retry_count = retry_count + 1
    try_initialize()
    if retry_count >= MAX_RETRIES then
      stop_retry()
    end
  end)

  try_initialize()
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
