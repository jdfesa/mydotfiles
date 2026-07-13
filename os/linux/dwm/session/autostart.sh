#!/bin/sh

set -u

start_once() {
  process_name=$1
  shift

  if pgrep -u "$(id -u)" -x "$process_name" >/dev/null 2>&1; then
    return 0
  fi

  "$@" &
}

if command -v picom >/dev/null 2>&1; then
  start_once picom picom
fi

if command -v dwmblocks >/dev/null 2>&1; then
  start_once dwmblocks dwmblocks
fi

if [ "${DWM_ROTATE_WALLPAPER:-0}" = 1 ] \
  && command -v wallpaper-rotator >/dev/null 2>&1; then
  if ! pgrep -u "$(id -u)" -f '[w]allpaper-rotator' >/dev/null 2>&1; then
    wallpaper-rotator &
  fi
fi
