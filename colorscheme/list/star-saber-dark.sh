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
jd_color18=#027C94
# Markdown heading 2 - color02
jd_color19=#0b348c
# Markdown heading 3 - color03
jd_color20=#2F5A85
# Markdown heading 4 - color01
jd_color21=#9A9A9A
# Markdown heading 5 - color05
jd_color22=#8A0D0E
# Markdown heading 6 - color08
jd_color23=#645206
# Markdown heading foreground
# usually set to color10 which is the terminal background
jd_color26=#111112

jd_color04=#04d1f9
jd_color02=#1358ea
jd_color03=#539EEA
jd_color01=#FFFFFF
jd_color05=#ef1619
jd_color08=#FACF11
jd_color06=#97956F

# Terminal and neovim background
jd_color10=#111112
# Lualine across, 1 color to the right of background
# https://www.colorhexa.com/0d1116
jd_color17=#1b1b1c
# Markdown codeblock, 2 to the right of background
# https://www.colorhexa.com
jd_color07=#242426
# Background of inactive, 3 to the right of background
# https://www.colorhexa.come tmux pane
jd_color25=#2e2e30
# line across cursor, 5 to the right of background
# https://www.colorhexa.com
jd_color13=#2e2e30
# Tmux inactive windows, 7 colors to the right of background
# https://www.colorhexa.com
jd_color15=#545459

# Comments
jd_color09=#999999
# Underline spellbad
jd_color11=#ef1619
# Underline spellcap
jd_color12=#FACF11
# Cursor and tmux windows text
jd_color14=#FFFFFF
# Selected text
jd_color16=#00ffff
# Cursor color
jd_color24=#e93f92
