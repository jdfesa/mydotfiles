"""Translate Vial/QMK legends and apply presentation-only styles."""

from pathlib import Path
import json
import re
import sys

import yaml


LABELS = {
    "SCOLON": ";", "SEMICOLON": ";", "SCLN": ";",
    "MINUS": "-", "MINS": "-", "EQUAL": "=", "EQL": "=",
    "LBRACKET": "[", "LEFT_BRACKET": "[", "LBRC": "[",
    "RBRACKET": "]", "RIGHT_BRACKET": "]", "RBRC": "]",
    "BSLASH": "\\", "BACKSLASH": "\\", "BSLS": "\\",
    "SLASH": "/", "COMMA": ",", "DOT": ".", "QUOTE": "'", "GRAVE": "`",
    "ESCAPE": "Esc", "ESC": "Esc", "BSPACE": "Bksp", "BSPC": "Bksp",
    "DELETE": "Del", "DEL": "Del", "CAPSLOCK": "Caps", "CAPS": "Caps",
    "SPACE": "Space", "SPC": "Space", "ENTER": "Enter", "ENT": "Enter", "TAB": "Tab",
    "LALT": "Alt", "RALT": "Alt", "LCTL": "Ctrl", "RCTL": "Ctrl", "Ctl": "Ctrl",
    "LCTRL": "Ctrl", "RCTRL": "Ctrl", "LGUI": "Gui", "RGUI": "Gui", "Sft": "Shift",
    "LSFT": "Shift", "RSFT": "Shift", "LSHIFT": "Shift", "RSHIFT": "Shift",
    "MEH": "Meh", "ALL": "Hyper", "HYPR": "Hyper",
    "TRNS": "▽", "TRANSPARENT": "▽", "sticky": "1-shot",
    "KP PLUS": "KP +", "KP MINUS": "KP -",
    "HOME": "Home", "END": "End", "PGUP": "PgUp", "PGDOWN": "PgDn",
    "LEFT": "←", "DOWN": "↓", "UP": "↑", "RIGHT": "→",
    "APPLICATION": "Menu", "VOLU": "Vol +", "VOLD": "Vol -",
    "MFFD": "Fwd", "MPRV": "Prev", "MNXT": "Next",
}
SHIFTED = dict(zip("1234567890`-=[]\\;',./", "!@#$%^&*()~_+{}|:\"<>?"))
DESTRUCTIVE = {"Esc", "Bksp", "Del", "Caps"}


def legend(label):
    """Keep unknown legends visible; never silently drop an unmapped binding."""
    label = str(label)
    if label.startswith("Sft+") and label.count("+") == 1:
        base = legend(label[4:])
        return SHIFTED.get(base, f"Shift+{base}")
    if "+" in label:
        return "+".join(legend(part) for part in label.split("+"))
    return LABELS.get(label.removeprefix("KC_"), label)


def style_key(key, binding=None):
    meta = dict(key) if isinstance(key, dict) else {"t": key}
    for field in ("t", "h", "s", "left", "right"):
        if field in meta:
            meta[field] = legend(meta[field])

    # This is a binding reference, not a simulated activation path. The parser
    # may clear held legends, so consult the source instead of guessing whether
    # a blank key was transparent or explicitly disabled with KC_NO.
    types = meta.get("type", "").split()
    if binding in ("KC_TRNS", "KC_TRANSPARENT", "_______"):
        meta["t"] = "▽"
    types = [value for value in types if value not in ("held", "alternate")]
    if meta.get("t") == "▽" and not meta.get("h"):
        types.append("trans")
    if any(re.fullmatch(r"L\d+", meta.get(field, "")) for field in ("t", "h")):
        types.append("layer")
    elif meta.get("t") in DESTRUCTIVE:
        types.append("destructive")
    meta.pop("type", None)
    if types:
        meta["type"] = " ".join(dict.fromkeys(types))
    return meta if set(meta) != {"t"} else meta["t"]


def process(data, source):
    for layer_index, rows in enumerate(data["layers"].values()):
        position = 0
        for row in rows:
            for index, key in enumerate(row):
                styled = style_key(key, source["layers"][layer_index][position])
                # Personal usage note, not a disabled key or a firmware change.
                # After Vial conversion, positions 0–11 span both top rows.
                if layer_index == 0 and position < 12:
                    styled = dict(styled) if isinstance(styled, dict) else {"t": styled}
                    styled["tr"] = "×"
                    styled["type"] = " ".join(filter(None, (styled.get("type"), "avoided")))
                row[index] = styled
                position += 1
    return data


def represent_str(dumper, value):
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str", value, style="|" if "\n" in value else None
    )


yaml.SafeDumper.add_representer(str, represent_str)


def main():
    layers_path, source_path, output_path = map(Path, sys.argv[1:])
    data = yaml.safe_load(layers_path.read_text(encoding="utf-8"))
    source = json.loads(source_path.read_text(encoding="utf-8"))
    output_path.write_text(
        yaml.safe_dump(process(data, source), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
