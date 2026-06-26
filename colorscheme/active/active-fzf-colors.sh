#!/usr/bin/env bash

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/mydotfiles}"
colorscheme_file="${COLORSCHEME_FILE:-$DOTFILES_DIR/colorscheme/active/active-colorscheme.sh}"

if [[ -f "$colorscheme_file" ]]; then
  # shellcheck disable=SC1090
  source "$colorscheme_file"
fi

# Las paletas importadas aun usan jd_* como namespace interno.
jd_fzf_colors="bg:${jd_color10:-#000000},fg:${jd_color14:-#ffffff}"
jd_fzf_colors+=",hl:${jd_color03:-#66ff99},hl+:${jd_color03:-#66ff99}"
jd_fzf_colors+=",info:${jd_color09:-#888888},header:${jd_color09:-#888888}"
jd_fzf_colors+=",prompt:${jd_color02:-#00e65c}"
jd_fzf_colors+=",pointer:${jd_color11:-#c96d00}"
jd_fzf_colors+=",marker:${jd_color12:-#d98a00}"
jd_fzf_colors+=",spinner:${jd_color13:-#183818}"
jd_fzf_colors+=",fg+:${jd_color14:-#ffffff}"
jd_fzf_colors+=",bg+:${jd_color13:-#183818}"
jd_fzf_colors+=",gutter:${jd_color10:-#000000}"

export jd_fzf_colors
