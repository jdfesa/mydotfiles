#!/usr/bin/env bash

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/mydotfiles}"
colorscheme_file="${COLORSCHEME_FILE:-$DOTFILES_DIR/colorscheme/active/active-colorscheme.sh}"

if [[ -f "$colorscheme_file" ]]; then
  # shellcheck disable=SC1090
  source "$colorscheme_file"
fi

# Las paletas importadas aun usan linkarzu_* como namespace interno.
linkarzu_fzf_colors="bg:${linkarzu_color10:-#000000},fg:${linkarzu_color14:-#ffffff}"
linkarzu_fzf_colors+=",hl:${linkarzu_color03:-#66ff99},hl+:${linkarzu_color03:-#66ff99}"
linkarzu_fzf_colors+=",info:${linkarzu_color09:-#888888},header:${linkarzu_color09:-#888888}"
linkarzu_fzf_colors+=",prompt:${linkarzu_color02:-#00e65c}"
linkarzu_fzf_colors+=",pointer:${linkarzu_color11:-#c96d00}"
linkarzu_fzf_colors+=",marker:${linkarzu_color12:-#d98a00}"
linkarzu_fzf_colors+=",spinner:${linkarzu_color13:-#183818}"
linkarzu_fzf_colors+=",fg+:${linkarzu_color14:-#ffffff}"
linkarzu_fzf_colors+=",bg+:${linkarzu_color13:-#183818}"
linkarzu_fzf_colors+=",gutter:${linkarzu_color10:-#000000}"

export linkarzu_fzf_colors
