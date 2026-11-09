#!/usr/bin/env python3
"""Valida workspaces y highlight con dobles, sin tocar la sesión gráfica."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[4]
AEROSPACE_DIR = ROOT / "os/macos/aerospace"
WORKSPACES = ["1", "2", "3", "4", "5"]
ROUTES = {
    "1": [
        "com.google.Chrome", "com.apple.Safari",
        "org.mozilla.firefoxdeveloperedition", "org.qutebrowser.qutebrowser",
        "com.brave.Browser", "app.zen-browser.zen",
    ],
    "2": [
        "com.openai.codex", "com.microsoft.VSCode", "com.mitchellh.ghostty",
        "net.kovidgoyal.kitty", "com.apple.Terminal", "dev.kiro.desktop",
        "com.google.antigravity", "com.google.antigravity-ide",
    ],
    "3": [
        "md.obsidian", "abnerworks.Typora", "com.apple.Notes", "TeXShop",
        "com.wondershare.PDFelement",
    ],
    "4": [
        "com.apple.finder", "com.apple.ActivityMonitor",
        "com.microsoft.rdc.macos", "today.vial", "com.codeweavers.CrossOver",
    ],
    "5": [
        "com.tdesktop.Telegram", "com.hnc.Discord", "com.apple.iCal",
        "com.github.th-ch.youtube-music", "org.videolan.vlc",
    ],
}


class WorkspaceConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (AEROSPACE_DIR / "aerospace.toml").open("rb") as source:
            cls.config = tomllib.load(source)

    def test_five_persistent_workspaces(self):
        self.assertEqual(self.config["persistent-workspaces"], WORKSPACES)

    def test_numeric_bindings_without_letter_aliases(self):
        bindings = self.config["mode"]["main"]["binding"]
        for workspace in WORKSPACES:
            self.assertEqual(bindings[f"cmd-alt-ctrl-shift-{workspace}"],
                             f"workspace {workspace}")
            self.assertEqual(bindings[f"alt-ctrl-shift-{workspace}"],
                             f"move-node-to-workspace {workspace}")
        for letter in "uiopyn":
            self.assertNotIn(f"cmd-alt-ctrl-shift-{letter}", bindings)
            self.assertNotIn(f"alt-ctrl-shift-{letter}", bindings)
        destinations = [value.split()[-1] for value in bindings.values()
                        if isinstance(value, str) and value.startswith(
                            ("workspace ", "move-node-to-workspace "))]
        self.assertEqual(sorted(destinations), sorted(WORKSPACES * 2))

    def test_all_application_rules_keep_the_agreed_destinations(self):
        expected = {app: f"move-node-to-workspace {workspace}"
                    for workspace, apps in ROUTES.items() for app in apps}
        rules = self.config["on-window-detected"]
        self.assertEqual(len(rules), len(expected))
        self.assertEqual({rule["if"]["app-id"]: rule["run"] for rule in rules},
                         expected)

    def test_window_navigation_and_modes_remain_available(self):
        main = self.config["mode"]["main"]["binding"]
        for key, direction in zip("hjkl", ["left", "down", "up", "right"]):
            self.assertEqual(main[f"cmd-alt-ctrl-shift-{key}"], f"focus {direction}")
            self.assertEqual(main[f"alt-ctrl-shift-{key}"], f"move {direction}")
        self.assertEqual(main["cmd-enter"], "exec-and-forget open -n -a kitty")
        self.assertEqual(main["cmd-alt-ctrl-shift-tab"], "workspace-back-and-forth")
        self.assertEqual(main["alt-ctrl-shift-m"][0], "mode resize")
        self.assertEqual(main["alt-ctrl-shift-semicolon"][0], "mode service")
        self.assertEqual(set(self.config["mode"]), {"main", "resize", "service"})


class HighlightTests(unittest.TestCase):
    def run_hook(self, workspaces, focused, status=0):
        with tempfile.TemporaryDirectory(prefix="aerospace-workspaces-") as directory:
            fixture = Path(directory)
            aerospace = fixture / "fake aerospace"
            sketchybar = fixture / "fake sketchybar"
            log = fixture / "calls.jsonl"
            aerospace.write_text(
                '#!/bin/bash\n'
                '[[ "$*" = "list-workspaces --all" ]] || exit 64\n'
                '[[ "$TEST_AEROSPACE_STATUS" = 0 ]] || exit "$TEST_AEROSPACE_STATUS"\n'
                'printf "%s" "$TEST_WORKSPACES"\n'
            )
            sketchybar.write_text(
                f'#!{sys.executable}\n'
                'import json, os, sys\n'
                'with open(os.environ["TEST_LOG"], "a") as log:\n'
                '    log.write(json.dumps(sys.argv[1:]) + "\\n")\n'
            )
            aerospace.chmod(0o700)
            sketchybar.chmod(0o700)
            result = subprocess.run(
                ["/bin/bash", str(AEROSPACE_DIR / "scripts/update_sketchybar_workspace.sh")],
                env={**os.environ, "AEROSPACE_BIN": str(aerospace),
                     "SKETCHYBAR_BIN": str(sketchybar), "TEST_LOG": str(log),
                     "TEST_WORKSPACES": workspaces,
                     "TEST_AEROSPACE_STATUS": str(status),
                     "AEROSPACE_FOCUSED_WORKSPACE": focused},
                capture_output=True, text=True, timeout=10,
            )
            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, calls

    def assert_highlight(self, workspaces, focused):
        result, calls = self.run_hook("\n".join(workspaces) + "\n", focused)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), len(workspaces))
        for workspace, call in zip(workspaces, calls):
            active = workspace == focused
            state = "on" if active else "off"
            color = "0xffb4befe" if active else "0xff45475a"
            self.assertEqual(call, ["--set", f"space.{workspace}",
                                    f"icon.highlight={state}", f"label.highlight={state}",
                                    f"background.border_color={color}"])

    def test_each_numeric_workspace(self):
        for workspace in WORKSPACES:
            with self.subTest(workspace=workspace):
                self.assert_highlight(WORKSPACES, workspace)

    def test_legacy_process_before_reload(self):
        self.assert_highlight(["U", "I", "O", "P", "Y", "N"], "I")

    def test_mixed_workspaces_during_migration(self):
        self.assert_highlight(WORKSPACES + ["U", "N"], "4")

    def test_empty_list_does_not_change_bar(self):
        result, calls = self.run_hook("\n\n", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, [])

    def test_failed_query_does_not_change_bar(self):
        result, calls = self.run_hook("", "1", status=7)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
