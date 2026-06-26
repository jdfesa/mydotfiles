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
jd_color18=#20925b
# Markdown heading 2 - color02
jd_color19=#027d95
# Markdown heading 3 - color03
jd_color20=#4d9472
# Markdown heading 4 - color01
jd_color21=#2f8696
# Markdown heading 5 - color05
jd_color22=#029494
# Markdown heading 6 - color08
# Also inactive tmux window, make it 6 darker to the right
jd_color23=#1f645e
# Markdown heading foreground
# usually set to color10 which is the terminal background
jd_color26=#0D1116

jd_color04=#37f499
jd_color02=#04d1f9
jd_color03=#81f8bf
jd_color01=#4fe0fc
jd_color05=#04F9F8
jd_color08=#4ffced
jd_color06=#9deefd

# Colors to the right from https://www.colorhexa.com
# Terminal and neovim background
jd_color10=#000000
# Lualine across, 1 color to the right of background
jd_color17=#141b22
# Markdown codeblock, 2 to the right of background
jd_color07=#1c242f
# Background of inactive tmux pane, 3 to the right of background
jd_color25=#232e3b
# line across cursor, 5 to the right of background
jd_color13=#314154
# Tmux inactive windows, 7 colors to the right of background
jd_color15=#013e4a

# Comments
jd_color09=#a5afc2
# Underline spellbad, color02 7 tones to the left in colorhexa
jd_color11=#026072
# Underline spellcap, color04 7 tones to the left in colorhexa
jd_color12=#089954
# Cursor and tmux windows text
jd_color14=#ebfafa
# Selected text
jd_color16=#ccfce5
# Cursor color, color04 9 tones to the left in colorhexa
jd_color24=#06743f

# Wallpaper for this colorscheme
# wallpaper="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Images/wallpapers/official/minty-lemon.jpg"
wallpaper="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Images/wallpapers/batman/batman-darker.png"
