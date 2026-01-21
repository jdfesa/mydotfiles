local ram = SBAR.add("graph", "widgets.ram", 42, {
  position = "right",
  graph = { color = COLORS.blue },
  background = {
    height = 22,
    color = { alpha = 0 },
    border_color = { alpha = 0 },
    drawing = true,
  },
  icon = { string = ICONS.ram, color = COLORS.red },
  label = {
    string = "RAM ??%",
    font = { size = 9.0 },
    align = "right",
    padding_right = 0,
    width = 0,
    y_offset = 4,
  },
  update_freq = 5,
  updates = "on",
  padding_right = PADDINGS,
  script = "sh $CONFIG_DIR/items/monitor/ram.sh"
})
