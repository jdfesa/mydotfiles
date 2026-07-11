#!/usr/bin/env bash
set -euo pipefail

wallpapers_dir="${WALLPAPERS_DIR:-$HOME/Pictures/wallpapers}"
interval="${WALLPAPER_INTERVAL:-1800}"
startup_delay="${WALLPAPER_STARTUP_DELAY:-4}"

if ! command -v feh >/dev/null 2>&1; then
  printf 'wallpaper-rotator: feh is required\n' >&2
  exit 127
fi

if [[ ! -d "$wallpapers_dir" ]]; then
  printf 'wallpaper-rotator: directory not found: %s\n' "$wallpapers_dir" >&2
  exit 1
fi

if [[ ! "$interval" =~ ^[1-9][0-9]*$ || ! "$startup_delay" =~ ^[0-9]+$ ]]; then
  printf 'wallpaper-rotator: intervals must be non-negative integers\n' >&2
  exit 2
fi

sleep "$startup_delay"

while true; do
  mapfile -d '' wallpapers < <(
    find "$wallpapers_dir" -type f \
      \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) \
      -print0 | sort -z
  )

  if (( ${#wallpapers[@]} == 0 )); then
    printf 'wallpaper-rotator: no supported images in %s\n' "$wallpapers_dir" >&2
    exit 1
  fi

  for wallpaper in "${wallpapers[@]}"; do
    feh --no-fehbg --bg-fill "$wallpaper"
    sleep "$interval"
  done
done
