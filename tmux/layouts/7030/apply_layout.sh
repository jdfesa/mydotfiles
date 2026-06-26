#!/bin/bash

LAYOUT=$(cat ~/mydotfiles/tmux/layouts/7030/layout.txt)
tmux select-layout "$LAYOUT"
