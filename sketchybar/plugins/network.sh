#!/bin/bash

NAME="network"
INTERFACE="en0"

# Usa solo la primera línea coincidente con 'en0'
RX_BYTES=$(netstat -ib | awk '$1 == "'$INTERFACE'" {print $7; exit}')
TX_BYTES=$(netstat -ib | awk '$1 == "'$INTERFACE'" {print $10; exit}')

sleep 1

RX_BYTES_NEW=$(netstat -ib | awk '$1 == "'$INTERFACE'" {print $7; exit}')
TX_BYTES_NEW=$(netstat -ib | awk '$1 == "'$INTERFACE'" {print $10; exit}')

# Calcula diferencias
RX_DIFF=$((RX_BYTES_NEW - RX_BYTES))
TX_DIFF=$((TX_BYTES_NEW - TX_BYTES))

# Convierte a KB/s
RX_KB=$((RX_DIFF / 1024))
TX_KB=$((TX_DIFF / 1024))

LABEL="↓ ${RX_KB} KB/s  ↑ ${TX_KB} KB/s"

sketchybar --set "$NAME" label="$LABEL"
