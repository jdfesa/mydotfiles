#!/bin/bash

LAYOUT=$(cat ~/mydotfiles/shared/tmux/layouts/2x3/layout.txt)
tmux select-layout "$LAYOUT"
