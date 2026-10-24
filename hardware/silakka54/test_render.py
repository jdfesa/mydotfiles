"""Run with .venv/bin/python -m unittest discover -s hardware/silakka54."""

import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest
import xml.etree.ElementTree as ET

import yaml

from convert_vial import convert
from post_process import legend, process, style_key


HERE = Path(__file__).resolve().parent
# Stable fixture: changing the real backup must not require updating test labels.
EMPTY = [["KC_TRNS"] * 6 for _ in range(10)]
EMPTY[4][:3] = EMPTY[9][:3] = [-1, -1, -1]
SOURCE = {"layout": [copy.deepcopy(EMPTY) for _ in range(8)]}
SOURCE["layout"][0] = [
    ["KC_ESCAPE", "KC_1", "KC_2", "KC_3", "KC_4", "KC_5"],
    ["KC_LALT", "KC_Q", "KC_W", "KC_E", "KC_R", "KC_T"],
    ["LCTL_T(KC_ESCAPE)", "KC_A", "KC_S", "KC_D", "KC_F", "KC_G"],
    ["OSM(MOD_LSFT)", "KC_Z", "KC_X", "KC_C", "KC_V", "KC_B"],
    [-1, -1, -1, "LGUI_T(KC_ESCAPE)", "LT1(KC_TAB)", "KC_SPACE"],
    ["KC_BSPACE", "KC_0", "KC_9", "KC_8", "KC_7", "KC_6"],
    ["KC_MINUS", "KC_P", "KC_O", "KC_I", "KC_U", "KC_Y"],
    ["MEH_T(KC_TRNS)", "KC_SCOLON", "KC_L", "KC_K", "KC_J", "KC_H"],
    ["KC_RSHIFT", "KC_SLASH", "KC_DOT", "KC_COMMA", "KC_M", "KC_N"],
    [-1, -1, -1, "ALL_T(KC_ENTER)", "LT2(KC_DELETE)", "RGUI_T(KC_BSPACE)"],
]
SOURCE["layout"][1][4][4] = SOURCE["layout"][1][9][4] = "MO(3)"
SOURCE["layout"][2][1][1:3] = ["LSFT(KC_LBRACKET)", "LSFT(KC_RBRACKET)"]
SOURCE["layout"][2][9][4] = "KC_NO"  # disabled at an inferred held-key position
SOURCE_FILES = (
    "render.sh", "watch.py", "convert_vial.py", "post_process.py",
    "draw_config.yaml", "qmk_info.json", "requirements.txt",
)


def flat(layer):
    return [key for row in layer for key in row]


def tap(key):
    return key.get("t", "") if isinstance(key, dict) else key


