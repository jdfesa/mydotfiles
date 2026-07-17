#!/usr/bin/env bash
set -uo pipefail

cpu_temp=N/A
cpu_use=N/A
mem_use=N/A
gpu_temp=N/A
gpu_use=N/A

if command -v sensors >/dev/null 2>&1; then
  cpu_temp="$(
    sensors 2>/dev/null | awk '
      /^(Tdie|Package id|Core 0|CPU|temp1):/ {
        for (i = 2; i <= NF; i++) {
          value = $i
          gsub(/[+°C]/, "", value)
          if (value ~ /^[0-9]+([.][0-9]+)?$/) {
            sub(/[.].*/, "", value)
            print value
            exit
          }
        }
      }'
  )"
  gpu_temp="$(
    sensors 2>/dev/null | awk '
      /^(edge|junction):/ {
        value = $2
        gsub(/[+°C]/, "", value)
        sub(/[.].*/, "", value)
        print value
        exit
      }'
  )"
fi

if command -v mpstat >/dev/null 2>&1; then
  cpu_use="$(mpstat 1 1 | awk '/Average:/ { printf "%d", 100 - $NF }')"
fi

if command -v free >/dev/null 2>&1; then
  mem_use="$(free -m | awk '/^Mem:/ { printf "%.1f", $3 / 1024 }')"
fi

# Point this at a command that prints only the AMD GPU utilization percentage
# to override automatic detection.
# Example: AMDGPU_LOAD_COMMAND="$HOME/.local/bin/read-amdgpu-load"
if [[ -n "${AMDGPU_LOAD_COMMAND:-}" ]]; then
  if [[ -x "$AMDGPU_LOAD_COMMAND" ]]; then
    gpu_use="$($AMDGPU_LOAD_COMMAND 2>/dev/null || true)"
  else
    printf 'status-sensors: AMDGPU_LOAD_COMMAND is not executable: %s\n' \
      "$AMDGPU_LOAD_COMMAND" >&2
  fi
else
  drm_class_dir=${DRM_CLASS_DIR:-/sys/class/drm}
  for busy_file in "$drm_class_dir"/card[0-9]*/device/gpu_busy_percent; do
    [[ -r "$busy_file" ]] || continue
    device_dir=${busy_file%/gpu_busy_percent}
    driver=$(basename -- "$(readlink -f "$device_dir/driver")")
    [[ "$driver" == amdgpu ]] || continue

    gpu_use=$(<"$busy_file")
    [[ "$gpu_use" =~ ^[0-9]+$ ]] || gpu_use=N/A
    break
  done
fi

cpu_temp="${cpu_temp:-N/A}"
cpu_use="${cpu_use:-N/A}"
mem_use="${mem_use:-N/A}"
gpu_temp="${gpu_temp:-N/A}"
gpu_use="${gpu_use:-N/A}"

printf ' CPU %s°C (%s%%)  MEM %s GiB  GPU %s°C (%s%%)\n' \
  "$cpu_temp" "$cpu_use" "$mem_use" "$gpu_temp" "$gpu_use"

case "${BLOCK_BUTTON:-}" in
  1)
    if [[ -n "${TERMINAL:-}" ]] && command -v htop >/dev/null 2>&1; then
      setsid -f "$TERMINAL" -e htop
    fi
    ;;
  3)
    if command -v notify-send >/dev/null 2>&1; then
      notify-send -t 10000 Stats \
        "CPU: ${cpu_temp}°C (${cpu_use}%)\nMemory: ${mem_use} GiB\nGPU: ${gpu_temp}°C (${gpu_use}%)"
    fi
    ;;
esac
