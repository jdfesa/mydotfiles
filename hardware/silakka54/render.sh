#!/usr/bin/env bash

set -euo pipefail

DIR=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
PYTHON="$DIR/.venv/bin/python3"

case "${1:-}" in
  --help|-h)
    printf 'Uso: %s [--watch]\nSin argumentos: genera una vez. --watch: regenera al guardar los archivos fuente.\n' "$0"
    exit 0
    ;;
  --watch|'') ;;
  *) printf 'Opción desconocida: %s\n' "$1" >&2; exit 2 ;;
esac
if (( $# > 1 )); then
  printf 'Usa --help para ver las opciones.\n' >&2
  exit 2
fi

if [[ ! -x "$PYTHON" ]] || ! "$PYTHON" -c 'import keymap_drawer, yaml' 2>/dev/null; then
  printf '❌ Falta el entorno de renderizado. Desde %s ejecuta:\n' "$DIR" >&2
  printf '   python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt\n' >&2
  exit 1
fi

if [[ "${1:-}" == --watch ]]; then
  exec "$PYTHON" "$DIR/watch.py" "$DIR"
fi

# Generate and validate everything before replacing the published artifacts.
# Use the same filesystem for atomic renames of each completed file.
WORK_DIR=$(mktemp -d "$DIR/.render.XXXXXX")
trap 'rm -rf -- "$WORK_DIR"' EXIT
trap 'printf "❌ Falló la generación; no se publicaron resultados incompletos.\n" >&2' ERR

printf '🎨 Generando visualización del Silakka54...\n'
cp -- "$DIR/silakka54_main.vil" "$WORK_DIR/source.vil"
"$PYTHON" "$DIR/convert_vial.py" "$WORK_DIR/source.vil" > "$WORK_DIR/qmk.json"
"$PYTHON" -m keymap_drawer parse -c 12 -q "$WORK_DIR/qmk.json" > "$WORK_DIR/layers.yaml"
"$PYTHON" "$DIR/post_process.py" \
  "$WORK_DIR/layers.yaml" "$WORK_DIR/qmk.json" "$WORK_DIR/keymap.yaml"
"$PYTHON" -m keymap_drawer -c "$DIR/draw_config.yaml" draw "$WORK_DIR/keymap.yaml" \
  --qmk-info-json "$DIR/qmk_info.json" > "$WORK_DIR/keymap.svg"

# Reject empty/broken SVGs and missing keys before publishing.
"$PYTHON" - "$WORK_DIR" <<'PYCODE'
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

work = Path(sys.argv[1])
layers = json.loads((work / "qmk.json").read_text())["layers"]
root = ET.parse(work / "keymap.svg").getroot()
assert root.tag == "{http://www.w3.org/2000/svg}svg", "SVG inválido"
keys = [node for node in root.iter() if node.tag.endswith("}rect") and "key" in node.get("class", "").split()]
assert len(keys) == sum(map(len, layers)), "El gráfico no contiene todas las teclas"
PYCODE

# Do not publish a stale snapshot if Vial saved again while drawing.
cmp -s "$DIR/silakka54_main.vil" "$WORK_DIR/source.vil"
mv -f -- "$WORK_DIR/keymap.yaml" "$DIR/keymap.yaml"
mv -f -- "$WORK_DIR/keymap.svg" "$DIR/keymap.svg"
printf '✅ Gráfico actualizado: %s/keymap.svg\n' "$DIR"
