#!/bin/sh

NAME="weather"

LAT="-23.1325"
LON="-64.3242"

# Ficheros de estado para no “romper” el label si falla la red
STATE_DIR="/tmp/sketchybar_weather"
mkdir -p "$STATE_DIR"
LAST_LABEL_FILE="$STATE_DIR/last_label"
LAST_ICON_FILE="$STATE_DIR/last_icon"

# Peticiones (más robustas)
BASE="https://api.open-meteo.com/v1/forecast"
CUR_Q="current=temperature_2m,weather_code,precipitation,is_day&timezone=auto&temperature_unit=celsius"
HRS_Q="hourly=precipitation&forecast_hours=2&timezone=auto&precipitation_unit=mm"

DATA=$(curl -m 6 --fail -sS "$BASE?latitude=$LAT&longitude=$LON&$CUR_Q" 2>/dev/null)
FORECAST=$(curl -m 6 --fail -sS "$BASE?latitude=$LAT&longitude=$LON&$HRS_Q" 2>/dev/null)

# Si alguna llamada falla, usa últimos valores guardados y sal tranquilo
if [ -z "$DATA" ] || [ -z "$FORECAST" ]; then
  LAST_LABEL="--°C"
  [ -f "$LAST_LABEL_FILE" ] && LAST_LABEL=$(cat "$LAST_LABEL_FILE")
  LAST_ICON=""
  [ -f "$LAST_ICON_FILE" ] && LAST_ICON=$(cat "$LAST_ICON_FILE")
  sketchybar --set "$NAME" icon="$LAST_ICON" label="$LAST_LABEL"
  exit 0
fi

# Parse robusto
TEMP=$(echo "$DATA" | jq -r '.current.temperature_2m // empty')
CODE=$(echo "$DATA" | jq -r '.current.weather_code // empty')
PRECIP_NOW=$(echo "$DATA" | jq -r '.current.precipitation // 0')
IS_DAY=$(echo "$DATA" | jq -r '.current.is_day // 1')

# Precip próximas 2h (suma segura)
RAIN_NEXT_2HRS=$(echo "$FORECAST" | jq -r '[.hourly.precipitation[0:2][]] | add // 0')

# Fallbacks
[ -z "$TEMP" ] && TEMP="--"
[ -z "$CODE" ] && CODE="999"

# Íconos (Nerd Fonts “seguros”)
SUN=""          # \uf185
MOON=""         # \uf186
CLOUD=""        # \uf0c2
PARTLY=""       # \ue30c
FOG=""          # \ue313
DRIZZLE=""      # \ue308
RAIN=""         # \ue318
SHOWERS=""      # \ue316
SNOW="󰖘"         # U+F0598 (NF)
THUNDER="󰖓"      # U+F0593 (NF)
UNKNOWN=""      # \ue370

# Map WMO → icono (mínimos cambios + día/noche en 0)
case "$CODE" in
  0)
    if [ "$IS_DAY" = "1" ]; then ICON="$SUN"; else ICON="$MOON"; fi
    ;;
  1|2) ICON="$PARTLY" ;;
  3)   ICON="$CLOUD"  ;;
  45|48) ICON="$FOG" ;;
  51|53|55|56|57) ICON="$DRIZZLE" ;;
  61|63|65|66|67) ICON="$RAIN" ;;
  71|73|75|77|85|86) ICON="$SNOW" ;;
  80|81|82) ICON="$SHOWERS" ;;
  95|96|99) ICON="$THUNDER" ;;
  *) ICON="$UNKNOWN" ;;
esac

# Label temperatura (mantiene tu formato)
if [ "$TEMP" = "--" ]; then
  TEMP_LABEL="--°C"
else
  # redondeo como antes
  TEMP_LABEL="$(printf '%.0f°C' "$TEMP")"
fi

# mm próximas 2h: mostrar sólo si supera umbral (evita “0.0 mm” molestos)
# usa 0.05 como umbral mínimo
SHOW_MM=0
if command -v bc >/dev/null 2>&1; then
  SHOW_MM=$(echo "$RAIN_NEXT_2HRS > 0.05" | bc -l)
fi

if [ "$SHOW_MM" -eq 1 ]; then
  MM_LABEL=$(printf '%.1f' "$RAIN_NEXT_2HRS")
  LABEL="$TEMP_LABEL, ${MM_LABEL} mm"
  COLOR="0xFF89b4fa"
  sketchybar --set "$NAME" icon="$ICON" label="$LABEL" icon.color=$COLOR label.color=$COLOR
else
  LABEL="$TEMP_LABEL"
  sketchybar --set "$NAME" icon="$ICON" label="$LABEL"
fi

# Guarda último estado por si falla red la próxima
printf '%s' "$LABEL" > "$LAST_LABEL_FILE"
printf '%s' "$ICON"  > "$LAST_ICON_FILE"