class ConversionTests(unittest.TestCase):
    def test_real_backup_has_valid_physical_shape(self):
        convert(json.loads((HERE / "silakka54_main.vil").read_text()))

    def test_all_layers_and_54_keys(self):
        converted = convert(SOURCE)["layers"]
        self.assertEqual(len(converted), len(SOURCE["layout"]))
        self.assertTrue(all(len(layer) == 54 for layer in converted))

    def test_every_position_matches_physical_order(self):
        data = copy.deepcopy(SOURCE)
        for layer in data["layout"]:
            for row_index, row in enumerate(layer):
                for column, key in enumerate(row):
                    if key != -1:
                        row[column] = f"r{row_index}c{column}"
        expected = []
        for row in range(4):
            expected += [f"r{row}c{col}" for col in range(6)]
            expected += [f"r{row + 5}c{col}" for col in reversed(range(6))]
        expected += ["r4c3", "r4c4", "r4c5", "r9c5", "r9c4", "r9c3"]
        self.assertEqual(convert(data)["layers"][0], expected)

    def test_layer_taps_normalized_and_input_unchanged(self):
        before = copy.deepcopy(SOURCE)
        layer = convert(SOURCE)["layers"][0]
        self.assertEqual(layer[49], "LT(1,KC_TAB)")
        self.assertEqual(layer[52], "LT(2,KC_DELETE)")
        self.assertEqual(SOURCE, before)

    def test_rejects_bad_shape_placeholders_and_keycodes(self):
        cases = []
        data = copy.deepcopy(SOURCE)
        data["layout"][0].pop()
        cases.append(data)
        data = copy.deepcopy(SOURCE)
        data["layout"][0][0].pop()
        cases.append(data)
        for row, col, value in ((4, 0, "KC_A"), (0, 0, -1), (0, 0, 42)):
            data = copy.deepcopy(SOURCE)
            data["layout"][0][row][col] = value
            cases.append(data)
        cases.extend(({}, {"layout": []}))
        for data in cases:
            with self.subTest(data=str(data)[:70]), self.assertRaises(ValueError):
                convert(data)

    def test_symbol_and_shortcut_legends(self):
        for raw, expected in {
            "Sft+LBRACKET": "{", "Sft+RBRACKET": "}", "Sft+BSLASH": "|",
            "Sft+1": "!", "Sft+0": ")", "Sft+;": ":",
            "Sft+Gui+4": "Shift+Gui+4", "Ctl+C": "Ctrl+C",
            "KC_RSHIFT": "Shift", "TRNS": "▽", "ALL": "Hyper",
            "SOME_NEW_KEY": "SOME_NEW_KEY",
        }.items():
            with self.subTest(raw=raw):
                self.assertEqual(legend(raw), expected)

    def test_modifiers_are_not_layers(self):
        self.assertEqual(style_key({"t": "ESCAPE", "h": "LCTL"}),
                         {"t": "Esc", "h": "Ctrl", "type": "destructive"})
        self.assertEqual(style_key({"t": "TRNS", "h": "MEH"}), {"t": "▽", "h": "Meh"})
        self.assertEqual(style_key({"t": "TAB", "h": "L1"})["type"], "layer")
        self.assertEqual(style_key("L3")["type"], "layer")

    def test_restore_transparency_not_guessed_held_state(self):
        self.assertEqual(style_key({"type": "held"}, "KC_TRNS"), {"t": "▽", "type": "trans"})
        self.assertEqual(style_key({"type": "held"}, "KC_NO"), {})
        self.assertEqual(style_key({"t": "L3", "type": "held"}), {"t": "L3", "type": "layer"})

    def test_usage_annotation_preserves_bindings_and_other_layers(self):
        labels = [f"Key{i}" for i in range(54)]
        data = {"layers": {"L0": [labels[:12], labels[12:]], "L1": [labels[:]]}}
        original = copy.deepcopy(data)
        source = {"layers": [labels[:], labels[:]]}
        process(data, source)
        base = flat(data["layers"]["L0"])
        self.assertEqual([tap(key) for key in base], labels)
        self.assertTrue(all(key["tr"] == "×" and key["type"] == "avoided" for key in base[:12]))
        self.assertEqual(base[12:], labels[12:])
        self.assertEqual(data["layers"]["L1"], original["layers"]["L1"])


class RenderingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="silakka54 test's ")
        self.directory = Path(self.temp.name)
        for name in SOURCE_FILES:
            shutil.copy2(HERE / name, self.directory / name)
        (self.directory / "silakka54_main.vil").write_text(json.dumps(SOURCE))
        (self.directory / ".venv").symlink_to(HERE / ".venv", target_is_directory=True)
        self.backup_hash = hashlib.sha256((self.directory / "silakka54_main.vil").read_bytes()).digest()

    def tearDown(self):
        self.temp.cleanup()

    def render(self):
        return subprocess.run(["bash", str(self.directory / "render.sh")],
                              cwd="/", capture_output=True, text=True)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def outputs(self):
        return {name: (self.directory / name).read_bytes() for name in ("keymap.yaml", "keymap.svg")}

    def test_current_layout_and_svg_have_every_key(self):
        self.assert_success(self.render())
        data = yaml.safe_load((self.directory / "keymap.yaml").read_text())
        self.assertEqual(list(data["layers"]), [f"L{i}" for i in range(len(SOURCE["layout"]))])
        self.assertTrue(all(len(flat(layer)) == 54 for layer in data["layers"].values()))
        base = flat(data["layers"]["L0"])
        self.assertEqual([tap(key) for key in base[12:24]], list("Alt Q W E R T Y U I O P -".split()))
        self.assertEqual([tap(key) for key in base[48:]], ["Esc", "Tab", "Space", "Bksp", "Del", "Enter"])
        self.assertEqual([key.get("h", "") if isinstance(key, dict) else "" for key in base[48:]],
                         ["Gui", "L1", "", "Gui", "L2", "Hyper"])
        self.assertEqual([tap(key) for key in flat(data["layers"]["L2"])[13:15]], ["{", "}"])
        self.assertEqual(tap(flat(data["layers"]["L2"])[52]), "")
        self.assertTrue(all(tap(key) == "▽" for key in flat(data["layers"]["L4"])))
        root = ET.parse(self.directory / "keymap.svg").getroot()
        keys = [node for node in root.iter() if node.tag.endswith("}rect") and "key" in node.get("class", "").split()]
        self.assertEqual(len(keys), 54 * len(SOURCE["layout"]))
        self.assertEqual(hashlib.sha256((self.directory / "silakka54_main.vil").read_bytes()).digest(), self.backup_hash)

    def test_repeated_render_is_identical(self):
        self.assert_success(self.render())
        before = self.outputs()
        self.assert_success(self.render())
        self.assertEqual(self.outputs(), before)
        self.assertFalse(list(self.directory.glob(".render.*")))

    def test_only_base_top_row_has_usage_marks_and_labels_remain_visible(self):
        self.assert_success(self.render())
        data = yaml.safe_load((self.directory / "keymap.yaml").read_text())
        base = flat(data["layers"]["L0"])
        self.assertEqual([tap(key) for key in base[:12]],
                         ["Esc", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Bksp"])
        self.assertTrue(all(key["tr"] == "×" and "avoided" in key["type"].split() for key in base[:12]))
        for layer_index, layer in enumerate(data["layers"].values()):
            for position, key in enumerate(flat(layer)):
                if layer_index != 0 or position >= 12:
                    self.assertNotIn("avoided", key.get("type", "") if isinstance(key, dict) else "")
                    self.assertNotIn("tr", key if isinstance(key, dict) else {})
        root = ET.parse(self.directory / "keymap.svg").getroot()
        marks = [node for node in root.iter() if "avoided" in node.get("class", "").split()
                 and "tr" in node.get("class", "").split()]
        self.assertEqual(len(marks), 12)
        self.assertTrue(all(node.text == "×" for node in marks))

    def test_invalid_vil_preserves_both_previous_outputs(self):
        self.assert_success(self.render())
        before = self.outputs()
        (self.directory / "silakka54_main.vil").write_text("{incomplete")
        self.assertNotEqual(self.render().returncode, 0)
        self.assertEqual(self.outputs(), before)
        self.assertFalse(list(self.directory.glob(".render.*")))

    def test_draw_failure_preserves_both_previous_outputs(self):
        self.assert_success(self.render())
        before = self.outputs()
        (self.directory / "qmk_info.json").write_text("{}")
        self.assertNotEqual(self.render().returncode, 0)
        self.assertEqual(self.outputs(), before)
        self.assertFalse(list(self.directory.glob(".render.*")))

    def test_missing_environment_fails_without_replacing_outputs(self):
        (self.directory / ".venv").unlink()
        for name in ("keymap.yaml", "keymap.svg"):
            (self.directory / name).write_text("previous")
        before = self.outputs()
        self.assertNotEqual(self.render().returncode, 0)
        self.assertEqual(self.outputs(), before)

    def test_watch_regenerates_on_save_before_any_git_commit(self):
        def wait_for_label(expected):
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                if (self.directory / "keymap.yaml").exists():
                    data = yaml.safe_load((self.directory / "keymap.yaml").read_text())
                    if tap(flat(data["layers"]["L0"])[13]) == expected:
                        return
                time.sleep(0.1)
            self.fail(f"El observador no generó la tecla {expected}: "
                      + (self.directory / "watch.log").read_text())

        with (self.directory / "watch.log").open("w") as log:
            watcher = subprocess.Popen(["bash", str(self.directory / "render.sh"), "--watch"],
                                       stdout=log, stderr=log)
            try:
                wait_for_label("Q")
                (self.directory / "silakka54_main.vil").write_text("{incomplete")
                deadline = time.monotonic() + 10
                while "No se actualizó" not in (self.directory / "watch.log").read_text():
                    if time.monotonic() > deadline:
                        self.fail("El observador no informó el guardado inválido")
                    time.sleep(0.1)
                wait_for_label("Q")  # last successful render is still intact
                data = copy.deepcopy(SOURCE)
                data["layout"][0][1][1] = "KC_F24"
                (self.directory / "silakka54_main.vil").write_text(json.dumps(data))
                wait_for_label("F24")
                # Publication happens immediately after YAML; wait for cleanup.
                deadline = time.monotonic() + 3
                while list(self.directory.glob(".render.*")) and time.monotonic() < deadline:
                    time.sleep(0.1)
                self.assertFalse((self.directory / ".git").exists())
            finally:
                watcher.terminate()
                watcher.wait(timeout=5)

    def test_commit_hook_no_longer_generates_or_stages_artifacts(self):
        self.assertFalse((HERE.parent.parent / ".githooks" / "pre-commit").exists())


if __name__ == "__main__":
    unittest.main()
