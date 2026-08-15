-- Hyprland Quattro Lab entrypoint.
-- Adapted from Omarchy v4.0.0 (MIT), revision f0020448ca87329199de7cb12f2015ebc4a3e5e7.

local home = os.getenv("HOME")
local config_root = os.getenv("HYPRLAND_QUATTRO_ROOT")
  or ((os.getenv("XDG_CONFIG_HOME") or (home .. "/.config")) .. "/hypr-quattro")

package.path = config_root .. "/?.lua;" .. config_root .. "/?/init.lua;" .. package.path

require("quattro.helpers")
require("quattro.environment")
require("quattro.monitors")
require("quattro.input")
require("quattro.looknfeel")
require("quattro.windows")
require("quattro.bindings")
require("quattro.autostart")
