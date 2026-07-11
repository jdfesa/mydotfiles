#!/usr/bin/env bash

# Generic tmux session picker for ~/mydotfiles.
# Usage:
#   tmux-sessionizer.sh
#   tmux-sessionizer.sh ~/mydotfiles
#   tmux-sessionizer.sh search ~/Developer

set -euo pipefail

pick_from_roots() {
  local roots=(
    "$HOME/mydotfiles"
    "$HOME/Developer"
    "$HOME/github"
    "$HOME/Documents"
    "$HOME/Downloads"
  )

  local existing_roots=()
  local root
  for root in "${roots[@]}"; do
    if [ -d "$root" ]; then
      existing_roots+=("$root")
    fi
  done

  if [ "${#existing_roots[@]}" -eq 0 ]; then
    return 1
  fi

  find "${existing_roots[@]}" -mindepth 0 -maxdepth 1 -type d | sort -u | fzf
}

pick_from_dir() {
  local dir_to_search=$1

  if [ ! -d "$dir_to_search" ]; then
    tmux display-message -d 3000 "Directory does not exist: $dir_to_search"
    exit 1
  fi

  find "$dir_to_search" -mindepth 1 -maxdepth 1 -type d | sort -u | fzf
}

if [ "$#" -eq 0 ]; then
  selected="$(pick_from_roots || true)"
elif [ "$#" -eq 1 ]; then
  selected="$1"
elif [ "$#" -eq 2 ] && [ "$1" = "search" ]; then
  selected="$(pick_from_dir "$2" || true)"
else
  tmux display-message -d 3000 "Usage: tmux-sessionizer.sh [path] OR tmux-sessionizer.sh search [dir]"
  exit 1
fi

if [ -z "${selected:-}" ]; then
  exit 0
fi

selected="$(cd "$selected" && pwd)"
selected_name="$(basename "$selected" | tr ' .-' '___')"

if [ -z "${TMUX:-}" ]; then
  tmux new-session -A -s "$selected_name" -c "$selected"
  exit 0
fi

if ! tmux has-session -t="$selected_name" 2>/dev/null; then
  tmux new-session -ds "$selected_name" -c "$selected"
fi

tmux switch-client -t "$selected_name"
