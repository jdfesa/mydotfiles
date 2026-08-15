# Omarchy Quattro Audit Evidence

## Snapshot

- Audited on: `2026-08-15`
- Source: `https://github.com/basecamp/omarchy`
- Release: `v4.0.0`
- Revision: `f0020448ca87329199de7cb12f2015ebc4a3e5e7`
- Revision date: `2026-08-14T16:57:59+02:00`
- License: `MIT`
- Raw source: ignored under `references/inbox/`

## Static Findings

- 50 Lua files participate in the shipped Hyprland configuration.
- 95 QML files implement the integrated Quickshell desktop.
- 425 top-level `bin/` commands/scripts exist in the release.
- 22 first-party theme directories are present.
- The audited Hyprland trees contain more than one hundred distinct string
  references involving `omarchy-*` commands.
- The user bootstrap defaults to `/usr/share/omarchy` through `OMARCHY_PATH`.
- `default/hypr/bindings/tiling.lua` contains a substantial portable subset
  implemented directly with the Hyprland Lua API.
- Menus, notifications, capture, panels and system actions are tightly coupled
  to the Omarchy command surface and shell IPC.

## Canary Findings

- Host: `arch-desktop` (`jd@192.168.8.47`).
- Hyprland: `0.56.2`; Lua configuration support is therefore available.
- Present: UWSM, Waybar, Mako, Wofi, hyprlock, hypridle, hyprpaper,
  NetworkManager, WirePlumber, `xdg-desktop-portal-hyprland` and
  `wl-clipboard`.
- Absent from the audited package query: `quickshell-git`, `lua51`,
  `luarocks`, Foot, `wtype`, `udiskie`, `hyprsunset`, `brightnessctl` and
  `pamixer`.
- No `omarchy-*` commands are installed.
- SDDM currently exposes Hyprland managed by UWSM, direct Hyprland and XFCE
  Wayland, so a parallel session is feasible without replacing recovery paths.

## Limitations

- Static reference counts do not determine the minimal runtime closure.
- An official Omarchy release does not prove each extracted component on this
  older desktop hardware.
- QML plugins execute unsandboxed and must be reviewed before activation.
- Wallpapers, fonts and other transitive assets require their own provenance
  review before copying.
