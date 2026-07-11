local weather = SBAR.add("item", "weather", {
  position = "right",
  padding_right = 10,
  update_freq = 1200, -- 20 min
  icon = {
    font = { family = "Hack Nerd Font", style = "Regular", size = 16.0 },
    color = 0xffffffff,
  },
  label = {
    font = { size = 13.0 },
    color = 0xffffffff,
  },
  script = " "
})

local script_path = (os.getenv("HOME") or "~") .. "/.config/sketchybar/items/weather/weather.sh"
SBAR.exec("sketchybar --set weather script='" .. script_path .. "'")

weather:subscribe("mouse.clicked", function(env)
  SBAR.exec("open 'https://weather.com/weather/today/l/" .. "-23.13,-64.32" .. "'")
end)
