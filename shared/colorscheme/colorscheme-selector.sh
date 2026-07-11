#!/usr/bin/env bash

set -euo pipefail

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/mydotfiles}"
SHARED_DIR="${SHARED_DIR:-$DOTFILES_DIR/shared}"
COLORSCHEME_DIR="${COLORSCHEME_DIR:-$SHARED_DIR/colorscheme/list}"
ACTIVE_COLORSCHEME_FILE="${ACTIVE_COLORSCHEME_FILE:-$SHARED_DIR/colorscheme/active/active-colorscheme.sh}"
FZF_COLORS_FILE="${FZF_COLORS_FILE:-$SHARED_DIR/colorscheme/active/active-fzf-colors.sh}"

if ! command -v fzf &>/dev/null; then
  echo "fzf is not installed. Please install it first."
  exit 1
fi

if [[ ! -d "$COLORSCHEME_DIR" ]]; then
  echo "Colorscheme directory not found: $COLORSCHEME_DIR"
  exit 1
fi

if [[ -f "$FZF_COLORS_FILE" ]]; then
  set +u
  # shellcheck disable=SC1090
  source "$FZF_COLORS_FILE"
  set -u
fi

schemes=()
while IFS= read -r scheme; do
  schemes+=("$(basename "$scheme")")
done < <(find "$COLORSCHEME_DIR" -maxdepth 1 -type f -name "*.sh" | sort)

if (( ${#schemes[@]} == 0 )); then
  echo "No color scheme scripts found in $COLORSCHEME_DIR."
  exit 1
fi

fzf_args=(--height=100% --reverse --header="Type or move using arrows" --prompt="Select a colorscheme > ")
if [[ -n "${jd_fzf_colors:-}" ]]; then
  fzf_args+=(--color="$jd_fzf_colors")
fi

selected_scheme="$(printf "%s\n" "${schemes[@]}" | fzf "${fzf_args[@]}")" || {
  echo "No color scheme selected."
  exit 0
}

mkdir -p "$(dirname "$ACTIVE_COLORSCHEME_FILE")"
{
  printf '#!/usr/bin/env bash\n\n'
  printf '# Active colorscheme generated for jd/mydotfiles from %s.\n\n' "$selected_scheme"
  sed \
    -e '1{/^#!\/usr\/bin\/env bash$/d;}' \
    "$COLORSCHEME_DIR/$selected_scheme"
} > "$ACTIVE_COLORSCHEME_FILE"

echo "Active colorscheme set to $selected_scheme"
