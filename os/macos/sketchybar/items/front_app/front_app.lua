local helpers_path = os.getenv("HOME") .. "/.config/sketchybar/helpers/"
local app_icons = require("helpers.spaces_util.app_icons")

local front_app = SBAR.add("item", "front_app", {
  display = "active",
  icon = { drawing = true, font = "sketchybar-app-font:Regular:16.0" },
  updates = true,
  click_script = helpers_path .. "sketchymenu/app_menu.sh toggle",
})

front_app:subscribe("front_app_switched", function(env)
  front_app:set({
    icon = {
      background = {
        image = {
          string = "app." .. env.INFO,
          scale = 0.8,
        },
        drawing = true,
      },
      drawing = true, -- The icon item itself needs to be drawn
      string = "",    -- But clear the text so it doesn't overlap
      width = 30,     -- Space for the image
    },
    label = { string = env.INFO }
  })
end)
