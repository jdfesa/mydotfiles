-- Selected Omarchy Quattro application rules adapted to local applications.

q.window(".*", { suppress_event = "maximize" })
q.window(".*", { tag = "+default-opacity" })

q.window({
  class = "^$",
  title = "^$",
  xwayland = true,
  float = true,
  fullscreen = false,
  pin = false,
}, { no_focus = true })

q.window("(Alacritty|kitty|foot|org\\.codeberg\\.dnkl\\.foot|com\\.mitchellh\\.ghostty)", {
  tag = "+terminal",
})

q.window("((google-)?[cC]hrom(e|ium)|[bB]rave-browser|Vivaldi-stable|helium)", {
  tag = "+chromium-based-browser",
})
q.window("([fF]irefox|zen|librewolf)", { tag = "+firefox-based-browser" })
q.window({ tag = "chromium-based-browser" }, {
  tag = "-default-opacity",
  tile = true,
  opacity = "1.0 0.985",
})
q.window({ tag = "firefox-based-browser" }, {
  tag = "-default-opacity",
  opacity = "1.0 0.985",
})

q.window("^(Bitwarden)$", { no_screen_share = true, tag = "+floating-window" })
q.window("chrome-nngceckbapebfimnlniiiahkandclblb-Default", {
  no_screen_share = true,
  tag = "+floating-window",
})

q.window("^(org\\.pulseaudio\\.pavucontrol|nm-connection-editor)$", {
  tag = "+floating-window",
})
q.window({ title = "^(Open File|Save File|Choose Files)$" }, {
  tag = "+floating-window",
})
q.window({ tag = "floating-window" }, { float = true })
q.window({ tag = "floating-window" }, { center = true })

q.window({ title = ".*is sharing.*" }, { workspace = "special silent" })
q.window({ tag = "default-opacity" }, { opacity = "0.985 0.96" })
