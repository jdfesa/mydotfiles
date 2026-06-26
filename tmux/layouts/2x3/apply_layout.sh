#!/bin/bash

LAYOUT=$(cat ~/mydotfiles/tmux/layouts/2x3/layout.txt)
tmux select-layout "$LAYOUT"
