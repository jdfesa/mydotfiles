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
jd_color18=#5b4996
# Markdown heading 2 - color02
jd_color19=#21925b
# Markdown heading 3 - color03
jd_color20=#027d95
# Markdown heading 4 - color01
jd_color21=#585c89
# Markdown heading 5 - color05
jd_color22=#0f857c
# Markdown heading 6 - color08
jd_color23=#396592
# Markdown heading foreground
# usually set to color10 which is the terminal background
jd_color26=#0D1116

jd_color04=#987afb
jd_color02=#37f499
jd_color03=#04d1f9
jd_color01=#949ae5
jd_color05=#19dfcf
jd_color08=#5fa9f4
jd_color06=#1682ef

# Colors to the right from https://www.colorhexa.com
# Terminal and neovim background
jd_color10=#0D1116
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
# Underline spellbad
jd_color11=#f16c75
# Underline spellcap
jd_color12=#f1fc79
# Cursor and tmux windows text
jd_color14=#ebfafa
# Selected text
jd_color16=#e9b3fd
# Cursor color
jd_color24=#f94dff

# Wallpaper for this colorscheme
wallpaper="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Images/wallpapers/official/skyrim-dragon-4.webp"
