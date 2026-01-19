#!/bin/bash

# Obtiene la ruta donde está este script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ruta al ejecutable dentro del entorno virtual
KEYMAP_CMD="$DIR/.venv/bin/keymap"

echo "🎨 Generando visualización del Silakka54..."

# Verifica si la herramienta existe
if [ ! -f "$KEYMAP_CMD" ]; then
    echo "❌ Error: No encuentro el entorno virtual."
    echo "   Ejecuta: python3 -m venv .venv && source .venv/bin/activate && pip install keymap-drawer"
    exit 1
fi

# 1. Convertir tu JSON (exportado de Vial) a YAML para el dibujante
# 1. Convertir VIal (.vil) a formato compatible QMK JSON (wrapper de "layers")
python3 -c "import json; d=json.load(open('$DIR/silakka54_main.vil')); print(json.dumps({'layers': [[(k if isinstance(k, str) else 'KC_NO') for r in [l[0], l[5][::-1], l[1], l[6][::-1], l[2], l[7][::-1], l[3], l[8][::-1], l[4][::-1], l[9][::-1]] for k in r if k != -1] for l in d['layout']]}))" > "$DIR/temp_qmk.json"

# 2. Parsear el JSON temporal
"$KEYMAP_CMD" parse -c 12 -q "$DIR/temp_qmk.json" > "$DIR/keymap_layers.yaml"
rm "$DIR/temp_qmk.json"

# 3. Combinar config visual + post-procesar (style types)
"$DIR/.venv/bin/python3" "$DIR/post_process.py" "$DIR"
rm "$DIR/keymap_layers.yaml"

# 4. Dibujar el SVG
"$KEYMAP_CMD" draw "$DIR/keymap.yaml" --qmk-info-json "$DIR/qmk_info.json" > "$DIR/keymap.svg"

echo "✅ Grafico actualizado: keymap.svg"