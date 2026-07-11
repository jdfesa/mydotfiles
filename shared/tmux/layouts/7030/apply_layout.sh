#!/bin/bash

LAYOUT=$(cat ~/mydotfiles/shared/tmux/layouts/7030/layout.txt)
tmux select-layout "$LAYOUT"
