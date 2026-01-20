#!/bin/bash

VM_STATS=$(vm_stat)
PAGES_WIRED=$(echo "$VM_STATS" | awk '/Pages wired down/ { print $4 }' | sed 's/\.//')
PAGES_COMPRESSED=$(echo "$VM_STATS" | awk '/Pages occupied by compressor/ { print $5 }' | sed 's/\.//')
PAGES_ANONYMOUS=$(echo "$VM_STATS" | awk '/Anonymous pages/ { print $3 }' | sed 's/\.//')

# Total pages (usually 4096 bytes per page)
# sysctl hw.memsize returns bytes.
TOTAL_BYTES=$(sysctl -n hw.memsize)
TOTAL_PAGES=$(($TOTAL_BYTES / 4096))

USED_PAGES=$(($PAGES_WIRED + $PAGES_COMPRESSED + $PAGES_ANONYMOUS))
PERCENT=$(($USED_PAGES * 100 / $TOTAL_PAGES))

echo "Wired: $PAGES_WIRED"
echo "Compressed: $PAGES_COMPRESSED"
echo "Anonymous: $PAGES_ANONYMOUS"
echo "Used: $USED_PAGES / $TOTAL_PAGES"
echo "Percent: $PERCENT%"
