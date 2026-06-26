#!/usr/bin/env bash

# These files have to be executable

# Lighter markdown headings
# 4 colors to the right for these ligher headings
# https://www.color-hex.com/color/987afb
#
# Given that color A (#987afb) becomes color B (#5b4996) when darkened 4 steps
# to the right, apply the same darkening ratio/pattern to calculate what color
# C (#37f499) becomes when darkened 4 steps to the right.
#
# Markdown heading 1 - color04
jd_color18=#494949
# Markdown heading 2 - color02
jd_color19=#2a2a2a
# Markdown heading 3 - color03
jd_color20=#1a1a1a
# Markdown heading 4 - color01
jd_color21=#645313
# Markdown heading 5 - color05
jd_color22=#2f363d
# Markdown heading 6 - color08
jd_color23=#999999
# Markdown heading foreground
# usually set to color10 which is the terminal background
jd_color26=#000000

jd_color04=#b2b2b2
jd_color02=#939393
jd_color03=#d1d1d1
jd_color01=#a88a1f
jd_color05=#4f5b66
jd_color08=#ffffff
jd_color06=#027085

# Colors to the right from https://www.colorhexa.com
# Terminal and neovim background
jd_color10=#000000
# Lualine across, 1 color to the right of background
jd_color17=#0a0a0a
# Markdown codeblock, 2 to the right of background
jd_color07=#141414
# Background of inactive tmux pane, 3 to the right of background
jd_color25=#1f1f1f
# line across cursor, 5 to the right of background
jd_color13=#333333
# Tmux inactive windows, 7 colors to the right of background
jd_color15=#474747

# Comments
jd_color09=#5f7f89
# Underline spellbad
jd_color11=#ff7676
# Underline spellcap
jd_color12=#b7a54c
# Cursor and tmux windows text
jd_color14=#ffffff
# Selected text
jd_color16=#0390ac
# Cursor color
jd_color24=#04d1f9

# Wallpaper for this colorscheme
wallpaper="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Images/wallpapers/batman/batman-darker.png"
