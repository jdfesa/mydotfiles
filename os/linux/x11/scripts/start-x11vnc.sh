#!/usr/bin/env bash
set -euo pipefail

# Share the physical Linux X11 display through x11vnc.
# Passwords must live outside this repo:
#
#   mkdir -p ~/.vnc
#   x11vnc -storepasswd ~/.vnc/passwd
#   chmod 600 ~/.vnc/passwd
#
# Connect through an SSH tunnel:
#
#   ssh -L 5900:localhost:5900 jd@192.168.8.15
#   vncviewer localhost:5900

display_num="${DISPLAY_NUM:-:0}"
rfb_port="${RFB_PORT:-5900}"
passwd_file="${X11VNC_PASSWD_FILE:-$HOME/.vnc/passwd}"

if ! command -v x11vnc >/dev/null 2>&1; then
  echo "x11vnc not found. Install it with: sudo pacman -S x11vnc" >&2
  exit 127
fi

if [[ ! -r "$passwd_file" ]]; then
  cat >&2 <<EOF
VNC password file not found or not readable: $passwd_file

Create it once on the remote machine:
  mkdir -p ~/.vnc
  x11vnc -storepasswd ~/.vnc/passwd
  chmod 600 ~/.vnc/passwd
EOF
  exit 1
fi

auth_file="$(
  ps -ef \
    | awk '/[X]org/ { for (i = 1; i <= NF; i++) if ($i ~ /^\/run\/sddm\/xauth_/) print $i }' \
    | head -n 1
)"

auth_args=(-auth guess)
if [[ -n "$auth_file" ]]; then
  auth_args=(-auth "$auth_file")
fi

exec sudo x11vnc \
  -display "$display_num" \
  "${auth_args[@]}" \
  -rfbauth "$passwd_file" \
  -localhost \
  -forever \
  -repeat \
  -rfbport "$rfb_port"
