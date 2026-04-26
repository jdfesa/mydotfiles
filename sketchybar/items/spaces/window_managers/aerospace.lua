-- AeroSpace workspace integration for Sketchybar
-- Uses "item" type instead of "space" type since AeroSpace workspaces
-- are not macOS native spaces (they use string IDs like "U", "I", "O").
---@diagnostic disable: need-check-nil
local app_icons = require("helpers.spaces_util.app_icons")

local function parse_string_to_table(s)
  local result = {}
  for line in s:gmatch("([^\n]+)") do
    table.insert(result, line)
  end
  return result
end

local function get_workspaces()
  local file = io.popen("aerospace list-workspaces --all")
  local result = file:read("*a")
  file:close()
  return parse_string_to_table(result)
end

local function get_current_workspace()
  local file = io.popen("aerospace list-workspaces --focused")
  local result = file:read("*a")
  file:close()
  return parse_string_to_table(result)[1]
end

local aerospace_workspaces = get_workspaces()
local initial_current_workspace = get_current_workspace()

-- Register custom events triggered from aerospace.toml
SBAR.add("event", "aerospace_workspace_change")
SBAR.add("event", "aerospace_mode_change")

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

    -- Highlight on workspace change
    space_item:subscribe("aerospace_workspace_change", function(env)
      local is_selected = env.FOCUSED_WORKSPACE == workspace
      space_item:set({
        icon = { highlight = is_selected },
        label = { highlight = is_selected },
        background = { border_color = is_selected and COLORS.lavender or COLORS.surface1 },
      })
    end)

    -- Click to switch workspace
    space_item:subscribe("mouse.clicked", function(env)
      if env.BUTTON == "left" then
        SBAR.exec("aerospace workspace " .. workspace)
      end
    end)
  end

  -- Mode indicator — hidden by default, visible when in a non-main mode
  local mode_item = SBAR.add("item", "aerospace_mode", {
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

  mode_item:subscribe("aerospace_mode_change", function(env)
    local mode = env.MODE or "main"
    if mode ~= "main" then
      local mode_labels = { service = "[S]" }
      mode_item:set({
        drawing = true,
        icon = { string = mode_labels[mode] or ("[" .. mode .. "]") },
      })
    else
      mode_item:set({ drawing = false })
    end
  end)

  -- Initial app icon update
  self:update_space_labels()
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

  -- Also update labels on workspace change
  watcher:subscribe("aerospace_workspace_change", function(env)
    self:update_space_labels()
  end)
end

function Window_Manager:update_space_labels()
  for _, workspace in ipairs(aerospace_workspaces) do
    SBAR.exec(
      "aerospace list-windows --workspace " .. workspace .. " --format '%{app-name}' ",
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
