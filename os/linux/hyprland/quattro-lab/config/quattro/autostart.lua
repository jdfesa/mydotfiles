-- Stable Wayland services retained while Quickshell is audited separately.

hl.on("hyprland.start", function()
  hl.exec_cmd("systemctl --user import-environment $(env | cut -d'=' -f 1)")
  hl.exec_cmd("dbus-update-activation-environment --systemd --all")
  hl.exec_cmd(q.launch("waybar"))
  hl.exec_cmd(q.launch("mako"))
  hl.exec_cmd(q.launch("hypridle --config " .. q.shell_quote((os.getenv("HYPRLAND_QUATTRO_ROOT") or (os.getenv("HOME") .. "/.config/hypr-quattro")) .. "/hypridle.conf")))
  hl.exec_cmd("systemctl --user start hyprpolkitagent.service")
end)
