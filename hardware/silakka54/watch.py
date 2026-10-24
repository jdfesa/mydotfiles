"""Opt-in, dependency-free watcher; rendering is independent of Git commits."""

import hashlib
from pathlib import Path
import subprocess
import sys
import time


INPUTS = (
    "silakka54_main.vil", "convert_vial.py", "post_process.py",
    "draw_config.yaml", "qmk_info.json", "render.sh", "requirements.txt",
)


def fingerprint(directory):
    result = []
    for name in INPUTS:
        try:
            result.append(hashlib.sha256((directory / name).read_bytes()).digest())
        except FileNotFoundError:
            # Editors/Vial may briefly remove a file during an atomic save.
            result.append(None)
    return tuple(result)


def watch(directory):
    print("👀 Observando fuentes del teclado. Guardá el .vil para regenerar; Ctrl+C para salir.", flush=True)
    pending = fingerprint(directory)
    rendered = None
    stable_since = time.monotonic()
    try:
        while True:
            current = fingerprint(directory)
            if current != pending:
                pending = current
                stable_since = time.monotonic()
            elif current != rendered and time.monotonic() - stable_since >= 0.5:
                if None not in current:
                    result = subprocess.run(["bash", str(directory / "render.sh")], check=False)
                    if result.returncode:
                        print("⚠️ No se actualizó el gráfico. Corregí el error y guardá otra vez.", flush=True)
                    rendered = current
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nObservación finalizada.", flush=True)


if __name__ == "__main__":
    watch(Path(sys.argv[1]).resolve())
