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
jd_color18=#124726
# Markdown heading 2 - color02
jd_color19=#5b2d00
# Markdown heading 3 - color03
jd_color20=#18522d
# Markdown heading 4 - color01
jd_color21=#6d3800
# Markdown heading 5 - color05
jd_color22=#226739
# Markdown heading 6 - color08
# Also inactive tmux window, make it 6 darker to the right
jd_color23=#2a1400
# Markdown heading foreground
# usually set to color10 which is the terminal background
jd_color26=#000000

jd_color04=#00e65c
jd_color02=#ff9d00
jd_color03=#66ff99
jd_color01=#ffc94a
jd_color05=#98ff98
jd_color08=#ffe07a
jd_color06=#caffca

# Colors to the right from https://www.colorhexa.com
# Terminal and neovim background
jd_color10=#000000
# Lualine across, 1 color to the right of background
jd_color17=#061006
# Markdown codeblock, 2 to the right of background
jd_color07=#0b180b
# Background of inactive tmux pane, 3 to the right of background
jd_color25=#102210
# line across cursor, 5 to the right of background
jd_color13=#183818
# Tmux inactive windows, 7 colors to the right of background
jd_color15=#245224

# Comments
jd_color09=#4e6f4e
# Underline spellbad, color02 7 tones to the left in colorhexa
jd_color11=#c96d00
# Underline spellcap, color04 7 tones to the left in colorhexa
jd_color12=#d98a00
# Cursor and tmux windows text
jd_color14=#d8ffd8
# Selected text
jd_color16=#ffe680
# Cursor color, color04 9 tones to the left in colorhexa
jd_color24=#00cc4f

# Wallpaper for this colorscheme
wallpaper="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Images/wallpapers/batman/batman-green.png"
