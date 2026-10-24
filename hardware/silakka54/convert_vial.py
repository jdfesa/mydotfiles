"""Convert the Silakka54 Vial backup to keymap-drawer's QMK JSON input.

The physical order matches qmk_info.json: four 12-key rows, then six thumb
keys. Vial stores each half separately, with the right half reversed.
The .vil source is only ever read, never rewritten.
"""

import json
from pathlib import Path
import re
import sys


def convert(data):
    layers = data.get("layout")
    if not isinstance(layers, list) or not layers:
        raise ValueError("El .vil no contiene capas en 'layout'.")

    converted = []
    for layer_index, layer in enumerate(layers):
        if not isinstance(layer, list) or len(layer) != 10:
            raise ValueError(f"L{layer_index}: se esperaban 10 filas Vial.")
        for row_index, row in enumerate(layer):
            if not isinstance(row, list) or len(row) != 6:
                raise ValueError(f"L{layer_index}, fila {row_index}: se esperaban 6 posiciones.")
            for column, key in enumerate(row):
                placeholder = row_index in (4, 9) and column < 3
                if (placeholder and key != -1) or (not placeholder and not isinstance(key, str)):
                    raise ValueError(
                        f"L{layer_index}, fila {row_index}, columna {column}: posición inválida."
                    )

        keys = []
        for row_index in range(5):
            for row in (layer[row_index], reversed(layer[row_index + 5])):
                for key in row:
                    if key != -1:
                        # Vial's LT1(KC_TAB) is QMK's LT(1,KC_TAB).
                        keys.append(re.sub(r"\bLT(\d+)\(", r"LT(\1,", key))
        converted.append(keys)
    return {"layers": converted}


def main():
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    json.dump(convert(data), sys.stdout)
    print()


if __name__ == "__main__":
    main()
